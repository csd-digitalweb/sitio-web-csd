import os
import re
from datetime import datetime
from photo_optimizer import process_gallery_photos, optimize_image

BASE_DIR = r"C:\Users\julio\dev\sitio-web-csd"
DEFAULT_PORTADA = "/assets/logo.png"

# Diccionario de correcciones ortográficas y tipográficas frecuentes
CORRECTIONS = {
    r"\bmicrofutbolde\b": "microfútbol de",
    r"\bmicrofutbol\b": "microfútbol",
    r"\binterclses\b": "interclases",
    r"\binterclase\b": "interclases",
    r"\bcsd\b": "Colegio CSD",
    r"\bse jugo\b": "Se jugó",
    r"\bjugo\b": "jugó",
    r"\bdia\b": "día",
    r"\bdiversion\b": "diversión",
    r"\bizal\b": "izada",
    r"\bfisica\b": "física",
    r"\bquimica\b": "química",
    r"\bmatematicas\b": "matemáticas",
    r"\bpedagogico\b": "pedagógico",
    r"\bacademico\b": "académico",
    r"\bbachillerato\b": "Bachillerato",
    r"\bprimaria\b": "Primaria",
    r"\bpreescolar\b": "Preescolar",
}

def clean_text_orthography(text):
    """
    Corrige errores de ortografía, tildes y mayúsculas comunes.
    """
    cleaned = text
    for pattern, replacement in CORRECTIONS.items():
        cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)

    # Asegurar mayúscula inicial
    if cleaned and len(cleaned) > 0:
        cleaned = cleaned[0].upper() + cleaned[1:]

    return cleaned

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
    Transforma un borrador o mensaje informal en un artículo periodístico profundo,
    con gancho, estructura institucional y redacción profesional.
    """
    title_clean = clean_text_orthography(title)
    idea_clean = clean_text_orthography(raw_idea)

    # Construcción de un artículo periodístico estructurado con gancho
    p1_hook = (
        f"Con gran entusiasmo y un ambiente lleno de alegría, nuestra comunidad educativa del "
        f"**Colegio CSD (Sede La Cumbre)** vivió una jornada destacada en el desarrollo del evento: "
        f"**{title_clean}**."
    )

    p2_body = (
        f"Durante la jornada, nuestros estudiantes demostraron su compromiso, talento y espíritu de superación. "
        f"{idea_clean} La participación activa de los alumnos y el acompañamiento docente reafirmaron el valor "
        f"del aprendizaje vivencial y el trabajo en equipo dentro y fuera del aula de clase."
    )

    p3_values = (
        f"En el **Colegio CSD**, cada actividad deportiva, cultural y académica se enmarca en nuestras tres "
        f"columnas fundamentales: **Estudio, Amor y Paz**. Fomentamos un entorno de convivencia sana, respeto mutuo "
        f"y desarrollo integral para preparar a nuestros jóvenes como líderes con principios sólidos."
    )

    p4_closing = (
        f"Felicitamos a todos los participantes por su excelente entrega y agradecemos de corazón a las familias "
        f"por su constante confianza y respaldo a cada una de las iniciativas de nuestro colegio."
    )

    cuerpo_completo = f"{p1_hook}\n\n{p2_body}\n\n{p3_values}\n\n{p4_closing}"

    resumen = (
        f"Una jornada inolvidable de integración y aprendizaje vivió nuestra comunidad escolar en el "
        f"Colegio CSD durante el evento de {title_clean.lower()}."
    )

    return title_clean, resumen, cuerpo_completo

def create_news_article(title, raw_idea, category="Noticias", author="Equipo Pedagógico CSD", portada="", published=True):
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")

    title_clean, resumen, cuerpo = enhance_article_text(title, raw_idea)
    slug = slugify(title_clean)
    filename = f"{date_str}-{slug}.md"
    file_path = os.path.join(BASE_DIR, "src", "noticias", filename)

    # Si no tiene portada asignada, usar la portada por defecto institucional
    if not portada:
        portada = DEFAULT_PORTADA

    content = f"""---
title: "{title_clean}"
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
    title_clean = clean_text_orthography(title)
    desc_clean = clean_text_orthography(description)

    slug = slugify(title_clean)
    filename = f"{date_str}-{slug}.md"
    file_path = os.path.join(BASE_DIR, "src", "galeria", filename)

    optimized_rel_paths = process_gallery_photos(photo_paths, slug, BASE_DIR)
    fotos_yaml = "\n".join([f'  - src: "{p}"' for p in optimized_rel_paths])

    content = f"""---
title: "{title_clean}"
fecha: {date_str}
descripcion: "{desc_clean}"
publicado: {str(published).lower()}
fotos:
{fotos_yaml}
---
"""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return file_path, filename

def approve_content_file(folder_name, filename):
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
    print("Motor mejorado del Community Manager listo.")
