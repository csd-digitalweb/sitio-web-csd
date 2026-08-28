import os
import sys
import time
import requests
from dotenv import load_dotenv

load_dotenv(r"C:\Users\julio\dev\sitio-web-csd\.env")

from community_manager import create_news_article, create_gallery_album, approve_content_file
from publisher import publish_to_web

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
ALLOWED_USERS_RAW = os.getenv("ALLOWED_USERS", "")
ALLOWED_USERS = [u.strip().lower().lstrip('@') for u in ALLOWED_USERS_RAW.split(',') if u.strip()]
DIRECTOR_CHAT_ID = os.getenv("DIRECTOR_CHAT_ID", "")
API_URL = f"https://api.telegram.org/bot{TOKEN}" if TOKEN else ""

def is_user_authorized(from_user):
    if not ALLOWED_USERS:
        return True
    user_id = str(from_user.get("id", ""))
    username = from_user.get("username", "").lower()
    return (user_id in ALLOWED_USERS or username in ALLOWED_USERS)

def get_updates(offset=None):
    if not TOKEN:
        return []
    url = f"{API_URL}/getUpdates?timeout=30"
    if offset:
        url += f"&offset={offset}"
    try:
        r = requests.get(url, timeout=35)
        if r.status_code == 200:
            return r.json().get("result", [])
    except Exception as e:
        print(f"Error al consultar actualizaciones de Telegram: {e}")
    return []

def send_message(chat_id, text, reply_markup=None):
    if not TOKEN:
        print(f"[Simulación Telegram -> Chat {chat_id}]: {text}")
        return
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if reply_markup:
        data["reply_markup"] = reply_markup
    try:
        requests.post(f"{API_URL}/sendMessage", json=data)
    except Exception as e:
        print(f"Error al enviar mensaje a Telegram: {e}")

def edit_message_text(chat_id, message_id, text, reply_markup=None):
    if not TOKEN:
        return
    data = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": "Markdown"}
    if reply_markup:
        data["reply_markup"] = reply_markup
    try:
        requests.post(f"{API_URL}/editMessageText", json=data)
    except Exception as e:
        print(f"Error al editar mensaje en Telegram: {e}")

def handle_text_message(chat_id, from_user, text):
    lines = text.strip().split('\n')
    title = lines[0].replace("/noticia", "").strip()
    if not title:
        title = "Noticia Institucional CSD"
    raw_idea = "\n".join(lines[1:]) if len(lines) > 1 else lines[0]
    author_name = from_user.get("first_name", "Equipo CSD")

    # Si hay DIRECTOR_CHAT_ID se crea en borrador (published=False) para pedir aprobación sin límite de tiempo
    require_approval = bool(DIRECTOR_CHAT_ID)
    published_initial = not require_approval

    file_path, filename = create_news_article(
        title, raw_idea, category="Noticias", author=author_name, published=published_initial
    )

    if require_approval:
        # Enviar notificación a la Dirección con botón de aprobación SIN límite de tiempo
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
        send_message(chat_id, f"📝 Noticia redactada y enviada a la Dirección para su aprobación final.")

    else:
        # Publicar inmediatamente
        success, msg = publish_to_web(f"Nueva noticia: {title}")
        if success:
            send_message(
                chat_id,
                f"🎉 *¡Noticia Publicada Exitosamente en csd.edu.co!*\n\n"
                f"📌 *Título:* {title}\n"
                f"📄 *Archivo:* `{filename}`\n\n"
                f"🌐 La página web se ha actualizado en tiempo real."
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
        requests.post(f"{API_URL}/answerCallbackQuery", json={"callback_query_id": callback_id, "text": "⛔ No autorizado", "show_alert": True})
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
    print("🤖 BOT COMMUNITY MANAGER DEL COLEGIO CSD ACTIVO")
    print("=" * 60)
    if not TOKEN:
        print("⚠️ No se ha configurado TELEGRAM_BOT_TOKEN en el archivo .env.")
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

            if not chat_id:
                continue

            if not is_user_authorized(from_user):
                send_message(
                    chat_id,
                    "⛔ *Acceso Restringido*\n\n"
                    "Este bot es exclusivo para el equipo pedagógico y directivo del Colegio CSD.\n"
                    "Tu usuario de Telegram no está en la lista de personal autorizado."
                )
                continue

            if text.startswith("/start"):
                send_message(
                    chat_id,
                    "👋 *¡Hola! Soy el Bot Community Manager del Colegio CSD.*\n\n"
                    "Para enviar una **noticia o artículo de interés** para la página web `csd.edu.co`:\n"
                    "Escríbeme el título en la primera línea y luego los detalles o borrador.\n\n"
                    " Ejemplo:\n"
                    "`Izada de Bandera del 7 de Agosto`\n"
                    "`Hoy todos los cursos de primaria participaron con muestras de danza y música.`"
                )
            elif text:
                send_message(chat_id, "✍️ Procesando tu noticia y creando el borrador institucional...")
                handle_text_message(chat_id, from_user, text)

        time.sleep(2)

if __name__ == "__main__":
    run_bot()
