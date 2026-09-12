# Pantalla LED — 3863 × 336

Paquete de producción para el contenido de la pantalla del evento.
Imágenes en ChatGPT, video en DaVinci Resolve.

**Marca del evento:** Cumbre de los Millonarios Conscientes. Blanco sobre negro,
monocromo. **Productora:** Aura Productions, que aparece solo en la placa de
créditos y es la única pieza con dorado.

## Ficha técnica

| | |
|---|---|
| Resolución declarada | 3863 × 336 px |
| **Resolución de trabajo** | **3864 × 336 px** |
| Relación de aspecto | 11,5 : 1 |
| Cuadros por segundo | 30 (confirmar con el técnico) |
| Espacio de color | Rec.709, gamma 2.4 |
| Área segura | 193 px a los lados, 34 px arriba y abajo |
| Altura de mayúscula mínima | 90 px texto principal, 48 px secundario |

### Por qué 3864 y no 3863

3863 es impar. H.264, H.265 y ProRes trabajan con submuestreo de croma que
exige ancho y alto pares, así que un video de 3863 px de ancho no se puede
codificar. Se renderiza en 3864 y el procesador de LED descarta o rellena esa
columna sobrante: 1 px en 3863 es invisible.

Si el técnico insiste en los 3863 exactos, la salida tiene que ser una
**secuencia de PNG**, que no tiene esa restricción. Es más pesada y no todos
los servidores de reproducción la aceptan. Preguntale antes de renderizar.

**Tres cosas para confirmarle al proveedor de la pantalla antes de empezar:**

1. Resolución exacta de entrada del procesador y si acepta 3864.
2. Cuadros por segundo: 30 o 60. Si entregás a 25 y la pantalla corre a 30, va
   a saltar.
3. Si la pantalla es una sola superficie o varios módulos con procesadores
   separados. Si son varios, puede que necesiten el archivo ya partido.

## El flujo, de punta a punta

```
ChatGPT  ──►  imágenes 1536×1024  ──►  DaVinci Resolve  ──►  MP4 / ProRes
(fondos)      (se recortan a banda)     (montaje, texto,      3864×336
                                         logo, movimiento)
```

El reparto de tareas importa:

- **ChatGPT hace los fondos.** Texturas, atmósfera, luz, niebla.
- **Resolve hace todo lo que tiene que leerse.** Texto, logos, números, nombres.

Nunca al revés. El texto generado por IA sale mal escrito y a baja resolución,
y en una pantalla de 336 px de alto cualquier pérdida de nitidez se nota.

## Antes de nada: poner los logos

El generador de plantillas busca cada logo dentro de `public/images/`:

| Marca | Archivo que espera | Estado |
|---|---|---|
| Cumbre | `public/images/cumbre-logo.png` | **falta, hay que agregarlo** |
| Aura | `public/images/logo.png` | ya está |

El de la Cumbre tiene que ser **PNG con fondo transparente y al menos 1500 px de
alto**. Un JPG con fondo negro no sirve: en la pantalla se va a ver el borde del
recuadro contra el fondo del video.

Mientras el archivo no esté, las placas se generan igual, pero con un recuadro
punteado que dice "FALTA EL LOGO" en el lugar y el tamaño exactos. Sirve para
seguir maquetando, no para renderizar.

## Paso 1 — Imágenes en ChatGPT

Los prompts están en **[`prompts-chatgpt.md`](prompts-chatgpt.md)**: diez escenas
listas para copiar y pegar, más la placa de productora, con los bloques de estilo
de cada marca ya incluidos.

Lo esencial: ChatGPT Plus genera como máximo 1536 × 1024. No existe forma de
pedirle la banda de 3863 × 336 directamente. Se genera en horizontal y el
recorte se hace en Resolve, así que los prompts le piden que ponga lo importante
en la franja media del cuadro.

Adjuntale `plantillas/cumbre_guia-recorte-chatgpt_1536x1024.png` junto con el
prompt. Es la imagen que le muestra qué parte del cuadro sobrevive al recorte.

Guardá todo en una carpeta sola, con nombres numerados:
`~/CumbreLED/imagenes/01-ambiente.png`, `02-apertura-panel1.png`, y así.

## Paso 2 — Montaje en DaVinci Resolve

### Configurar el proyecto

Project Settings (engranaje abajo a la derecha) > Master Settings:

- Timeline resolution → **Custom** → `3864` × `336`
- Timeline frame rate → el que te confirmó el técnico
- Playback frame rate → el mismo
- Image Scaling > Input scaling → **Scale entire image to fit**

