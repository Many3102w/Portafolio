# 🚀 Mi Portafolio de Programador

Portafolio web personal (una sola página, estático) pensado para compartir tu CV mediante un **código QR**.

- **Tecnología:** HTML + CSS + JavaScript (sin dependencias, sin compilación)
- **Hosting:** GitHub Pages (gratis)
- **Estilo:** Oscuro moderno · Responsive (se ve bien en móvil)

---

## 📁 Estructura

```
Portafolio Programacion/
├── index.html        ← La página principal (aquí editas tu contenido)
├── styles.css        ← Los estilos (colores, tipografía, etc.)
├── script.js         ← Interactividad (menú, animaciones, efecto de escritura)
├── generar-qr.html   ← Herramienta para crear tu código QR
├── cv/
│   └── (pon aquí tu CV en PDF)
└── assets/
    └── (pon aquí tu foto y otras imágenes)
```

---

## ✏️ 1. Personalízalo

Abre **`index.html`** y busca los comentarios `👇 EDITA`. Cambia:

- [ ] Tu **nombre** (aparece varias veces) y el `<title>` de la pestaña
- [ ] El texto de presentación (hero) y la sección **Sobre mí**
- [ ] Tus **habilidades** (añade o quita etiquetas)
- [ ] Tus **proyectos** (duplica una tarjeta `<article class="project">` por cada uno)
- [ ] Tu **experiencia** y formación
- [ ] Tus datos de **contacto** (email, GitHub, LinkedIn)
- [ ] Las **iniciales** del avatar (`TN`) o cámbialo por una foto (ver abajo)

**Roles que rotan en el hero:** edita la lista `ROLES` al inicio de `script.js`.

**Cambiar colores:** edita las variables `--accent` y `--accent-2` al inicio de `styles.css`.

### Poner tu foto (opcional)
1. Guarda tu foto en `assets/foto.jpg`
2. En `index.html`, dentro de `<div class="hero__avatar">`, reemplaza el bloque del avatar por:
   ```html
   <img src="assets/foto.jpg" alt="Tu Nombre" class="hero__photo">
   ```

### Tu CV en PDF (web)
El CV que se descarga desde la web está en `cv/CV_Christopher_Gomez_Martinez.pdf` y es una
**versión sin datos sensibles** (sin CURP/RFC/NSS). Se genera con el script `generar_cv.py`:
```powershell
python generar_cv.py
```
Edita el contenido dentro de ese script y vuelve a ejecutarlo para regenerarlo.
⚠️ No publiques tu CV con CURP/RFC/NSS: guarda esa versión completa solo para envíos privados.

### Diseño 3D (galería por scroll)
La sección **Diseño 3D** muestra modelos que la gente puede girar, hacer zoom y ver en
**realidad aumentada (AR)** desde el móvil. El visor queda fijo y **cambia de modelo solo al
hacer scroll** (sin botones): cada "paso" (`.showcase__step`) activa su modelo al entrar en
pantalla. Modelos de muestra:

| Paso | Archivo |
|---|---|
| 🛢️ Tanque industrial | `assets/tanque.glb` |
| 🧱 Obra civil (dados de colado) | `assets/obra-civil.glb` |
| ⚙️ Obra mecánica (tubería) | `assets/obra-mecanica.glb` |
| 🚰 Casa de bombas | `assets/casa-bombas.glb` |
| 🏭 Techado de taller | `assets/techado-taller.glb` |
| 🏗️ Maquinaria pesada (excavadora) | `assets/excavadora.glb` |
| 🗼 Torre | `assets/modelo.glb` |

Los modelos de muestra se generaron con **trimesh**:
- `generar_modelos_industriales.py` → tanque y obra mecánica
- `generar_modelos_obra.py` → obra civil (dados de colado) y techado de taller
- `generar_casa_bombas.py` → casa de bombas
- `generar_excavadora.py` → excavadora hidráulica sobre orugas (estilo DEVELON)
- `generar_modelo.py` → torre

Para poner **tus propios diseños de AutoCAD**:
1. En AutoCAD, exporta tu diseño 3D a **FBX**, **OBJ** o **STL** (comando `EXPORT` / `FBXEXPORT`).
2. Conviértelo a **GLB** (el formato de la web). Opciones gratis:
   - **Blender**: importa el FBX/OBJ y usa *File → Export → glTF 2.0 (.glb)*.
   - O un convertidor online (busca "FBX/OBJ to GLB").
3. Guarda tu archivo en `assets/` (por ejemplo `assets/mi-diseno.glb`).
4. En `index.html` (sección `id="diseno3d"`), apunta un paso a tu archivo cambiando su
   `data-model="assets/mi-diseno.glb"` (y el título `<h3>` / texto del `.showcase__step`).
   Si añades o quitas pasos, ajusta también el número de puntos (`.showcase__dot`) y los rótulos "01 / 05".

---

## 👀 2. Pruébalo en tu computadora

La forma más simple: **doble clic en `index.html`** para abrirlo en el navegador.

Para una vista más fiel (recomendado), levanta un servidor local:

```powershell
# Si tienes Python instalado:
python -m http.server 8000
# Luego abre: http://localhost:8000
```

> En VS Code también puedes usar la extensión **Live Server** (clic derecho → "Open with Live Server").

---

## 🌐 3. Publícalo en GitHub Pages (gratis)

1. Crea una cuenta en [github.com](https://github.com) si no tienes.
2. Crea un **repositorio nuevo** (por ejemplo `portafolio`), público.
3. Sube todos los archivos de esta carpeta al repositorio. Puedes:
   - Arrastrarlos en la web de GitHub (botón **Add file → Upload files**), o
   - Usar Git desde la terminal:
     ```powershell
     git init
     git add .
     git commit -m "Mi portafolio"
     git branch -M main
     git remote add origin https://github.com/TU-USUARIO/portafolio.git
     git push -u origin main
     ```
4. En el repositorio, ve a **Settings → Pages**.
5. En **Source**, elige la rama **`main`** y la carpeta **`/ (root)`**. Guarda.
6. Espera 1–2 minutos. GitHub te dará una URL como:
   ```
   https://TU-USUARIO.github.io/portafolio/
   ```
   ¡Esa es la dirección pública de tu portafolio! 🎉

---

## 📱 4. Genera tu código QR

1. Abre **`generar-qr.html`** en tu navegador (doble clic).
2. Pega la URL de tu portafolio (la de GitHub Pages del paso anterior).
3. Pulsa **Generar QR** y luego **Descargar PNG**.
4. Imprime el QR o ponlo en tu CV, tarjetas de presentación, firma de correo, etc.

> 💡 Prueba siempre el QR con la cámara de tu móvil antes de imprimirlo.

---

## ✅ Checklist final

- [ ] Reemplacé todos los textos de ejemplo por los míos
- [ ] Puse mi CV en PDF dentro de `cv/`
- [ ] (Opcional) Añadí mi foto
- [ ] Revisé que los enlaces (GitHub, LinkedIn, email) funcionan
- [ ] Publiqué en GitHub Pages y abrí la URL para confirmar
- [ ] Generé el QR apuntando a mi URL y lo probé con el móvil

¡Listo! Ahora cualquiera que escanee tu QR llegará directo a tu portafolio y CV. 💜
