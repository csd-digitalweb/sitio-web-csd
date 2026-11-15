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

rep16 = opener.open('https://educolombia.org/querys/excel/reportes.php?reporte=16').read().decode('utf-8', errors='ignore')
r16 = list(csv.DictReader(io.StringIO(rep16), delimiter=';'))

with open(r'C:\Users\julio\dev\sitio-web-csd\src\admisiones\admitidos_hash.json', encoding='utf-8') as f:
    local_hash = json.load(f)

for row in r16:
    doc = re.sub(r'[^0-9]', '', row.get('doc', ''))
    if not doc:
        continue
    h = hashlib.sha256(doc.encode('utf-8')).hexdigest()
    salon_edu = row.get('nombre', '').strip()
    nom = f"{row.get('apellido1txt','')} {row.get('apellido2','')} {row.get('nombre1txt','')} {row.get('nombre2','')}".strip()
    
    if h not in local_hash:
        print(f"NO ESTA EN LOCAL HASH: doc={doc} salon={salon_edu} nom={nom}")
    elif local_hash[h].get('salon') != salon_edu:
        print(f"SALON CAMBIO: doc={doc} local={local_hash[h].get('salon')} edu={salon_edu} nom={nom}")
