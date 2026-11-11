# -*- coding: utf-8 -*-
import os

filepath = r"C:\Users\julio\dev\sitio-web-csd\src\admisiones.njk"
with open(filepath, "r", encoding="utf-8") as f:
    c = f.read()

# Normalize line breaks
c = c.replace("\r\n", "\n")

# 1. Quick test buttons
old_tags = """        <!-- Acciones Rápidas para Pruebas del Evaluador -->
        <div style="margin-top:22px; padding-top:18px; border-top:1px solid rgba(255,255,255,0.15); text-align:center; font-size:0.84rem;">
          <span style="color:#CBD5E1; margin-right:8px;">Prueba rápida con 1 clic:</span>
          <button type="button" onclick="probarDocAdmision('1097138223')" style="background:rgba(255,255,255,0.16); border:1px solid rgba(255,201,27,0.5); color:#FFF; font-size:0.8rem; padding:5px 14px; border-radius:999px; cursor:pointer; margin:4px; font-weight:600;">
            ✅ Caso A: Con Salón Asignado (1097138223)
          </button>
          <button type="button" onclick="probarDocAdmision('9999999999')" style="background:rgba(255,255,255,0.16); border:1px solid rgba(255,255,255,0.3); color:#FFF; font-size:0.8rem; padding:5px 14px; border-radius:999px; cursor:pointer; margin:4px; font-weight:600;">
            ⏳ Caso B: Aún Sin Salón / En Revisión (9999999999)
          </button>
        </div>"""

new_tags = """        <!-- Acciones Rápidas para Pruebas del Evaluador -->
        <div style="margin-top:22px; padding-top:18px; border-top:1px solid rgba(255,255,255,0.15); text-align:center; font-size:0.84rem;">
          <span style="color:#CBD5E1; margin-right:8px;">Pruebas rápidas oficiales con 1 clic:</span>
          <button type="button" onclick="probarDocAdmision('1234342096')" style="background:#FEF3C7; border:1px solid #FDE68A; color:#92400E; font-size:0.8rem; padding:6px 14px; border-radius:999px; cursor:pointer; margin:4px; font-weight:700;">
            ⭐ Estudiante Nuevo Admitido: Miguel Moreno (1234342096)
          </button>
          <button type="button" onclick="probarDocAdmision('1142727051')" style="background:#E0E7FF; border:1px solid #C7D2FE; color:#3730A3; font-size:0.8rem; padding:6px 14px; border-radius:999px; cursor:pointer; margin:4px; font-weight:700;">
            ✅ Christopher Sanchez (1142727051)
          </button>
          <button type="button" onclick="probarDocAdmision('1097922547')" style="background:#FEE2E2; border:1px solid #FECACA; color:#991B1B; font-size:0.8rem; padding:6px 14px; border-radius:999px; cursor:pointer; margin:4px; font-weight:700;">
            ⏳ En Revisión / Sin Salón (1097922547)
          </button>
        </div>"""

# 2. Grado al que fue admitido
old_grado = """              <div>
                <span style="color:#64748B; font-size:0.78rem; text-transform:uppercase; font-weight:700; display:block;">Salón Asignado en EduColombia:</span>
                <span style="display:inline-block; background:#DCFCE7; color:#15803D; font-weight:800; font-size:0.95rem; padding:4px 12px; border-radius:999px; border:1px solid #86EFAC; margin-top:2px;" id="res-salon-educolombia">-</span>
              </div>
              <div>
                <span style="color:#64748B; font-size:0.78rem; text-transform:uppercase; font-weight:700; display:block;">Grado a Cursar en 2027:</span>
                <strong style="color:#2563EB; font-size:1.15rem; display:block; margin-top:2px;" id="res-grado-2027">-</strong>
              </div>"""

new_grado = """              <div style="grid-column: 1 / -1;">
                <span style="color:#64748B; font-size:0.8rem; text-transform:uppercase; font-weight:700; display:block;">Grado al que fué admitido en el 2027:</span>
                <strong style="color:#2563EB; font-size:1.3rem; text-transform:uppercase; display:block; margin-top:2px;" id="res-grado-admitido">-</strong>
                <span id="res-grado-2027" style="display:none;">-</span>
                <span id="res-salon-educolombia" style="display:none;">-</span>
              </div>"""

# 3. Precio $331.400
old_price = """.400 <span style="font-size:1.05rem; color:#64748B; font-weight:600;">COP</span>"""
new_price = """$331.400 <span style="font-size:1.05rem; color:#64748B; font-weight:600;">COP</span>"""

# 4. Checklist item 1
old_check = """<small style="color:#64748B; font-size:0.85rem;">Soporte original por el valor de .400.</small>"""
new_check = """<small style="color:#64748B; font-size:0.85rem;">Soporte original por el valor de $331.400.</small>"""

# 5. JS grado
old_js = """      // Caso A: ADMITIDO CON SALÓN
      document.getElementById('res-nombre-estudiante').textContent = estudiante.nombre;
      document.getElementById('res-doc-estudiante').textContent = estudiante.doc;
      document.getElementById('res-salon-educolombia').textContent = estudiante.salon;
      document.getElementById('res-grado-2027').textContent = estudiante.grado_2027;
      document.getElementById('res-acudiente').textContent = estudiante.acudiente || 'Acudiente Registrado';
      document.getElementById('res-doc-acudiente').textContent = estudiante.doc_acudiente || 'C.C. Registrada';"""

new_js = """      // Caso A: ADMITIDO CON SALÓN
      document.getElementById('res-nombre-estudiante').textContent = estudiante.nombre;
      document.getElementById('res-doc-estudiante').textContent = estudiante.doc;
      const gradoAdmitido = estudiante.grado_2027 || estudiante.salon || 'PRIMERO';
      if (document.getElementById('res-grado-admitido')) document.getElementById('res-grado-admitido').textContent = gradoAdmitido;
      if (document.getElementById('res-grado-2027')) document.getElementById('res-grado-2027').textContent = gradoAdmitido;
      if (document.getElementById('res-salon-educolombia')) document.getElementById('res-salon-educolombia').textContent = estudiante.salon;
      document.getElementById('res-acudiente').textContent = estudiante.acudiente || 'Acudiente Registrado';
      document.getElementById('res-doc-acudiente').textContent = estudiante.doc_acudiente || 'C.C. Registrada';"""

assert old_tags in c, "old_tags not found"
assert old_grado in c, "old_grado not found"
assert old_price in c, "old_price not found"
assert old_check in c, "old_check not found"
assert old_js in c, "old_js not found"

c = c.replace(old_tags, new_tags)
c = c.replace(old_grado, new_grado)
c = c.replace(old_price, new_price)
c = c.replace(old_check, new_check)
c = c.replace(old_js, new_js)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(c)

print("SUCCESS: All 5 updates applied to src/admisiones.njk")
