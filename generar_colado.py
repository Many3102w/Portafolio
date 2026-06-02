# -*- coding: utf-8 -*-
"""
Genera un modelo 3D de DEMOSTRACION de un COLADO DE LOSA / FIRME en proceso
-> assets/colado.glb

Cuenta la secuencia constructiva para que se "lea" de un vistazo:
  base de grava  ->  malla electrosoldada (armado) sobre silletas  ->
  concreto colado y nivelado con regla  ->  cimbra de borde con estacas.

Regenerar:  python generar_colado.py
"""
import os
import numpy as np
import trimesh
from trimesh.transformations import rotation_matrix as ROT

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "colado.glb")

# ── Colores ──────────────────────────────────────────────────────────
SOIL   = [104, 88, 70, 255]      # terreno / subrasante
GRAVEL = [150, 142, 130, 255]    # base de grava compactada
STONE  = [120, 116, 110, 255]    # escombro / piedra suelta
CONC_W = [150, 152, 158, 255]    # concreto fresco (humedo)
CONC_L = [176, 178, 184, 255]    # concreto nivelado (superficie acabada)
WOOD   = [156, 120, 74, 255]     # cimbra de madera
STAKE  = [120, 92, 56, 255]      # estacas
MESH   = [150, 154, 164, 255]    # malla electrosoldada (acero galvanizado)
CHAIR  = [120, 124, 132, 255]    # silletas / separadores
RAIL   = [70, 74, 82, 255]       # riel guia metalica
ALU    = [184, 188, 196, 255]    # regla de aluminio
HANDLE = [150, 120, 74, 255]     # mango de madera

P = []

def box(sx, sy, sz, pos, color):
    m = trimesh.creation.box(extents=[sx, sy, sz])
    m.apply_translation(pos); m.visual.face_colors = color; P.append(m)

def seg(p0, p1, r, color, sections=8):
    m = trimesh.creation.cylinder(radius=r, segment=[p0, p1], sections=sections)
    m.visual.face_colors = color; P.append(m)

def blob(cx, cy, cz, sx, sy, sz, color):
    """Monticulo irregular (concreto fresco amontonado)."""
    m = trimesh.creation.icosphere(subdivisions=1, radius=1.0)
    m.apply_scale([sx, sy, sz]); m.apply_translation([cx, cy, cz])
    m.visual.face_colors = color; P.append(m)

# ── Dimensiones de la losa ───────────────────────────────────────────
LX, LZ, T = 4.0, 3.0, 0.15        # largo, ancho, espesor
hx, hz = LX / 2, LZ / 2
front = 0.4                        # frente de colado (x): izq=colado, der=armado

# ── Terreno + base de grava ──────────────────────────────────────────
box(LX + 1.4, 0.40, LZ + 1.2, [0, -0.20, 0], SOIL)          # subrasante
box(LX + 0.5, 0.16, LZ + 0.4, [0, 0.0, 0], GRAVEL)          # base de grava (cara superior en y=0.08)
for _ in range(40):                                          # textura de grava
    gx = np.random.uniform(-hx - 0.2, hx + 0.2)
    gz = np.random.uniform(-hz - 0.15, hz + 0.15)
    box(0.10, 0.06, 0.10, [gx, 0.10, gz], STONE)

base_y = 0.08                      # cara superior de la base (nivel inferior de losa)

# ── Cimbra de borde (madera) + estacas ───────────────────────────────
for z in (-hz, hz):
    box(LX + 0.1, 0.22, 0.04, [0, base_y + 0.07, z], WOOD)
for x in (-hx, hx):
    box(0.04, 0.22, LZ + 0.1, [x, base_y + 0.07, 0], WOOD)
for x in np.linspace(-hx, hx, 5):                            # estacas exteriores
    for z in (-hz - 0.10, hz + 0.10):
        seg([x, base_y - 0.05, z], [x, base_y + 0.18, z], 0.025, STAKE, 6)

# ── Lado DERECHO: malla electrosoldada (armado) sobre silletas ───────
mx0, mx1 = front + 0.05, hx - 0.1
mz0, mz1 = -hz + 0.15, hz - 0.15
my = base_y + 0.05
for x in np.arange(mx0, mx1 + 1e-3, 0.2):                    # barras longitudinales
    seg([x, my, mz0], [x, my, mz1], 0.012, MESH, 6)
for z in np.arange(mz0, mz1 + 1e-3, 0.2):                    # barras transversales
    seg([mx0, my, z], [mx1, my, z], 0.012, MESH, 6)
for x in np.arange(mx0 + 0.2, mx1, 0.6):                     # silletas (separadores)
    for z in np.arange(mz0 + 0.2, mz1, 0.6):
        seg([x, base_y, z], [x, my, z], 0.02, CHAIR, 6)

# ── Lado IZQUIERDO: concreto colado ──────────────────────────────────
pour_len = front - (-hx)                 # franja colada (de -hx al frente)
pour_cx = (-hx + front) / 2
box(pour_len, T, LZ, [pour_cx, base_y + T / 2, 0], CONC_W)            # losa de concreto
# Tramo ya nivelado (acabado liso), dejando una franja humeda junto al frente
lev_x0, lev_x1 = -hx, front - 0.5
box(lev_x1 - lev_x0, 0.02, LZ - 0.06,
    [(lev_x0 + lev_x1) / 2, base_y + T + 0.001, 0], CONC_L)           # superficie nivelada
# Monticulos de concreto fresco en el frente de colado
for z in np.linspace(-hz + 0.5, hz - 0.5, 4):
    blob(front - 0.15, base_y + 0.14, z + np.random.uniform(-0.1, 0.1),
         0.28, 0.12, 0.26, CONC_W)

# ── Riel guia + regla de aluminio (nivelando el frente) ──────────────
seg([front, base_y + T, -hz], [front, base_y + T, hz], 0.03, RAIL, 8)   # riel/guia
# Regla apoyada sobre la cimbra, ligeramente inclinada hacia el frente
ry = base_y + T + 0.03
box(0.08, 0.05, LZ + 0.5, [front - 0.05, ry, 0], ALU)        # regla (aluminio)
seg([front - 0.05, ry, -hz - 0.25], [front + 0.25, ry + 0.5, -hz - 0.55], 0.025, HANDLE, 6)  # mango

# ── Escombro suelto al costado derecho (como en la foto) ─────────────
for _ in range(30):
    sx = np.random.uniform(hx + 0.1, hx + 0.7)
    sz = np.random.uniform(-hz, hz)
    s = np.random.uniform(0.06, 0.16)
    box(s, s * 0.6, s, [sx, 0.05, sz], STONE)

# ── Exportar ─────────────────────────────────────────────────────────
mesh = trimesh.util.concatenate(P)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
mesh.export(OUT)
b = mesh.bounds
print("colado.glb generado  tris=%d  dims X%.2f Y%.2f Z%.2f" % (len(mesh.faces), *(b[1] - b[0])))
