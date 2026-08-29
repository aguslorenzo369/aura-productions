/**
 * Parser de archivos .lrc (letra sincronizada).
 *
 * Soporta:
 *   [00:12.34] Texto de la línea
 *   [00:12.34][01:45.10] Texto repetido (estribillo)
 *   [ti:Título] [ar:Artista] [al:Álbum] [offset:-250]  ← metadata
 */

export type LyricLine = {
  /** Segundos desde el inicio del track */
  time: number
  text: string
}

export type ParsedLrc = {
  title?: string
  artist?: string
  album?: string
  /** Corrimiento global en ms — positivo adelanta la letra */
  offset: number
  lines: LyricLine[]
}

const TIME_TAG = /\[(\d{1,3}):(\d{1,2})(?:[.:](\d{1,3}))?\]/g
const META_TAG = /^\[(ti|ar|al|offset):(.*)\]$/i

export function parseLrc(raw: string): ParsedLrc {
  const result: ParsedLrc = { offset: 0, lines: [] }

  for (const rawLine of raw.split(/\r?\n/)) {
    const line = rawLine.trim()
    if (!line) continue

    const meta = line.match(META_TAG)
    if (meta) {
      const key = meta[1].toLowerCase()
      const value = meta[2].trim()
      if (key === 'ti') result.title = value
      else if (key === 'ar') result.artist = value
      else if (key === 'al') result.album = value
      else if (key === 'offset') result.offset = parseInt(value, 10) || 0
      continue
    }

    // Todos los timestamps al inicio de la línea apuntan al mismo texto
    TIME_TAG.lastIndex = 0
    const stamps: number[] = []
    let match: RegExpExecArray | null
    while ((match = TIME_TAG.exec(line)) !== null) {
      const [min, sec, frac] = [match[1], match[2], match[3]]
      // .5 → 500ms, .50 → 500ms, .500 → 500ms
      const ms = frac ? parseInt(frac.padEnd(3, '0'), 10) : 0
      stamps.push(parseInt(min, 10) * 60 + parseInt(sec, 10) + ms / 1000)
    }
    if (!stamps.length) continue

    const text = line.replace(TIME_TAG, '').trim()
    for (const time of stamps) result.lines.push({ time, text })
  }

  result.lines.sort((a, b) => a.time - b.time)

  if (result.offset !== 0) {
    const shift = result.offset / 1000
    result.lines = result.lines.map((l) => ({
      ...l,
      time: Math.max(0, l.time + shift),
    }))
  }

  return result
}

/**
 * Índice de la línea que suena en `time`, o -1 si todavía no arrancó
 * la primera. Búsqueda binaria: se llama en cada frame.
 */
export function activeLineIndex(lines: LyricLine[], time: number): number {
  let lo = 0
  let hi = lines.length - 1
  let found = -1

  while (lo <= hi) {
    const mid = (lo + hi) >> 1
    if (lines[mid].time <= time) {
      found = mid
      lo = mid + 1
    } else {
      hi = mid - 1
    }
  }

  return found
}

export function formatTime(seconds: number): string {
  if (!Number.isFinite(seconds) || seconds < 0) return '0:00'
  const m = Math.floor(seconds / 60)
  const s = Math.floor(seconds % 60)
  return `${m}:${s.toString().padStart(2, '0')}`
}
