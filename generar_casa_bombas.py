# -*- coding: utf-8 -*-
"""
Genera una CASA DE BOMBAS (estacion de bombeo) en 3D -> assets/casa-bombas.glb
Industria mecanica: bombas centrifugas (motor + voluta) sobre skid, colectores de
succion y descarga, valvulas con volante, tablero electrico y estructura techada.

Regenerar:  python generar_casa_bombas.py
"""
import numpy as np
import trimesh
from trimesh.transformations import rotation_matrix as ROT

OUT = r"C:\Users\Many\Desktop\Portafolio Programacion\assets\casa-bombas.glb"

CONC  = [150, 150, 156, 255]
STEEL = [122, 130, 143, 255]
DARK  = [74, 80, 92, 255]
PUMP  = [52, 102, 168, 255]    # azul industrial (bombas/colectores)
MOTOR = [96, 104, 120, 255]
FLG   = [90, 95, 108, 255]
ROOFM = [142, 150, 162, 255]

P = []

def box(sx, sy, sz, pos, color):
    m = trimesh.creation.box(extents=[sx, sy, sz]); m.apply_translation(pos); m.visual.face_colors = color; P.append(m)

def seg(p0, p1, r, color, sections=16):
    m = trimesh.creation.cylinder(radius=r, segment=[p0, p1], sections=sections); m.visual.face_colors = color; P.append(m)

def ring_y(Rmaj, rmin, y, color, cx=0.0, cz=0.0, mj=20, mn=9):
    m = trimesh.creation.torus(Rmaj, rmin, major_sections=mj, minor_sections=mn)
    m.apply_transform(ROT(np.pi / 2, [1, 0, 0])); m.apply_translation([cx, y, cz]); m.visual.face_colors = color; P.append(m)

def flange(center, axis, r, color=FLG):
    d = np.array(axis, float); d /= np.linalg.norm(d); c = np.array(center, float)
    seg((c - d * 0.04).tolist(), (c + d * 0.04).tolist(), r, color, 18)

def roof_panel(Lx, slope_len, thick, center, angle_x, color):
    m = trimesh.creation.box(extents=[Lx, thick, slope_len]); m.apply_transform(ROT(angle_x, [1, 0, 0]))
    m.apply_translation(center); m.visual.face_colors = color; P.append(m)

# ── Losa ─────────────────────────────────────────────────────────────
box(5.6, 0.3, 3.6, [0, 0.15, 0], CONC)

# ── Colectores (headers) ─────────────────────────────────────────────
SUC_Y, SUC_Z = 0.55, 1.15      # succion (bajo, al frente)
DIS_Y, DIS_Z = 2.30, 0.20      # descarga (alto)
seg([-2.3, SUC_Y, SUC_Z], [2.3, SUC_Y, SUC_Z], 0.24, PUMP, 24)
seg([-2.3, DIS_Y, DIS_Z], [2.3, DIS_Y, DIS_Z], 0.22, PUMP, 24)
for hx in (-2.3, 2.3):
    flange([hx, SUC_Y, SUC_Z], [1, 0, 0], 0.3)
    flange([hx, DIS_Y, DIS_Z], [1, 0, 0], 0.28)

