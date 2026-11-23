import urllib.request, urllib.parse, http.cookiejar, csv, io
from collections import Counter

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
login_data = urllib.parse.urlencode({'user': 'semillerosec', 'pwd': 'Semillero2025', 'hash': 'frmweb'}).encode('utf-8')
opener.open('https://educolombia.org/querys/usuarios/login.php', data=login_data)

try:
    rep19 = opener.open('https://educolombia.org/querys/excel/reportes.php?reporte=19').read().decode('utf-8', errors='ignore')
    r19 = list(csv.DictReader(io.StringIO(rep19), delimiter=';'))
    print(f"Reporte 19 tiene {len(r19)} registros.")
    if r19:
        print("Columnas rep 19:", list(r19[0].keys()))
        oks = Counter(r.get('ok', '') for r in r19)
        print("Valores de ok en rep 19:", dict(oks))
        for r in r19[:5]:
            print(r)
except Exception as e:
    print("Error rep 19:", e)
