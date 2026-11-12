import urllib.request
import urllib.parse
import http.cookiejar
import csv
import io

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
login_data = urllib.parse.urlencode({'user': 'semillerosec', 'pwd': 'Semillero2025', 'hash': 'frmweb'}).encode('utf-8')
opener.open('https://educolombia.org/querys/usuarios/login.php', data=login_data)

r1 = list(csv.DictReader(io.StringIO(opener.open('https://educolombia.org/querys/excel/reportes.php?reporte=1').read().decode('utf-8', errors='ignore')), delimiter=';'))
r16 = list(csv.DictReader(io.StringIO(opener.open('https://educolombia.org/querys/excel/reportes.php?reporte=16').read().decode('utf-8', errors='ignore')), delimiter=';'))

docs_r1 = set(r.get('doc', '').strip() for r in r1 if r.get('doc', '').strip())
print(f'Docs en Reporte 1: {len(docs_r1)}')
print(f'Docs en Reporte 16: {len(r16)}')

nuevos = [r for r in r16 if r.get('doc', '').strip() not in docs_r1]
print(f'Estudiantes en Reporte 16 pero NO en Reporte 1 ({len(nuevos)}):')
for n in nuevos:
    doc = n.get('doc', '')
    salon = n.get('nombre', '')
    nom = f"{n.get('apellido1txt','')} {n.get('apellido2','')} {n.get('nombre1txt','')} {n.get('nombre2','')}".strip()
    print(f"Doc: {doc:12} Salon: {salon:14} Nombre: {nom}")
