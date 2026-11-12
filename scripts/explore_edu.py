import urllib.request
import urllib.parse
import http.cookiejar
import re
import csv
import io
import json

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')]

login_data = urllib.parse.urlencode({'user': 'semillerosec', 'pwd': 'Semillero2025', 'hash': 'frmweb'}).encode('utf-8')
opener.open('https://educolombia.org/querys/usuarios/login.php', data=login_data)

# Check panel html
try:
    resp = opener.open('https://educolombia.org/panel/').read().decode('utf-8', errors='ignore')
    found = re.findall(r'href=["\']([^"\']+)["\']', resp)
    print("Links en panel:")
    for l in set(found):
        if any(k in l.lower() for k in ['alumno', 'matricula', 'aspirante', 'reporte', 'pin', 'inscrip', 'nuevo', 'admision']):
            print("  ", l)
except Exception as e:
    print("Error panel:", e)

# Also check Reporte 16 in detail
try:
    rep16 = opener.open('https://educolombia.org/querys/excel/reportes.php?reporte=16', timeout=15).read().decode('utf-8', errors='ignore')
    r16 = list(csv.DictReader(io.StringIO(rep16), delimiter=';'))
    print(f"\nReporte 16 tiene {len(r16)} registros.")
    # Salones en reporte 16:
    from collections import Counter
    salones = Counter(r.get('nombre', '').strip() for r in r16)
    print("Salones en reporte 16:", dict(salones))
except Exception as e:
    print("Error rep 16:", e)
