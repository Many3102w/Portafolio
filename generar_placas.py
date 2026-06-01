# -*- coding: utf-8 -*-
"""
Genera modelos 3D de DEMOSTRACION de placas electronicas para el visor 3D
del portafolio:
  - assets/esp32.glb         -> placa de desarrollo ESP32 DevKit (WROOM-32)
  - assets/dwm1001-dev.glb    -> placa de desarrollo Qorvo DWM1001-DEV (UWB)

Modeladas con trimesh (mismo estilo low-poly que los demas modelos).
Regenerar:  python generar_placas.py
"""
import os
import numpy as np
import trimesh
from trimesh.transformations import rotation_matrix as ROT

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

# ── Colores ──────────────────────────────────────────────────────────
PCB_BLUE = [28, 64, 110, 255]    # PCB azul (ESP32)
PCB_DARK = [22, 30, 44, 255]     # PCB negro-azulado (DWM1001)
SILK     = [228, 232, 238, 255]  # serigrafia blanca
SHIELD   = [196, 199, 205, 255]  # lata metalica del modulo (RF shield)
SHADE    = [150, 153, 160, 255]  # metal en sombra
GOLD     = [214, 178, 70, 255]   # pines / pads dorados
BLACK    = [26, 27, 31, 255]     # plastico de headers / chips
USBMET   = [205, 208, 214, 255]  # conector USB metalico
COPPER   = [194, 122, 64, 255]   # antena PCB (traza de cobre)
RED      = [206, 64, 56, 255]    # LED rojo
BLUE_LED = [70, 132, 210, 255]   # LED azul
ANT_CHIP = [226, 222, 210, 255]  # antena chip (ceramica)
CAP      = [188, 150, 96, 255]   # capacitores (tantalo)

# ── Helpers ──────────────────────────────────────────────────────────
def box(parts, sx, sy, sz, pos, color):
    m = trimesh.creation.box(extents=[sx, sy, sz])
    m.apply_translation(pos); m.visual.face_colors = color; parts.append(m)

def cyl_y(parts, r, h, pos, color, sections=18):
    m = trimesh.creation.cylinder(radius=r, height=h, sections=sections)
    m.apply_translation(pos); m.visual.face_colors = color; parts.append(m)

def pin_row(parts, x0, x1, n, z, color=GOLD, plastic=BLACK, top=0.10):
    """Tira de header: base de plastico negro + pines dorados encima."""
    xs = np.linspace(x0, x1, n)
    L = abs(x1 - x0) + 0.18
    box(parts, L, 0.10, 0.22, [(x0 + x1) / 2, top, z], plastic)   # plastico
    for x in xs:
        box(parts, 0.11, 0.12, 0.11, [x, top + 0.10, z], color)  # pin dorado

def export(parts, name):
    mesh = trimesh.util.concatenate(parts)
    out = os.path.join(BASE, name)
    os.makedirs(BASE, exist_ok=True)
    mesh.export(out)
    b = mesh.bounds
    print("%-20s tris=%-5d  dims X%.2f Y%.2f Z%.2f" % (name, len(mesh.faces), *(b[1] - b[0])))

# ════════════════════════ ESP32 DEVKIT (WROOM-32) ════════════════════════
e = []
LX, LZ, T = 5.1, 2.55, 0.16        # largo, ancho, espesor del PCB
top = T / 2.0                       # cara superior del PCB
box(e, LX, T, LZ, [0, 0, 0], PCB_BLUE)                      # PCB
# Filetes de serigrafia (marco) y franja del modulo
box(e, LX - 0.2, 0.01, 0.06, [0, top, LZ / 2 - 0.18], SILK)
box(e, LX - 0.2, 0.01, 0.06, [0, top, -LZ / 2 + 0.18], SILK)

# Headers a ambos lados (15 pines por lado)
pin_row(e, -2.2, 2.2, 15, LZ / 2 - 0.13, top=top)
pin_row(e, -2.2, 2.2, 15, -(LZ / 2 - 0.13), top=top)

