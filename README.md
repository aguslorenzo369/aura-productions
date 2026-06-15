# Aura Productions — Next.js Web

## Stack
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Framer Motion (ready to use)
- GSAP (ready to use)

## Estructura de carpetas

```
src/
├── app/
│   ├── layout.tsx        ← Root layout (meta, fonts)
│   └── page.tsx          ← Página principal (compone secciones)
├── components/
│   ├── layout/
│   │   ├── Navbar.tsx
│   │   └── Footer.tsx
│   └── sections/
│       ├── Hero.tsx       ← Hero con fénix animado + partículas
│       ├── Ticker.tsx     ← Banda de datos en movimiento
│       ├── Services.tsx   ← Grid de 3 servicios
│       ├── Numbers.tsx    ← Stats de impacto
│       ├── Manifesto.tsx  ← Cita filosófica
│       └── CtaFinal.tsx   ← CTA + contacto
├── styles/
│   └── globals.css
public/
└── images/
    └── logo.png           ← ⚠️ COPIAR LOGO AQUÍ
```

## Setup local

```bash
npm install
npm run dev
# → http://localhost:3000
```

## ⚠️ Antes de correr: agregar el logo

Copiá el archivo `Logo_principal_-_AURA_PRODUCTIONS.png` (o `3.png`) a:
```
public/images/logo.png
```

## Deploy en Hostinger

Hostinger Business soporta Node.js. Pasos:

### Opción A — Node.js app (recomendado)
1. En hPanel → Websites → tu sitio → Node.js
2. Configurar: Node version 18+, startup file: `server.js`
3. Subir el proyecto via Git o FTP
4. En el root del proyecto: `npm install && npm run build`
5. Crear `server.js`:
```js
const { createServer } = require('http')
const { parse } = require('url')
const next = require('next')
const app = next({ dev: false })
const handle = app.getRequestHandler()
app.prepare().then(() => {
  createServer((req, res) => {
    const parsedUrl = parse(req.url, true)
    handle(req, res, parsedUrl)
  }).listen(3000)
})
```

### Opción B — Export estático (más simple)
Cambiar en `next.config.js`:
```js
output: 'export'
```
Luego `npm run build` genera carpeta `out/` — subí esa carpeta via FTP a `public_html/`.

> ⚠️ Export estático no soporta Server Components con data fetching dinámico. Para esta web es suficiente.

## Próximas secciones a agregar
- [ ] Quiénes somos (About)
- [ ] Portfolio / Proyectos
- [ ] Filosofía expandida
- [ ] Formulario de contacto
- [ ] Página: Propuesta CMC 2026 (protegida)
- [ ] Página: Staff Hub CMC 2026 (protegida)

## Tipografías usadas
- **Space Grotesk** — cuerpo, UI, botones
- **Playfair Display** — títulos em, manifesto, citas

## Paleta
| Token | Hex |
|-------|-----|
| Gold | `#C9A84C` |
| Gold Light | `#E8C97A` |
| Black | `#000000` |
| Deep | `#08080F` |
| Text muted | `rgba(255,255,255,0.38)` |
