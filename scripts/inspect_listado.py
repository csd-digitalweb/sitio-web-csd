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

resp_listado = opener.open(urllib.request.Request(f"{BASE_URL}/alumnos/semillero/2010/listado", headers={"User-Agent": "Mozilla/5.0"})).read().decode("utf-8", errors="ignore")
print("Listado length:", len(resp_listado))

# Find buttons, selects, links, forms
forms = re.findall(r'<form[^>]*action=[\'"]([^\'"]*)[\'"][^>]*>(.*?)</form>', resp_listado, re.DOTALL)
for act, body in forms:
    print("Form action:", act)
    inputs = re.findall(r'<input[^>]+name=[\'"]([^\'"]+)[\'"]', body)
    selects = re.findall(r'<select[^>]+name=[\'"]([^\'"]+)[\'"]', body)
    print("  inputs:", inputs)
    print("  selects:", selects)

links = re.findall(r'<a[^>]+href=[\'"]([^\'"]+)[\'"][^>]*>(.*?)</a>', resp_listado, re.DOTALL)
for href, txt in links:
    clean_txt = re.sub(r'<[^>]+>', '', txt).strip()
    if any(k in href.lower() or k in clean_txt.lower() for k in ["salon", "alumno", "matri", "premat", "nuevo", "aspiran", "buscar", "filtro", "2027", "2026"]):
        print(f"Listado Link: {clean_txt} -> {href}")
