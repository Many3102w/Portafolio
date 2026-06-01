# -*- coding: utf-8 -*-
"""
Genera un modelo 3D de DEMOSTRACION (torre de vigilancia) y lo exporta a GLB
para el visor 3D del portafolio (assets/modelo.glb).

Reemplaza este modelo por tu diseno real de AutoCAD exportado a GLB/GLTF.
Para regenerar el demo:  python generar_modelo.py
"""
import numpy as np
import trimesh
from trimesh.transformations import rotation_matrix

OUT = r"C:\Users\Many\Desktop\Portafolio Programacion\assets\modelo.glb"

STEEL = [120, 128, 142, 255]
DARK  = [74, 80, 92, 255]
ROOF  = [56, 60, 70, 255]
WOOD  = [96, 84, 70, 255]

parts = []

def box(sx, sy, sz, pos, color):
    m = trimesh.creation.box(extents=[sx, sy, sz])
    m.apply_translation(pos)
    m.visual.face_colors = color
    parts.append(m)

def strut(p0, p1, r, color, sections=10):
    m = trimesh.creation.cylinder(radius=r, segment=[p0, p1], sections=sections)
    m.visual.face_colors = color
    parts.append(m)

# ── Parametros ───────────────────────────────────────────────────────
hx, hz = 1.25, 1.25          # media base (m)
leg_h  = 4.0                 # altura de las patas
post   = 0.18                # grosor de columna
corners = [(-hx, -hz), (hx, -hz), (hx, hz), (-hx, hz)]

# ── Zapatas + columnas ───────────────────────────────────────────────
for (x, z) in corners:
    box(0.45, 0.35, 0.45, [x, 0.175, z], DARK)          # zapata
    box(post, leg_h, post, [x, leg_h / 2, z], STEEL)    # columna

# ── Vigas horizontales (anillo superior y medio) ─────────────────────
for i in range(4):
    x0, z0 = corners[i]
    x1, z1 = corners[(i + 1) % 4]
    strut([x0, leg_h, z0], [x1, leg_h, z1], 0.06, STEEL)        # anillo arriba
    strut([x0, leg_h * 0.5, z0], [x1, leg_h * 0.5, z1], 0.05, STEEL)  # anillo medio

# ── Arriostramiento en X en cada cara ────────────────────────────────
for i in range(4):
    x0, z0 = corners[i]
    x1, z1 = corners[(i + 1) % 4]
    strut([x0, 0.3, z0], [x1, leg_h - 0.15, z1], 0.04, STEEL)
    strut([x1, 0.3, z1], [x0, leg_h - 0.15, z0], 0.04, STEEL)

# ── Plataforma ───────────────────────────────────────────────────────
plat_y = leg_h + 0.1
box(2 * hx + 0.6, 0.18, 2 * hz + 0.6, [0, plat_y, 0], WOOD)

# ── Barandal (pasamanos + balaustres) ────────────────────────────────
rail_top = plat_y + 0.55
ext = hx + 0.28
ring = [(-ext, -ext), (ext, -ext), (ext, ext), (-ext, ext)]
for i in range(4):
    x0, z0 = ring[i]
    x1, z1 = ring[(i + 1) % 4]
    strut([x0, rail_top, z0], [x1, rail_top, z1], 0.035, STEEL)   # pasamanos
    for t in np.linspace(0, 1, 4)[1:-1]:                          # balaustres
        bx, bz = x0 + (x1 - x0) * t, z0 + (z1 - z0) * t
        box(0.05, 0.55, 0.05, [bx, plat_y + 0.30, bz], STEEL)

# ── Cabina ───────────────────────────────────────────────────────────
cab_w, cab_h, cab_d = 2.3, 1.5, 2.3
cab_y0 = plat_y + 0.09
box(cab_w, cab_h, cab_d, [0, cab_y0 + cab_h / 2, 0], STEEL)

# ── Techo (piramide de 4 lados) ──────────────────────────────────────
roof_h = 0.85
roof = trimesh.creation.cone(radius=1.85, height=roof_h, sections=4)
roof.apply_transform(rotation_matrix(-np.pi / 2, [1, 0, 0]))   # eje Z -> Y (apunta arriba)
roof.apply_transform(rotation_matrix(np.pi / 4, [0, 1, 0]))    # alinea la base cuadrada
roof.apply_translation([0, cab_y0 + cab_h, 0])
roof.visual.face_colors = ROOF
parts.append(roof)

# ── Unir y exportar ──────────────────────────────────────────────────
mesh = trimesh.util.concatenate(parts)
mesh.apply_translation([0, 0, 0])
mesh.export(OUT)
print("Modelo GLB generado en:", OUT)
print("Triangulos:", len(mesh.faces), "| Vertices:", len(mesh.vertices))
ext = mesh.bounds
print("Dimensiones (m)  X:%.2f  Y:%.2f  Z:%.2f" % tuple(ext[1] - ext[0]))
