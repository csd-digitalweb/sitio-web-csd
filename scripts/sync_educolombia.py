#!/usr/bin/env python3
"""
Sincronizador automático desde EduColombia para Colegio CSD
Conecta con la plataforma EduColombia, extrae todos los salones y actualiza:
1. src/reserva-cupo/prematriculas_semillero.csv (Reporte completo)
2. src/reserva-cupo/prematriculas_hash.json (Consulta de PIN y reserva de cupos)
3. src/admisiones/admitidos_hash.json (Consulta de Admisión Paso 4 y asignación de salón para matrícula)
"""

import urllib.request
import urllib.parse
import http.cookiejar
import re
import json
import hashlib
import csv
import os
import sys

if sys.stdout and getattr(sys.stdout, 'encoding', None) and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_URL = "https://educolombia.org"
LOGIN_URL = f"{BASE_URL}/querys/usuarios/login.php"
PREMAT_URL = f"{BASE_URL}/alumnos/semillero/2010/prematriculas"

USER = "semillerosec"
PWD = "Semillero2025"

SALONES = [
    (1, "PREJARDIN"),
    (2, "JARDIN"),
    (3, "TRANSICION"),
    (4, "PRIMERO"),
    (5, "SEGUNDO"),
    (6, "TERCERO"),
    (7, "CUARTO"),
    (8, "QUINTO"),
    (9, "SEXTO"),
    (10, "SEPTIMO"),
    (11, "OCTAVO"),
    (12, "NOVENO"),
    (13, "DECIMO"),
    (14, "UNDECIMO"),
    (-1, "SIN ASIGNAR")
]

SIGUIENTE_GRADO = {
    "PREJARDIN": "JARDIN",
    "JARDIN": "TRANSICION",
    "TRANSICION": "PRIMERO",
    "PRIMERO": "SEGUNDO",
    "SEGUNDO": "TERCERO",
    "TERCERO": "CUARTO",
    "CUARTO": "QUINTO",
    "QUINTO": "SEXTO",
    "SEXTO": "SEPTIMO",
    "SEPTIMO": "OCTAVO",
    "OCTAVO": "NOVENO",
    "NOVENO": "DECIMO",
    "DECIMO": "UNDECIMO",
    "UNDECIMO": "EGRESADO",
    "SIN ASIGNAR": "SIN ASIGNAR"
}

def format_title_name(name):
    if not name:
        return ""
    clean = re.sub(r'[-_]', ' ', name)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return " ".join(w.capitalize() for w in clean.split())

