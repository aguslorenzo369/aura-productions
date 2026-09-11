#!/usr/bin/env python3
"""
Genera las plantillas base para la pantalla LED de 3864 x 336 px.

Uso:
    pip install Pillow
    python3 docs/pantallas-led/plantillas/generar_plantillas.py

Salida: los PNG quedan en la misma carpeta que este script.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ---------------------------------------------------------------- constantes

W, H = 3864, 336          # lienzo de trabajo (ancho par para codecs)
W_REAL = 3863             # ancho real declarado por el proveedor de LED

GOLD = (201, 168, 76)     # #C9A84C
GOLD_LIGHT = (232, 201, 122)
DEEP = (8, 8, 15)         # #08080F

MARGEN_X = 193            # 5 % del ancho
MARGEN_Y = 34             # ~10 % del alto
CAP_PRINCIPAL = 90        # altura de mayúscula mínima, texto principal
CAP_SECUNDARIO = 48       # altura de mayúscula mínima, texto secundario
PANELES = 4               # paneles de ChatGPT que forman el mosaico

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
FUENTES = "/mnt/skills/examples/canvas-design/canvas-fonts"


def fuente(nombre, tam):
    ruta = os.path.join(FUENTES, nombre)
    if os.path.exists(ruta):
        return ImageFont.truetype(ruta, tam)
    return ImageFont.load_default()


def linea_punteada(d, xy, color, ancho=2, trazo=18, hueco=14):
    x1, y1, x2, y2 = xy
    largo = math.hypot(x2 - x1, y2 - y1)
    if largo == 0:
        return
    ux, uy = (x2 - x1) / largo, (y2 - y1) / largo
    pos = 0.0
    while pos < largo:
        fin = min(pos + trazo, largo)
        d.line(
            [x1 + ux * pos, y1 + uy * pos, x1 + ux * fin, y1 + uy * fin],
            fill=color, width=ancho,
        )
        pos = fin + hueco


def guardar(img, nombre):
    ruta = os.path.join(AQUI, nombre)
    img.save(ruta, "PNG")
    print(f"  {nombre}  ({img.size[0]}x{img.size[1]})")


# ------------------------------------------------------- 1. guía de encuadre

def guia_encuadre():
    img = Image.new("RGBA", (W, H), DEEP + (255,))
    d = ImageDraw.Draw(img)

    f_chico = fuente("InstrumentSans-Regular.ttf", 18)
    f_medio = fuente("InstrumentSans-Bold.ttf", 22)

    # cuadrícula de fondo cada 100 px
    for x in range(0, W, 100):
        d.line([x, 0, x, H], fill=(255, 255, 255, 10), width=1)
    for y in range(0, H, 100):
        d.line([0, y, W, y], fill=(255, 255, 255, 10), width=1)

    # borde del lienzo
    d.rectangle([0, 0, W - 1, H - 1], outline=GOLD + (110,), width=2)

    # área segura
    linea_punteada(d, (MARGEN_X, MARGEN_Y, W - MARGEN_X, MARGEN_Y), GOLD + (200,))
    linea_punteada(d, (MARGEN_X, H - MARGEN_Y, W - MARGEN_X, H - MARGEN_Y), GOLD + (200,))
    linea_punteada(d, (MARGEN_X, MARGEN_Y, MARGEN_X, H - MARGEN_Y), GOLD + (200,))
    linea_punteada(d, (W - MARGEN_X, MARGEN_Y, W - MARGEN_X, H - MARGEN_Y), GOLD + (200,))

    # eje central y tercios
    d.line([W // 2, 0, W // 2, H], fill=GOLD + (90,), width=2)
    d.line([0, H // 2, W, H // 2], fill=GOLD + (60,), width=1)
    for n in (1, 2):
        x = W * n // 3
        linea_punteada(d, (x, 0, x, H), (255, 255, 255, 45), ancho=1, trazo=10, hueco=12)

    # costuras del mosaico de 4 paneles
    for n in range(1, PANELES):
        x = W * n // PANELES
        d.line([x, 0, x, H], fill=(255, 90, 90, 120), width=2)
        d.text((x + 10, H - 30), f"costura {n}", font=f_chico, fill=(255, 120, 120, 200))

    # barras de altura de mayúscula
    base_y = H // 2 + CAP_PRINCIPAL // 2
    d.rectangle([MARGEN_X + 20, base_y - CAP_PRINCIPAL, MARGEN_X + 34, base_y],
                fill=GOLD + (190,))
    d.text((MARGEN_X + 48, base_y - CAP_PRINCIPAL - 4),
           f"{CAP_PRINCIPAL} px  cap principal", font=f_medio, fill=GOLD + (230,))
    d.rectangle([MARGEN_X + 20, base_y + 24, MARGEN_X + 34, base_y + 24 + CAP_SECUNDARIO],
                fill=(255, 255, 255, 120))
    d.text((MARGEN_X + 48, base_y + 26),
           f"{CAP_SECUNDARIO} px  cap secundario", font=f_chico, fill=(255, 255, 255, 170))

    # rótulos
    d.text((MARGEN_X + 20, MARGEN_Y + 12),
           f"AURA PRODUCTIONS · PANTALLA LED · {W_REAL} x {H} (trabajar en {W} x {H})",
           font=f_medio, fill=GOLD + (235,))
    d.text((W - MARGEN_X - 430, MARGEN_Y + 14),
           f"area segura: margen {MARGEN_X} px lateral / {MARGEN_Y} px vertical",
           font=f_chico, fill=(255, 255, 255, 150))
    d.text((W - MARGEN_X - 430, H - MARGEN_Y - 34),
           "capa de guia: apagar antes de renderizar",
           font=f_chico, fill=(255, 120, 120, 200))

    guardar(img, f"guia-encuadre_{W}x{H}.png")


# ------------------------------------------------------- 2. base degradado

def base_degradado():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    px = img.load()

    cx, cy = W / 2, H / 2
    radio = W * 0.42
    for y in range(H):
        for x in range(0, W, 2):          # de a 2 px: el degradado es suave
            dx = (x - cx) / radio
            dy = (y - cy) / (H * 0.9)
            dist = math.sqrt(dx * dx + dy * dy)
            k = max(0.0, 1.0 - dist) ** 2.2
            r = int(DEEP[0] + (GOLD[0] - DEEP[0]) * k * 0.16)
            g = int(DEEP[1] + (GOLD[1] - DEEP[1]) * k * 0.16)
            b = int(DEEP[2] + (GOLD[2] - DEEP[2]) * k * 0.16)
            px[x, y] = (r, g, b, 255)
            if x + 1 < W:
                px[x + 1, y] = (r, g, b, 255)

    img = img.filter(ImageFilter.GaussianBlur(6))

    # filetes dorados arriba y abajo
    d = ImageDraw.Draw(img)
    for i in range(3):
        a = int(70 * (1 - i / 3))
        d.line([0, i, W, i], fill=GOLD + (a,), width=1)
        d.line([0, H - 1 - i, W, H - 1 - i], fill=GOLD + (a,), width=1)

    guardar(img, f"base-degradado_{W}x{H}.png")


# ------------------------------------------------------- 3. viñeta dorada

def vineta():
    """Capa para poner en modo Overlay/Screen encima de la imagen de ChatGPT."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = img.load()

    for y in range(H):
        for x in range(0, W, 2):
            bx = min(x, W - 1 - x) / (W * 0.30)
            by = min(y, H - 1 - y) / (H * 0.42)
            k = 1.0 - min(1.0, min(bx, by))
            a = int(235 * (k ** 1.6))
            px[x, y] = (0, 0, 0, a)
            if x + 1 < W:
                px[x + 1, y] = (0, 0, 0, a)

    img = img.filter(ImageFilter.GaussianBlur(18))
    guardar(img, f"vineta-bordes_{W}x{H}.png")


