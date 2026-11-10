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
opener.open(req, timeout=15)

# Inspect prematriculas table in detail to see if there is an edit/view link or popup
html_transicion = opener.open(urllib.request.Request(f"{BASE_URL}/alumnos/semillero/2010/prematriculas/3", headers={"User-Agent": "Mozilla/5.0"})).read().decode("utf-8", errors="ignore")

# Find table row for one student, e.g., Sara Valentina Carreno Ruiz (1097922513) or Andres Felipe Martinez (1097922323)
matches = re.findall(r'<tr[^>]*>.*?1097922323.*?</tr>', html_transicion, re.DOTALL)
if matches:
    print("Found row for 1097922323:")
    print(matches[0][:1000])
else:
    print("Row not found in Transicion, let's search in all salones")
    # let's search across salones
    for sid in range(1, 15):
        h = opener.open(urllib.request.Request(f"{BASE_URL}/alumnos/semillero/2010/prematriculas/{sid}", headers={"User-Agent": "Mozilla/5.0"})).read().decode("utf-8", errors="ignore")
        if "1097922323" in h:
            print(f"Found 1097922323 in salón {sid}!")
            m = re.findall(r'<tr[^>]*>.*?1097922323.*?</tr>', h, re.DOTALL)
            if m:
                print(m[0][:1500])
            break
