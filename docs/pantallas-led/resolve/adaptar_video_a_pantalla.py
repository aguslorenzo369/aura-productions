#!/usr/bin/env python3
"""
Adapta un video que ya existe a la pantalla LED y le pone el logo encima.

Para cuando ya tenes el video (las nubes en movimiento, por ejemplo) y solo
hay que llevarlo a 3864 x 336 y componerle el logo.

Que hace:
  1. Crea el proyecto con la linea de tiempo en 3864 x 336.
  2. Importa el video y el logo.
  3. Pone el video en V1 y lo agranda hasta cubrir todo el ancho de la banda.
  4. Pone el logo en V2, centrado, a la altura correcta.

Como correrlo
-------------
Abri Resolve, anda a Workspace > Console, elegi la pestana Py3 y pega:

    exec(open("/ruta/a/adaptar_video_a_pantalla.py").read())

Antes, en Resolve: Project Settings > Image Scaling > Input scaling >
"Scale entire image to fit". Las cuentas de zoom dependen de eso.
"""

import os
import sys

# ------------------------------------------------------------------ ajustes

VIDEO = os.path.expanduser("~/CumbreLED/nubes.mp4")          # el video que ya tenes
LOGO = os.path.expanduser("~/CumbreLED/cumbre-logo.png")     # PNG con transparencia

NOMBRE_PROYECTO = "CUMBRE LED 3864x336"
ANCHO, ALTO = 3864, 336
FPS = "30"

MARGEN_LOGO = 34        # px libres arriba y abajo del logo
POSICION_Y = 0          # mové esto para elegir qué franja del video se ve.
                        # Positivo sube la imagen, negativo la baja.


# ------------------------------------------------------------------ conexion

def conectar():
    if "resolve" in globals():
        return globals()["resolve"]
    try:
        import DaVinciResolveScript as dvr
    except ImportError:
        sys.exit("Corré el script desde Workspace > Console dentro de Resolve.")
    r = dvr.scriptapp("Resolve")
    if r is None:
        sys.exit("Resolve no esta abierto, o el scripting externo esta desactivado.")
    return r


def resolucion(clip):
    """Devuelve (ancho, alto) del clip, o None si Resolve no lo informa."""
    texto = clip.GetClipProperty("Resolution")
    try:
        w, h = texto.lower().split("x")
        return int(w), int(h)
    except (AttributeError, ValueError):
        return None


def zoom_para_cubrir(ancho_origen, alto_origen):
    """Cuanto agrandar para que el clip cubra todo el ancho de la banda.

    Con "Scale entire image to fit", zoom 1,0 deja la imagen entera dentro del
    cuadro. La cuenta se reduce a la relacion entre los dos aspectos.
    """
    return (ANCHO / ALTO) / (ancho_origen / alto_origen)


# ------------------------------------------------------------------ montaje

def preparar_proyecto(resolve):
    pm = resolve.GetProjectManager()
    proyecto = pm.LoadProject(NOMBRE_PROYECTO) or pm.CreateProject(NOMBRE_PROYECTO)
    if proyecto is None:
        sys.exit(f"No pude crear ni abrir el proyecto '{NOMBRE_PROYECTO}'.")
    for clave, valor in {
        "timelineResolutionWidth": str(ANCHO),
        "timelineResolutionHeight": str(ALTO),
        "timelineOutputResolutionWidth": str(ANCHO),
        "timelineOutputResolutionHeight": str(ALTO),
        "timelineFrameRate": FPS,
        "timelinePlaybackFrameRate": FPS,
    }.items():
        if not proyecto.SetSetting(clave, valor):
            print(f"  aviso: no se pudo fijar {clave}")
    print(f"Proyecto: {proyecto.GetName()}  ->  {ANCHO}x{ALTO} @ {FPS} fps")
    return proyecto


def importar(resolve, rutas):
    faltan = [r for r in rutas if not os.path.exists(r)]
    if faltan:
        sys.exit("No encuentro estos archivos:\n  " + "\n  ".join(faltan))
    clips = resolve.GetMediaStorage().AddItemListToMediaPool(rutas)
    if len(clips or []) != len(rutas):
        sys.exit("Resolve no importo todos los archivos. Revisa los formatos.")
    return clips


def colocar_video(item, clip):
    med = resolucion(clip)
    if med is None:
        print("  Resolve no informa la resolucion del video. "
              "Ajusta el Zoom a mano en el Inspector.")
        return
    z = zoom_para_cubrir(*med)
    item.SetProperty("ZoomX", z)
    item.SetProperty("ZoomY", z)
    item.SetProperty("Pan", 0)
    item.SetProperty("Tilt", POSICION_Y)
    visible = ALTO / (ANCHO / med[0])
    print(f"  video {med[0]}x{med[1]}  ->  Zoom {z:.3f}")
    print(f"  de sus {med[1]} px de alto se ven {visible:.0f}. "
          f"Cambia POSICION_Y para elegir cual franja.")


def colocar_logo(item, clip):
    med = resolucion(clip)
    if med is None:
        print("  Resolve no informa la resolucion del logo. Ajustalo a mano.")
        return
    lw, lh = med
    alto_util = ALTO - MARGEN_LOGO * 2
    # Con "scale to fit", zoom 1,0 ya encaja el logo entero en el cuadro.
    # Esto lo achica hasta dejarle el margen.
    encaje = min(ANCHO / lw, ALTO / lh)
    z = (alto_util / lh) / encaje
    item.SetProperty("ZoomX", z)
    item.SetProperty("ZoomY", z)
    item.SetProperty("Pan", 0)
    item.SetProperty("Tilt", 0)
    print(f"  logo {lw}x{lh}  ->  Zoom {z:.3f}  "
          f"(queda en {alto_util} px de alto, centrado)")


def montar(proyecto, clip_video, clip_logo):
    pool = proyecto.GetMediaPool()
    linea = pool.CreateEmptyTimeline("LED · video + logo")
    if linea is None:
        sys.exit("No pude crear la linea de tiempo.")

    if linea.GetTrackCount("video") < 2:
        linea.AddTrack("video")

    items_video = pool.AppendToTimeline([{"mediaPoolItem": clip_video}])
    if not items_video:
        sys.exit("No pude poner el video en la linea de tiempo.")
    colocar_video(items_video[0], clip_video)

    duracion = items_video[0].GetDuration()
    linea.SetCurrentTimecode(linea.GetStartTimecode())
    proyecto.SetCurrentTimeline(linea)

    items_logo = pool.AppendToTimeline([
        {"mediaPoolItem": clip_logo, "startFrame": 0, "endFrame": duracion - 1,
         "trackIndex": 2, "recordFrame": linea.GetStartFrame()}
    ])
    if items_logo:
        colocar_logo(items_logo[0], clip_logo)
    else:
        print("  no pude poner el logo en V2. Arrastralo a mano: "
              "el script ya dejo la pista creada.")
    return linea


if __name__ == "__main__":
    app = conectar()
    proy = preparar_proyecto(app)
    video, logo = importar(app, [VIDEO, LOGO])
    montar(proy, video, logo)
    print("\nListo. Abri la pagina Edit.")
