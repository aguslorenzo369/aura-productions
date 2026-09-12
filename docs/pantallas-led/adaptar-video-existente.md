# Adaptar un video que ya existe a la pantalla

Para cuando el video ya está hecho (las nubes en movimiento, por ejemplo) y
solo falta llevarlo a **3864 × 336** y ponerle el logo encima.

Esto no necesita Fusion. Se hace en la página Edit, con el Inspector.

## A mano, cuatro pasos

**1. Poné la línea de tiempo en 3864 × 336.**

Project Settings (engranaje abajo a la derecha) > Master Settings:

- Timeline resolution → **Custom** → `3864` × `336`
- Image Scaling > Input scaling → **Scale entire image to fit**

Ese segundo punto no es opcional: el número de Zoom del paso 3 depende de eso.

**2. Poné el video en la pista V1 y el logo en V2.**

**3. Seleccioná el video y en el Inspector poné el Zoom.**

| Si tu video es | Zoom |
|---|---|
| 1920 × 1080, 3840 × 2160, 1280 × 720, o cualquier 16:9 | `6,469` |
| 1080 × 1080 (cuadrado) | `11,500` |
| 1080 × 1920 (vertical) | `20,444` |

Para cualquier otra medida:

```
Zoom = 11,5 ÷ (ancho del video ÷ alto del video)
```

Después movés **Position Y** hasta que se vea la franja del video que querés.
De un video 16:9 de 1080 px de alto solo entran 167 px en la banda, así que
elegir bien esa franja es la decisión que más cambia el resultado.

**4. Seleccioná el logo y ajustale el tamaño** hasta que ocupe unos 268 px de
alto, que deja 34 px de margen arriba y abajo. Centrado.

## Con el script

`resolve/adaptar_video_a_pantalla.py` hace los cuatro pasos solo: crea el
proyecto, importa las dos piezas, calcula el Zoom leyendo la resolución real de
tu video y las coloca.

Editá `VIDEO` y `LOGO` arriba del archivo con las rutas de tus archivos, y
correlo desde Workspace > Console (pestaña Py3) dentro de Resolve:

```python
exec(open("/ruta/a/adaptar_video_a_pantalla.py").read())
```

Si el encuadre no te gusta, cambiá `POSICION_Y` y volvé a correrlo.

## Antes de renderizar

Tres cosas de la pantalla LED que aplican a este video:

- **Bajá el brillo.** Nubes blancas al sol es casi todo el cuadro en la zona de
  riesgo. Un nodo de color al final con el Gain bajado hasta que el pico marque
  92 % en el scope de forma de onda.
- **Verificá el loop.** El primer fotograma tiene que ser igual al último, si no
  se ve un salto cada vez que da la vuelta, toda la noche.
- **El logo tiene que estar quieto.** Si el video ya trae el logo incrustado y
  encima le ponés otro, vas a ver los dos.

Los ajustes de render están en [`README.md`](README.md).

## Una advertencia sobre el logo

Si el archivo de logo es el completo (símbolo + CUMBRE + la bajada), a 268 px de
alto la línea "DE LOS MILLONARIOS CONSCIENTES" mide unos 8 px. Desde la platea
no se lee.

Para la pantalla conviene la versión horizontal: el símbolo a un lado y el texto
al lado, no apilado. Las placas de `plantillas/` están armadas para eso.
