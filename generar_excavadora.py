# -*- coding: utf-8 -*-
"""
Genera un modelo 3D de una EXCAVADORA hidraulica sobre orugas (estilo DEVELON)
y lo exporta a GLB para el visor 3D del portafolio -> assets/excavadora.glb

Maquinaria pesada de obra: tren de rodaje (orugas), estructura giratoria con
cabina y contrapeso, pluma (boom), brazo (stick), cucharon (bucket) y los
cilindros hidraulicos que los mueven.

Regenerar:  python generar_excavadora.py
"""
import os
import numpy as np
import trimesh
from trimesh.transformations import rotation_matrix as ROT

# Ruta portatil: <carpeta del script>/assets/excavadora.glb
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "excavadora.glb")

# ── Colores (paleta DEVELON: naranja sobre acero/negro) ──────────────
ORANGE = [232, 108, 26, 255]    # naranja maquinaria
ORDARK = [176, 78, 16, 255]     # naranja sombra / detalles
STEEL  = [128, 134, 146, 255]   # acero / cilindros
ROD    = [196, 200, 208, 255]   # vastago cromado del cilindro
DARK   = [48, 50, 56, 255]      # orugas / chasis oscuro
BLACK  = [28, 29, 33, 255]      # gomas / detalles
GLASS  = [120, 168, 188, 180]   # cristales de la cabina
GREY   = [92, 96, 104, 255]     # rodillos / zapatas
BUCKET = [58, 60, 66, 255]      # cucharon (acero ennegrecido)

P = []

# ── Helpers ──────────────────────────────────────────────────────────
def box(sx, sy, sz, pos, color):
    m = trimesh.creation.box(extents=[sx, sy, sz])
    m.apply_translation(pos); m.visual.face_colors = color; P.append(m)

def seg(p0, p1, r, color, sections=18):
    m = trimesh.creation.cylinder(radius=r, segment=[p0, p1], sections=sections)
    m.visual.face_colors = color; P.append(m)

def cyl_z(r, p0, p1, color, sections=24):
    """Cilindro entre dos puntos (eje libre); util para ruedas/rodillos en Z."""
    seg(p0, p1, r, color, sections)

def beam(p0, p1, depth, width, color):
    """Viga rectangular orientada en el plano XY (rota sobre el eje Z).
    depth = canto (en el plano)  ·  width = ancho (en Z)."""
    p0 = np.array(p0, float); p1 = np.array(p1, float)
    d = p1 - p0
    L = np.linalg.norm(d)
    ang = np.arctan2(d[1], d[0])
    m = trimesh.creation.box(extents=[L, depth, width])
    m.apply_transform(ROT(ang, [0, 0, 1]))
    m.apply_translation((p0 + p1) / 2.0)
    m.visual.face_colors = color; P.append(m)

def ram(p0, p1, rbody, color=STEEL, color_rod=ROD):
    """Cilindro hidraulico: cuerpo + vastago mas delgado que sale por un extremo."""
    p0 = np.array(p0, float); p1 = np.array(p1, float)
    d = p1 - p0; L = np.linalg.norm(d); u = d / L
    body_end = p0 + u * (L * 0.62)
    seg(p0.tolist(), body_end.tolist(), rbody, color, 16)            # camisa
    seg(body_end.tolist(), p1.tolist(), rbody * 0.55, color_rod, 14) # vastago

# ════════════════════════ TREN DE RODAJE (ORUGAS) ════════════════════════
TW = 0.92               # semiancho: orugas en z = ±TW
shoe_w = 0.46           # ancho de cada oruga (en Z)
wheel_r = 0.42          # radio rueda guia / motriz
xf, xr = 1.85, -1.85    # ejes delantero / trasero
ay = wheel_r            # altura del eje de las ruedas

for z in (-TW, TW):
    z0, z1 = z - shoe_w / 2, z + shoe_w / 2
    # Banda/zapatas de la oruga: cuerpo central + extremos redondeados
    box(xf - xr, wheel_r * 2.0, shoe_w, [0, ay, z], DARK)
    cyl_z(wheel_r, [xf, ay, z0], [xf, ay, z1], DARK)   # rueda guia (delantera)
    cyl_z(wheel_r, [xr, ay, z0], [xr, ay, z1], DARK)   # rueda motriz (trasera)
    # Maza/llanta interior de las ruedas
    cyl_z(wheel_r * 0.45, [xf, ay, z0 - 0.02], [xf, ay, z1 + 0.02], GREY)
    cyl_z(wheel_r * 0.45, [xr, ay, z0 - 0.02], [xr, ay, z1 + 0.02], GREY)
    # Rodillos inferiores
    for rx in np.linspace(-1.25, 1.25, 4):
        cyl_z(0.16, [rx, 0.16, z0], [rx, 0.16, z1], GREY, 16)
    # Cubierta lateral del bastidor de la oruga
    box(xf - xr - 0.2, 0.42, shoe_w * 0.5, [0, ay + 0.05, z], BLACK)

# Travesano central que une ambas orugas (carbody)
box(2.4, 0.5, 2 * TW - shoe_w, [0, ay + 0.05, 0], DARK)

# ════════════════════════ ESTRUCTURA GIRATORIA (HOUSE) ════════════════════════
deck_y = ay + 0.30                 # altura de la plataforma giratoria
# Corona de giro (slewing ring) + base de plataforma
seg([0, ay + 0.18, 0], [0, deck_y, 0], 1.05, STEEL, 40)
box(2.9, 0.34, 2.0, [0.1, deck_y + 0.17, 0], ORANGE)   # plataforma giratoria

base_y = deck_y + 0.34

