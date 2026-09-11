# Prompts para ChatGPT — pantalla LED Aura Productions

Pantalla real **3863 × 336 px**. Se trabaja en **3864 × 336** (ver `README.md`).

## Antes de empezar: lo que ChatGPT no puede hacer

ChatGPT Plus genera imágenes en tres tamaños y **ninguno es la banda que necesitás**:

| Formato | Tamaño | Sirve para |
|---|---|---|
| Horizontal | 1536 × 1024 | Todo lo de acá abajo |
| Cuadrado | 1024 × 1024 | Nada, para este caso |
| Vertical | 1024 × 1536 | Nada, para este caso |

No le pidas 3863 × 336: te va a devolver 1536 × 1024 igual, o una imagen con barras
negras dibujadas adentro. Se genera **siempre en horizontal** y el recorte a banda
se hace después, en DaVinci.

## Las dos estrategias

**A — Mosaico de 4 paneles.** Cuatro imágenes horizontales, una al lado de la otra.
Cada una aporta 966 × 336 del resultado final. Todo baja de escala, así que queda
nítido. Es la estrategia para fondos con detalle real.

**B — Panel único estirado.** Una sola imagen que cubre los 3864 px de ancho.
Es una ampliación de 2,5×, así que **solo funciona con imágenes suaves**: humo,
bokeh, degradados, partículas desenfocadas. Con detalle fino se ve pastoso.

Cada prompt de abajo dice cuál de las dos usar.

## Bloque de estilo (va pegado al final de todos los prompts)

```
Style: cinematic, ultra-wide horizontal composition, deep near-black background
(#08080F), antique gold accents (#C9A84C) and warm light gold (#E8C97A).
Elegant, premium, restrained. No text, no letters, no logos, no watermarks,
no people's faces in focus. Keep the middle horizontal third of the frame as
the important area — the top and bottom of the image will be cropped away.
Leave the center calm and uncluttered: text and a logo go on top later.
High contrast against black, no bright white areas, no pure white.
```

> El pedido de que lo importante caiga en la **franja media** es lo que hace que el
> recorte funcione. Si lo sacás, la imagen se va a componer centrada verticalmente
> y vas a perder la cabeza del motivo al recortar. Adjuntale también
> `plantillas/guia-recorte-chatgpt_1536x1024.png` para que vea el encuadre.

---

## 01 · Fondo ambiente (loop base)

**Estrategia B** · Se usa el 70 % del tiempo, debajo de todo lo demás.

```
An abstract dark background of slow-drifting golden dust particles and soft
light bokeh over deep black. Very soft focus, no sharp objects, gentle depth
of field. The gold is sparse and scattered, mostly empty black space. Subtle
warm glow rising from the lower edge.
[bloque de estilo]
```

Pedile **4 variantes** y elegí la más vacía. En la pantalla, menos es más.

## 02 · Apertura de marca

**Estrategia A** · 4 paneles. Es el momento del fénix, va debajo de la placa del logo.

```
Panel [N] of 4 of one continuous ultra-wide image, read left to right.
Volumetric golden light rays cutting through darkness and fine embers rising,
over deep black. Panel 1: almost empty black with a few embers at the right.
Panel 2: the light intensifies toward the right edge. Panel 3: the brightest
concentration of golden light, then it falls off. Panel 4: embers fading back
into black.
[bloque de estilo]
```

Generá los 4 en el **mismo chat**, uno por mensaje, pidiéndole que mantenga la
continuidad con el anterior. Las costuras se disimulan después en DaVinci.

## 03 · Bienvenida / recepción

**Estrategia B**

```
A dark elegant architectural texture: a polished black surface catching a thin
sweep of warm golden light across it. Minimal, geometric, like the facade of a
modern concert hall at night. Mostly darkness, one clean band of light.
[bloque de estilo]
```

## 04 · Escenario / orador en vivo

**Estrategia B** · Fondo bajo el nombre del orador. Tiene que ser **muy** tranquilo.

```
An almost entirely black background with a barely visible golden gradient
glow in the lower center, like distant stage light. Extremely minimal, 90%
pure darkness, no objects, no texture detail. Just atmosphere.
[bloque de estilo]
```

## 05 · Transición de energía

**Estrategia A** · 4 paneles. Corte entre bloques del evento.

```
Panel [N] of 4 of one continuous ultra-wide image. Streaks of golden light in
motion, long horizontal motion-blur trails over black, like a long-exposure
photograph. The streaks travel left to right across the four panels and get
denser toward panel 3.
[bloque de estilo]
```

## 06 · Fondo de sponsors

**Estrategia B** · Los logos de los sponsors se montan arriba en DaVinci.

```
A very dark neutral background with a soft, even golden vignette glow and an
extremely subtle diagonal texture. Flat, calm, uniform brightness across the
whole width, nothing that competes for attention.
[bloque de estilo]
```

## 07 · Cuenta regresiva

**Estrategia B** · Los números se hacen en Resolve, no acá.

```
A dark background with concentric thin golden circles and faint radial lines,
like an elegant technical instrument dial, glowing softly over black. The
center of the image is empty black. Very fine lines, sparse, precise.
[bloque de estilo]
```

> Cuidado con este: líneas finas en LED titilan. Pedile líneas **gruesas y pocas**,
> y si igual titila, aplicale un desenfoque de 1–2 px en Resolve.

## 08 · Networking / coffee break

**Estrategia B**

```
Warm golden bokeh lights out of focus over a dark background, like a busy
evening venue seen through a wide-aperture lens. Soft, welcoming, blurred.
No recognizable shapes.
[bloque de estilo]
```

## 09 · Momento emocional / cierre

**Estrategia A** · 4 paneles. El pico del evento.

```
Panel [N] of 4 of one continuous ultra-wide image. A vast dark sky filled with
slowly rising golden embers and particles of light, growing from sparse at the
edges to dense at the center. Cinematic, emotional, epic scale, deep black.
[bloque de estilo]
```

## 10 · Placa neutra de respaldo

**Estrategia B** · Para cuando algo falla y necesitás algo digno en pantalla ya.

```
A pure deep black background with a single very soft warm golden glow centered
horizontally, fading to black at both edges. Nothing else. Absolutely minimal.
[bloque de estilo]
```

---

## Cómo pedirlas bien

1. Un chat por escena. Si mezclás, ChatGPT arrastra el estilo de la anterior.
2. En mosaicos (estrategia A), un panel por mensaje y **siempre en el mismo chat**.
3. Pedí 2–4 variantes de cada una. Vas a descartar la mayoría.
4. Descargá siempre el archivo, no la captura de pantalla.
5. Nombrá los archivos `01-ambiente-v2.png`, `02-apertura-panel1.png`, etc.
   El script de Resolve ordena por nombre.
6. Guardalas todas en una carpeta sola, por ejemplo `~/AuraLED/imagenes/`.

## Lo que no le pidas a ChatGPT

- **Texto.** Sale mal escrito y a baja resolución. Todo el texto se hace en Resolve.
- **El logo de Aura.** Ya lo tenés en `public/images/logo.png` a 6250 × 6250, y las
  placas listas están en `plantillas/`.
- **Blancos puros.** En LED se queman y encandilan a la platea.
- **Caras reconocibles.** Ni de asistentes ni de oradores.
