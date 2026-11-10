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
req = urllib.request.Request(LOGIN_URL, data=login_data, headers={
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded"
})
opener.open(req, timeout=15)

html = opener.open(urllib.request.Request(f"{PREMAT_URL}/-1", headers={"User-Agent": "Mozilla/5.0"})).read().decode("utf-8", errors="ignore")

filas = re.findall(
    r"<tr class=['\"][^'\"]*['\"]>\s*<td>.*?rel-alu=['\"]([^'\"]+)['\"].*?"
    r"<td align=['\"]center['\"]>([0-9]+)</td>.*?"
    r"<span id=['\"]est-[^'\"]*['\"][^>]*>([^<]+)</span>.*?"
    r"name=['\"]pin['\"][^>]*value=['\"]([^\'\"]+)['\"].*?"
    r"(?:mail=['\"]([^'\"]*)['\"])?",
    html,
    re.DOTALL
)

print(f"Estudiantes en SIN ASIGNAR: {len(filas)}")
for f in filas:
    print(f"  • {f[1]} - {f[0].strip()} | Estado: {f[2]} | PIN: {f[3]}")
