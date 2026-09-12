# Nubes en movimiento — receta de Fusion

Cómo convertir la placa fija de nubes en un loop con movimiento, para la banda
de 3864 × 336.

## Qué es "el prompt" acá

Resolve no es una herramienta generativa: no hay ningún campo donde describir
lo que querés y esperar a que lo genere.

Lo más cercano, y funciona muy bien, es que **Fusion acepta un árbol de nodos
pegado como texto**. Copiás un bloque, apretás `Ctrl+V` en el editor de nodos y
el efecto queda armado. Ese bloque está en este repositorio y la sección que
sigue explica cómo usarlo.

Si lo que buscás es que una IA anime la foto directamente, eso es otra
categoría de herramienta (imagen a video: Runway, Kling, Sora, Higgsfield).
Al final del documento está el prompt para ese camino, con sus limitaciones.

## Antes de empezar: dos problemas con la placa actual

### 1. La composición no entra en la banda

La placa mide unos 1920 × 820. Para cubrir los 3864 px de ancho hay que
ampliarla 2,01×, y entonces de los 820 px de alto del original **solo se ven
167**: el 20 %.

Esa torre de cúmulos que ocupa toda la imagen queda reducida a una tira
horizontal. Se pierde el motivo.

Tres salidas, de mejor a peor:

1. **Regenerar la placa encuadrada para banda**, con el prompt 02 de
   `prompts-chatgpt.md` en mosaico de 4 paneles. Es la que da más detalle.
2. **Elegir a mano qué franja de los 820 px usar** y aceptarla. Sirve si hay una
   zona de nubes que funcione sola, sin la silueta de la torre.
3. **Usarla tal cual, ampliada.** A 2× las nubes aguantan porque son suaves,
   pero perdés la composición.

### 2. El logo está pegado a la imagen

Si deformás la imagen completa, el logo se deforma con ella y se ve como si
respirara. En una pantalla de 3863 px de ancho eso se nota desde el fondo de la
sala.

Necesitás las dos piezas por separado:

- La placa de nubes **sin logo**
- El logo como **PNG con transparencia**

Si solo tenés la imagen compuesta, hay un parche al final del documento.

## El atajo: pegar el árbol ya armado

Fusion acepta un árbol de nodos pegado como texto. No hace falta crear nada a
mano.

El archivo es **[`resolve/nubes-en-movimiento.setting`](resolve/nubes-en-movimiento.setting)**.

1. Antes que nada, poné la línea de tiempo en **3864 × 336**. La composición de
   Fusion hereda ese tamaño, así que si la línea de tiempo está en 1920 × 1080
   todo va a salir mal.
2. Poné la imagen en la línea de tiempo, seleccionala y entrá a la página
   **Fusion**.
3. Abrí el archivo `.setting` en cualquier editor de texto y copiá **todo** el
   contenido.
4. En el editor de nodos de Fusion, hacé clic en una zona vacía y `Ctrl+V`.

Aparecen los cinco nodos ya conectados entre sí. Falta enchufarlos a los dos
que ya estaban:

- `MediaIn1` → entrada de `Transform1`
- salida de `BrightnessContrast1` → `MediaOut1`

Eso es todo. Con eso ya ves las nubes moverse en la ventana de reproducción.

### No lo pude probar

No tengo Resolve en esta sesión, así que el bloque está escrito a partir del
formato de composición de Fusion, sin verificarlo contra el programa.

Si Fusion ignora alguno de los valores, no rompe nada: crea el nodo con el valor
por omisión. Estos tres son los que conviene mirar en el Inspector después de
pegar, porque son los que hacen el efecto:

| Nodo | Campo | Valor |
|---|---|---|
| FastNoise1 | Scale | `10` |
| FastNoise1 | Seethe Rate | `0.02` |
| Displace1 | X Refraction | `0.012` |

