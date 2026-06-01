/* ═══════════════════════════════════════════════════════════════
   Control del modelo 3D con la MANO
   Cámara + MediaPipe Hands (tasks-vision). Mueve la mano para girar
   el modelo y pellizca (pulgar + índice) para acercar/alejar.
   Todo corre en el navegador del visitante; la librería se carga solo
   al pulsar el botón (no afecta la velocidad de la página).
   ═══════════════════════════════════════════════════════════════ */
(() => {
  const btn = document.getElementById('handBtn');
  const mv = document.getElementById('mv3d');
  const camBox = document.getElementById('handCam');
  const video = document.getElementById('handVideo');
  const statusEl = document.getElementById('handStatus');
  if (!btn || !mv) return;

  const TV = 'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.18';
  const MODEL =
    'https://storage.googleapis.com/mediapipe-models/hand_landmarker/' +
    'hand_landmarker/float16/1/hand_landmarker.task';

  let active = false;
  let stream = null;
  let landmarker = null;
  let raf = null;
  let hadAutoRotate = false;
  let baseRadius = null;          // radio de cámara al iniciar (metros)

  // Suavizado de los movimientos (evita temblor)
  let sTheta = null, sPhi = null, sFactor = 1;
  const lerp = (a, b, t) => a + (b - a) * t;

  const setStatus = (t) => { if (statusEl) statusEl.textContent = t; };

  btn.addEventListener('click', () => (active ? stop() : start()));

  async function start() {
    if (!navigator.mediaDevices?.getUserMedia) {
      setStatus('Tu navegador no permite usar la cámara.');
      camBox.hidden = false;
      return;
    }
    try {
      btn.disabled = true;
      camBox.hidden = false;

      if (!landmarker) {
        setStatus('Cargando detección de manos…');
        const vision = await import(TV);
        const fileset = await vision.FilesetResolver.forVisionTasks(TV + '/wasm');
        landmarker = await vision.HandLandmarker.createFromOptions(fileset, {
          baseOptions: { modelAssetPath: MODEL, delegate: 'GPU' },
          runningMode: 'VIDEO',
          numHands: 1,
        });
      }

      setStatus('Pidiendo permiso de cámara…');
      stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'user', width: { ideal: 640 }, height: { ideal: 480 } },
        audio: false,
      });
      video.srcObject = stream;
      await video.play();

      // Guardamos el estado de la cámara del visor para restaurarlo al salir
      const orbit = mv.getCameraOrbit();
      baseRadius = orbit.radius;
      hadAutoRotate = mv.hasAttribute('auto-rotate');
      mv.removeAttribute('auto-rotate');     // detenemos el giro automático

      active = true;
      btn.disabled = false;
      btn.textContent = '✋ Detener control con la mano';
      btn.classList.add('is-active');
      setStatus('¡Listo! Mueve la mano frente a la cámara.');
      loop();
    } catch (e) {
      console.error('[hand-control]', e);
      const msg = e?.name === 'NotAllowedError'
        ? 'Permiso de cámara denegado.'
        : (e?.message || 'No se pudo iniciar.');
      setStatus('Error: ' + msg);
      btn.disabled = false;
      cleanup();
    }
  }

  function loop() {
    if (!active) return;
    let res = null;
    try { res = landmarker.detectForVideo(video, performance.now()); } catch (_) {}

    if (res && res.landmarks && res.landmarks.length) {
      const lm = res.landmarks[0];
      const palm = lm[9];                 // base del dedo medio ≈ centro de la palma
      const thumb = lm[4], index = lm[8]; // puntas de pulgar e índice

      // Cámara selfie (espejo): mano a la derecha → gira a la derecha
      const targetTheta = (palm.x - 0.5) * 320;       // grados de azimut
      const targetPhi = 25 + palm.y * 85;             // 25°(arriba)–110°(abajo)

      // Pellizco: distancia pulgar↔índice → factor de zoom (0.6 cerca, 1.6 lejos)
      const pinch = Math.hypot(thumb.x - index.x, thumb.y - index.y);
      const targetFactor = Math.min(1.6, Math.max(0.6, pinch / 0.18 + 0.45));

      sTheta = sTheta == null ? targetTheta : lerp(sTheta, targetTheta, 0.25);
      sPhi   = sPhi   == null ? targetPhi   : lerp(sPhi, targetPhi, 0.25);
      sFactor = lerp(sFactor, targetFactor, 0.20);

      const rad = (baseRadius || 4) * sFactor;
      mv.cameraOrbit = `${sTheta.toFixed(1)}deg ${sPhi.toFixed(1)}deg ${rad.toFixed(2)}m`;
      setStatus('✋ Detectando tu mano…');
    } else {
      setStatus('Muestra tu mano abierta frente a la cámara.');
    }
    raf = requestAnimationFrame(loop);
  }

  function stop() {
    active = false;
    btn.textContent = '✋ Controlar con la mano';
    btn.classList.remove('is-active');
    if (hadAutoRotate) mv.setAttribute('auto-rotate', '');
    cleanup();
    setStatus('');
    camBox.hidden = true;
  }

  function cleanup() {
    if (raf) { cancelAnimationFrame(raf); raf = null; }
    if (stream) { stream.getTracks().forEach((t) => t.stop()); stream = null; }
    if (video) video.srcObject = null;
    sTheta = sPhi = null; sFactor = 1;
  }

  // Si el usuario cambia de pestaña, liberamos la cámara
  document.addEventListener('visibilitychange', () => {
    if (document.hidden && active) stop();
  });
})();
