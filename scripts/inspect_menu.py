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

resp_home = opener.open(urllib.request.Request(f"{BASE_URL}/alumnos/semillero/2010/", headers={"User-Agent": "Mozilla/5.0"})).read().decode("utf-8", errors="ignore")

# Find all <a> tags with text and href
all_links = re.findall(r'<a[^>]+href=[\'"]([^\'"]+)[\'"][^>]*>(.*?)</a>', resp_home, re.DOTALL)
for href, text in all_links:
    clean_text = re.sub(r'<[^>]+>', '', text).strip()
    if clean_text:
        print(f"{clean_text} -> {href}")
