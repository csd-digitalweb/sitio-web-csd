import urllib.request
import urllib.parse
import http.cookiejar
import re

BASE_URL = "https://educolombia.org"
LOGIN_URL = f"{BASE_URL}/querys/usuarios/login.php"
USER = "semillerosec"
PWD = "Semillero2025"

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

login_data = urllib.parse.urlencode({"user": USER, "pwd": PWD}).encode("utf-8")
req = urllib.request.Request(LOGIN_URL, data=login_data, headers={
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded"
})
resp = opener.open(req, timeout=15).read().decode("utf-8", errors="ignore")
print("Login response:", resp[:200])

# Inspect main panel or routes
req_home = urllib.request.Request(f"{BASE_URL}/alumnos/semillero/2010/", headers={"User-Agent": "Mozilla/5.0"})
try:
    resp_home = opener.open(req_home, timeout=15).read().decode("utf-8", errors="ignore")
    print("Home length:", len(resp_home))
    links = re.findall(r'href=[\'"]([^\'"]+)[\'"]', resp_home)
    for l in sorted(set(links)):
        if any(k in l.lower() for k in ["premat", "inscri", "admis", "matri", "alumno", "salon", "cupo", "estudiant", "aspiran", "nuevo"]):
            print("Link:", l)
except Exception as e:
    print("Error fetching home:", e)

# Also test known URLs or querys
test_urls = [
    f"{BASE_URL}/alumnos/semillero/2010/prematriculas",
    f"{BASE_URL}/alumnos/semillero/2010/inscripciones",
    f"{BASE_URL}/alumnos/semillero/2010/admisiones",
    f"{BASE_URL}/alumnos/semillero/2010/matriculas",
    f"{BASE_URL}/alumnos/semillero/2010/aspirantes",
    f"{BASE_URL}/alumnos/semillero/2010/nuevos",
    f"{BASE_URL}/alumnos/semillero/2010/listas",
    f"{BASE_URL}/alumnos/semillero/2010/salones",
]

for url in test_urls:
    try:
        r = opener.open(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=10)
        c = r.read().decode("utf-8", errors="ignore")
        print(f"URL: {url} -> Status: {r.status}, Length: {len(c)}")
        title = re.findall(r'<title>([^<]+)</title>', c, re.IGNORECASE)
        print("   Title:", title)
    except Exception as e:
        print(f"URL: {url} -> Error: {e}")
