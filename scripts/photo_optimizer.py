import os
from PIL import Image

def optimize_image(input_path, output_dir, max_dimension=1400, quality=82):
    """
    Optimiza y comprime una imagen para la web.
    - Reduce dimensiones si supera max_dimension.
    - Preserva la proporción de aspecto original.
    - Comprime el peso del archivo para carga ultra rápida en celulares.
    """
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.basename(input_path)
    name, ext = os.path.splitext(filename)
    output_filename = f"{name}.jpg"
    output_path = os.path.join(output_dir, output_filename)

    with Image.open(input_path) as img:
        # Convertir a RGB si es necesario (ej. PNG con transparencia o RGBA)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Calcular nuevas dimensiones manteniendo proporciones
        width, height = img.size
        if width > max_dimension or height > max_dimension:
            if width > height:
                new_width = max_dimension
                new_height = int(height * (max_dimension / width))
            else:
                new_height = max_dimension
                new_width = int(width * (max_dimension / height))
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Guardar comprimido
        img.save(output_path, "JPEG", quality=quality, optimize=True)

    return output_path

def process_gallery_photos(image_paths, event_slug, base_dir=r"C:\Users\julio\dev\sitio-web-csd"):
    """
    Procesa un grupo de fotos de un evento y las guarda en src/assets/galeria/<event_slug>/
    """
    output_dir = os.path.join(base_dir, "src", "assets", "galeria", event_slug)
    optimized_files = []

    for img_path in image_paths:
        if os.path.exists(img_path):
            out_file = optimize_image(img_path, output_dir)
            rel_path = f"/assets/galeria/{event_slug}/{os.path.basename(out_file)}"
            optimized_files.append(rel_path)

    return optimized_files

if __name__ == "__main__":
    print("Módulo optimizador de imágenes listo.")
