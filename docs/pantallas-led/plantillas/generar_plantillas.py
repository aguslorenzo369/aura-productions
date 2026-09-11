#!/usr/bin/env python3
"""
Genera las plantillas base para la pantalla LED de 3864 x 336 px.

Uso:
    pip install Pillow
    python3 docs/pantallas-led/plantillas/generar_plantillas.py cumbre
    python3 docs/pantallas-led/plantillas/generar_plantillas.py aura
    python3 docs/pantallas-led/plantillas/generar_plantillas.py todas

Los PNG quedan en la misma carpeta que este script, con el nombre de la marca
como prefijo.

El logo
-------
Cada marca apunta a un archivo de logo dentro del repositorio. Si el archivo no
esta, la placa igual se genera pero con un recuadro punteado en lugar del logo,
marcando el tamano y la posicion exactos. Poné el PNG donde dice MARCAS y
volvé a correr el script.

El logo tiene que ser PNG con fondo transparente y por lo menos 1500 px de alto.
Un JPG con fondo negro no sirve: el borde del recuadro se ve contra el fondo.
"""

import math
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ---------------------------------------------------------------- el lienzo

W, H = 3864, 336          # ancho par: los codecs de video lo exigen
W_REAL = 3863             # ancho declarado por el proveedor de LED

MARGEN_X = 193            # 5 % del ancho
MARGEN_Y = 34             # ~10 % del alto
CAP_PRINCIPAL = 90        # altura de mayuscula minima, texto principal
CAP_SECUNDARIO = 48       # altura de mayuscula minima, texto secundario
PANELES = 4               # paneles de ChatGPT que forman el mosaico

BLANCO_LED = (235, 235, 235)   # no 255: el blanco puro se quema en LED
NEGRO = (0, 0, 0)

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
FUENTES = "/mnt/skills/examples/canvas-design/canvas-fonts"


# ---------------------------------------------------------------- las marcas

MARCAS = {
    # Cumbre de los Millonarios Conscientes: el evento. Monocromo.
    "cumbre": {
        "titulo": "CUMBRE DE LOS MILLONARIOS CONSCIENTES",
        "acento": BLANCO_LED,
        "fondo": (6, 6, 6),
        "logo": os.path.join(RAIZ, "public", "images", "cumbre-logo.png"),
        # El logotipo apila monograma + CUMBRE + bajada. A 336 px de alto la
        # bajada seria ilegible, asi que la placa usa solo el monograma de
        # arriba y el texto se arma como texto vivo en Resolve.
        "recorte_marca": 0.62,
    },
    # Aura Productions: la productora. Dorado sobre negro.
    "aura": {
        "titulo": "AURA PRODUCTIONS",
        "acento": (201, 168, 76),
        "fondo": (8, 8, 15),
        "logo": os.path.join(RAIZ, "public", "images", "logo.png"),
        "recorte_marca": 0.755,
    },
}


# ---------------------------------------------------------------- utilidades

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
        d.line([x1 + ux * pos, y1 + uy * pos, x1 + ux * fin, y1 + uy * fin],
               fill=color, width=ancho)
        pos = fin + hueco


def rect_punteado(d, caja, color, ancho=2):
    x1, y1, x2, y2 = caja
    linea_punteada(d, (x1, y1, x2, y1), color, ancho)
    linea_punteada(d, (x1, y2, x2, y2), color, ancho)
    linea_punteada(d, (x1, y1, x1, y2), color, ancho)
    linea_punteada(d, (x2, y1, x2, y2), color, ancho)


def guardar(img, marca, nombre):
    ruta = os.path.join(AQUI, f"{marca}_{nombre}")
    img.save(ruta, "PNG")
    print(f"  {marca}_{nombre}  ({img.size[0]}x{img.size[1]})")


# ------------------------------------------------------------------ el logo

def cargar_marca(cfg, alto_destino):
    """Devuelve solo el simbolo del logotipo, sin el texto de abajo.

    Devuelve None si el archivo no esta: quien llama dibuja el recuadro guia.
    """
    ruta = cfg["logo"]
    if not os.path.exists(ruta):
        return None
    logo = Image.open(ruta).convert("RGBA")
    if logo.getchannel("A").getextrema()[0] == 255:
        print(f"  aviso: {os.path.basename(ruta)} no tiene transparencia; "
              f"la placa va a llevar el fondo del archivo.")
    caja = logo.getchannel("A").getbbox() or (0, 0, *logo.size)
    logo = logo.crop(caja)
    logo = logo.crop((0, 0, logo.size[0], int(logo.size[1] * cfg["recorte_marca"])))
    caja = logo.getchannel("A").getbbox()
    if caja:
        logo = logo.crop(caja)
    escala = alto_destino / logo.size[1]
    return logo.resize(
        (max(1, round(logo.size[0] * escala)), alto_destino), Image.LANCZOS
    )


