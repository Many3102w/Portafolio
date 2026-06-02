/* ═══════════════════════════════════════════════════════════════
   Interactividad del portafolio
   ═══════════════════════════════════════════════════════════════ */

// ── 1. Año actual en el footer ──────────────────────────────────
document.getElementById('year').textContent = new Date().getFullYear();

// ── 2. Menú móvil ───────────────────────────────────────────────
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');

navToggle.addEventListener('click', () => {
  const open = navLinks.classList.toggle('is-open');
  navToggle.classList.toggle('is-open', open);
  navToggle.setAttribute('aria-expanded', String(open));
});

// Cerrar el menú al pulsar un enlace
navLinks.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('is-open');
    navToggle.classList.remove('is-open');
    navToggle.setAttribute('aria-expanded', 'false');
  });
});

// ── 3. Efecto de escritura en el hero ───────────────────────────
//    👇 EDITA: cambia estos roles por los tuyos
const ROLES = [
  'Ing. Industrial y de Sistemas',
  'Desarrollador web y de apps (APK)',
  'Andamiero · Pailero · Punteador',
  'Campo industrial + software',
];

const typedEl = document.getElementById('typed');

(function typeLoop() {
  let roleIndex = 0;
  let charIndex = 0;
  let deleting = false;

  function tick() {
    const role = ROLES[roleIndex];
    typedEl.textContent = role.slice(0, charIndex);

    if (!deleting && charIndex < role.length) {
      charIndex++;
      setTimeout(tick, 90);
    } else if (deleting && charIndex > 0) {
      charIndex--;
      setTimeout(tick, 45);
    } else {
      deleting = !deleting;
      if (!deleting) roleIndex = (roleIndex + 1) % ROLES.length;
      setTimeout(tick, deleting ? 1400 : 350);
    }
  }
  tick();
})();

// ── 4. Animación al hacer scroll (scroll-reveal) ────────────────
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.12 }
);

document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));

// ── 5. Galería 3D dirigida por scroll ───────────────────────────
const modelViewer = document.querySelector('#mv3d');
const steps = document.querySelectorAll('.showcase__step');
const dots = document.querySelectorAll('.showcase__dot');

if (modelViewer && steps.length) {
  let currentModel = modelViewer.getAttribute('src');
  let stepObserver = null;

  const activate = (step) => {
    const idx = [...steps].indexOf(step);
    steps.forEach((s) => s.classList.remove('is-active'));
    step.classList.add('is-active');
    dots.forEach((d, i) => d.classList.toggle('is-active', i === idx));

    const model = step.dataset.model;
    if (model && model !== currentModel) {
      currentModel = model;
      modelViewer.setAttribute('src', model);
      if (step.dataset.orbit) modelViewer.setAttribute('camera-orbit', step.dataset.orbit);
      const heading = step.querySelector('h3');
      if (heading) modelViewer.setAttribute('alt', heading.textContent);
    }
  };

  // La "zona activa" va al centro en escritorio y más abajo en móvil
  // (donde el visor fijo ocupa la parte de arriba), y se recalcula al redimensionar.
  const buildObserver = () => {
    if (stepObserver) stepObserver.disconnect();
    const mobile = window.matchMedia('(max-width: 860px)').matches;
    const rootMargin = mobile ? '-68% 0px -16% 0px' : '-45% 0px -45% 0px';
    stepObserver = new IntersectionObserver(
      (entries) => entries.forEach((e) => { if (e.isIntersecting) activate(e.target); }),
      { rootMargin, threshold: 0 }
    );
    steps.forEach((s) => stepObserver.observe(s));
  };

  buildObserver();

  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(buildObserver, 250);
  });
}

// ── 6. Figuras 3D del hero: cambian solas cada 4 segundos ───────
const hero3d = document.querySelector('#hero3d');
if (hero3d) {
  const HERO_MODELS = [
    { src: 'assets/tanque.glb', orbit: '30deg 78deg auto' },
    { src: 'assets/obra-civil.glb', orbit: '40deg 70deg auto' },
    { src: 'assets/colado.glb', orbit: '32deg 68deg auto' },
    { src: 'assets/obra-mecanica.glb', orbit: '45deg 72deg auto' },
    { src: 'assets/casa-bombas.glb', orbit: '42deg 76deg auto' },
    { src: 'assets/techado-taller.glb', orbit: '46deg 70deg auto' },
    { src: 'assets/excavadora.glb', orbit: '25deg 80deg auto' },
    { src: 'assets/esp32.glb', orbit: '35deg 65deg auto' },
    { src: 'assets/dwm1001-dev.glb', orbit: '30deg 68deg auto' },
  ];
  let heroIdx = 0;
  setInterval(() => {
    heroIdx = (heroIdx + 1) % HERO_MODELS.length;
    hero3d.setAttribute('src', HERO_MODELS[heroIdx].src);
    hero3d.setAttribute('camera-orbit', HERO_MODELS[heroIdx].orbit);
  }, 4000);
}
