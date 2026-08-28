import os
import sys
import time
import json
import subprocess
from dotenv import load_dotenv

load_dotenv(r"C:\Users\julio\dev\sitio-web-csd\.env")

from community_manager import create_news_article, create_gallery_album, approve_content_file, BASE_DIR
from photo_optimizer import optimize_image
from publisher import publish_to_web

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
ALLOWED_USERS_RAW = os.getenv("ALLOWED_USERS", "")
ALLOWED_PHONES_RAW = os.getenv("ALLOWED_PHONES", "")
DIRECTOR_CHAT_ID = os.getenv("DIRECTOR_CHAT_ID", "")

ALLOWED_USERS = [u.strip().lower().lstrip('@') for u in ALLOWED_USERS_RAW.split(',') if u.strip()]
ALLOWED_PHONES = [p.strip().replace("+", "").replace(" ", "").replace("-", "") for p in ALLOWED_PHONES_RAW.split(',') if p.strip()]

API_URL = f"https://api.telegram.org/bot{TOKEN}" if TOKEN else ""
FILE_URL = f"https://api.telegram.org/file/bot{TOKEN}" if TOKEN else ""

def call_telegram_api(method, data=None):
    if not TOKEN:
        return None
    url = f"{API_URL}/{method}"
    cmd = ["curl.exe", "-s", "-X", "POST", url, "-H", "Content-Type: application/json"]
    if data:
        cmd.extend(["-d", json.dumps(data)])

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=35)
        if res.returncode == 0 and res.stdout:
            return json.loads(res.stdout)
    except Exception as e:
        print(f"Error en llamada a Telegram API ({method}): {e}")
    return None

def download_telegram_file(file_id, output_path):
    res = call_telegram_api("getFile", {"file_id": file_id})
    if res and res.get("ok"):
        file_path_remote = res.get("result", {}).get("file_path")
        if file_path_remote:
            dl_url = f"{FILE_URL}/{file_path_remote}"
            cmd = ["curl.exe", "-s", "-o", output_path, dl_url]
            res_dl = subprocess.run(cmd, capture_output=True, timeout=30)
            if res_dl.returncode == 0 and os.path.exists(output_path):
                return output_path
    return None

def is_user_authorized(from_user, phone_number=""):
    if not ALLOWED_USERS and not ALLOWED_PHONES:
        return True

    user_id = str(from_user.get("id", ""))
    username = from_user.get("username", "").lower()

    if user_id in ALLOWED_USERS or username in ALLOWED_USERS:
        return True

    if phone_number:
        clean_phone = phone_number.replace("+", "").replace(" ", "").replace("-", "")
        for allowed in ALLOWED_PHONES:
            if clean_phone.endswith(allowed) or allowed.endswith(clean_phone):
                return True

    return False

def get_updates(offset=None):
    payload = {"timeout": 30}
    if offset:
        payload["offset"] = offset
    res = call_telegram_api("getUpdates", payload)
    if res and res.get("ok"):
        return res.get("result", [])
    return []

def send_message(chat_id, text, reply_markup=None):
    if not TOKEN:
        print(f"[Simulación Telegram -> Chat {chat_id}]: {text}")
        return
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if reply_markup:
        data["reply_markup"] = reply_markup
    return call_telegram_api("sendMessage", data)

def edit_message_text(chat_id, message_id, text, reply_markup=None):
    data = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": "Markdown"}
    if reply_markup:
        data["reply_markup"] = reply_markup
    return call_telegram_api("editMessageText", data)

