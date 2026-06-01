# -*- coding: utf-8 -*-
"""
Genera modelos 3D industriales de DEMOSTRACION para el visor del portafolio:
  - assets/tanque.glb          -> tanque de almacenamiento industrial
  - assets/obra-mecanica.glb   -> rack de tuberia / obra mecanica

Reemplaza por tus disenos reales de AutoCAD exportados a GLB.
Regenerar:  python generar_modelos_industriales.py
"""
import numpy as np
import trimesh
from trimesh.transformations import rotation_matrix as ROT

BASE = r"C:\Users\Many\Desktop\Portafolio Programacion\assets"

# ── Colores ──────────────────────────────────────────────────────────
WHITE = [205, 209, 214, 255]
STEEL = [122, 130, 143, 255]
DARK  = [72, 78, 90, 255]
CONC  = [96, 96, 102, 255]
ROOFC = [96, 104, 120, 255]
FLG   = [88, 93, 106, 255]
PIPEA = [156, 120, 84, 255]
PIPEB = [104, 138, 150, 255]
PIPEC = [176, 176, 184, 255]

# ── Helpers ──────────────────────────────────────────────────────────
def box(parts, sx, sy, sz, pos, color):
    m = trimesh.creation.box(extents=[sx, sy, sz])
    m.apply_translation(pos); m.visual.face_colors = color; parts.append(m)

def seg(parts, p0, p1, r, color, sections=18):
    m = trimesh.creation.cylinder(radius=r, segment=[p0, p1], sections=sections)
    m.visual.face_colors = color; parts.append(m)

def cyl_y(parts, r, h, ybase, color, cx=0.0, cz=0.0, sections=40):
    m = trimesh.creation.cylinder(radius=r, height=h, sections=sections)
    m.apply_transform(ROT(np.pi / 2, [1, 0, 0]))
    m.apply_translation([cx, ybase + h / 2.0, cz]); m.visual.face_colors = color; parts.append(m)

def cone_y(parts, r, h, ybase, color, sections=40):
    m = trimesh.creation.cone(radius=r, height=h, sections=sections)
    m.apply_transform(ROT(-np.pi / 2, [1, 0, 0]))
    m.apply_translation([0, ybase, 0]); m.visual.face_colors = color; parts.append(m)

def ring_y(parts, Rmaj, rmin, y, color, cx=0.0, cz=0.0, mj=28, mn=10):
    m = trimesh.creation.torus(Rmaj, rmin, major_sections=mj, minor_sections=mn)
    m.apply_transform(ROT(np.pi / 2, [1, 0, 0]))
    m.apply_translation([cx, y, cz]); m.visual.face_colors = color; parts.append(m)

def export(parts, name):
    mesh = trimesh.util.concatenate(parts)
    out = BASE + "\\" + name
    mesh.export(out)
    b = mesh.bounds
    print("%-22s tris=%-5d  dims X%.2f Y%.2f Z%.2f" % (name, len(mesh.faces), *(b[1] - b[0])))

# ════════════════════════ TANQUE DE ALMACENAMIENTO ════════════════════════
t = []
body_r, body_h, y0 = 2.4, 5.0, 0.7
cyl_y(t, 2.75, 0.40, 0.0, CONC, sections=44)        # cimentacion
cyl_y(t, 2.50, 0.30, 0.4, DARK, sections=44)        # anillo base
cyl_y(t, body_r, body_h, y0, WHITE, sections=56)    # cuerpo del tanque
for yy in (y0 + 1.6, y0 + 3.2):                      # costuras de soldadura
    ring_y(t, body_r + 0.01, 0.03, yy, STEEL, mj=48, mn=8)
roof_y = y0 + body_h
cone_y(t, body_r + 0.06, 1.15, roof_y, ROOFC, sections=56)   # techo conico
# barandal del techo + balaustres
hr_y, hr_R = roof_y + 0.55, body_r - 0.05
ring_y(t, hr_R, 0.04, hr_y, STEEL, mj=36, mn=8)
for a in np.linspace(0, 2 * np.pi, 16, endpoint=False):
    bx, bz = hr_R * np.cos(a), hr_R * np.sin(a)
    seg(t, [bx, roof_y, bz], [bx, hr_y, bz], 0.025, STEEL, sections=6)