# ── Contrapeso trasero (bloque pesado naranja, cara curva) ───────────
cw_x = -1.45
box(0.9, 1.15, 2.05, [cw_x, base_y + 0.55, 0], ORANGE)
box(0.18, 1.0, 1.85, [cw_x - 0.5, base_y + 0.52, 0], ORDARK)   # franja inferior
seg([cw_x - 0.45, base_y + 0.95, -0.95],
    [cw_x - 0.45, base_y + 0.95, 0.95], 0.2, ORDARK, 18)        # canto superior redondeado

# ── Capot del motor (engine hood) ────────────────────────────────────
box(1.7, 0.85, 2.0, [-0.35, base_y + 0.42, 0], ORANGE)
box(1.4, 0.06, 0.5, [-0.35, base_y + 0.86, 0.55], ORDARK)      # rejilla / detalle
box(0.5, 0.5, 1.9, [0.55, base_y + 0.25, 0], ORANGE)           # transicion a la base de la pluma
# Tubo de escape
seg([-0.7, base_y + 0.85, -0.7], [-0.7, base_y + 1.35, -0.7], 0.07, STEEL, 12)

# ── Cabina del operador (lado izquierdo / +Z) ────────────────────────
cab_x, cab_z = 0.35, 0.72
cw, ch, cd = 0.92, 1.18, 0.92
cy0 = base_y
# Carcasa de la cabina (marco naranja)
box(cw, ch, cd, [cab_x, cy0 + ch / 2, cab_z], ORANGE)
# Cristales (frente, lateral y techo parcial)
box(0.03, ch * 0.74, cd * 0.84, [cab_x + cw / 2 + 0.005, cy0 + ch * 0.55, cab_z], GLASS)  # frente
box(cw * 0.84, ch * 0.74, 0.03, [cab_x, cy0 + ch * 0.55, cab_z + cd / 2 + 0.005], GLASS)  # lateral
box(cw * 0.7, 0.03, cd * 0.7, [cab_x, cy0 + ch - 0.02, cab_z], GLASS)                     # techo
# Pasamanos de acceso
seg([cab_x + cw / 2, cy0, cab_z - cd / 2], [cab_x + cw / 2, cy0 + ch, cab_z - cd / 2], 0.03, STEEL, 8)

# ════════════════════════ PLUMA · BRAZO · CUCHARON ════════════════════════
# Articulacion de la pluma al frente de la estructura giratoria
pivot   = np.array([1.15, base_y + 0.10, 0.0])
b_bend  = np.array([2.55, base_y + 1.85, 0.0])   # codo de la pluma
b_tip   = np.array([3.95, base_y + 1.05, 0.0])   # punta de la pluma
a_tip   = np.array([4.95, base_y - 0.55, 0.0])   # punta del brazo (stick)

# Pluma (boom) en dos tramos, viga de seccion en caja
beam(pivot.tolist(), b_bend.tolist(), 0.42, 0.34, ORANGE)
beam(b_bend.tolist(), b_tip.tolist(), 0.40, 0.34, ORANGE)
seg(pivot.tolist(), (pivot + [0, 0, 0]).tolist(), 0.18, ORDARK, 12)   # buje del pivote
# Orejas del pivote en la estructura
box(0.5, 0.6, 0.7, [1.05, base_y + 0.1, 0], ORANGE)

# Brazo (stick)
beam(b_tip.tolist(), a_tip.tolist(), 0.34, 0.28, ORANGE)

# ── Cilindros hidraulicos ────────────────────────────────────────────
# 2 cilindros de pluma (estructura -> bajo la pluma)
for dz in (-0.30, 0.30):
    ram([0.55, base_y + 0.30, dz], [2.05, base_y + 1.35, dz], 0.12)
# Cilindro del brazo (sobre la pluma -> cabeza del brazo)
ram([2.0, base_y + 2.0, 0.0], [3.7, base_y + 1.35, 0.0], 0.12)
# Cilindro del cucharon (cabeza del brazo -> articulacion del cucharon)
ram([3.85, base_y + 1.35, 0.0], [4.78, base_y - 0.05, 0.0], 0.10)

# ── Cucharon (bucket) con dientes ────────────────────────────────────
# Articulacion + varillaje (links)
seg([4.95, base_y - 0.55, -0.16], [4.95, base_y - 0.55, 0.16], 0.10, STEEL, 12)
beam([4.78, base_y - 0.05, 0.0], [5.05, base_y - 0.7, 0.0], 0.10, 0.1, STEEL)  # link
bw = 0.62   # ancho del cucharon (Z)
# Cuerpo del cucharon: dorso, fondo curvado y labio
bx, by = 5.05, base_y - 0.78
box(0.62, 0.62, bw, [bx, by + 0.18, 0], BUCKET)                 # caja del cucharon
beam([bx - 0.28, by + 0.42, 0], [bx + 0.34, by - 0.18, 0], 0.1, bw, BUCKET)  # dorso inclinado
beam([bx - 0.30, by - 0.18, 0], [bx + 0.30, by - 0.30, 0], 0.12, bw, BUCKET) # fondo / labio
# Dientes del cucharon
for tz in np.linspace(-bw / 2 + 0.07, bw / 2 - 0.07, 5):
    seg([bx + 0.28, by - 0.26, tz], [bx + 0.48, by - 0.34, tz], 0.04, ROD, 8)

# ════════════════════════ EXPORTAR ════════════════════════
mesh = trimesh.util.concatenate(P)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
mesh.export(OUT)
b = mesh.bounds
print("excavadora.glb generada en:", OUT)
print("Triangulos:", len(mesh.faces), "| Vertices:", len(mesh.vertices))
print("Dimensiones (m)  X:%.2f  Y:%.2f  Z:%.2f" % tuple(b[1] - b[0]))
