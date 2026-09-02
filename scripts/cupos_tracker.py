import os
import json
import datetime
from telegram_bot import send_message, DIRECTOR_CHAT_ID

BASE_DIR = r"C:\Users\julio\dev\sitio-web-csd"
DATA_FILE = os.path.join(BASE_DIR, "data", "reservas_cupo.json")

def load_reservas():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_reserva(estudiante, grado, acudiente, telefono, confirmacion, observaciones=""):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    reservas = load_reservas()
    
    registro = {
        "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estudiante": estudiante,
        "grado": grado,
        "acudiente": acudiente,
        "telefono": telefono,
        "confirmacion": confirmacion,
        "observaciones": observaciones
    }
    
    # Evitar duplicados por estudiante
    reservas = [r for r in reservas if r.get("estudiante", "").strip().lower() != estudiante.strip().lower()]
    reservas.append(registro)
    
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(reservas, f, ensure_ascii=False, indent=2)
        
    return registro

def generate_weekly_report():
    reservas = load_reservas()
    total = len(reservas)
    
    confirmados = [r for r in reservas if "SÍ" in r.get("confirmacion", "").upper() or "CONFIRMO" in r.get("confirmacion", "").upper()]
    rechazados = [r for r in reservas if "NO" in r.get("confirmacion", "").upper()]
    dudas = [r for r in reservas if "DUDA" in r.get("confirmacion", "").upper() or "PENDIENTE" in r.get("confirmacion", "").upper()]
    
    # Agrupar por grado
    por_grado = {}
    for r in confirmados:
        g = r.get("grado", "Sin Grado Specified")
        por_grado[g] = por_grado.get(g, 0) + 1

    reporte_grados = "\n".join([f"  • *{g}:* {cant} estudiantes" for g, cant in sorted(por_grado.items())])
    if not reporte_grados:
        reporte_grados = "  • _Aún no hay confirmaciones registradas esta semana._"

    report_text = f"""📊 *REPORTE SEMANAL DE RESERVA DE CUPOS — COLEGIO CSD*
📅 *Fecha del Informe:* {datetime.datetime.now().strftime('%d/%m/%Y')}

✅ *Cupos Confirmados (SÍ continúan):* {len(confirmados)}
❌ *No continúan el próximo año:* {len(rechazados)}
❓ *En duda / Pendientes:* {len(dudas)}
📈 *Total Respuestas Procesadas:* {total}

---
🎒 *DESGLOSE DE CUPOS CONFIRMADOS POR GRADO:*
{reporte_grados}

---
💡 _Este informe se genera automáticamente cada semana para el seguimiento de la Dirección del Colegio CSD._
"""
    return report_text

def send_weekly_report_to_telegram():
    report = generate_weekly_report()
    print(report)
    if DIRECTOR_CHAT_ID:
        send_message(DIRECTOR_CHAT_ID, report)
        print("Reporte enviado exitosamente al Telegram de la Dirección.")
    else:
        print("💡 DIRECTOR_CHAT_ID no configurado aún en .env. El reporte se imprimió en consola.")

if __name__ == "__main__":
    send_weekly_report_to_telegram()