# ------------------------------------------------------- 4. placas de marca

FENIX_RECORTE = 0.755   # el fenix ocupa el 75,5 % superior del logotipo;
                        # debajo viene "AURA PRODUCTIONS", que a 336 px de alto
                        # quedaria ilegible y por eso va como texto vivo en Resolve.


def _fenix(alto_destino):
    """Devuelve solo la marca del fenix, sin el texto del logotipo."""
    ruta = os.path.join(RAIZ, "public", "images", "logo.png")
    if not os.path.exists(ruta):
        return None
    logo = Image.open(ruta).convert("RGBA")
    logo = logo.crop(logo.getchannel("A").getbbox())
    logo = logo.crop((0, 0, logo.size[0], int(logo.size[1] * FENIX_RECORTE)))
    logo = logo.crop(logo.getchannel("A").getbbox())
    escala = alto_destino / logo.size[1]
    return logo.resize(
        (max(1, round(logo.size[0] * escala)), alto_destino), Image.LANCZOS
    )


def _con_resplandor(lienzo, marca, x, y, fuerza=11):
    glow = Image.new("RGBA", lienzo.size, (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse(
        [x - 70, y - 50, x + marca.size[0] + 70, y + marca.size[1] + 50],
        fill=GOLD + (fuerza,),
    )
    lienzo.alpha_composite(glow.filter(ImageFilter.GaussianBlur(90)))
    lienzo.alpha_composite(marca, (x, y))


def placa_fenix_centrado():
    marca = _fenix(H - MARGEN_Y * 2)
    if marca is None:
        print("  (salteado: falta public/images/logo.png)")
        return
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    _con_resplandor(img, marca, (W - marca.size[0]) // 2, (H - marca.size[1]) // 2)
    guardar(img, f"placa-fenix-centrado_{W}x{H}.png")


def placa_fenix_izquierda():
    """Fenix pegado al margen izquierdo; el resto de la banda queda libre
    para el texto vivo que se arma en Resolve."""
    marca = _fenix(H - MARGEN_Y * 2 - 16)
    if marca is None:
        return
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x = MARGEN_X
    _con_resplandor(img, marca, x, (H - marca.size[1]) // 2, fuerza=9)

    # filete separador: marca donde arranca el bloque de texto
    d = ImageDraw.Draw(img)
    sep = x + marca.size[0] + 90
    d.line([sep, H // 2 - 70, sep, H // 2 + 70], fill=GOLD + (70,), width=2)

    guardar(img, f"placa-fenix-izquierda_{W}x{H}.png")


# ------------------------------------ 5. guía de recorte para ChatGPT

def guia_recorte_chatgpt():
    """1536x1024 con la banda util marcada, para encuadrar los prompts."""
    w, h = 1536, 1024
    banda = round(h * 0.52)                     # 532 px -> se baja a 336
    y0 = (h - banda) // 2

    img = Image.new("RGBA", (w, h), (18, 18, 24, 255))
    d = ImageDraw.Draw(img)

    f_titulo = fuente("InstrumentSans-Bold.ttf", 34)
    f_texto = fuente("InstrumentSans-Regular.ttf", 24)
    f_chico = fuente("InstrumentSans-Regular.ttf", 20)

    d.rectangle([0, 0, w, y0], fill=(0, 0, 0, 255))
    d.rectangle([0, y0 + banda, w, h], fill=(0, 0, 0, 255))
    d.rectangle([0, y0, w - 1, y0 + banda], outline=GOLD + (255,), width=4)

    d.text((40, y0 - 78), "SE DESCARTA", font=f_titulo, fill=(255, 90, 90, 220))
    d.text((40, y0 + banda + 34), "SE DESCARTA", font=f_titulo, fill=(255, 90, 90, 220))
    d.text((40, y0 + 26),
           f"BANDA UTIL  {w} x {banda}  ->  se reduce a 966 x 336 en Resolve",
           font=f_titulo, fill=GOLD)
    d.text((40, y0 + 74),
           "Todo lo importante de la imagen tiene que caer dentro de este rectangulo.",
           font=f_texto, fill=(255, 255, 255, 190))
    d.text((40, y0 + banda - 48),
           "Cuatro imagenes como esta, lado a lado = 3864 x 336.",
           font=f_chico, fill=(255, 255, 255, 140))

    d.line([w // 2, y0, w // 2, y0 + banda], fill=GOLD + (70,), width=2)

    guardar(img, f"guia-recorte-chatgpt_{w}x{h}.png")


if __name__ == "__main__":
    print(f"Generando plantillas en {AQUI}")
    guia_encuadre()
    base_degradado()
    vineta()
    placa_fenix_centrado()
    placa_fenix_izquierda()
    guia_recorte_chatgpt()
    print("Listo.")