def sync():
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

    print("🔐 [1/3] Iniciando sesión en EduColombia...")
    login_data = urllib.parse.urlencode({"user": USER, "pwd": PWD}).encode("utf-8")
    req = urllib.request.Request(LOGIN_URL, data=login_data, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Content-Type": "application/x-www-form-urlencoded"
    })
    
    try:
        resp = opener.open(req, timeout=15).read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"❌ Error conectando a EduColombia: {e}")
        sys.exit(1)

    if "OK++||semillero" not in resp:
        print(f"❌ Error en autenticación con EduColombia: {resp}")
        sys.exit(1)
    print("✅ Sesión iniciada con éxito.")

    estudiantes = []
    print("📥 [2/3] Extrayendo prematrículas de los salones...")

    for sid, sname in SALONES:
        url = f"{PREMAT_URL}/{sid}"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })
        try:
            html = opener.open(req, timeout=15).read().decode("utf-8", errors="ignore")
        except Exception as e:
            print(f"⚠️ Error obteniendo salón {sname}: {e}")
            continue

        filas = re.findall(
            r"<tr class=['\"][^'\"]*['\"]>\s*<td>.*?rel-alu=['\"]([^'\"]+)['\"].*?"
            r"<td align=['\"]center['\"]>([0-9]+)</td>.*?"
            r"<span id=['\"]est-[^'\"]*['\"][^>]*>([^<]+)</span>.*?"
            r"name=['\"]pin['\"][^>]*value=['\"]([^\'\"]+)['\"].*?"
            r"(?:mail=['\"]([^'\"]*)['\"])?",
            html,
            re.DOTALL
        )

        for match in filas:
            alu_nombre = re.sub(r'[-_]', ' ', match[0])
            alu_nombre = re.sub(r'\s+', ' ', alu_nombre).strip()
            
            documento = match[1].strip()
            estado = match[2].strip()
            pin = match[3].strip()
            mail = (match[4] or "").strip()

            estudiantes.append({
                "documento": documento,
                "nombre": alu_nombre,
                "nombre_display": format_title_name(alu_nombre),
                "grado": sname,
                "estado": estado,
                "pin": pin,
                "email": mail
            })
        print(f"  • {sname:12}: {len(filas)} estudiantes")

    total = len(estudiantes)
    confirmados = sum(1 for e in estudiantes if "sigue" in e["estado"].lower())
    pendientes = total - confirmados
    print(f"\n📊 Total estudiantes: {total} | Confirmados (Cupo Apartado): {confirmados} | Pendientes: {pendientes}")

    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_reserva = os.path.join(repo_dir, "src", "reserva-cupo")
    target_admisiones = os.path.join(repo_dir, "src", "admisiones")
    os.makedirs(target_reserva, exist_ok=True)
    os.makedirs(target_admisiones, exist_ok=True)

    # 1. Guardar CSV de reserva de cupo
    csv_path = os.path.join(target_reserva, "prematriculas_semillero.csv")
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Documento", "Nombre Completo", "Grado", "Estado", "PIN Prematricula", "Email Acudiente"])
        for est in estudiantes:
            writer.writerow([
                est["documento"],
                est["nombre"],
                est["grado"],
                est["estado"],
                est["pin"],
                est["email"]
            ])
    print(f"💾 [3/3] Guardado CSV: {csv_path}")

    # 2. Guardar JSON con Hash SHA-256 para Reserva de Cupos (Antiguos)
    hash_data = {}
    for est in estudiantes:
        doc_clean = re.sub(r'[^0-9]', '', est["documento"])
        doc_hash = hashlib.sha256(doc_clean.encode("utf-8")).hexdigest()
        hash_data[doc_hash] = {
            "nombre": est["nombre_display"],
            "grado": est["grado"],
            "pin": est["pin"],
            "estado": est["estado"]
        }

    json_path = os.path.join(target_reserva, "prematriculas_hash.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(hash_data, f, ensure_ascii=False, indent=2)
    print(f"💾 Guardado JSON de Reserva de Cupo: {json_path}")

    # 3. Actualizar JSON con Hash SHA-256 para Admisiones (Paso 4 - Asignación de Salón para Matrícula)
    adm_path = os.path.join(target_admisiones, "admitidos_hash.json")
    adm_data = {}
    if os.path.exists(adm_path):
        try:
            with open(adm_path, "r", encoding="utf-8") as f:
                adm_data = json.load(f)
        except Exception as e:
            print(f"⚠️ Error leyendo admitidos_hash.json existente: {e}")

    # Actualizar o agregar salón según la asignación en vivo de EduColombia
    actualizados_adm = 0
    for est in estudiantes:
        doc_clean = re.sub(r'[^0-9]', '', est["documento"])
        doc_hash = hashlib.sha256(doc_clean.encode("utf-8")).hexdigest()
        
        salon_actual = est["grado"]
        grado_2027 = SIGUIENTE_GRADO.get(salon_actual, salon_actual)

        if doc_hash in adm_data:
            # Mantener acudiente/doc_acudiente/celular si ya existen, y actualizar salón en vivo
            registro = adm_data[doc_hash]
            registro["salon"] = salon_actual
            registro["grado_2027"] = grado_2027
            registro["nombre"] = est["nombre_display"]
            actualizados_adm += 1
        else:
            # Nuevo estudiante registrado en EduColombia
            adm_data[doc_hash] = {
                "doc": doc_clean,
                "nombre": est["nombre_display"],
                "grado_2027": grado_2027,
                "salon": salon_actual,
                "acudiente": "Acudiente Registrado",
                "doc_acudiente": "",
                "celular": "",
                "estado_pago": "PENDIENTE"
            }
            actualizados_adm += 1

    with open(adm_path, "w", encoding="utf-8") as f:
        json.dump(adm_data, f, ensure_ascii=False, indent=2)
    print(f"💾 Guardado JSON de Admisiones y Asignación de Salón ({len(adm_data)} registros): {adm_path}")
    print("✨ Sincronización completada exitosamente.")

if __name__ == "__main__":
    sync()