Ese último punto no es opcional: los números de recorte de más abajo asumen esa
configuración.

### Armarlo con el script

`resolve/armar_pantalla_led.py` crea el proyecto con la resolución correcta,
importa la carpeta de imágenes y arma la línea de tiempo con una duración fija
por imagen. Editá `CARPETA_IMAGENES` arriba del archivo y correlo desde
Workspace > Console (pestaña Py3) dentro de Resolve:

```python
exec(open("/ruta/a/armar_pantalla_led.py").read())
```

El encabezado del script explica también cómo correrlo desde la terminal.

### Recortar una imagen a la banda, a mano

En el Inspector del clip, con la imagen de 1536 × 1024 seleccionada:

| Uso | Zoom | Position X | Position Y |
|---|---|---|---|
| Fondo único, cubre todo el ancho | 7,667 | 0 | 0 |
| Mosaico, panel 1 de 4 | 1,917 | −1449 | 0 |
| Mosaico, panel 2 de 4 | 1,917 | −483 | 0 |
| Mosaico, panel 3 de 4 | 1,917 | 483 | 0 |
| Mosaico, panel 4 de 4 | 1,917 | 1449 | 0 |

El fondo único es una ampliación de 2,5×, así que solo usalo con imágenes
suaves: niebla, bokeh, degradados. Con detalle fino se ve pastoso. El mosaico,
en cambio, reduce la escala y queda nítido.

Position Y en 0 toma la franja central de la imagen. Movelo si el motivo quedó
alto o bajo en el cuadro.

Las costuras del mosaico se disimulan poniendo cada panel en su propia pista de
video, con un poco de superposición y una máscara de bordes suaves en el nodo de
color. Un desenfoque de 20–30 px sobre el borde alcanza.

### Darle movimiento a una imagen fija

**[`fusion-nubes-en-movimiento.md`](fusion-nubes-en-movimiento.md)** tiene el
árbol de nodos completo para animar una placa de nubes: deformación con ruido
Perlin, deriva lenta, cómo cerrar el loop y cómo mantener el logo quieto y
nítido mientras el fondo se mueve. La misma receta sirve para niebla, humo y
cualquier textura suave.

### Las plantillas

En `plantillas/` está esto, con el nombre de la marca como prefijo:

| Archivo | Para qué |
|---|---|
| `<marca>_guia-encuadre_3864x336.png` | Capa de guía: área segura, tercios, costuras del mosaico, alturas de texto. **Apagala antes de renderizar.** |
| `<marca>_base-degradado_3864x336.png` | Placa de fondo neutra, por si una imagen de ChatGPT no convence |
| `<marca>_placa-simbolo-centrado_3864x336.png` | El símbolo centrado, con transparencia |
| `<marca>_placa-lockup-izquierda_3864x336.png` | El símbolo contra el margen izquierdo, dejando la banda libre para el texto |
| `<marca>_guia-recorte-chatgpt_1536x1024.png` | Para adjuntar a los prompts |
| `comun_vineta-bordes_3864x336.png` | Viñeta para poner encima de la imagen, en modo Multiply. Apaga los bordes y concentra la atención en el centro |

Las placas traen **solo el símbolo, sin el texto del logotipo**. Los dos logos
apilan símbolo arriba y nombre abajo: a 336 px de alto, la bajada "DE LOS
MILLONARIOS CONSCIENTES" mediría unos 8 px y el "PRODUCTIONS" de Aura unos 6.
Ilegibles. El texto va como texto vivo en Resolve, al lado del símbolo, y por eso
existe la placa de lockup izquierda.

Se regeneran con:

```bash
pip install Pillow
python3 docs/pantallas-led/plantillas/generar_plantillas.py cumbre
python3 docs/pantallas-led/plantillas/generar_plantillas.py todas
```

El diccionario `MARCAS`, arriba del script, tiene el color de acento, el fondo y
la ruta del logo de cada marca. Si la Cumbre tiene un color de acento en su
manual, cambialo ahí y se propaga a todas las plantillas.

### Texto y tipografías

La tipografía de la Cumbre es la del logotipo: una geométrica ancha, de
mayúsculas cuadradas. **Pedile el archivo al diseñador que armó el logo** antes
de maquetar. Si la elegís de memoria vas a maquetar todo el evento con una que
no es.

Para Aura: **Space Grotesk** en el cuerpo, **Playfair Display** en títulos.
Instalá las fuentes en el sistema antes de abrir Resolve, si no el Text+ no las
va a ofrecer.

