# Prompts para ChatGPT — pantalla LED

Pantalla real **3863 × 336 px**. Se trabaja en **3864 × 336** (ver `README.md`).

La marca del evento es la **Cumbre de los Millonarios Conscientes**: blanco sobre
negro, monocromo. Aura Productions aparece solo como productora, en la placa de
créditos, y ahí sí va el dorado.

## Antes de empezar: lo que ChatGPT no puede hacer

ChatGPT Plus genera imágenes en tres tamaños y **ninguno es la banda que necesitás**:

| Formato | Tamaño | Sirve para |
|---|---|---|
| Horizontal | 1536 × 1024 | Todo lo de acá abajo |
| Cuadrado | 1024 × 1024 | Nada, para este caso |
| Vertical | 1024 × 1536 | Nada, para este caso |

No le pidas 3863 × 336: te va a devolver 1536 × 1024 igual, o una imagen con
barras negras dibujadas adentro. Se genera **siempre en horizontal** y el recorte
a banda se hace después, en DaVinci.

## Las dos estrategias

**A — Mosaico de 4 paneles.** Cuatro imágenes horizontales, una al lado de la
otra. Cada una aporta 966 × 336 del resultado final. Todo baja de escala, así que
queda nítido. Es la estrategia para imágenes con detalle real.

**B — Panel único estirado.** Una sola imagen que cubre los 3864 px de ancho.
Es una ampliación de 2,5×, así que **solo funciona con imágenes suaves**: niebla,
bokeh, degradados, partículas desenfocadas. Con detalle fino se ve pastoso.

Cada prompt dice cuál de las dos usar.

## Bloque de estilo — Cumbre (va al final de todos los prompts)

```
Style: cinematic black and white. Monochrome only, absolutely no colour
anywhere in the image. Ultra-wide horizontal composition, deep black
background, soft silver-grey highlights. Elegant, premium, restrained,
high contrast. No text, no letters, no logos, no watermarks, no recognisable
faces. Keep the middle horizontal third of the frame as the important area —
the top and bottom of the image will be cropped away. Leave the centre calm
and uncluttered: text and a logo go on top later. No pure white areas, keep
the brightest highlights at soft grey-white.
```

> Dos pedidos hacen todo el trabajo acá. El de la **franja media** es lo que
> permite el recorte: sin eso la imagen se compone centrada y perdés el motivo.
> El de **nada de blanco puro** es por la pantalla: el LED a máximo brillo
> encandila a la platea. Adjuntale también
> `plantillas/cumbre_guia-recorte-chatgpt_1536x1024.png` con cada prompt.

---

El símbolo de la Cumbre es un pico. Las escenas están construidas sobre esa idea:
altura, ascenso, aire enrarecido, la vista desde arriba.

## 01 · Ambiente base (loop)

**Estrategia B** · Se usa el 70 % del tiempo, debajo de todo lo demás.

```
Slow-drifting high-altitude mist and thin cloud layers over deep black.
Very soft focus, no sharp objects, mostly empty dark space with faint
silver-grey light seeping through from above.
[bloque de estilo]
```

Pedile **4 variantes** y elegí la más vacía. En la pantalla, menos es más.

## 02 · Apertura

**Estrategia A** · 4 paneles. Va debajo de la placa del logo.

```
Panel [N] of 4 of one continuous ultra-wide image, read left to right.
A vast mountain range at dawn seen from above the cloud line, sharp ridges
emerging from a sea of mist. Panel 1: almost empty, low cloud only. Panel 2:
the first ridges appear. Panel 3: the highest peak, the focal point of the
whole image. Panel 4: the range descends back into cloud.
[bloque de estilo]
```

Generá los 4 en el **mismo chat**, uno por mensaje, pidiéndole que mantenga la
continuidad con el anterior. Las costuras se disimulan después en DaVinci.

## 03 · Bienvenida / recepción

**Estrategia B**

```
A dark polished architectural surface catching a single thin sweep of cold
light across it. Minimal, geometric, like the facade of a modern concert hall
at night. Mostly darkness, one clean band of light.
[bloque de estilo]
```

## 04 · Escenario / orador en vivo

**Estrategia B** · Fondo bajo el nombre del orador. Tiene que ser **muy** tranquilo.

