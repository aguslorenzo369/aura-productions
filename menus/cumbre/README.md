# Menú — Cumbre de los Millonarios Conscientes · RosaNegra CDMX

PDF A4 (3 páginas) para enviar a clientes:

1. Portada — logo Cumbre + RosaNegra CDMX
2. Menú 01 — primer tiempo, segundo tiempo y postre
3. Silver | Open Bar

**Sin precios** (por pedido: no se incluye el costo por persona ni el del open bar).

## Regenerar

```bash
./build.sh          # → Menu-Cumbre-RosaNegra-CDMX.pdf
```

Editá `menu.html` (todo el contenido y el diseño están ahí) y volvé a correr `build.sh`.

## Archivos

- `menu.html` — fuente del documento (HTML + CSS de impresión, A4)
- `assets/fonts.css` — Cinzel, Poppins y Michroma embebidas en base64 (el PDF no depende de internet)
- `assets/logo-cumbre.svg` — monograma Cumbre vectorizado
- `build.sh` — render a PDF con Chromium headless

> El monograma está reconstruido en vector y el wordmark **CUMBRE** usa Michroma como sustituto.
> Si se reemplaza `assets/logo-cumbre.svg` por el logo original (SVG/PNG en alta), el PDF queda 100% oficial.