def request_phone_authorization(chat_id):
    keyboard = {
        "keyboard": [
            [
                {"text": "📱 Verificar mi número de celular para ingresar", "request_contact": True}
            ]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }
    send_message(
        chat_id,
        "🔒 *Sistema de Seguridad Institucional Colegio CSD*\n\n"
        "Este bot es exclusivo para profesores y directivos autorizados.\n"
        "Toca el botón azul de abajo **'📱 Verificar mi número de celular'** para autenticar tu ingreso automáticamente.",
        reply_markup=keyboard
    )

def handle_text_message(chat_id, from_user, text, portada_rel_path=""):
    lines = text.strip().split('\n')
    title = lines[0].replace("/noticia", "").strip()
    if not title:
        title = "Noticia Institucional CSD"
    raw_idea = "\n".join(lines[1:]) if len(lines) > 1 else lines[0]
    author_name = from_user.get("first_name", "Equipo CSD")

    require_approval = bool(DIRECTOR_CHAT_ID)
    published_initial = not require_approval

    file_path, filename = create_news_article(
        title, raw_idea, category="Noticias", author=author_name, portada=portada_rel_path, published=published_initial
    )

    if require_approval:
        inline_keyboard = {
            "inline_keyboard": [
                [
                    {"text": "✅ Aprobar y Publicar en csd.edu.co", "callback_data": f"pub_noticias_{filename}"},
                    {"text": "❌ Descartar", "callback_data": f"del_noticias_{filename}"}
                ]
            ]
        }
        send_message(
            DIRECTOR_CHAT_ID,
            f"📥 *NUEVA NOTICIA ENVIADA POR EL PROFESOR*\n\n"
            f"👤 *Autor:* {author_name}\n"
            f"📌 *Título:* {title}\n"
            f"📄 *Archivo:* `{filename}`\n\n"
            f"Puedes hacer clic en el botón de aprobación en **cualquier momento** (sin límite de tiempo).",
            reply_markup=inline_keyboard
        )
        send_message(chat_id, f"📝 Noticia redactada con ortografía y estilo periodístico. Enviada a la Dirección para su aprobación final.")
    else:
        success, msg = publish_to_web(f"Nueva noticia: {title}")
        if success:
            send_message(
                chat_id,
                f"🎉 *¡Noticia Redactada y Publicada Exitosamente en csd.edu.co!*\n\n"
                f"📌 *Título:* {title}\n"
                f"📄 *Archivo:* `{filename}`\n\n"
                f"🌐 La página web se ha actualizado en tiempo real con corrección ortográfica y redacción institucional."
            )
        else:
            send_message(chat_id, f"⚠️ El artículo se guardó pero hubo un problema al publicar: {msg}")

def handle_callback_query(callback):
    callback_id = callback.get("id")
    from_user = callback.get("from", {})
    message = callback.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    message_id = message.get("message_id")
    data = callback.get("data", "")

    if not is_user_authorized(from_user):
        call_telegram_api("answerCallbackQuery", {"callback_query_id": callback_id, "text": "⛔ No autorizado", "show_alert": True})
        return

    if data.startswith("pub_"):
        parts = data.split("_", 2)
        folder = parts[1]
        filename = parts[2]

        if approve_content_file(folder, filename):
            success, msg = publish_to_web(f"Aprobación de contenido: {filename}")
            if success:
                edit_message_text(
                    chat_id, message_id,
                    f"🎉 *¡CONTENIDO APROBADO Y PUBLICADO EN VIVO EN csd.edu.co!*\n\n"
                    f"📄 *Archivo publicado:* `{filename}`\n"
                    f"🌐 Los cambios ya se reflejan en el sitio oficial del colegio."
                )
            else:
                edit_message_text(chat_id, message_id, f"⚠️ Aprobado en código pero hubo error de publicación: {msg}")
        else:
            edit_message_text(chat_id, message_id, f"⚠️ No se encontró el archivo `{filename}` para aprobación.")

    elif data.startswith("del_"):
        edit_message_text(chat_id, message_id, "❌ *Noticia descartada.* No fue publicada en el sitio web.")

def run_bot():
    print("=" * 60)
    print(" [BOT] COMMUNITY MANAGER DEL COLEGIO CSD ACTIVO (@CSDnoticiasbot)")
    print("=" * 60)
    if not TOKEN:
        print("[!] No se ha configurado TELEGRAM_BOT_TOKEN en el archivo .env.")
        return

    print("Escuchando mensajes de Telegram en segundo plano...")
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates:
            offset = update["update_id"] + 1

            if "callback_query" in update:
                handle_callback_query(update["callback_query"])
                continue

            message = update.get("message", {})
            chat_id = message.get("chat", {}).get("id")
            from_user = message.get("from", {})
            text = message.get("text", "")
            caption = message.get("caption", "")
            photos = message.get("photo", [])
            contact = message.get("contact", {})

            if not chat_id:
                continue

            if contact:
                phone_num = contact.get("phone_number", "")
                if is_user_authorized(from_user, phone_number=phone_num):
                    send_message(
                        chat_id,
                        f"✅ *¡Teléfono Verificado Exitosamente!*\n\n"
                        f"Hola *{from_user.get('first_name', '')}*. Tu número de celular (`{phone_num}`) "
                        f"ha sido autorizado para publicar en el Colegio CSD.\n\n"
                        f"Ya puedes enviarme noticias o fotos cuando quieras."
                    )
                else:
                    send_message(
                        chat_id,
                        f"⛔ *Acceso Denegado*\n\n"
                        f"El número `{phone_num}` no figura en la lista de celulares autorizados del colegio."
                    )
                continue

            if not is_user_authorized(from_user):
                request_phone_authorization(chat_id)
                continue

            # Procesar mensaje con foto adjunta
            portada_rel_path = ""
            if photos:
                largest_photo = photos[-1]
                file_id = largest_photo.get("file_id")
                tmp_dir = os.path.join(BASE_DIR, "scratch", "tmp_downloads")
                os.makedirs(tmp_dir, exist_ok=True)
                tmp_photo_path = os.path.join(tmp_dir, f"photo_{int(time.time())}.jpg")

                if download_telegram_file(file_id, tmp_photo_path):
                    output_dir = os.path.join(BASE_DIR, "src", "assets", "noticias")
                    opt_file = optimize_image(tmp_photo_path, output_dir)
                    portada_rel_path = f"/assets/noticias/{os.path.basename(opt_file)}"

            final_text = caption if caption else text

            if final_text.startswith("/start") or final_text.startswith("/id"):
                send_message(
                    chat_id,
                    f"👋 *¡Hola {from_user.get('first_name', '')}! Soy el Bot del Colegio CSD.*\n\n"
                    f"📱 *Tu ID Único de Celular:* `{from_user.get('id')}`\n\n"
                    f"Para enviar una **noticia o artículo de interés** para la página `csd.edu.co`:\n"
                    f"Escríbeme el título en la primera línea y luego los detalles o borrador (¡puedes adjuntar foto!).\n\n"
                    f" Ejemplo:\n"
                    f"`Izada de Bandera del 7 de Agosto`\n"
                    f"`Hoy todos los cursos de primaria participaron con muestras de danza y música.`"
                )
            elif final_text:
                send_message(chat_id, "✍️ Procesando tu noticia, aplicando corrección ortográfica y generando el artículo con gancho...")
                handle_text_message(chat_id, from_user, final_text, portada_rel_path=portada_rel_path)

        time.sleep(2)

if __name__ == "__main__":
    run_bot()
