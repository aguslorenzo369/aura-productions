import { parseLrc, type LyricLine } from '@/lib/lrc'

/**
 * KAI — MOSKA
 * https://open.spotify.com/track/0F5kzrD66lNCKGEty5QgJh
 *
 * ─────────────────────────────────────────────────────────────
 *  CÓMO CARGAR LA LETRA
 * ─────────────────────────────────────────────────────────────
 * La letra NO viene incluida: es obra de terceros y hay que
 * obtenerla de una fuente con licencia. Opciones:
 *
 *   1. El .lrc oficial del sello / distribuidora.
 *   2. Musixmatch, LyricFind o Genius vía su API con licencia.
 *   3. La letra que te pase directamente el artista.
 *
 * Una vez que la tengas, pegá el contenido del .lrc entre los
 * backticks de KAI_LRC. Formato:
 *
 *   [ti:KAI]
 *   [ar:MOSKA]
 *   [00:14.20] primera línea de la letra
 *   [00:18.65] segunda línea
 *   [00:22.10]
 *   [00:24.00] (una línea vacía marca una pausa instrumental)
 *
 * Si tenés la letra sin sincronizar, podés marcar los tiempos
 * escuchando el tema en /kai: el reproductor muestra el timestamp
 * exacto y hay un botón para copiarlo en formato [mm:ss.xx].
 */
export const KAI_LRC = ``

export const KAI_TRACK = {
  title: 'KAI',
  artist: 'MOSKA',
  spotifyUrl: 'https://open.spotify.com/track/0F5kzrD66lNCKGEty5QgJh',
  /**
   * Archivo de audio en public/. Dejá el string vacío y el
   * reproductor cae automáticamente al embed de Spotify.
   * Usá un audio del que tengas los derechos de reproducción.
   */
  audioSrc: '/audio/kai.mp3',
  /** ID del track para el embed de Spotify (fallback sin audio local) */
  spotifyId: '0F5kzrD66lNCKGEty5QgJh',
}

const parsed = parseLrc(KAI_LRC)

export const kaiLyrics: LyricLine[] = parsed.lines
export const kaiHasLyrics = parsed.lines.length > 0
