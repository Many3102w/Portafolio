# -*- coding: utf-8 -*-
"""
Genera modelos 3D de DEMOSTRACION de obra civil y techado de taller:
  - assets/obra-civil.glb      -> dados de colado, cimentacion, armado de varilla, cimbra
  - assets/techado-taller.glb  -> estructura de techo de taller (columnas, cerchas, lamina)

Reemplaza por tus disenos reales de AutoCAD exportados a GLB.
Regenerar:  python generar_modelos_obra.py
"""
import numpy as np
import trimesh
from trimesh.transformations import rotation_matrix as ROT

BASE = r"C:\Users\Many\Desktop\Portafolio Programacion\assets"

# ── Colores ──────────────────────────────────────────────────────────
CONC  = [150, 150, 156, 255]   # concreto
REBAR = [156, 98, 70, 255]     # varilla
STEEL = [122, 130, 143, 255]   # acero
DARK  = [74, 80, 92, 255]      # placas / acero oscuro
WOOD   = [122, 100, 72, 255]   # cimbra
ROOFM = [142, 150, 162, 255]   # lamina de techo

# ── Helpers ──────────────────────────────────────────────────────────
def box(parts, sx, sy, sz, pos, color):
    m = trimesh.creation.box(extents=[sx, sy, sz])
    m.apply_translation(pos); m.visual.face_colors = color; parts.append(m)

def seg(parts, p0, p1, r, color, sections=14):
    m = trimesh.creation.cylinder(radius=r, segment=[p0, p1], sections=sections)
    m.visual.face_colors = color; parts.append(m)

def square_tie(parts, cx, cz, s, y, r, color):
    pts = [(cx - s, cz - s), (cx + s, cz - s), (cx + s, cz + s), (cx - s, cz + s)]
    for i in range(4):
        a, b = pts[i], pts[(i + 1) % 4]
        seg(parts, [a[0], y, a[1]], [b[0], y, b[1]], r, color, sections=4)

def roof_panel(parts, Lx, slope_len, thick, center, angle_x, color):
    m = trimesh.creation.box(extents=[Lx, thick, slope_len])
    m.apply_transform(ROT(angle_x, [1, 0, 0]))
    m.apply_translation(center); m.visual.face_colors = color; parts.append(m)

def export(parts, name):
    mesh = trimesh.util.concatenate(parts)
    out = BASE + "\\" + name
    mesh.export(out)
    b = mesh.bounds
    print("%-22s tris=%-5d  dims X%.2f Y%.2f Z%.2f" % (name, len(mesh.faces), *(b[1] - b[0])))

# ════════════════════════ OBRA CIVIL — DADOS DE COLADO ════════════════════════
c = []
box(c, 7.0, 0.3, 5.0, [0, 0.15, 0], CONC)   # losa de cimentacion

def dado(cx, cz, b=1.2, h1=0.45, top=0.8, h2=0.55):
    box(c, b, h1, b, [cx, 0.3 + h1 / 2, cz], CONC)
    box(c, top, h2, top, [cx, 0.3 + h1 + h2 / 2, cz], CONC)
    ty = 0.3 + h1 + h2
    off = top * 0.3
    for sx in (-off, off):
        for sz in (-off, off):
            seg(c, [cx + sx, ty, cz + sz], [cx + sx, ty + 0.3, cz + sz], 0.03, STEEL, sections=6)
            box(c, 0.09, 0.06, 0.09, [cx + sx, ty + 0.32, cz + sz], STEEL)   # tuerca

dado(-2.2, -1.3)
dado(-2.2, 1.3)
dado(2.2, 1.3)

# dado con arranque de columna (jaula de varilla / estribos)
gx, gz = 2.2, -1.3
box(c, 1.3, 0.5, 1.3, [gx, 0.55, gz], CONC)
g0, s = 0.8, 0.45
verts = [(-s, -s), (s, -s), (s, s), (-s, s), (0, -s), (s, 0), (0, s), (-s, 0)]
for vx, vz in verts:
    seg(c, [gx + vx, g0, gz + vz], [gx + vx, g0 + 1.8, gz + vz], 0.028, REBAR, sections=6)
