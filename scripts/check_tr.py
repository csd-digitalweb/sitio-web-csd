import urllib.request
import urllib.parse
import http.cookiejar
import re

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
login_data = urllib.parse.urlencode({'user': 'semillerosec', 'pwd': 'Semillero2025', 'hash': 'frmweb'}).encode('utf-8')
opener.open('https://educolombia.org/querys/usuarios/login.php', data=login_data)

for sid in [2, 3, 4, 8, 9, 10, 11, -1]:
    url = f'https://educolombia.org/alumnos/semillero/2010/prematriculas/{sid}'
    html = opener.open(url).read().decode('utf-8', errors='ignore')
    for doc in ['1097922547', '1142727051', '1234343032', '1234342096', '1097917913', '1097507078', '1142619412']:
        if doc in html:
            for tr in re.findall(r'<tr[^>]*>.*?</tr>', html, re.DOTALL):
                if doc in tr:
                    clean_tr = re.sub(r'\s+', ' ', tr)
                    print(f"Doc {doc} en salon {sid}: {clean_tr}")
