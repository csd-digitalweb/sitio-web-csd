import urllib.request
import json
import hashlib

# Load live admitidos_hash.json
adm_url = 'https://csd.edu.co/admisiones/admitidos_hash.json'
adm_db = json.loads(urllib.request.urlopen(adm_url).read().decode('utf-8'))

# Load live prematriculas_hash.json
res_url = 'https://csd.edu.co/reserva-cupo/prematriculas_hash.json'
res_db = json.loads(urllib.request.urlopen(res_url).read().decode('utf-8'))

test_docs = ['1097922547', '1142727051', '1234343032', '1234342096', '1097917913', '1097507078', '1142619412', '1025146048', '1095846190']

print("=== PRUEBA EN ADMISIONES (Paso 4: Consulta de Admisión) ===")
for doc in test_docs:
    h = hashlib.sha256(doc.encode('utf-8')).hexdigest()
    est = adm_db.get(h)
    if est:
        salon = est.get('salon', '')
        if salon and salon != 'SIN ASIGNAR':
            print(f"Doc {doc} ({est.get('nombre')}): ADMITIDO CON SALÓN -> {salon}. Grado 2027: {est.get('grado_2027')}")
        else:
            print(f"Doc {doc} ({est.get('nombre')}): NO ADMITIDO / SIN SALÓN ASIGNADO (salon='{salon}')")
    else:
        print(f"Doc {doc}: NO EXISTE en base de admisiones")

print("\n=== PRUEBA EN RESERVA-CUPO (Antiguos) ===")
for doc in test_docs:
    h = hashlib.sha256(doc.encode('utf-8')).hexdigest()
    est = res_db.get(h)
    if est:
        estado = est.get('estado', '')
        prom = est.get('promovido', 0)
        print(f"Doc {doc} ({est.get('nombre')}): estado='{estado}', promovido={prom}")
    else:
        print(f"Doc {doc}: NO EXISTE en reserva-cupo")
