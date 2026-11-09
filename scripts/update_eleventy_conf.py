import pathlib

path = pathlib.Path(r"C:\Users\julio\dev\sitio-web-csd\.eleventy.js")
text = path.read_text(encoding="utf-8")

old_line = 'eleventyConfig.addPassthroughCopy({ "src/reserva-cupo/prematriculas_semillero.csv": "reserva-cupo/prematriculas_semillero.csv" });'
new_line = old_line + '\n  eleventyConfig.addPassthroughCopy({ "src/admisiones/admitidos_hash.json": "admisiones/admitidos_hash.json" });'

if old_line in text:
    text = text.replace(old_line, new_line)
    path.write_text(text, encoding="utf-8")
    print("SUCCESS")
else:
    print("NOT FOUND")
