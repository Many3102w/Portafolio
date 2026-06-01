# -*- coding: utf-8 -*-
"""
Genera el CV de Christopher Gómez Martínez en PDF para la web.
VERSIÓN SIN DATOS SENSIBLES: no incluye CURP, RFC ni NSS.
Perfil combinado: trabajo industrial + desarrollo web y apps (APK).

Para regenerarlo tras editar el contenido:
    python generar_cv.py
"""
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                HRFlowable, KeepTogether)
from reportlab.lib.styles import ParagraphStyle

OUT = r"C:\Users\Many\Desktop\Portafolio Programacion\cv\CV_Christopher_Gomez_Martinez.pdf"

# ── Colores ──────────────────────────────────────────────────────────
ACCENT = HexColor('#4f46e5')   # indigo (igual marca que el portafolio)
DARK   = HexColor('#1f2430')
MUTED  = HexColor('#5b6472')
RULE   = HexColor('#c7ccd6')

# ── Estilos ──────────────────────────────────────────────────────────
S = dict(
    name    = ParagraphStyle('name', fontName='Helvetica-Bold', fontSize=20, leading=23, textColor=ACCENT, spaceAfter=2),
    role    = ParagraphStyle('role', fontName='Helvetica', fontSize=9.8, leading=13, textColor=DARK, spaceAfter=3),
    contact = ParagraphStyle('contact', fontName='Helvetica', fontSize=8.8, leading=12, textColor=MUTED, spaceAfter=2),
    section = ParagraphStyle('section', fontName='Helvetica-Bold', fontSize=11.5, leading=14, textColor=ACCENT, spaceBefore=11, spaceAfter=2),
    body    = ParagraphStyle('body', fontName='Helvetica', fontSize=9.3, leading=13, textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=3),
    jtitle  = ParagraphStyle('jtitle', fontName='Helvetica-Bold', fontSize=10, leading=12.5, textColor=DARK, spaceBefore=6),
    jmeta   = ParagraphStyle('jmeta', fontName='Helvetica-Oblique', fontSize=8.6, leading=11, textColor=MUTED, spaceAfter=2),
    bullet  = ParagraphStyle('bullet', fontName='Helvetica', fontSize=9.0, leading=12, textColor=DARK, leftIndent=13, bulletIndent=3, spaceAfter=1),
    skill   = ParagraphStyle('skill', fontName='Helvetica', fontSize=9.1, leading=13, textColor=DARK, spaceAfter=2),
)

def section(title):
    return [Paragraph(title, S['section']),
            HRFlowable(width='100%', thickness=0.8, color=RULE, spaceBefore=1, spaceAfter=4)]

def bullets(items):
    return [Paragraph(t, S['bullet'], bulletText='•') for t in items]

def job(title, meta, items):
    return KeepTogether([Paragraph(title, S['jtitle']), Paragraph(meta, S['jmeta'])] + bullets(items))

def skill(label, items):
    return Paragraph('<b>%s:</b> %s' % (label, items), S['skill'])

# ── Contenido ────────────────────────────────────────────────────────
story = []

# Encabezado
story.append(Paragraph('Christopher Manfred G&#243;mez Mart&#237;nez', S['name']))
story.append(Paragraph(
    'Ingenier&#237;a Industrial y de Sistemas (pasante) &#183; Andamiero &#183; Pailero Tipo A &#183; '
    'Punteador &#183; Desarrollo web y apps Android (APK)', S['role']))
story.append(Paragraph(
    'Altamira, Tamaulipas, M&#233;xico &#160;&#183;&#160; Tel / WhatsApp: 814 601 5247 &#160;&#183;&#160; '
    'kikinmanfred@gmail.com', S['contact']))
story.append(HRFlowable(width='100%', thickness=1.2, color=ACCENT, spaceBefore=5, spaceAfter=2))

# Perfil profesional
story += section('PERFIL PROFESIONAL')
story.append(Paragraph(
    'Egresado de Ingenier&#237;a Industrial y de Sistemas (carta pasante) con un perfil que une dos mundos. '
    'Por un lado, experiencia industrial desde los 18 a&#241;os en los principales puertos de Altamira: armado de '
    'andamios (fijos, de fachada, m&#243;viles, voladizos y multidireccionales hasta 5&#8211;6 plantas), pailer&#237;a y '
    'punteo de soldadura (flux core, galvanizado, acero al carb&#243;n e inoxidable), y operaci&#243;n de equipo de '
    'izaje como Genie y manlift. Por otro, el desarrollo de software: creo p&#225;ginas web y aplicaciones Android '
    '(APK), apoy&#225;ndome en herramientas de IA. Esta combinaci&#243;n me permite aportar tanto en campo como en la '
    'parte t&#233;cnica y administrativa (reportes, software t&#233;cnico, automatizaci&#243;n). Disponibilidad para '
    'viajar a cualquier lugar.', S['body']))
story.append(Paragraph(
    '<b>Objetivo:</b> auxiliar de calidad, supervisi&#243;n, seguridad, almac&#233;n o general, '
    'y/o desarrollo de software.', S['body']))

# Experiencia laboral
story += section('EXPERIENCIA LABORAL')
story.append(job(
    'Pailero Tipo A', 'MEGSA &#183; Puerto Industrial Altamira &#183; Ene 2025',
    ['Tanques de membrana y pontones en acero al carb&#243;n: empate y ajuste de la membrana y punteo.',
     'Operaci&#243;n de Genie para retirar la cinta de protecci&#243;n de la soldadura del tanque.']))
