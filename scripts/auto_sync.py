#!/usr/bin/env python3
"""
Sincronización Continua y Publicación Automática con EduColombia para Colegio CSD
Conecta con EduColombia, detecta cupos y salones nuevos y, si hay cambios, publica inmediatamente a la web.
"""

import os
import sys
import subprocess
import time

if sys.stdout and getattr(sys.stdout, 'encoding', None) and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = r"C:\Users\julio\dev\sitio-web-csd"
sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))

from sync_educolombia import sync
from publisher import publish_to_web

def check_and_publish():
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Iniciando verificación con EduColombia...")
    sync()

    # 1. Verificar si hay cambios en los archivos de prematrícula o admisiones
    res_status = subprocess.run(["git", "status", "--porcelain"], cwd=BASE_DIR, capture_output=True, text=True)
    # 2. Verificar si hay commits locales pendientes de subir a origin/main
    subprocess.run(["git", "fetch", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
    res_ahead = subprocess.run(["git", "log", "origin/main..HEAD", "--oneline"], cwd=BASE_DIR, capture_output=True, text=True)

    has_file_changes = "prematriculas" in res_status.stdout or "admitidos" in res_status.stdout
    has_unpushed_commits = bool(res_ahead.stdout.strip())

    if has_file_changes or has_unpushed_commits:
        print("⚡ Nuevos cupos o cambios pendientes por publicar. Publicando a la web en vivo...")
        success, msg = publish_to_web("chore(sync): actualizar cupos y asignación de salones desde EduColombia")
        print(f"Estado de publicación: {msg}")
    else:
        print("✅ Base de datos al día. No hay cambios pendientes.")

if __name__ == "__main__":
    check_and_publish()
