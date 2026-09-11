#!/usr/bin/env python3
"""
Arma en DaVinci Resolve el proyecto de la pantalla LED de Aura Productions.

Qué hace:
  1. Crea (o abre) el proyecto con la línea de tiempo en 3864 x 336.
  2. Importa todas las imágenes de una carpeta.
  3. Las pone en la línea de tiempo con una duración fija cada una.
  4. Opcional: coloca un mosaico de 4 paneles de ChatGPT lado a lado.

Cómo correrlo
-------------
Lo más simple: abrí Resolve, andá a Workspace > Console, elegí la pestaña Py3
y pegá:

    exec(open("/ruta/a/armar_pantalla_led.py").read())

Desde la terminal también funciona, si antes exportás las variables de entorno
que documenta Blackmagic:

    # macOS
    export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
    export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
    export PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
    python3 armar_pantalla_led.py

Antes de correrlo, en Resolve: Project Settings > Image Scaling >
"Scale entire image to fit". Los números del mosaico dependen de eso.
"""

import os
import sys

# ------------------------------------------------------------------ ajustes

CARPETA_IMAGENES = os.path.expanduser("~/AuraLED/imagenes")

NOMBRE_PROYECTO = "AURA LED 3864x336"
ANCHO, ALTO = 3864, 336        # ancho par: los codecs de video lo exigen
FPS = "30"                     # confirmalo con el técnico de la pantalla
SEGUNDOS_POR_IMAGEN = 8

EXTENSIONES = (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".exr")

# Mosaico: cuatro imágenes de 1536x1024 que cubren los 3864 px de ancho.
# ZoomX/ZoomY 1.0 = imagen entera encajada en el cuadro; 1.9167 la lleva a
# 966 px de ancho visible, dejando ver una franja de 534 px del original.
MOSAICO_ZOOM = 1.9167
MOSAICO_PAN = [-1449, -483, 483, 1449]


# ------------------------------------------------------------------ conexión

def conectar():
    """Devuelve el objeto Resolve, ya sea desde la consola o desde afuera."""
    if "resolve" in globals():
        return globals()["resolve"]
    try:
        import DaVinciResolveScript as dvr
    except ImportError:
        sys.exit(
            "No encuentro DaVinciResolveScript.\n"
            "Corré el script desde Workspace > Console dentro de Resolve, o\n"
            "exportá RESOLVE_SCRIPT_API / RESOLVE_SCRIPT_LIB / PYTHONPATH\n"
            "como explica el encabezado de este archivo."
        )
    r = dvr.scriptapp("Resolve")
    if r is None:
        sys.exit("Resolve no está abierto, o el scripting externo está desactivado "
                 "(Preferences > System > General > External scripting using).")
    return r


def abrir_proyecto(resolve):
    pm = resolve.GetProjectManager()
    proyecto = pm.LoadProject(NOMBRE_PROYECTO) or pm.CreateProject(NOMBRE_PROYECTO)
    if proyecto is None:
        sys.exit(f"No pude crear ni abrir el proyecto '{NOMBRE_PROYECTO}'.")

    ajustes = {
        "timelineResolutionWidth": str(ANCHO),
        "timelineResolutionHeight": str(ALTO),
        "timelineOutputResolutionWidth": str(ANCHO),
        "timelineOutputResolutionHeight": str(ALTO),
        "timelineFrameRate": FPS,
        "timelinePlaybackFrameRate": FPS,
    }
    for clave, valor in ajustes.items():
        if not proyecto.SetSetting(clave, valor):
            print(f"  aviso: no se pudo fijar {clave} = {valor}")

    print(f"Proyecto: {proyecto.GetName()}  ->  {ANCHO}x{ALTO} @ {FPS} fps")
    return proyecto


# ------------------------------------------------------------------ importar

def importar(resolve, proyecto):
    if not os.path.isdir(CARPETA_IMAGENES):
        sys.exit(f"No existe la carpeta de imágenes: {CARPETA_IMAGENES}")

    archivos = sorted(
        os.path.join(CARPETA_IMAGENES, n)
        for n in os.listdir(CARPETA_IMAGENES)
        if n.lower().endswith(EXTENSIONES) and not n.startswith(".")
    )
    if not archivos:
        sys.exit(f"La carpeta {CARPETA_IMAGENES} no tiene imágenes.")

    pool = proyecto.GetMediaPool()
    clips = resolve.GetMediaStorage().AddItemListToMediaPool(archivos)
    if not clips:
        sys.exit("Resolve no importó ninguna imagen. ¿Formato soportado?")

    print(f"Importadas {len(clips)} imágenes de {CARPETA_IMAGENES}:")
    for c in clips:
        print(f"  · {c.GetName()}")
    return pool, clips


# ------------------------------------------------------------------ montaje

def montar(pool, clips):
    duracion = int(float(FPS) * SEGUNDOS_POR_IMAGEN)
    linea = pool.CreateEmptyTimeline("LED · montaje base")
    if linea is None:
        sys.exit("No pude crear la línea de tiempo.")

    items = pool.AppendToTimeline([
        {"mediaPoolItem": c, "startFrame": 0, "endFrame": duracion - 1}
        for c in clips
    ])
    print(f"Línea de tiempo armada: {len(items or [])} clips de "
          f"{SEGUNDOS_POR_IMAGEN} s ({duracion} cuadros) cada uno.")
    return linea, items or []


def acomodar_mosaico(items):
    """Coloca los primeros 4 clips como un mosaico horizontal.

    Solo tiene sentido si esos 4 clips son los paneles de una misma escena.
    Si no, dejá MOSAICO en False más abajo.
    """
    if len(items) < 4:
        print("Mosaico salteado: hacen falta al menos 4 clips.")
        return
    for i, item in enumerate(items[:4]):
        item.SetProperty("ZoomX", MOSAICO_ZOOM)
        item.SetProperty("ZoomY", MOSAICO_ZOOM)
        item.SetProperty("Pan", MOSAICO_PAN[i])
        item.SetProperty("Tilt", 0)
        print(f"  panel {i + 1}: zoom {MOSAICO_ZOOM}  pan {MOSAICO_PAN[i]}")
    print("Mosaico acomodado. Revisá las costuras y suavizalas con máscaras "
          "en el nodo de color, o con un Merge en Fusion.")


# ------------------------------------------------------------------ main

MOSAICO = False   # ponelo en True cuando la carpeta tenga los 4 paneles

if __name__ == "__main__":
    resolve_app = conectar()
    proyecto_actual = abrir_proyecto(resolve_app)
    pool_actual, clips_actuales = importar(resolve_app, proyecto_actual)
    _, items_actuales = montar(pool_actual, clips_actuales)
    if MOSAICO:
        acomodar_mosaico(items_actuales)
    print("\nListo. Abrí la página Edit en Resolve.")