story.append(job(
    'Ayudante de Soldador / Punteador Flux Core', 'McDermott &#183; Puerto Industrial Altamira &#183; Ago 2024 (4 meses)',
    ['Proyecto Manatee: fabricaci&#243;n de contenedores con soldadura flux core.',
     'Punteo flux core y elaboraci&#243;n de probetas (sobremesa, vertical y sobre cabeza); arcair con carbones.']))
story.append(job(
    'Andamiero de Primera', 'Mexichem (subcontratista de &#193;guila) &#183; Valle Esmeralda &#183; Jul 2024 (1 mes &#8211; paro de planta)',
    ['Zona de resinas: andamios Layher multidireccionales y voladizos dentro de tanques; torre m&#243;vil, fija y de fachada.']))
story.append(job(
    'Andamiero de Primera', 'Secoivsa (Alpek) &#183; Puerto Industrial Alpek &#183; Jun 2024 (1 mes &#8211; paro de planta)',
    ['Andamios voladizos para la tuber&#237;a de &#225;cido ac&#233;tico y trabajo en espacios confinados.',
     'Apoyo a tuberos: apertura de bridas, empaques y manejo de tecles, polipastos y eslingas.']))
story.append(job(
    'Auxiliar de Bombero', 'Beria Energy (subcontratista de PEMEX) &#183; Playa de Madero &#183; Mar 2024 (1 mes &#8211; paro de planta)',
    ['Cambio de bridas, reparaci&#243;n de material, pintado y sandblasteo.',
     'Desarmado y armado de v&#225;lvulas con liberaci&#243;n previa de presi&#243;n.']))
story.append(job(
    'Ayudante General y Andamiero', 'Grupo M&#233;xico &#183; Valle Esmeralda, Altamira &#183; May 2023 (~1 a&#241;o)',
    ['Montaje de estructura para tuber&#237;a y obra el&#233;ctrica; andamios de 5&#8211;6 plantas anclados a vigas.',
     'Operaci&#243;n de manlift y Genie; pistola de impacto el&#233;ctrica/neum&#225;tica y pulidor.']))
story.append(job(
    'Pailero Tipo A', '&#193;guila &#183; Valle Esmeralda, Altamira &#183; Jun 2022 (~1 a&#241;o)',
    ['Taller de fabricaci&#243;n para ensambles; uso de equipo de corte.',
     'Punteo de barandales con inversora en galvanizado, acero al carb&#243;n e inoxidable.']))

# Desarrollo de software
story += section('DESARROLLO DE SOFTWARE')
story += bullets([
    'P&#225;ginas y aplicaciones web funcionales con React (frontend) y Django / Python (backend).',
    'Aplicaciones Android (APK) desarrolladas con Android Studio, de la idea a una versi&#243;n funcional en uso.',
    'Uso de herramientas de IA (ChatGPT, Copilot, Gemini) para resolver problemas y acelerar el desarrollo; '
    'conocimientos en ESP32 e IoT.',
])
story.append(Paragraph('<i>Proyectos disponibles para mostrar a solicitud.</i>', S['body']))

# Formación
story += section('FORMACI&#211;N ACAD&#201;MICA')
story += bullets([
    '<b>Ingenier&#237;a Industrial y de Sistemas</b> &#8211; Universidad Interamericana del Norte (carta pasante).',
    '<b>Laboratorista Qu&#237;mico</b> &#8211; CBTIS 105.',
])

# Certificaciones
story += section('CERTIFICACIONES Y SEGURIDAD')
story += bullets([
    'DC-3 Armado seguro de andamios.',
    'DC-3 Trabajo en alturas.',
    'Inducci&#243;n de seguridad industrial.',
    'Credencial de Andamiero.',
])

# Habilidades
story += section('HABILIDADES Y CONOCIMIENTOS')
story.append(skill('Andamios e izaje', 'fijos, de fachada, m&#243;viles, voladizos, multidireccionales (Layher), Genie, manlift, maniobras'))
story.append(skill('Pailer&#237;a y soldadura', 'pailer&#237;a Tipo A, punteo, flux core, galvanizado, acero al carb&#243;n, inoxidable, probetas, arcair'))
story.append(skill('Obra y tuber&#237;a', 'obra mec&#225;nica, el&#233;ctrica y civil, tuber&#237;a, bridas y empaques, colados, armado y lectura de varilla'))
story.append(skill('Software t&#233;cnico', 'AutoCAD, Visio, Excel, Word, PowerPoint, Access, PowerShell, Canva'))
story.append(skill('Programaci&#243;n', 'HTML, Python, React, Django, Android Studio (APK), ESP32, IA'))
story.append(skill('Soporte y hardware', 'armado y reparaci&#243;n de PC, cambio de componentes, formateo e instalaci&#243;n de Windows, redes b&#225;sicas'))

# Idiomas y aptitudes
story += section('IDIOMAS Y APTITUDES')
story.append(skill('Idiomas', 'Espa&#241;ol (nativo), Ingl&#233;s b&#225;sico'))
story.append(skill('Aptitudes', 'puntualidad, comunicaci&#243;n efectiva, trabajo en equipo, resoluci&#243;n de problemas, '
                                 'adaptabilidad, pensamiento cr&#237;tico, proactividad, gesti&#243;n del tiempo'))

# Referencias
story += section('REFERENCIAS')
story.append(Paragraph('Cartas de recomendaci&#243;n y referencias disponibles a solicitud.', S['body']))

# ── Construir el PDF ─────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUT, pagesize=LETTER,
    leftMargin=0.62 * inch, rightMargin=0.62 * inch,
    topMargin=0.55 * inch, bottomMargin=0.5 * inch,
    title='CV - Christopher Gomez Martinez',
    author='Christopher Manfred Gomez Martinez',
    subject='Curriculum Vitae',
)
doc.build(story)
print('PDF generado en:', OUT)
