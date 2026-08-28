import os
import re
from datetime import datetime
from photo_optimizer import process_gallery_photos

BASE_DIR = r"C:\Users\julio\dev\sitio-web-csd"

def slugify(text):
    text = text.lower()
    text = re.sub(r'[áäâà]', 'a', text)
    text = re.sub(r'[éëêè]', 'e', text)
    text = re.sub(r'[íïîì]', 'i', text)
    text = re.sub(r'[óöôò]', 'o', text)
    text = re.sub(r'[úüûù]', 'u', text)
    text = re.sub(r'[ñ]', 'n', text)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text).strip('-')
    return text[:50]

def enhance_article_text(title, raw_idea):
    """
    Toma una idea cruda o punteada y la expande a un artículo institucional formal,
    cálido y profesional para el Colegio CSD.
    """
    paragraphs = [p.strip() for p in raw_idea.split('\n') if p.strip()]
    cuerpo = "\n\n".join(paragraphs)

    # Si la idea es muy breve, darle estructura institucional enriquecida
    if len(raw_idea) < 150:
        cuerpo = (
            f"En el **Colegio CSD (Sede La Cumbre)**, nos llena de orgullo compartir las actividades "
            f"y logros de nuestra comunidad educativa.\n\n"
            f"{raw_idea}\n\n"
            f"Continuamos trabajando día a día bajo nuestro lema de **Estudio, Amor y Paz**, "
            f"brindando una educación personalizada, un ambiente seguro y una formación de excelencia."
        )

    resumen = paragraphs[0][:160] + "..." if paragraphs else f"Noticia sobre {title} en el Colegio CSD."
    return resumen, cuerpo

def create_news_article(title, raw_idea, category="Noticias", author="Equipo Pedagógico CSD", portada="", published=True):
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    slug = slugify(title)
    filename = f"{date_str}-{slug}.md"
    file_path = os.path.join(BASE_DIR, "src", "noticias", filename)

    resumen, cuerpo = enhance_article_text(title, raw_idea)

    content = f"""---
title: "{title}"
fecha: {date_str}
autor: "{author}"
categoria: "{category}"
resumen: "{resumen}"
portada: "{portada}"
publicado: {str(published).lower()}
---

{cuerpo}
"""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return file_path, filename

def create_gallery_album(title, description, photo_paths, published=True):
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    slug = slugify(title)
    filename = f"{date_str}-{slug}.md"
    file_path = os.path.join(BASE_DIR, "src", "galeria", filename)

    # Procesar y optimizar fotos
    optimized_rel_paths = process_gallery_photos(photo_paths, slug, BASE_DIR)

    fotos_yaml = "\n".join([f'  - src: "{p}"' for p in optimized_rel_paths])

    content = f"""---
title: "{title}"
fecha: {date_str}
descripcion: "{description}"
publicado: {str(published).lower()}
fotos:
{fotos_yaml}
---
"""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return file_path, filename

def approve_content_file(folder_name, filename):
    """
    Cambia el estado de publicado: false a publicado: true en un archivo de noticias o galería.
    Sin límite de tiempo.
    """
    file_path = os.path.join(BASE_DIR, "src", folder_name, filename)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("publicado: false", "publicado: true")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

if __name__ == "__main__":
    print("Motor del Community Manager listo.")