# Modulo ESP-WROOM-32: lata metalica + tapa + antena PCB
mod_x = -1.25
box(e, 1.75, 0.30, 1.75, [mod_x, top + 0.15, 0], SHIELD)    # lata RF
box(e, 1.55, 0.02, 1.55, [mod_x, top + 0.31, 0], SHADE)     # tapa (relieve)
box(e, 0.95, 0.022, 1.55, [-2.25, top + 0.012, 0], COPPER)  # antena PCB (zigzag)
for zz in np.linspace(-0.6, 0.6, 6):                         # "dientes" del zigzag
    box(e, 0.5, 0.024, 0.08, [-2.25, top + 0.013, zz], PCB_BLUE)

# Conector micro-USB (sobresale por un extremo)
box(e, 0.75, 0.34, 0.95, [2.45, top + 0.17, 0], USBMET)
box(e, 0.20, 0.18, 0.62, [2.83, top + 0.12, 0], BLACK)      # boca del USB

# Botones EN / BOOT
box(e, 0.34, 0.20, 0.34, [1.75, top + 0.10, 0.78], BLACK)
box(e, 0.34, 0.20, 0.34, [1.75, top + 0.10, -0.78], BLACK)
# Regulador AMS1117 + LEDs + capacitores
box(e, 0.45, 0.18, 0.30, [0.95, top + 0.09, 0.0], BLACK)
box(e, 0.16, 0.10, 0.10, [0.30, top + 0.05, 0.55], RED)
box(e, 0.16, 0.10, 0.10, [0.30, top + 0.05, -0.55], BLUE_LED)
for cx, cz in [(0.0, 0.65), (0.55, -0.6), (-0.2, -0.4)]:
    cyl_y(e, 0.10, 0.22, [cx, top + 0.11, cz], CAP, 14)

export(e, "esp32.glb")

# ════════════════════════ DWM1001-DEV (UWB / Qorvo) ════════════════════════
d = []
LX, LZ, T = 9.2, 2.55, 0.16
top = T / 2.0
box(d, LX, T, LZ, [0, 0, 0], PCB_DARK)                      # PCB largo
box(d, LX - 0.3, 0.01, 0.05, [0, top, LZ / 2 - 0.16], SILK) # serigrafia
box(d, LX - 0.3, 0.01, 0.05, [0, top, -LZ / 2 + 0.16], SILK)

# Headers Arduino-style a ambos lados
pin_row(d, -3.6, 3.4, 20, LZ / 2 - 0.13, top=top)
pin_row(d, -3.6, 3.4, 20, -(LZ / 2 - 0.13), top=top)

# ── Modulo DWM1001C (UWB): lata + antena chip ceramica en la punta ──
mod_x = 3.0
box(d, 1.55, 0.26, 1.85, [mod_x, top + 0.13, 0], SHIELD)    # lata del modulo
box(d, 1.35, 0.02, 1.65, [mod_x, top + 0.27, 0], SHADE)     # tapa
box(d, 0.42, 0.22, 0.30, [4.25, top + 0.11, 0.45], ANT_CHIP)# antena chip (UWB)
box(d, 0.6, 0.02, 0.6, [4.2, top + 0.011, -0.4], COPPER)    # pad de RF

# ── Seccion J-Link / debugger (extremo opuesto) ──
box(d, 1.1, 0.16, 1.0, [-3.0, top + 0.08, 0], BLACK)        # micro nRF (QFN)
box(d, 0.7, 0.12, 0.6, [-1.9, top + 0.06, 0.55], BLACK)     # chip interface
# Conector micro-USB
box(d, 0.75, 0.34, 0.95, [-4.55, top + 0.17, 0], USBMET)
box(d, 0.20, 0.18, 0.62, [-4.92, top + 0.12, 0], BLACK)

# Boton de reset + LEDs (fila de 4) + capacitores
box(d, 0.30, 0.20, 0.30, [-3.0, top + 0.10, 0.95], BLACK)
for i, cz in enumerate(np.linspace(-0.6, 0.6, 4)):
    col = [RED, BLUE_LED, RED, BLUE_LED][i]
    box(d, 0.14, 0.09, 0.10, [-1.0, top + 0.05, cz], col)
for cx, cz in [(0.2, 0.7), (0.9, -0.7), (1.7, 0.6), (-0.4, -0.7)]:
    cyl_y(d, 0.09, 0.20, [cx, top + 0.10, cz], CAP, 14)

export(d, "dwm1001-dev.glb")
print("Listo.")
