#!/usr/bin/env python3
"""
Genera el PDF del menú.

Si existe el logo oficial en assets/ (logo-cumbre.svg | .png | .jpg), se inserta
tal cual en portada, encabezados y marca de agua. Si no existe, el documento sale
con el nombre CUMBRE en tipografía y un recuadro indicando dónde va el logo.
"""
import base64, pathlib, subprocess, sys

DIR = pathlib.Path(__file__).resolve().parent
OUT = DIR / "Menu-Cumbre-RosaNegra-CDMX.pdf"
CHROME = "/opt/pw-browsers/chromium"
MIME = {".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}

def find_logo():
    for ext in (".svg", ".png", ".jpg", ".jpeg"):
        p = DIR / "assets" / ("logo-cumbre" + ext)
        if p.exists():
            return p
    return None

def data_uri(p):
    return "data:%s;base64,%s" % (MIME[p.suffix.lower()],
                                  base64.b64encode(p.read_bytes()).decode())

logo = find_logo()
if logo:
    uri = data_uri(logo)
    cover  = '<img class="logo-cover" src="%s" alt="Cumbre de los Millonarios Conscientes">' % uri
    header = '<img class="logo-header" src="%s" alt="Cumbre">' % uri
    wm     = '<div class="watermark"><img class="logo-wm" src="%s" alt=""></div>' % uri
    print("Logo oficial:", logo.name)
else:
    cover = '<div class="logo-space"></div>'
    header = ('<div class="txt"><div class="t1">CUMBRE</div>'
              '<div class="t2">DE LOS MILLONARIOS CONSCIENTES</div></div>')
    wm = ""
    print("Sin logo oficial en assets/ — la tapa queda con el espacio libre para colocarlo a mano.")
    print("   Para el logo real: guardalo en assets/logo-cumbre.svg (o .png) y volvé a correr este script.")

html = (DIR / "menu.html").read_text(encoding="utf-8")
html = (html.replace("<!--LOGO_COVER-->", cover)
            .replace("<!--LOGO_HEADER-->", header)
            .replace("<!--LOGO_WATERMARK-->", wm))

tmp = DIR / ".build.html"
tmp.write_text(html, encoding="utf-8")
try:
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--no-pdf-header-footer", "--virtual-time-budget=4000",
                    "--print-to-pdf=%s" % OUT, tmp.as_uri()],
                   check=True, capture_output=True)
finally:
    tmp.unlink(missing_ok=True)
print("PDF:", OUT)