```
An almost entirely black background with a barely visible grey gradient glow
in the lower centre, like distant stage light. Extremely minimal, 90% pure
darkness, no objects, no texture detail. Just atmosphere.
[bloque de estilo]
```

## 05 · Transición

**Estrategia A** · 4 paneles. Corte entre bloques del evento.

```
Panel [N] of 4 of one continuous ultra-wide image. Long horizontal streaks of
cold light in motion over black, like a long-exposure photograph of wind over
a ridge. The streaks travel left to right across the four panels and get
denser toward panel 3.
[bloque de estilo]
```

## 06 · Fondo de sponsors

**Estrategia B** · Los logos de los sponsors se montan arriba en DaVinci.

```
A very dark neutral background with a soft even vignette and an extremely
subtle diagonal texture. Flat, calm, uniform brightness across the whole
width, nothing that competes for attention.
[bloque de estilo]
```

## 07 · Cuenta regresiva

**Estrategia B** · Los números se hacen en Resolve, no acá.

```
A dark background with a few thick concentric circles and sparse radial
lines, like an elegant altimeter dial, glowing softly over black. The centre
of the image is empty black. Few lines, thick, precise.
[bloque de estilo]
```

> Cuidado con este: las líneas finas titilan en LED. Por eso el prompt pide
> **gruesas y pocas**. Si igual titila, aplicale un desenfoque de 1–2 px en
> Resolve.

## 08 · Networking / coffee break

**Estrategia B**

```
Cold bokeh lights out of focus over a dark background, like a busy evening
venue seen through a wide-aperture lens. Soft, blurred, no recognisable
shapes.
[bloque de estilo]
```

## 09 · Momento cumbre / cierre

**Estrategia A** · 4 paneles. El pico del evento, literal.

```
Panel [N] of 4 of one continuous ultra-wide image. The view from a summit at
night: a vast dark sky dense with stars, the curve of the horizon far below,
a single sharp ridge line in silhouette. Growing from empty at the edges to
its densest at the centre. Cinematic, emotional, epic scale.
[bloque de estilo]
```

## 10 · Placa neutra de respaldo

**Estrategia B** · Para cuando algo falla y necesitás algo digno en pantalla ya.

```
A pure deep black background with a single very soft cold glow centred
horizontally, fading to black at both edges. Nothing else. Absolutely minimal.
[bloque de estilo]
```

---

## Placa de productora (Aura Productions)

Es la única pieza que lleva dorado. Va en los créditos, no en el cuerpo del
evento. Cambiá el bloque de estilo por este:

```
Style: cinematic, ultra-wide horizontal composition, deep near-black
background (#08080F), antique gold accents (#C9A84C) and warm light gold
(#E8C97A). Elegant, premium, restrained. No text, no letters, no logos, no
watermarks. Keep the middle horizontal third of the frame as the important
area. Leave the centre calm and uncluttered. No pure white areas.
```

**Estrategia B**

```
An abstract dark background of slow-drifting golden dust particles and soft
light bokeh over deep black. Very soft focus, sparse and scattered, mostly
empty black space.
[bloque de estilo dorado]
```

La placa del fénix va encima, desde `plantillas/aura_placa-simbolo-centrado_3864x336.png`.

---

## Cómo pedirlas bien

1. Un chat por escena. Si mezclás, ChatGPT arrastra el estilo de la anterior.
2. En mosaicos (estrategia A), un panel por mensaje y **siempre en el mismo chat**.
3. Pedí 2–4 variantes de cada una. Vas a descartar la mayoría.
4. Descargá siempre el archivo, no la captura de pantalla.
5. Nombrá los archivos `01-ambiente-v2.png`, `02-apertura-panel1.png`, etc.
   El script de Resolve ordena por nombre.
6. Guardalas todas en una carpeta sola, por ejemplo `~/CumbreLED/imagenes/`.

## Lo que no le pidas a ChatGPT

- **Texto.** Sale mal escrito y a baja resolución. Todo el texto se hace en Resolve.
- **Los logos.** Van desde archivo, en `plantillas/`.
- **Color, en las piezas de la Cumbre.** Un solo destello de color rompe el
  sistema monocromo, y en una pantalla de 3863 px de ancho se nota desde el fondo
  de la sala.
- **Blancos puros.** En LED se queman y encandilan a la platea.
- **Caras reconocibles.** Ni de asistentes ni de oradores.
