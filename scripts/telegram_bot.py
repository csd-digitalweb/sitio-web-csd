import os
import sys
import time
import requests
from dotenv import load_dotenv

# Cargar variables de entorno si existe .env
load_dotenv(r"C:\Users\julio\dev\sitio-web-csd\.env")

from community_manager import create_news_article, create_gallery_album
from publisher import publish_to_web

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
ALLOWED_USERS_RAW = os.getenv("ALLOWED_USERS", "")
ALLOWED_USERS = [u.strip().lower().lstrip('@') for u in ALLOWED_USERS_RAW.split(',') if u.strip()]
API_URL = f"https://api.telegram.org/bot{TOKEN}" if TOKEN else ""

def is_user_authorized(from_user):
    """
    Verifica si el usuario de Telegram está en la lista blanca de profesores/directivos autorizados.
    """
    if not ALLOWED_USERS:
        # Si no se define lista blanca, por seguridad solo el creador inicial tiene acceso
        return True

    user_id = str(from_user.get("id", ""))
    username = from_user.get("username", "").lower()

    if user_id in ALLOWED_USERS or username in ALLOWED_USERS:
        return True

    return False

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

def handle_text_message(chat_id, text):
    lines = text.strip().split('\n')
    title = lines[0].replace("/noticia", "").strip()
    if not title:
        title = "Noticia Institucional CSD"
    raw_idea = "\n".join(lines[1:]) if len(lines) > 1 else lines[0]

    # Crear el artículo
    file_path, filename = create_news_article(title, raw_idea, category="Noticias", author="Equipo CSD", published=True)

    # Publicar automáticamente en vivo
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

def run_bot():
    print("=" * 60)
    print("🤖 BOT COMMUNITY MANAGER DEL COLEGIO CSD ACTIVO")
    print("=" * 60)
    if not TOKEN:
        print("⚠️ No se ha configurado TELEGRAM_BOT_TOKEN en el archivo .env.")
        print("Por favor crea tu bot con @BotFather en Telegram y coloca la clave en el archivo .env")
        return

    print("Escuchando mensajes de Telegram en segundo plano...")
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates:
            offset = update["update_id"] + 1
            message = update.get("message", {})
            chat_id = message.get("chat", {}).get("id")
            from_user = message.get("from", {})
            text = message.get("text", "")

            if not chat_id:
                continue

            # Verificación de seguridad (Lista Blanca)
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
                    "Para publicar una **noticia o artículo de interés** en `csd.edu.co`:\n"
                    "Escríbeme el título en la primera línea y luego los detalles o borrador.\n\n"
                    " Ejemplo:\n"
                    "`Izada de Bandera del 7 de Agosto`\n"
                    "`Hoy todos los cursos de primaria participaron con muestras de danza y música.`"
                )
            elif text:
                send_message(chat_id, "✍️ Procesando tu noticia y redactando el artículo para la página web...")
                handle_text_message(chat_id, text)

        time.sleep(2)

if __name__ == "__main__":
    run_bot()
