#!/usr/bin/env python3
"""
Demonio de Sincronización en Vivo con EduColombia - Colegio CSD
Ejecuta la sincronización cada 3 minutos de forma silenciosa en segundo plano.
Si detecta nuevos cupos apartados en EduColombia, publica inmediatamente a la web.
"""

import time
import os
import sys

BASE_DIR = r"C:\Users\julio\dev\sitio-web-csd"
sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))

LOG_FILE = os.path.join(BASE_DIR, "scripts", "sync_daemon.log")

class TeeLogger:
    def __init__(self, filepath, orig_stream):
        self.file = open(filepath, "a", encoding="utf-8", buffering=1)
        self.orig = orig_stream

    def write(self, data):
        try:
            self.file.write(data)
            self.file.flush()
        except Exception:
            pass
        if self.orig:
            try:
                self.orig.write(data)
                self.orig.flush()
            except Exception:
                pass

    def flush(self):
        try:
            self.file.flush()
        except Exception:
            pass
        if self.orig:
            try:
                self.orig.flush()
            except Exception:
                pass

sys.stdout = TeeLogger(LOG_FILE, sys.stdout)
sys.stderr = TeeLogger(LOG_FILE, sys.stderr)

from auto_sync import check_and_publish

INTERVAL_SECONDS = 180  # 3 minutos

def main():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Demonio de sincronización en vivo CSD iniciado (frecuencia: cada 3 minutos)...")
    while True:
        try:
            check_and_publish()
        except Exception as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Error en ciclo de sincronización: {e}")
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