for yy in np.arange(g0 + 0.2, g0 + 1.8, 0.35):
    square_tie(c, gx, gz, s, yy, 0.02, REBAR)

# zapata en colado con cimbra (formwork) y varillas de espera
fx, fz = 0.0, 1.55
box(c, 1.0, 0.55, 0.05, [fx, 0.575, fz - 0.5], WOOD)
box(c, 1.0, 0.55, 0.05, [fx, 0.575, fz + 0.5], WOOD)
box(c, 0.05, 0.55, 1.0, [fx - 0.5, 0.575, fz], WOOD)
box(c, 0.05, 0.55, 1.0, [fx + 0.5, 0.575, fz], WOOD)
for vx, vz in [(-0.22, -0.22), (0.22, -0.22), (0.22, 0.22), (-0.22, 0.22)]:
    seg(c, [fx + vx, 0.3, fz + vz], [fx + vx, 1.2, fz + vz], 0.025, REBAR, sections=6)

export(c, "obra-civil.glb")

# ════════════════════════ TECHADO DE TALLER ════════════════════════
r = []
L, W, H, rise = 7.0, 4.0, 3.0, 1.3
ridge = H + rise
hw = W / 2.0
bents = [-L / 2 + 0.4, 0.0, L / 2 - 0.4]
theta = np.arctan2(rise, hw)

for x in bents:                                  # columnas + placas + zapatas
    for z in (-hw, hw):
        box(r, 0.20, H, 0.20, [x, H / 2, z], STEEL)
        box(r, 0.46, 0.12, 0.46, [x, 0.06, z], DARK)
        box(r, 0.72, 0.26, 0.72, [x, -0.0 + 0.13, z], CONC)   # zapata de concreto
for z in (-hw, hw):                              # vigas de borde
    seg(r, [-L / 2, H, z], [L / 2, H, z], 0.07, STEEL, sections=12)

for x in bents:                                  # cerchas (trusses)
    seg(r, [x, H, -hw], [x, H, hw], 0.06, STEEL, sections=10)      # cuerda inferior
    seg(r, [x, H, -hw], [x, ridge, 0], 0.06, STEEL, sections=10)   # cuerda superior izq
    seg(r, [x, H, hw], [x, ridge, 0], 0.06, STEEL, sections=10)    # cuerda superior der
    seg(r, [x, H, 0], [x, ridge, 0], 0.045, STEEL, sections=8)     # pendolon
    for zz in (-hw * 0.5, hw * 0.5):                               # montantes
        tcy = H + (1 - abs(zz) / hw) * rise
        seg(r, [x, H, zz], [x, tcy, zz], 0.035, STEEL, sections=6)

def purlin(zp):                                  # largueros sobre las pendientes
    yy = ridge - (abs(zp) / hw) * rise
    seg(r, [-L / 2 - 0.2, yy, zp], [L / 2 + 0.2, yy, zp], 0.04, STEEL, sections=8)
for zp in (-1.6, -0.8, 0.0, 0.8, 1.6):
    purlin(zp)

slope_len = (hw ** 2 + rise ** 2) ** 0.5         # laminas de techo (2 aguas)
cymid = (H + ridge) / 2.0
roof_panel(r, L + 0.5, slope_len + 0.1, 0.06, [0, cymid, hw / 2], theta, ROOFM)
roof_panel(r, L + 0.5, slope_len + 0.1, 0.06, [0, cymid, -hw / 2], -theta, ROOFM)
box(r, L + 0.3, 0.12, 0.18, [0, ridge + 0.03, 0], DARK)   # caballete (ridge)

export(r, "techado-taller.glb")
print("Listo.")
