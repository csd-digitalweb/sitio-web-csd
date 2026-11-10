import urllib.request
import urllib.parse
import http.cookiejar
import re

BASE_URL = "https://educolombia.org"
LOGIN_URL = f"{BASE_URL}/querys/usuarios/login.php"
PREMAT_URL = f"{BASE_URL}/alumnos/semillero/2010/prematriculas"
USER = "semillerosec"
PWD = "Semillero2025"

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

login_data = urllib.parse.urlencode({"user": USER, "pwd": PWD}).encode("utf-8")
opener.open(urllib.request.Request(LOGIN_URL, data=login_data, headers={
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded"
}))

html_transicion = opener.open(urllib.request.Request(f"{PREMAT_URL}/3", headers={"User-Agent": "Mozilla/5.0"})).read().decode("utf-8", errors="ignore")

for tr in html_transicion.split('<tr'):
    if "1097922323" in tr:
        print("<tr" + tr[:tr.find('</tr>') + 5])
        break