# ── Bomba centrifuga (motor + voluta) ────────────────────────────────
def bomba(px):
    sy = 0.3
    ay = sy + 0.18 + 0.26                      # eje de la bomba
    box(1.05, 0.18, 1.55, [px, sy + 0.09, -0.05], DARK)         # skid
    seg([px, ay, -0.78], [px, ay, -0.12], 0.26, MOTOR, 20)      # motor
    box(0.46, 0.16, 0.34, [px, ay + 0.30, -0.45], DARK)        # caja de bornes
    seg([px, ay, -0.12], [px, ay, 0.02], 0.10, DARK, 12)        # acople
    seg([px, ay, 0.02], [px, ay, 0.34], 0.32, PUMP, 22)         # voluta (cuerpo)
    flange([px, ay, 0.37], [0, 0, 1], 0.35)                    # brida de succion
    # Descarga: sube de la voluta al colector alto, con valvula de compuerta
    rz = 0.12
    seg([px, ay + 0.16, rz], [px, DIS_Y, rz], 0.15, PUMP, 16)
    seg([px, 1.45, rz], [px, 1.74, rz], 0.25, DARK, 16)         # cuerpo de valvula
    seg([px, 1.74, rz], [px, 1.99, rz], 0.03, STEEL, 8)         # vastago
    ring_y(0.21, 0.03, 1.99, STEEL, cx=px, cz=rz, mj=18, mn=8)  # volante
    seg([px, DIS_Y, rz], [px, DIS_Y, DIS_Z], 0.15, PUMP, 16)    # codo al colector
    flange([px, DIS_Y, DIS_Z - 0.02], [0, 0, 1], 0.2)
    # Succion: del colector bajo a la voluta, con valvula
    seg([px, SUC_Y, SUC_Z], [px, ay, SUC_Z], 0.16, PUMP, 16)    # sube del colector
    seg([px, ay, SUC_Z], [px, ay, 0.40], 0.16, PUMP, 16)        # entra a la voluta
    seg([px, 0.80, SUC_Z], [px, 1.02, SUC_Z], 0.23, DARK, 14)   # valvula succion
    seg([px, 1.02, SUC_Z], [px, 1.22, SUC_Z], 0.03, STEEL, 8)
    ring_y(0.18, 0.03, 1.22, STEEL, cx=px, cz=SUC_Z, mj=16, mn=8)

bomba(-1.15)
bomba(1.15)

# ── Tablero electrico ────────────────────────────────────────────────
box(0.75, 1.35, 0.36, [2.05, 0.3 + 0.675, -1.18], STEEL)
box(0.62, 1.05, 0.03, [2.05, 0.3 + 0.72, -1.00], DARK)        # puerta
seg([2.18, 0.78, -1.00], [2.18, 0.95, -1.00], 0.02, STEEL, 6) # manija

# ── Estructura techada (casa) ────────────────────────────────────────
L, W, H, rise = 5.0, 3.0, 2.8, 0.7
ridge, hw = H + rise, W / 2
theta = np.arctan2(rise, hw)
corners = [(-L / 2, -hw), (L / 2, -hw), (L / 2, hw), (-L / 2, hw)]
for cx, cz in corners:
    box(0.18, H, 0.18, [cx, H / 2, cz], STEEL)               # columna
    box(0.44, 0.12, 0.44, [cx, 0.36, cz], DARK)              # placa base
for cz in (-hw, hw):
    seg([-L / 2, H, cz], [L / 2, H, cz], 0.07, STEEL, 12)    # vigas de borde
for cx in (-L / 2, L / 2):                                    # cerchas en los extremos
    seg([cx, H, -hw], [cx, H, hw], 0.06, STEEL, 10)
    seg([cx, H, -hw], [cx, ridge, 0], 0.06, STEEL, 10)
    seg([cx, H, hw], [cx, ridge, 0], 0.06, STEEL, 10)
    seg([cx, H, 0], [cx, ridge, 0], 0.04, STEEL, 8)
seg([-L / 2, ridge, 0], [L / 2, ridge, 0], 0.05, STEEL, 10)  # cumbrera
slope_len = (hw ** 2 + rise ** 2) ** 0.5
cymid = (H + ridge) / 2
roof_panel(L + 0.4, slope_len + 0.1, 0.06, [0, cymid, hw / 2], theta, ROOFM)
roof_panel(L + 0.4, slope_len + 0.1, 0.06, [0, cymid, -hw / 2], -theta, ROOFM)
box(L + 0.3, 0.12, 0.16, [0, ridge + 0.02, 0], DARK)         # caballete

# ── Exportar ─────────────────────────────────────────────────────────
mesh = trimesh.util.concatenate(P)
mesh.export(OUT)
b = mesh.bounds
print("casa-bombas.glb  tris=%d  dims X%.2f Y%.2f Z%.2f" % (len(mesh.faces), *(b[1] - b[0])))
