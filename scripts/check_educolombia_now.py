import urllib.request
import urllib.parse
import http.cookiejar
import csv
import io
import json

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
login_data = urllib.parse.urlencode({'user': 'semillerosec', 'pwd': 'Semillero2025', 'hash': 'frmweb'}).encode('utf-8')
opener.open('https://educolombia.org/querys/usuarios/login.php', data=login_data)

rep16 = opener.open('https://educolombia.org/querys/excel/reportes.php?reporte=16').read().decode('utf-8', errors='ignore')
r16 = list(csv.DictReader(io.StringIO(rep16), delimiter=';'))

# Check all students in Report 16 who have salon != SIN ASIGNAR
print(f"Total en Reporte 16: {len(r16)}")
for r in r16:
    salon = r.get('nombre', '').strip()
    doc = r.get('doc', '').strip()
    nom = f"{r.get('apellido1txt','')} {r.get('apellido2','')} {r.get('nombre1txt','')} {r.get('nombre2','')}".strip()
    if salon != 'SIN ASIGNAR':
        # Let's see if this student is in local admitidos_hash.json
        pass
    else:
        print(f"SIN ASIGNAR: doc={doc:12} nom={nom}")
