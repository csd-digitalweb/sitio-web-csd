import urllib.request
import urllib.parse
import http.cookiejar
import csv
import io
import json

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')]

login_data = urllib.parse.urlencode({'user': 'semillerosec', 'pwd': 'Semillero2025', 'hash': 'frmweb'}).encode('utf-8')
opener.open('https://educolombia.org/querys/usuarios/login.php', data=login_data)

rep16 = opener.open('https://educolombia.org/querys/excel/reportes.php?reporte=16', timeout=15).read().decode('utf-8', errors='ignore')
r16 = list(csv.DictReader(io.StringIO(rep16), delimiter=';'))

# Check which students are in SIN ASIGNAR
sin_asignar = [r for r in r16 if r.get('nombre', '').strip() == 'SIN ASIGNAR']
print(f"Total SIN ASIGNAR: {len(sin_asignar)}")
for r in sin_asignar[:10]:
    print(r.get('doc'), r.get('apellido1txt'), r.get('nombre1txt'), r.get('nombre'))

# Also check if there are other reports or PIN registrations
# Let's check reportes available: 1 to 20
for i in range(1, 25):
    try:
        res = opener.open(f'https://educolombia.org/querys/excel/reportes.php?reporte={i}', timeout=5)
        raw = res.read().decode('utf-8', errors='ignore')
        lines = [l for l in raw.split('\n') if l.strip()]
        if len(lines) > 1 and ';' in lines[0]:
            print(f"Reporte {i}: {len(lines)} lineas. Header: {lines[0][:80]}")
    except Exception:
        pass
