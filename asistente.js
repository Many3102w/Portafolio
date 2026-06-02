/* ═══════════════════════════════════════════════════════════════
   Asistente "Inge Christopher"
   Chat flotante que responde sobre el CV de Christopher Gómez.
   100% en el navegador (sin servidor, sin API): coincidencia por
   temas a partir del contenido real del CV.
   ═══════════════════════════════════════════════════════════════ */
(() => {
  // ── Base de conocimiento (datos reales del CV) ──────────────────
  const KB = [
    { id: 'perfil', chip: 'Perfil', kw: ['perfil', 'sobre', 'quien es christopher', 'resumen', 'acerca', 'cuentame', 'descripcion'],
      html: '<b>Christopher Manfred Gómez Martínez</b> es pasante de <b>Ingeniería Industrial y de Sistemas</b>. ' +
        'Une dos mundos: 🔧 trabajo <b>industrial</b> en los puertos de Altamira (andamios, pailería y punteo de soldadura) ' +
        'desde los 18 años, y 💻 <b>desarrollo de software</b> (páginas web y apps Android/APK). ' +
        'Disponibilidad para viajar a cualquier lugar.' },

    { id: 'experiencia', chip: 'Experiencia', kw: ['experiencia', 'trabajo', 'laboral', 'empleos', 'trabajado', 'empresas', 'trayectoria'],
      html: '<b>Experiencia industrial:</b><br>• Pailero Tipo A — <b>MEGSA</b>, Altamira (2025)<br>' +
        '• Punteador Flux Core — <b>McDermott</b>, Proyecto Manatee (2024)<br>' +
        '• Andamiero de Primera — <b>Mexichem/Águila</b> y <b>Secoivsa/Alpek</b> (paros de planta, 2024)<br>' +
        '• Auxiliar de bombero — <b>Beria Energy/PEMEX</b> (2024)<br>' +
        '• Ayudante general y andamiero — <b>Grupo México</b> (~1 año, 2023)<br>' +
        '• Pailero Tipo A — <b>Águila</b> (~1 año, 2022)<br>¿Quieres detalle de andamios, pailería o software?' },

    { id: 'andamios', chip: null, kw: ['andamio', 'andamios', 'andamiero', 'layher', 'altura', 'alturas', 'izaje', 'genie', 'manlift'],
      html: '<b>Andamiero de Primera:</b> arma andamios fijos, de fachada, móviles, voladizos y ' +
        'multidireccionales (<b>Layher</b>) hasta 5–6 plantas, anclados a vigas y dentro de tanques/espacios confinados. ' +
        'Opera <b>Genie</b> y <b>manlift</b>. Certificado DC-3 en armado de andamios y trabajo en alturas.' },

    { id: 'soldadura', chip: null, kw: ['pailero', 'paileria', 'soldadura', 'soldar', 'punteo', 'punteador', 'flux', 'arcair', 'probetas', 'inoxidable'],
      html: '<b>Pailería Tipo A y punteo de soldadura:</b> flux core, galvanizado, acero al carbón e inoxidable; ' +
        'probetas (sobremesa, vertical y sobre cabeza) y arcair con carbones. Experiencia en tanques de membrana y ' +
        'pontones, barandales y estructuras.' },

    { id: 'software', chip: 'Software', kw: ['software', 'programacion', 'web', 'app', 'apk', 'react', 'django', 'python', 'android', 'desarrollo', 'iot', 'esp32', 'codigo', 'pagina', 'aplicacion'],
      html: '<b>Desarrollo de software:</b><br>• Web con <b>React</b> (frontend) y <b>Django/Python</b> (backend).<br>' +
        '• Apps <b>Android (APK)</b> con Android Studio, de la idea a versión funcional.<br>' +
        '• Apoyo en <b>IA</b> (ChatGPT, Copilot, Gemini) y conocimientos en <b>ESP32 e IoT</b>.<br>' +
        '<i>Proyectos disponibles a solicitud.</i>' },

    { id: 'habilidades', chip: 'Habilidades', kw: ['habilidad', 'habilidades', 'skills', 'conocimientos', 'capacidades', 'fortalezas', 'sabe hacer'],
      html: '<b>Habilidades:</b><br>• Andamios e izaje (Layher, Genie, manlift)<br>' +
        '• Pailería y soldadura (flux core, probetas, arcair)<br>' +
        '• Obra mecánica, eléctrica y civil; tubería, bridas, colados y armado de varilla<br>' +
        '• Software técnico: <b>AutoCAD</b>, Visio, Excel, Office, PowerShell, Canva<br>' +
        '• Programación: HTML, Python, React, Django, Android Studio, ESP32, IA<br>' +
        '• Soporte y hardware: armado/reparación de PC, Windows, redes básicas' },

    { id: 'formacion', chip: 'Formación', kw: ['formacion', 'estudios', 'educacion', 'carrera', 'universidad', 'estudio', 'titulo', 'academica', 'escuela'],
      html: '<b>Formación académica:</b><br>• <b>Ingeniería Industrial y de Sistemas</b> — Universidad Interamericana del Norte (carta pasante).<br>' +
        '• <b>Laboratorista Químico</b> — CBTIS 105.' },

    { id: 'certificaciones', chip: null, kw: ['certificacion', 'certificaciones', 'dc-3', 'dc3', 'seguridad', 'credencial', 'cursos'],
      html: '<b>Certificaciones y seguridad:</b><br>• DC-3 Armado seguro de andamios<br>• DC-3 Trabajo en alturas<br>' +
        '• Inducción de seguridad industrial<br>• Credencial de Andamiero' },

    { id: 'diseno3d', chip: 'Diseño 3D', kw: ['3d', 'autocad', 'diseno', 'modelo', 'modelos', 'maqueta', 'realidad aumentada', 'excavadora', 'tanque', 'placa', 'colado'],
      html: 'En el portafolio hay <b>9 diseños 3D</b> que Christopher modela: obra civil (dados y <b>colado de losa</b>), ' +
        'techado de taller, tanque, obra mecánica, casa de bombas, excavadora y placas electrónicas (ESP32, DWM1001). ' +
        'Puedes <b>girarlos</b>, ver <b>etiquetas</b> de sus partes y colocarlos en tu <b>piso en AR</b>. 👉 Mira la sección “Diseño 3D”.' },

    { id: 'contacto', chip: 'Contacto', kw: ['contacto', 'telefono', 'whatsapp', 'correo', 'email', 'mail', 'ubicacion', 'vive', 'llamar', 'numero'],
      html: '📞 <b>Tel/WhatsApp:</b> <a href="https://wa.me/528146015247" target="_blank" rel="noopener">814 601 5247</a><br>' +
        '✉️ <b>Correo:</b> <a href="mailto:kikinmanfred@gmail.com">kikinmanfred@gmail.com</a><br>' +
        '📍 Altamira, Tamaulipas, México &nbsp;·&nbsp; ✈️ Disponible para viajar.' },

    { id: 'cv', chip: '⬇ CV', kw: ['cv', 'curriculum', 'descargar', 'pdf', 'hoja de vida', 'resume'],
      html: 'Puedes descargar el CV en PDF aquí: 👉 <a href="cv/CV_Christopher_Gomez_Martinez.pdf" download>Descargar CV</a>.<br>' +
        '¿Quieres que te resuma el perfil, la experiencia o las habilidades?' },

    { id: 'idiomas', chip: null, kw: ['idioma', 'idiomas', 'ingles', 'lengua'],
      html: '<b>Idiomas:</b> Español (nativo) e Inglés básico.' },

    { id: 'objetivo', chip: null, kw: ['objetivo', 'puesto', 'busca', 'vacante', 'meta', 'aspira'],
      html: '<b>Objetivo:</b> auxiliar de calidad, supervisión, seguridad, almacén o general, y/o desarrollo de software. ' +
        'Busca sumar su experiencia industrial y de programación.' },

    { id: 'disponibilidad', chip: null, kw: ['disponibilidad', 'viajar', 'reubicar', 'mudarse', 'disponible'],
      html: 'Sí ✅ — tiene <b>disponibilidad para viajar a cualquier lugar</b>.' },

    { id: 'porque', chip: null, kw: ['porque', 'contratar', 'ventaja', 'aporta', 'valor'],
      html: '<b>¿Por qué Christopher?</b> Combina campo industrial (andamios, pailería, soldadura, obra) con software ' +
        '(web, apps, automatización). Aporta en obra y en lo técnico/administrativo: reportes, software técnico y AutoCAD. ' +
        'Además, disponibilidad para viajar.' },
  ];

  const FALLBACK =
    'Mmm, eso no lo tengo a la mano 🤔. Puedo contarte sobre: <b>Perfil</b>, <b>Experiencia</b>, <b>Habilidades</b>, ' +
    '<b>Formación</b>, <b>Certificaciones</b>, <b>Software</b>, <b>Diseño 3D</b> o <b>Contacto</b>. ' +
    'También puedes <a href="cv/CV_Christopher_Gomez_Martinez.pdf" download>descargar el CV</a>. ¿Qué te interesa?';

  const byId = (id) => KB.find((e) => e.id === id);
  const norm = (s) => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');

  function answerFor(text) {
    const t = ' ' + norm(text) + ' ';
    if (/\b(hola|buenas|buenos dias|buenas tardes|buenas noches|hey|que tal|saludos|inge)\b/.test(t))
      return '¡Hola! 👷 Soy <b>Inge Christopher</b>. Puedo contarte del <b>perfil</b>, <b>experiencia</b>, ' +
        '<b>habilidades</b>, <b>formación</b>, <b>diseños 3D</b> o el <b>contacto</b> de Christopher. ¿Qué te gustaría saber?';
    if (/\b(gracias|grac|thank)\b/.test(t)) return '¡Con gusto! 👷 ¿Algo más en lo que pueda ayudarle?';
    if (/\b(adios|hasta luego|bye|nos vemos|chao)\b/.test(t)) return '¡Hasta pronto! 👋 Aquí estaré si necesita algo más.';

    let best = null, score = 0;
    for (const e of KB) {
      let s = 0;
      for (const k of e.kw) if (t.includes(norm(k))) s += 1;
      if (s > score) { score = s; best = e; }
    }
    return best ? best.html : FALLBACK;
  }

  // ── Construcción de la interfaz ─────────────────────────────────
  const launcher = document.createElement('button');
  launcher.className = 'asst-launch';
  launcher.type = 'button';
  launcher.setAttribute('aria-label', 'Abrir asistente Inge Christopher');
  launcher.innerHTML = '<span class="asst-launch__ava">👷</span><span class="asst-launch__txt">Inge Christopher</span>';

  const panel = document.createElement('section');
  panel.className = 'asst-panel';
  panel.setAttribute('aria-live', 'polite');
  panel.hidden = true;
  panel.innerHTML =
    '<header class="asst-head">' +
      '<span class="asst-head__ava">👷</span>' +
      '<span class="asst-head__id"><strong>Inge Christopher</strong><small>Asistente del portafolio · en línea</small></span>' +
      '<button class="asst-head__voice" id="asstVoice" type="button" aria-label="Activar o silenciar voz" title="Voz">🔊</button>' +
      '<button class="asst-head__x" type="button" aria-label="Cerrar">✕</button>' +
    '</header>' +
    '<div class="asst-body" id="asstBody"></div>' +
    '<div class="asst-quick" id="asstQuick"></div>' +
    '<form class="asst-input" id="asstForm" autocomplete="off">' +
      '<button class="asst-mic" id="asstMic" type="button" aria-label="Hablar por voz" title="Hablar">🎤</button>' +
      '<input id="asstText" type="text" placeholder="Escribe o habla tu pregunta…" aria-label="Escribe tu pregunta" />' +
      '<button type="submit" aria-label="Enviar">➤</button>' +
    '</form>';

  document.body.appendChild(launcher);
  document.body.appendChild(panel);

  const body = panel.querySelector('#asstBody');
  const quick = panel.querySelector('#asstQuick');
  const form = panel.querySelector('#asstForm');
  const input = panel.querySelector('#asstText');
  const voiceBtn = panel.querySelector('#asstVoice');
  const micBtn = panel.querySelector('#asstMic');

  // ── Voz: leer las respuestas en voz alta (text-to-speech) ───────
  let voiceOn = true;
  const synth = window.speechSynthesis;
  const stripper = document.createElement('div');
  function toSpeech(html) {
    stripper.innerHTML = html;
    let t = stripper.textContent || '';
    // quita URLs y símbolos/emojis que no conviene leer
    t = t.replace(/https?:\/\/\S+/g, '').replace(/[•👷🔧💻📞✉️📍✈️👉⬇✅🤔👋🎉🔊🔇🎤]/g, ' ');
    return t.replace(/\s+/g, ' ').trim();
  }
  function pickVoice() {
    const vs = synth ? synth.getVoices() : [];
    return vs.find((v) => /^es(-|_)?mx/i.test(v.lang)) ||
           vs.find((v) => /^es(-|_|$)/i.test(v.lang)) || null;
  }
  function speak(text) {
    if (!voiceOn || !synth || !text) return;
    synth.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = 'es-MX'; u.rate = 1; u.pitch = 1;
    const v = pickVoice(); if (v) u.voice = v;
    synth.speak(u);
  }
  if (synth) synth.onvoiceschanged = pickVoice; // precarga voces

  voiceBtn.addEventListener('click', () => {
    voiceOn = !voiceOn;
    voiceBtn.textContent = voiceOn ? '🔊' : '🔇';
    voiceBtn.classList.toggle('is-off', !voiceOn);
    if (!voiceOn && synth) synth.cancel();
  });

  // ── Micrófono: hablarle al asistente (speech-to-text) ───────────
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  let recog = null, listening = false;
  if (SR) {
    recog = new SR();
    recog.lang = 'es-MX'; recog.interimResults = false; recog.maxAlternatives = 1;
    recog.onresult = (e) => {
      const said = e.results[0][0].transcript;
      send(said);
    };
    recog.onend = () => { listening = false; micBtn.classList.remove('is-listening'); };
    recog.onerror = () => { listening = false; micBtn.classList.remove('is-listening'); };
    micBtn.addEventListener('click', () => {
      if (listening) { recog.stop(); return; }
      if (synth) synth.cancel();          // no escucharse a sí mismo
      try { recog.start(); listening = true; micBtn.classList.add('is-listening'); } catch (_) {}
    });
  } else {
    micBtn.style.display = 'none';        // navegador sin reconocimiento de voz
  }

  function addMsg(content, who) {
    const m = document.createElement('div');
    m.className = 'asst-msg asst-msg--' + who;
    if (who === 'bot') m.innerHTML = content; else m.textContent = content;
    body.appendChild(m);
    body.scrollTop = body.scrollHeight;
    return m;
  }

  function botReply(content) {
    const typing = addMsg('<span class="asst-typing"><i></i><i></i><i></i></span>', 'bot');
    setTimeout(() => {
      typing.innerHTML = content;
      body.scrollTop = body.scrollHeight;
      speak(toSpeech(content));
    }, 380);
  }

  function send(text) {
    addMsg(text, 'user');
    botReply(answerFor(text));
  }

  // Chips de acceso rápido (temas con "chip")
  KB.filter((e) => e.chip).forEach((e) => {
    const b = document.createElement('button');
    b.className = 'asst-chip';
    b.type = 'button';
    b.textContent = e.chip;
    b.addEventListener('click', () => { addMsg(e.chip, 'user'); botReply(e.html); });
    quick.appendChild(b);
  });

  form.addEventListener('submit', (ev) => {
    ev.preventDefault();
    const v = input.value.trim();
    if (!v) return;
    input.value = '';
    send(v);
  });

  let greeted = false;
  function openPanel() {
    panel.hidden = false;
    launcher.classList.add('is-open');
    if (!greeted) {
      greeted = true;
      botReply('¡Hola! 👷 Soy <b>Inge Christopher</b>, asistente de este portafolio.<br><b>¿En qué puedo ayudarle?</b>');
      setTimeout(() => addMsg('Puedes tocar un tema de abajo o escribir tu pregunta. 👇', 'bot'), 760);
    }
    setTimeout(() => input.focus(), 120);
  }
  function closePanel() { panel.hidden = true; launcher.classList.remove('is-open'); }

  launcher.addEventListener('click', () => (panel.hidden ? openPanel() : closePanel()));
  panel.querySelector('.asst-head__x').addEventListener('click', closePanel);
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !panel.hidden) closePanel(); });
})();
