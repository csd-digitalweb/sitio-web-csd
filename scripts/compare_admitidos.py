import urllib.request
import urllib.parse
import http.cookiejar
import csv
import io
import json
import hashlib
import re

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
login_data = urllib.parse.urlencode({'user': 'semillerosec', 'pwd': 'Semillero2025', 'hash': 'frmweb'}).encode('utf-8')
opener.open('https://educolombia.org/querys/usuarios/login.php', data=login_data)

rep16 = opener.open('https://educolombia.org/querys/excel/reportes.php?reporte=16', timeout=15).read().decode('utf-8', errors='ignore')
r16 = list(csv.DictReader(io.StringIO(rep16), delimiter=';'))

with open(r'C:\Users\julio\dev\sitio-web-csd\src\admisiones\admitidos_hash.json', encoding='utf-8') as f:
    local_hash = json.load(f)

# Also fetch from live site https://csd.edu.co/admisiones/admitidos_hash.json
try:
    live_json = json.loads(urllib.request.urlopen('https://csd.edu.co/admisiones/admitidos_hash.json', timeout=10).read().decode('utf-8'))
    print(f"Total en live csd.edu.co: {len(live_json)}")
except Exception as e:
    print("Error fetching live admitidos_hash.json:", e)
    live_json = {}

print(f"Total en Reporte 16 (EduColombia): {len(r16)}")
print(f"Total en local src/admisiones/admitidos_hash.json: {len(local_hash)}")

# Compare each student in Reporte 16
diffs = []
for row in r16:
    doc = re.sub(r'[^0-9]', '', row.get('doc', ''))
    if not doc:
        continue
    h = hashlib.sha256(doc.encode('utf-8')).hexdigest()
    salon_edu = row.get('nombre', '').strip()
    nombre_edu = f"{row.get('apellido1txt','')} {row.get('apellido2','')} {row.get('nombre1txt','')} {row.get('nombre2','')}".strip()
    
    in_local = local_hash.get(h)
    in_live = live_json.get(h)
    
    if not in_live:
        diffs.append(f"NUEVO (No en live): doc={doc}, nombre={nombre_edu}, salon={salon_edu}")
    elif in_live.get('salon') != salon_edu:
        diffs.append(f"CAMBIO DE SALON: doc={doc}, live={in_live.get('salon')} -> edu={salon_edu}")

print(f"\nDiferencias encontradas con el sitio en vivo ({len(diffs)}):")
for d in diffs:
    print(" *", d)