# boquillas (nozzles) con bridas
for ang, yy, rr in [(0.4, y0 + 0.9, 0.14), (2.4, y0 + 2.6, 0.12), (4.2, y0 + 1.4, 0.13)]:
    c, s = np.cos(ang), np.sin(ang)
    p0 = np.array([body_r * c, yy, body_r * s])
    p1 = np.array([(body_r + 0.45) * c, yy, (body_r + 0.45) * s])
    seg(t, p0.tolist(), p1.tolist(), rr, STEEL, sections=12)
    d = (p1 - p0); d = d / np.linalg.norm(d)
    seg(t, (p1 - d * 0.04).tolist(), (p1 + d * 0.04).tolist(), rr + 0.1, FLG, sections=16)
# salida inferior con valvula y volante
ox, oy = body_r, y0 + 0.15
seg(t, [ox, oy, 0], [ox + 0.7, oy, 0], 0.13, STEEL, sections=12)
seg(t, [ox + 0.7, oy, 0], [ox + 0.7, 0.25, 0], 0.13, STEEL, sections=12)
seg(t, [ox + 0.25, oy, 0], [ox + 0.5, oy, 0], 0.22, DARK, sections=14)
seg(t, [ox + 0.375, oy, 0], [ox + 0.375, oy + 0.4, 0], 0.03, STEEL, sections=6)
ring_y(t, 0.2, 0.03, oy + 0.4, STEEL, cx=ox + 0.375, mj=18, mn=8)
# escalera lateral
lx = -(body_r + 0.16)
seg(t, [lx, 0.4, -0.28], [lx, roof_y, -0.28], 0.035, STEEL, sections=6)
seg(t, [lx, 0.4, 0.28], [lx, roof_y, 0.28], 0.035, STEEL, sections=6)
for yy in np.arange(0.8, roof_y, 0.4):
    seg(t, [lx, yy, -0.28], [lx, yy, 0.28], 0.022, STEEL, sections=6)
export(t, "tanque.glb")

# ════════════════════════ RACK DE TUBERIA / OBRA MECANICA ════════════════════════
m = []
L, Wd, H = 7.0, 2.2, 3.0
bents = [-L / 2 + 0.5, 0.0, L / 2 - 0.5]
for x in bents:
    for z in (-Wd / 2, Wd / 2):
        box(m, 0.18, H, 0.18, [x, H / 2, z], DARK)          # columna
        box(m, 0.42, 0.12, 0.42, [x, 0.06, z], DARK)        # placa base
    box(m, 0.16, 0.18, Wd + 0.18, [x, H + 0.04, 0], STEEL)  # viga transversal
for z in (-Wd / 2, Wd / 2):                                  # vigas longitudinales
    box(m, L, 0.14, 0.16, [0, H + 0.13, z], STEEL)
py = H + 0.45
seg(m, [-L / 2 - 0.3, py, -0.6], [L / 2 + 0.3, py, -0.6], 0.24, PIPEA, sections=22)   # tuberia grande
seg(m, [-L / 2 - 0.3, py, 0.05], [L / 2 + 0.3, py, 0.05], 0.17, PIPEB, sections=22)   # tuberia media
seg(m, [-L / 2 - 0.3, py + 0.06, 0.65], [L / 2 + 0.3, py + 0.06, 0.65], 0.12, PIPEC, sections=18)
for x in bents:                                              # soportes/silletas
    box(m, 0.16, 0.16, 0.16, [x, H + 0.28, -0.6], DARK)
    box(m, 0.14, 0.16, 0.14, [x, H + 0.25, 0.05], DARK)
for x in (-1.8, 1.8):                                        # bridas en tuberia grande
    seg(m, [x - 0.05, py, -0.6], [x + 0.05, py, -0.6], 0.36, FLG, sections=18)
ex = L / 2 + 0.3                                             # codo (elbow) que baja
seg(m, [ex, py, 0.05], [ex, 0.6, 0.05], 0.17, PIPEB, sections=18)
seg(m, [ex, 0.6, 0.05], [ex + 0.6, 0.6, 0.05], 0.17, PIPEB, sections=18)
seg(m, [-0.22, py, -0.6], [0.22, py, -0.6], 0.34, DARK, sections=16)   # valvula
seg(m, [0, py, -0.6], [0, py + 0.5, -0.6], 0.035, STEEL, sections=6)
ring_y(m, 0.24, 0.035, py + 0.5, STEEL, cx=0, cz=-0.6, mj=22, mn=8)    # volante
export(m, "obra-mecanica.glb")

print("Listo.")
