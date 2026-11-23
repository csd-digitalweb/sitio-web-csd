import json
import hashlib
import re

with open(r'C:\Users\julio\dev\sitio-web-csd\src\reserva-cupo\prematriculas_hash.json', encoding='utf-8') as f:
    db = json.load(f)

def test_consultar(raw_doc):
    doc = raw_doc if '_prom' in raw_doc else re.sub(r'[^0-9]', '', raw_doc)
    h = hashlib.sha256(doc.encode('utf-8')).hexdigest()
    alumno = db.get(h)
    if alumno and alumno.get('pin'):
        estado = (alumno.get('estado') or '').lower()
        ha_apartado = ('sigue' in estado or 'confirmad' in estado) and ('sin' not in estado)
        promovido = alumno.get('promovido')
        if not ha_apartado:
            return f"CASO C (Sin apartar cupo): {alumno.get('nombre')} - PIN: {alumno.get('pin')}"
        elif promovido in [1, '1', True]:
            return f"CASO A (Promovido): {alumno.get('nombre')} - Grado 2027: {alumno.get('grado_siguiente')}"
        else:
            return f"CASO B (Cupo apartado + espera notas): {alumno.get('nombre')} - Grado recibe: {alumno.get('grado_siguiente')}"
    else:
        return f"ERROR (No encontrado): {raw_doc}"

print("1. Con dots 1.102.645.772 ->", test_consultar("1.102.645.772"))
print("2. Normal 1102645772 ->", test_consultar("1102645772"))
print("3. Sin confirmar 1097795465 ->", test_consultar("1097795465"))
print("4. Demo promovido 1097917913_prom ->", test_consultar("1097917913_prom"))
print("5. Inexistente 9999999999 ->", test_consultar("9999999999"))
