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

# Let's inspect salón -1 ("SIN ASIGNAR") HTML
html_sin_asignar = opener.open(urllib.request.Request(f"{PREMAT_URL}/-1", headers={"User-Agent": "Mozilla/5.0"})).read().decode("utf-8", errors="ignore")

# Find table rows
rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html_sin_asignar, re.DOTALL)
print(f"Total rows in SIN ASIGNAR: {len(rows)}")
for r in rows[:5]:
    # strip tags
    cells = re.findall(r'<td[^>]*>(.*?)</td>', r, re.DOTALL)
    clean_cells = [re.sub(r'<[^>]+>', ' ', c).strip() for c in cells]
    print("Row cells:", clean_cells)