def poner_marca(lienzo, cfg, marca, x, y, ancho_guia, alto):
    """Compone el logo, o dibuja el recuadro guia si el archivo falta."""
    if marca is not None:
        glow = Image.new("RGBA", lienzo.size, (0, 0, 0, 0))
        ImageDraw.Draw(glow).ellipse(
            [x - 70, y - 50, x + marca.size[0] + 70, y + marca.size[1] + 50],
            fill=cfg["acento"] + (10,),
        )
        lienzo.alpha_composite(glow.filter(ImageFilter.GaussianBlur(90)))
        lienzo.alpha_composite(marca, (x, y))
        return marca.size[0]

    d = ImageDraw.Draw(lienzo)
    rect_punteado(d, (x, y, x + ancho_guia, y + alto), cfg["acento"] + (150,))
    d.text((x + 16, y + alto // 2 - 14), "FALTA EL LOGO  ->  ver MARCAS en el script",
           font=fuente("InstrumentSans-Regular.ttf", 22),
           fill=cfg["acento"] + (190,))
    return ancho_guia


# ------------------------------------------------------- 1. guia de encuadre

def guia_encuadre(nombre, cfg):
    acento = cfg["acento"]
    img = Image.new("RGBA", (W, H), cfg["fondo"] + (255,))
    d = ImageDraw.Draw(img)

    f_chico = fuente("InstrumentSans-Regular.ttf", 18)
    f_medio = fuente("InstrumentSans-Bold.ttf", 22)

    for x in range(0, W, 100):
        d.line([x, 0, x, H], fill=(255, 255, 255, 10), width=1)
    for y in range(0, H, 100):
        d.line([0, y, W, y], fill=(255, 255, 255, 10), width=1)

    d.rectangle([0, 0, W - 1, H - 1], outline=acento + (110,), width=2)

    for caja in ((MARGEN_X, MARGEN_Y, W - MARGEN_X, MARGEN_Y),
                 (MARGEN_X, H - MARGEN_Y, W - MARGEN_X, H - MARGEN_Y),
                 (MARGEN_X, MARGEN_Y, MARGEN_X, H - MARGEN_Y),
                 (W - MARGEN_X, MARGEN_Y, W - MARGEN_X, H - MARGEN_Y)):
        linea_punteada(d, caja, acento + (200,))

    d.line([W // 2, 0, W // 2, H], fill=acento + (90,), width=2)
    d.line([0, H // 2, W, H // 2], fill=acento + (60,), width=1)
    for n in (1, 2):
        linea_punteada(d, (W * n // 3, 0, W * n // 3, H),
                       (255, 255, 255, 45), ancho=1, trazo=10, hueco=12)

    for n in range(1, PANELES):
        x = W * n // PANELES
        d.line([x, 0, x, H], fill=(255, 90, 90, 120), width=2)
        d.text((x + 10, H - 30), f"costura {n}", font=f_chico, fill=(255, 120, 120, 200))

    base_y = H // 2 + CAP_PRINCIPAL // 2
    d.rectangle([MARGEN_X + 20, base_y - CAP_PRINCIPAL, MARGEN_X + 34, base_y],
                fill=acento + (190,))
    d.text((MARGEN_X + 48, base_y - CAP_PRINCIPAL - 4),
           f"{CAP_PRINCIPAL} px  cap principal", font=f_medio, fill=acento + (230,))
    d.rectangle([MARGEN_X + 20, base_y + 24, MARGEN_X + 34, base_y + 24 + CAP_SECUNDARIO],
                fill=(255, 255, 255, 120))
    d.text((MARGEN_X + 48, base_y + 26),
           f"{CAP_SECUNDARIO} px  cap secundario", font=f_chico, fill=(255, 255, 255, 170))

    d.text((MARGEN_X + 20, MARGEN_Y + 12),
           f"{cfg['titulo']} · PANTALLA LED · {W_REAL} x {H} (trabajar en {W} x {H})",
           font=f_medio, fill=acento + (235,))
    d.text((W - MARGEN_X - 430, MARGEN_Y + 14),
           f"area segura: margen {MARGEN_X} px lateral / {MARGEN_Y} px vertical",
           font=f_chico, fill=(255, 255, 255, 150))
    d.text((W - MARGEN_X - 430, H - MARGEN_Y - 34),
           "capa de guia: apagar antes de renderizar",
           font=f_chico, fill=(255, 120, 120, 200))

    guardar(img, nombre, f"guia-encuadre_{W}x{H}.png")


# ------------------------------------------------------- 2. base degradado

def base_degradado(nombre, cfg):
    acento, fondo = cfg["acento"], cfg["fondo"]
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    px = img.load()

    cx, cy = W / 2, H / 2
    radio = W * 0.42
    for y in range(H):
        for x in range(0, W, 2):
            dx, dy = (x - cx) / radio, (y - cy) / (H * 0.9)
            k = max(0.0, 1.0 - math.sqrt(dx * dx + dy * dy)) ** 2.2
            c = tuple(int(fondo[i] + (acento[i] - fondo[i]) * k * 0.16)
                      for i in range(3))
            px[x, y] = c + (255,)
            if x + 1 < W:
                px[x + 1, y] = c + (255,)

    img = img.filter(ImageFilter.GaussianBlur(6))
    d = ImageDraw.Draw(img)
    for i in range(3):
        a = int(70 * (1 - i / 3))
        d.line([0, i, W, i], fill=acento + (a,), width=1)
        d.line([0, H - 1 - i, W, H - 1 - i], fill=acento + (a,), width=1)

    guardar(img, nombre, f"base-degradado_{W}x{H}.png")


# ------------------------------------------------------- 3. vineta

def vineta():
    """Capa para poner encima de la imagen de ChatGPT, en modo Multiply.

    No depende de la marca: se genera una sola vez, con el prefijo "comun".
    """
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = img.load()
    for y in range(H):
        for x in range(0, W, 2):
            bx = min(x, W - 1 - x) / (W * 0.30)
            by = min(y, H - 1 - y) / (H * 0.42)
            a = int(235 * ((1.0 - min(1.0, min(bx, by))) ** 1.6))
            px[x, y] = (0, 0, 0, a)
            if x + 1 < W:
                px[x + 1, y] = (0, 0, 0, a)
    guardar(img.filter(ImageFilter.GaussianBlur(18)), "comun",
            f"vineta-bordes_{W}x{H}.png")


# ------------------------------------------------------- 4. placas de marca

def placa_centrada(nombre, cfg):
    alto = H - MARGEN_Y * 2
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    marca = cargar_marca(cfg, alto)
    ancho = marca.size[0] if marca else 300
    poner_marca(img, cfg, marca, (W - ancho) // 2, (H - alto) // 2, 300, alto)
    guardar(img, nombre, f"placa-simbolo-centrado_{W}x{H}.png")


def placa_lockup(nombre, cfg):
    """Simbolo contra el margen izquierdo; el resto queda libre para el texto
    vivo que se arma en Resolve."""
    alto = H - MARGEN_Y * 2 - 16
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    marca = cargar_marca(cfg, alto)
    ancho = poner_marca(img, cfg, marca, MARGEN_X, (H - alto) // 2, 300, alto)

    d = ImageDraw.Draw(img)
    sep = MARGEN_X + ancho + 90
    d.line([sep, H // 2 - 70, sep, H // 2 + 70], fill=cfg["acento"] + (70,), width=2)
    guardar(img, nombre, f"placa-lockup-izquierda_{W}x{H}.png")


# ------------------------------------ 5. guia de recorte para ChatGPT

def guia_recorte_chatgpt(nombre, cfg):
    w, h = 1536, 1024
    banda = round(h * 0.52)
    y0 = (h - banda) // 2
    acento = cfg["acento"]

    img = Image.new("RGBA", (w, h), (18, 18, 24, 255))
    d = ImageDraw.Draw(img)
    f_titulo = fuente("InstrumentSans-Bold.ttf", 34)
    f_texto = fuente("InstrumentSans-Regular.ttf", 24)
    f_chico = fuente("InstrumentSans-Regular.ttf", 20)

    d.rectangle([0, 0, w, y0], fill=(0, 0, 0, 255))
    d.rectangle([0, y0 + banda, w, h], fill=(0, 0, 0, 255))
    d.rectangle([0, y0, w - 1, y0 + banda], outline=acento + (255,), width=4)

    d.text((40, y0 - 78), "SE DESCARTA", font=f_titulo, fill=(255, 90, 90, 220))
    d.text((40, y0 + banda + 34), "SE DESCARTA", font=f_titulo, fill=(255, 90, 90, 220))
    d.text((40, y0 + 26), f"BANDA UTIL  {w} x {banda}  ->  se reduce a 966 x 336",
           font=f_titulo, fill=acento)
    d.text((40, y0 + 74),
           "Todo lo importante de la imagen tiene que caer dentro de este rectangulo.",
           font=f_texto, fill=(255, 255, 255, 190))
    d.text((40, y0 + banda - 48),
           "Cuatro imagenes como esta, lado a lado = 3864 x 336.",
           font=f_chico, fill=(255, 255, 255, 140))
    d.line([w // 2, y0, w // 2, y0 + banda], fill=acento + (70,), width=2)

    guardar(img, nombre, f"guia-recorte-chatgpt_{w}x{h}.png")


# ------------------------------------------------------------------ main

def generar(nombre):
    cfg = MARCAS[nombre]
    print(f"\n{cfg['titulo']}")
    if not os.path.exists(cfg["logo"]):
        print(f"  ! falta el logo: {os.path.relpath(cfg['logo'], RAIZ)}")
        print(f"    las placas salen con el recuadro guia en su lugar.")
    guia_encuadre(nombre, cfg)
    base_degradado(nombre, cfg)
    placa_centrada(nombre, cfg)
    placa_lockup(nombre, cfg)
    guia_recorte_chatgpt(nombre, cfg)


if __name__ == "__main__":
    pedido = sys.argv[1].lower() if len(sys.argv) > 1 else "todas"
    if pedido == "todas":
        objetivo = list(MARCAS)
    elif pedido in MARCAS:
        objetivo = [pedido]
    else:
        sys.exit(f"Marca desconocida: {pedido}. Opciones: {', '.join(MARCAS)}, todas")

    print(f"Generando plantillas en {AQUI}")
    vineta()
    for n in objetivo:
        generar(n)
    print("\nListo.")