| Marca | Color | |
|---|---|---|
| Cumbre | Blanco | `#EBEBEB` |
| Cumbre | Negro | `#000000` |
| Aura | Oro | `#C9A84C` |
| Aura | Oro claro | `#E8C97A` |
| Aura | Negro profundo | `#08080F` |

El blanco de la Cumbre es `#EBEBEB` y no `#FFFFFF` a propósito. Ver la sección
que sigue.

## Reglas de diseño para LED

Una pantalla LED no perdona lo que un monitor sí:

- **Nada de blanco puro.** Es la regla que más choca con una marca blanco sobre
  negro, y la que más importa. El LED a 255 encandila a la platea y quema todo
  el detalle del logo. Usá `#EBEBEB` y poné un nodo de color al final de la línea
  de tiempo con el Gain bajado hasta que el pico quede en 92 %.
- **Nada de líneas de 1 px horizontales.** Titilan. Mínimo 3 px, y si igual
  titila, un desenfoque de 1–2 px lo soluciona.
- **Movimiento lento.** En una banda de 11,5:1 el desplazamiento horizontal
  rápido produce arrastre. Un barrido de lado a lado no debería tardar menos de
  6 segundos.
- **Texto grande.** 90 px de altura de mayúscula para lo principal. Parece
  enorme en el monitor; en la sala, a 20 metros, es lo justo.
- **Contenido lejos de los bordes.** 193 px a los lados. Los módulos de los
  extremos suelen quedar tapados por estructura o fuera del ángulo de visión.
- **El loop tiene que cerrar.** Primer cuadro idéntico al último. Si no, se ve
  un salto cada vez que da la vuelta, toda la noche.

## Paso 3 — Renderizar

Página Deliver, preset Custom:

| Campo | Valor |
|---|---|
| Format | MP4 |
| Codec | H.264 |
| Resolution | Custom → 3864 × 336 |
| Frame rate | el del proyecto |
| Quality | Restrict to `80000` Kb/s |
| Key frames | Every `1` frame |
| Audio | Desactivado, salvo que el servidor lo pida |

Los 80 Mb/s son deliberadamente exagerados para una imagen tan chica. El archivo
pesa poco igual por la resolución, y evita que aparezcan bloques de compresión en
los degradados oscuros, que es exactamente donde vive todo este diseño.

**Key frames cada 1 cuadro** hace que el archivo se pueda cortar y loopear en
cualquier punto sin que el servidor tenga que reconstruir el cuadro.

Si el servidor de reproducción acepta ProRes 422 HQ o DNxHR HQ, entregá eso en
lugar de MP4: menos artefactos en las zonas oscuras.

**Data levels**: preguntá al técnico si el procesador espera Video (16–235) o
Full (0–255). Si le entregás el rango equivocado, los negros se van a ver grises
o se van a empastar. Es el error más común de todo este proceso, y en una marca
monocroma sobre negro es el que más se nota.

## Checklist de entrega

- [ ] Logo de la Cumbre en `public/images/cumbre-logo.png`, PNG con transparencia
- [ ] Tipografía de la Cumbre conseguida e instalada
- [ ] Resolución confirmada con el técnico de la pantalla
- [ ] Cuadros por segundo confirmados
- [ ] Data levels confirmados
- [ ] Capa de guía apagada en la línea de tiempo
- [ ] Loop verificado: primer cuadro igual al último
- [ ] Sin blancos por encima del 92 %
- [ ] Texto por encima de los mínimos de altura
- [ ] Archivo probado en la pantalla real, en el montaje, antes del evento
- [ ] Dos pendrives con el archivo, más una copia en la nube
- [ ] Placa neutra de respaldo renderizada por separado, por si algo falla

Ese último punto vale la media hora que lleva. Es lo que ponés en la pantalla
mientras resolvés cualquier otra cosa.

## Qué hay en esta carpeta

```
docs/pantallas-led/
├── README.md                       ← esto
├── prompts-chatgpt.md              ← los prompts, listos para copiar
├── fusion-nubes-en-movimiento.md   ← animar una placa fija en Fusion
├── plantillas/
│   ├── generar_plantillas.py       ← regenera los PNG, una marca o todas
│   ├── comun_vineta-bordes_3864x336.png
│   ├── cumbre_*.png                ← 5 plantillas
│   └── aura_*.png                  ← 5 plantillas
└── resolve/
    └── armar_pantalla_led.py       ← automatiza el armado del proyecto
```
