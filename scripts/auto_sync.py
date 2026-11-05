#!/usr/bin/env python3
"""
Sincronización Continua y Publicación Automática con EduColombia para Colegio CSD
Conecta con EduColombia, detecta cupos nuevos y, si hay cambios, publica inmediatamente a GitHub Pages.
"""

import os
import sys
import subprocess
import time

if sys.stdout.encoding.lower() != 'utf-8':
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

    # Verificar si hubo cambios en los archivos de prematrícula
    res = subprocess.run(["git", "status", "--porcelain"], cwd=BASE_DIR, capture_output=True, text=True)
    if "prematriculas" in res.stdout:
        print("⚡ Nuevos cupos o cambios detectados. Publicando a la web en vivo...")
        success, msg = publish_to_web("chore(sync): actualizar cupos confirmados en vivo desde EduColombia")
        print(f"Estado de publicación: {msg}")
    else:
        print("✅ Base de datos al día. No hay cambios pendientes.")

if __name__ == "__main__":
    check_and_publish()