Y revisá que en `Displace1` la imagen entre por **Background** y el `FastNoise1`
por **Foreground**. Si están al revés no se ve ningún error, simplemente no
pasa nada.

### Lo que trae armado

| Nodo | Qué hace |
|---|---|
| `Transform1` | Amplía la placa 2,013× para cubrir los 3864 px de ancho |
| `FastNoise1` | Genera el ruido Perlin que impulsa el movimiento. No se ve |
| `Displace1` | Deforma las nubes siguiendo ese ruido |
| `Transform2` | Deriva lenta a la derecha y acercamiento del 3 %, por expresión |
| `BrightnessContrast1` | Baja la ganancia a 0,92 para el límite de brillo del LED |

La deriva y el acercamiento van por **expresión**, no por fotogramas clave:
se reparten solos a lo largo del clip, dure lo que dure. Si alargás el clip,
el movimiento se estira con él y no hay que volver a tocar nada.

`Transform1 Size` está en `2.013`, que es `3864 ÷ 1920`. Si tu placa mide otro
ancho, rehacé esa división y cambiá el valor.

## Armarlo a mano

Si preferís entender cada pieza, o si el pegado no funciona, esto es lo mismo
paso a paso.

## El árbol de nodos

```
MediaIn1  (nubes, sin logo)
    │
Transform1 ───────────── encuadre a la banda
    │
Displace1 ◄── FastNoise1  las nubes se agitan
    │
Transform2 ───────────── deriva lenta
    │
  Merge1 ◄── MediaIn2     el logo, quieto y nítido
    │
ColorCorrector1 ───────── baja el pico al 92 %
    │
 MediaOut1
```

Se arma en la página Fusion. Para agregar un nodo: `Shift` + barra espaciadora
y escribís el nombre.

## Los ajustes, nodo por nodo

### Transform1 — encuadre

| Campo | Valor |
|---|---|
| Size | `2.013` para una placa de 1920 px de ancho |
| Center Y | movelo hasta que la franja caiga donde querés |

La fórmula es `3864 ÷ ancho del original`. Si la placa mide otra cosa, rehacé
la cuenta.

### FastNoise1 — el motor del movimiento

Este nodo no se ve en pantalla. Genera la textura que le dice al `Displace`
cuánto mover cada pixel.

| Campo | Valor | Qué hace |
|---|---|---|
| Type | `Perlin` | |
| Detail | `3.0` | más detalle, remolinos más finos |
| Contrast | `1.0` | |
| Scale | `10.0` | tamaño de los remolinos. Más alto, más grandes |
| Seethe Rate | `0.02` | **la velocidad**. Es el control que vas a tocar |
| Seethe | `0.0` | |

`Seethe Rate` en `0.02` da nubes que se agitan muy despacio, que es lo que
querés. Arriba de `0.1` empieza a parecer agua hirviendo.

### Displace1 — deforma las nubes

Tiene dos entradas. El **Background** es la imagen, el **Foreground** es el
`FastNoise`. Si las conectás al revés no pasa nada visible y vas a perder media
hora.

| Campo | Valor |
|---|---|
| Type | `X and Y` |
| X Channel / Y Channel | `Luminance` |
| X Offset / Y Offset | `0.5` (neutro, no lo toques) |
| X Refraction | `0.012` |
| Y Refraction | `0.006` |
| Edges | `Mirror` |

`X Refraction` es la intensidad. Empezá en `0.012` y subí de a `0.002`. Pasado
`0.03` las nubes se derriten en lugar de moverse.

Y en la mitad de X está a propósito: las nubes se mueven más en horizontal que
en vertical, y en una banda tan ancha el movimiento vertical se lee como error.

`Edges` en `Mirror` evita que aparezcan bordes transparentes cuando el
desplazamiento empuja pixeles fuera del cuadro.

### Transform2 — la deriva

El `Displace` agita las nubes en el lugar. Esto las hace viajar.

Poné dos fotogramas clave en **Center X**:

| Fotograma | Center X |
|---|---|
| primero del clip | `0.5` |
| último del clip | `0.52` |

Un 2 % del ancho a lo largo de todo el clip. Sobre 40 segundos son unos 2 px por
segundo: apenas perceptible, que es exactamente el punto. Movimiento rápido en
una banda de 11,5:1 produce arrastre en LED.

Poné también **Size** de `1.0` a `1.03` entre los mismos dos fotogramas. Ese
acercamiento mínimo es lo que hace que la imagen se sienta viva en lugar de
desplazada.

Seleccioná los cuatro fotogramas en el Spline y aplicales `Ease In/Out`, si no
el movimiento arranca y frena de golpe.

### Merge1 — el logo

`Background` es la salida de `Transform2`, `Foreground` es el `MediaIn2` del
logo. No le pongas ninguna animación: el logo tiene que estar absolutamente
quieto. Todo el efecto depende de ese contraste.

### ColorCorrector1 — el límite de brillo

Bajá el **Gain** hasta que el punto más brillante de las nubes marque 92 % en
el scope de forma de onda. El blanco puro en LED encandila a la platea y quema
el detalle.

Esta placa es especialmente delicada: son nubes blancas al sol, es decir casi
todo el cuadro en la zona de riesgo.

## El loop

`FastNoise` no cierra solo: el último fotograma nunca coincide con el primero.
El truco estándar:

1. Renderizá 60 segundos.
2. Traelo a la línea de tiempo dos veces, la segunda copia corrida 30 segundos.
3. Cruzá las dos con una disolvencia de 2 segundos.
4. Recortá el resultado a 30 segundos exactos, empezando después de la primera
   disolvencia.

Queda un loop de 30 segundos que cierra sin salto. Nadie va a notar la costura
porque las nubes no tienen una forma que el ojo pueda seguir.

## Parche: si el logo está pegado a la imagen

Funciona porque el logo cae sobre una zona de nubes bastante pareja.

1. Duplicá el `MediaIn1` y llamalo `MediaIn1_logo`.
2. Conectalo a su propio `Transform` con **los mismos valores** que `Transform1`,
   pero **sin** pasar por el `Displace`.
3. Agregale una `Ellipse` como máscara, cubriendo el logo con margen.
4. Subile el **Soft Edge** a `0.04`.
5. Merge por encima de todo.

El resultado: las nubes se mueven en todo el cuadro menos en un óvalo alrededor
del logo, donde quedan fijas. Se nota si lo buscás. Es mejor que un logo que
tiembla, y bastante peor que tener las dos piezas separadas.

## Si preferís el camino de IA

Si en lugar de armarlo en Fusion querés que una herramienta de imagen a video
anime la placa, el prompt es este:

```
Animate this still image. The clouds billow and drift very slowly to the
right, with soft internal churning motion, as in a long time-lapse of
cumulus clouds. Extremely slow and gentle. The camera does not move. The
logo and all text stay perfectly still, sharp and unchanged. No zoom, no
camera shake, no new elements, no colour change.
```

Dos advertencias. Casi todas esas herramientas entregan 5 o 10 segundos como
máximo, en 16:9 y a 720p o 1080p: vas a tener que ampliar mucho y armar el loop
igual. Y ninguna respeta del todo el "el logo queda quieto", así que revisá
fotograma a fotograma que no se haya deformado.

Para esta pieza en particular, Fusion da mejor resultado y es reproducible: si
mañana cambia la placa, cambiás el `MediaIn` y listo.

## Nota sobre el color

Esta placa es azul. Los prompts de `prompts-chatgpt.md` están escritos en
monocromo blanco sobre negro, a partir de la versión del logo sobre fondo negro.

Si la marca de la Cumbre tiene las dos versiones, hay que definir cuál manda en
la pantalla antes de generar el resto del material. Mezclar placas azules con
placas monocromas en la misma pantalla, a lo largo del evento, se ve como un
error de producción y no como una decisión.
