import os
import sys
from community_manager import create_news_article, create_gallery_album
from publisher import publish_to_web

def main():
    print("\n" + "=" * 60)
    print(" 🏫 COMMUNITY MANAGER DEL COLEGIO CSD — PANEL INTERACTIVO")
    print("=" * 60)
    print("1. 📰 Redactar y Publicar una Nueva Noticia / Artículo de Interés")
    print("2. 📸 Publicar un Nuevo Álbum de Fotos de un Evento")
    print("3. 🚀 Sincronizar y Publicar Cambios Pendientes")
    print("4. ❌ Salir")
    print("-" * 60)

    option = input("Selecciona una opción (1-4): ").strip()

    if option == "1":
        print("\n--- 📰 CREAR NOTICIA O ARTÍCULO DE INTERÉS ---")
        title = input("Título de la noticia: ").strip()
        print("Categorías disponibles: [1] Noticias  [2] Convivencia  [3] Eventos  [4] Egresado destacado")
        cat_op = input("Selecciona categoría (1-4, por defecto 1): ").strip()
        cat_map = {"1": "Noticias", "2": "Convivencia", "3": "Eventos", "4": "Egresado destacado"}
        category = cat_map.get(cat_op, "Noticias")

        author = input("Autor (por defecto 'Equipo Pedagógico CSD'): ").strip() or "Equipo Pedagógico CSD"
        print("\nEscribe o pega el borrador/idea de la noticia (presiona Enter 2 veces para finalizar):")

        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        raw_idea = "\n".join(lines) if lines else title

        print("\n✍️ Redactando noticia...")
        file_path, filename = create_news_article(title, raw_idea, category=category, author=author, published=True)
        print(f"✅ Noticia guardada en: {filename}")

        pub = input("\n¿Deseas publicarla en vivo inmediatamente en csd.edu.co? (s/n): ").strip().lower()
        if pub == 's':
            print("🚀 Publicando en internet...")
            success, msg = publish_to_web(f"Nueva noticia: {title}")
            print(f"\n{msg}")

    elif option == "2":
        print("\n--- 📸 CREAR ÁLBUM DE FOTOS DE EVENTO ---")
        title = input("Título del evento (ej: Izada de Bandera agosto): ").strip()
        desc = input("Descripción corta del evento: ").strip()
        folder = input("Ruta de la carpeta con las fotos en tu computador: ").strip()

        if os.path.exists(folder):
            valid_exts = (".jpg", ".jpeg", ".png", ".webp")
            photo_paths = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(valid_exts)]
            if photo_paths:
                print(f"🖼️ Se encontraron {len(photo_paths)} fotos. Comprimiendo y procesando...")
                file_path, filename = create_gallery_album(title, desc, photo_paths, published=True)
                print(f"✅ Álbum guardado en: {filename}")

                pub = input("\n¿Deseas publicarlo en vivo inmediatamente en csd.edu.co? (s/n): ").strip().lower()
                if pub == 's':
                    print("🚀 Publicando en internet...")
                    success, msg = publish_to_web(f"Nuevo álbum de fotos: {title}")
                    print(f"\n{msg}")
            else:
                print("⚠️ No se encontraron imágenes en esa carpeta.")
        else:
            print("⚠️ La ruta ingresada no existe.")

    elif option == "3":
        print("\n🚀 Sincronizando y publicando en internet...")
        success, msg = publish_to_web("Actualización manual desde Community Manager")
        print(f"\n{msg}")

    else:
        print("¡Hasta pronto!")

if __name__ == "__main__":
    main()
