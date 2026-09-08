# Menú — Cumbre de los Millonarios Conscientes · RosaNegra CDMX

PDF A4 de 3 páginas para enviar a clientes:

1. Portada — Cumbre + RosaNegra CDMX, con dirección y link a Google Maps
2. Menú 01 — primer tiempo, segundo tiempo y postre
3. Silver | Open Bar

**Sin precios** en todo el documento (por pedido).

## El logo

`build.py` busca el logo oficial en `assets/` con estos nombres:

```
assets/logo-cumbre.svg   (ideal)
assets/logo-cumbre.png
assets/logo-cumbre.jpg
```

- **Si el archivo está** → se inserta tal cual en la portada, en el encabezado de las
  páginas 2 y 3 y como marca de agua. Se embebe en el PDF, no queda referenciado.
- **Si no está** → la tapa queda con la mitad superior libre (sin texto ni marca) para
  colocar el logo a mano en Canva, Illustrator o similar. El bloque de abajo
  (menú de la noche · RosaNegra · dirección) queda anclado al pie.

> No hay ningún logo dibujado a mano en el proyecto: o va el archivo oficial, o va el
> espacio libre. Nunca una imitación.

Poné el archivo y corré:

```bash
./build.sh          # → Menu-Cumbre-RosaNegra-CDMX.pdf
```

## Archivos

- `menu.html` — contenido y diseño del documento (CSS de impresión, A4)
- `build.py` / `build.sh` — inserta el logo y renderiza el PDF con Chromium headless
- `assets/fonts.css` — Cinzel, Poppins y Michroma embebidas en base64 (el PDF no depende de internet)

## Dirección

RosaNegra Polanco — Av. Pdte. Masaryk 298, Polanco IV Secc, Miguel Hidalgo, 11550 CDMX.
El link a Google Maps está en la portada y en el pie de las páginas 2 y 3.
