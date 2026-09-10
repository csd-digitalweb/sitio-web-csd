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

def extract_smart_title_and_idea(raw_text):
    """
    Analiza el texto enviado por el usuario para extraer o generar un título periodístico atractivo.
    """
    text = raw_text.strip()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    if not lines:
        return "Noticia Institucional CSD", "Información destacada de nuestra comunidad educativa."

    first_line = lines[0].replace("/noticia", "").strip()

    # Si la primera línea es corta (< 65 caracteres) y no es un párrafo completo largo
    if len(first_line) <= 65 and not (first_line.endswith('.') and len(first_line) > 40):
        title = first_line
        raw_idea = "\n\n".join(lines[1:]) if len(lines) > 1 else first_line
    else:
        # Generar un título atractivo analizando palabras clave en todo el texto
        lower_text = text.lower()
        if "matematica" in lower_text or "pensar" in lower_text or "ejercicio" in lower_text:
            title = "Desarrollo del Pensamiento Lógico y Matemático en el Colegio CSD"
        elif "motricidad" in lower_text or "preescolar" in lower_text or "fina" in lower_text:
            title = "Fortalecimiento de la Motricidad Fina y Creatividad en Preescolar"
        elif "uis" in lower_text or "universidad" in lower_text or "oferta" in lower_text:
            title = "Estudiantes CSD Conocen la Oferta Académica de la UIS"
        elif "etica" in lower_text or "valores" in lower_text or "aula" in lower_text:
            title = "Formación en Ética y Valores en las Aulas del Colegio CSD"
        elif "futbol" in lower_text or "deporte" in lower_text or "interclases" in lower_text:
            title = "Jornada Deportiva e Interclases en el Colegio CSD"
        elif "izada" in lower_text or "bandera" in lower_text or "patria" in lower_text:
            title = "Izada de Bandera y Celebración de Valores Patrios CSD"
        else:
            words = re.findall(r'\b\w+\b', first_line)
            title = " ".join(words[:7]).capitalize()
            if not title:
                title = "Actividad Institucional Colegio CSD"

        raw_idea = text

    return clean_text_orthography(title), clean_text_orthography(raw_idea)

def enhance_article_text(title, raw_idea):
    """
    Transforma un borrador o mensaje informal en un artículo periodístico profundo,
    con gancho, estructura institucional y redacción profesional.
    """
    title_clean, idea_clean = extract_smart_title_and_idea(f"{title}\n{raw_idea}")

    p1_hook = (
        f"Con gran orgullo y entusiasmo, la comunidad educativa del **Colegio CSD (Sede La Cumbre)** "
        f"destaca el desarrollo y aprendizaje alcanzado en la jornada de **{title_clean}**."
    )

    p2_body = (
        f"Nuestros estudiantes participan activamente en experiencias pedagógicas que fortalecen sus habilidades "
        f"y competencias integrales. {idea_clean} La constante guía de nuestro cuerpo docente promueve el análisis, "
        f"la curiosidad y el deseo constante de superación en cada salón de clases."
    )

    p3_values = (
        f"En el **Colegio CSD**, respaldamos cada actividad bajo nuestros tres pilares institucionales: "
        f"**Estudio, Amor y Paz**, brindando salones pequeños, atención personalizada y formación académica exigente "
        f"desde los primeros años."
    )

    p4_closing = (
        f"Felicitamos a todos los estudiantes y docentes por su dedicación y reafirmamos nuestro compromiso "
        f"de seguir construyendo juntos una educación con excelencia y calidez humana."
    )

    cuerpo_completo = f"{p1_hook}\n\n{p2_body}\n\n{p3_values}\n\n{p4_closing}"

    resumen = (
        f"Nuestra comunidad escolar del Colegio CSD resalta la importancia y los logros alcanzados "
        f"durante la jornada de {title_clean.lower()}."
    )

    return title_clean, resumen, cuerpo_completo

def create_news_article(title, raw_idea, category="Noticias", author="Equipo Pedagógico CSD", portada="", published=True):
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")

    title_clean, resumen, cuerpo = enhance_article_text(title, raw_idea)
    slug = slugify(title_clean)
    filename = f"{date_str}-{slug}.md"
    file_path = os.path.join(BASE_DIR, "src", "noticias", filename)

    if not portada:
        portada = DEFAULT_PORTADA

    # Si hay una imagen de portada adjunta, la incluimos al inicio del cuerpo del artículo
    cuerpo_con_foto = cuerpo
    if portada and portada != DEFAULT_PORTADA:
        cuerpo_con_foto = f"![{title_clean}]({portada})\n\n{cuerpo}"

    content = f"""---
title: "{title_clean}"
fecha: {date_str}
autor: "{author}"
categoria: "{category}"
resumen: "{resumen}"
portada: "{portada}"
publicado: {str(published).lower()}
---

{cuerpo_con_foto}
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
