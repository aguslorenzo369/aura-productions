'use client'

import { useCallback, useEffect, useRef, useState } from 'react'
import { activeLineIndex, formatTime, type LyricLine } from '@/lib/lrc'

type Props = {
  title: string
  artist: string
  lines: LyricLine[]
  audioSrc: string
  spotifyId?: string
  spotifyUrl?: string
}

export default function LyricsPlayer({
  title,
  artist,
  lines,
  audioSrc,
  spotifyId,
  spotifyUrl,
}: Props) {
  const audioRef = useRef<HTMLAudioElement>(null)
  const scrollerRef = useRef<HTMLDivElement>(null)
  const lineRefs = useRef<(HTMLParagraphElement | null)[]>([])
  /** El usuario scrolleó a mano: pausamos el auto-scroll un rato */
  const userScrolling = useRef(false)
  const userScrollTimer = useRef<ReturnType<typeof setTimeout>>()

  const [playing, setPlaying] = useState(false)
  const [time, setTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const [current, setCurrent] = useState(-1)
  const [audioError, setAudioError] = useState(false)
  const [copied, setCopied] = useState(false)

  const hasLyrics = lines.length > 0

  // ── Sync loop ───────────────────────────────────────────────
  // requestAnimationFrame en vez de `timeupdate`: el evento nativo
  // dispara cada ~250ms y se nota el retraso en el resaltado.
  useEffect(() => {
    const audio = audioRef.current
    if (!audio) return

    let frame: number
    const tick = () => {
      setTime(audio.currentTime)
      if (hasLyrics) setCurrent(activeLineIndex(lines, audio.currentTime))
      frame = requestAnimationFrame(tick)
    }

    if (playing) frame = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(frame)
  }, [playing, lines, hasLyrics])

  // ── Auto-scroll de la línea activa ──────────────────────────
  useEffect(() => {
    if (current < 0 || userScrolling.current) return
    const el = lineRefs.current[current]
    const scroller = scrollerRef.current
    if (!el || !scroller) return

    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    scroller.scrollTo({
      top: el.offsetTop - scroller.clientHeight / 2 + el.clientHeight / 2,
      behavior: reduce ? 'auto' : 'smooth',
    })
  }, [current])

  const onManualScroll = useCallback(() => {
    userScrolling.current = true
    clearTimeout(userScrollTimer.current)
    userScrollTimer.current = setTimeout(() => {
      userScrolling.current = false
    }, 4000)
  }, [])

  useEffect(() => () => clearTimeout(userScrollTimer.current), [])

  // ── Controles ───────────────────────────────────────────────
  const toggle = useCallback(() => {
    const audio = audioRef.current
    if (!audio) return
    if (audio.paused) audio.play().catch(() => setAudioError(true))
    else audio.pause()
  }, [])

  const seek = useCallback((seconds: number) => {
    const audio = audioRef.current
    if (!audio) return
    audio.currentTime = Math.max(0, Math.min(seconds, audio.duration || seconds))
    setTime(audio.currentTime)
    if (lines.length) setCurrent(activeLineIndex(lines, audio.currentTime))
  }, [lines])

  // Barra espaciadora = play/pause, flechas = ±5s
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const tag = (e.target as HTMLElement)?.tagName
      if (tag === 'INPUT' || tag === 'TEXTAREA') return
      if (e.code === 'Space') {
        e.preventDefault()
        toggle()
      } else if (e.code === 'ArrowLeft') {
        seek(time - 5)
      } else if (e.code === 'ArrowRight') {
        seek(time + 5)
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [toggle, seek, time])

  /** Copia el tiempo actual como tag LRC, para sincronizar la letra a mano */
  const copyTimestamp = useCallback(() => {
    const m = Math.floor(time / 60)
    const s = Math.floor(time % 60)
    const cs = Math.floor((time % 1) * 100)
    const tag = `[${m.toString().padStart(2, '0')}:${s
      .toString()
      .padStart(2, '0')}.${cs.toString().padStart(2, '0')}]`
    navigator.clipboard?.writeText(tag).then(
      () => {
        setCopied(true)
        setTimeout(() => setCopied(false), 1400)
      },
      () => undefined
    )
  }, [time])

  const progress = duration > 0 ? (time / duration) * 100 : 0

  return (
    <section
      className="relative px-8 md:px-10 py-24 overflow-hidden"
      style={{ borderTop: '1px solid rgba(255,255,255,0.06)' }}
    >
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background:
            'radial-gradient(ellipse 70% 60% at 50% 40%, rgba(201,168,76,0.06) 0%, transparent 70%)',
        }}
      />

      <div className="relative max-w-3xl mx-auto">
        {/* ── Cabecera ───────────────────────────────────────── */}
        <div className="text-center mb-12">
          <span className="inline-flex items-center gap-2 text-[10px] tracking-[0.28em] uppercase text-[#C9A84C] border border-[#C9A84C]/25 px-3.5 py-1.5">
            <span
              className={`w-1.5 h-1.5 rounded-full bg-[#C9A84C] ${
                playing ? 'animate-pulse' : 'opacity-40'
              }`}
            />
            Now playing
          </span>

          <h1 className="mt-7 text-[52px] md:text-[64px] font-bold leading-[1.0] tracking-[-2px]">
            {title}
          </h1>
          <p className="mt-3 text-[11px] tracking-[0.28em] uppercase text-white/38">
            {artist}
          </p>
        </div>

        {/* ── Letra ──────────────────────────────────────────── */}
        {hasLyrics ? (
          <div
            ref={scrollerRef}
            onWheel={onManualScroll}
            onTouchMove={onManualScroll}
            className="relative h-[52vh] min-h-[320px] overflow-y-auto no-scrollbar"
            style={{
              maskImage:
                'linear-gradient(to bottom, transparent 0%, black 16%, black 84%, transparent 100%)',
              WebkitMaskImage:
                'linear-gradient(to bottom, transparent 0%, black 16%, black 84%, transparent 100%)',
            }}
          >
            {/* Padding para que la primera y última línea lleguen al centro */}
            <div className="py-[26vh]">
              {lines.map((line, i) => (
                <p
                  key={`${line.time}-${i}`}
                  ref={(el) => {
                    lineRefs.current[i] = el
                  }}
                  onClick={() => seek(line.time)}
                  className={`cursor-pointer text-center px-4 py-2.5 text-[24px] md:text-[30px] leading-[1.45] transition-all duration-500 ${
                    i === current
                      ? 'text-[#C9A84C] scale-[1.02]'
                      : i < current
                      ? 'text-white/20 hover:text-white/40'
                      : 'text-white/45 hover:text-white/70'
                  }`}
                  style={{
                    fontFamily: 'Playfair Display, serif',
                    fontStyle: 'italic',
                    textShadow:
                      i === current
                        ? '0 0 28px rgba(201,168,76,0.35)'
                        : undefined,
                  }}
                >
                  {line.text || '•'}
                </p>
              ))}
            </div>
          </div>
        ) : (
          <EmptyLyrics spotifyUrl={spotifyUrl} />
        )}

        {/* ── Controles ──────────────────────────────────────── */}
        {!audioError ? (
          <div className="mt-10">
            <div className="flex items-center gap-5">
              <button
                onClick={toggle}
                aria-label={playing ? 'Pausar' : 'Reproducir'}
                className="shrink-0 w-14 h-14 rounded-full border border-[#C9A84C]/40 text-[#C9A84C] flex items-center justify-center hover:bg-[#C9A84C] hover:text-black transition-colors"
              >
                {playing ? (
                  <svg width="14" height="16" viewBox="0 0 14 16" fill="currentColor">
                    <rect x="0" y="0" width="4.5" height="16" />
                    <rect x="9.5" y="0" width="4.5" height="16" />
                  </svg>
                ) : (
                  <svg width="14" height="16" viewBox="0 0 14 16" fill="currentColor">
                    <path d="M0 0l14 8-14 8z" />
                  </svg>
                )}
              </button>

              <div className="flex-1">
                <div
                  role="slider"
                  tabIndex={0}
                  aria-label="Progreso"
                  aria-valuemin={0}
                  aria-valuemax={Math.floor(duration)}
                  aria-valuenow={Math.floor(time)}
                  onClick={(e) => {
                    const r = e.currentTarget.getBoundingClientRect()
                    seek(((e.clientX - r.left) / r.width) * duration)
                  }}
                  onKeyDown={(e) => {
                    if (e.key === 'ArrowLeft') seek(time - 5)
                    if (e.key === 'ArrowRight') seek(time + 5)
                  }}
                  className="group relative h-1 bg-white/10 cursor-pointer"
                >
                  <div
                    className="absolute inset-y-0 left-0 bg-[#C9A84C]"
                    style={{ width: `${progress}%` }}
                  />
                  <div
                    className="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 w-2.5 h-2.5 rounded-full bg-[#C9A84C] opacity-0 group-hover:opacity-100 transition-opacity"
                    style={{ left: `${progress}%` }}
                  />
                </div>

                <div className="flex justify-between mt-2.5 text-[10px] tracking-[0.18em] text-white/30 tabular-nums">
                  <span>{formatTime(time)}</span>
                  <button
                    onClick={copyTimestamp}
                    title="Copiar timestamp en formato LRC — sirve para sincronizar la letra"
                    className="tracking-[0.18em] uppercase hover:text-[#C9A84C] transition-colors"
                  >
                    {copied ? 'copiado ✓' : 'copiar tiempo'}
                  </button>
                  <span>{formatTime(duration)}</span>
                </div>
              </div>
            </div>

            <p className="mt-5 text-center text-[10px] tracking-[0.2em] uppercase text-white/20">
              Espacio · play/pausa &nbsp;·&nbsp; ← → · ±5s
              {hasLyrics && ' · click en una línea · saltar ahí'}
            </p>
          </div>
        ) : (
          <SpotifyFallback spotifyId={spotifyId} audioSrc={audioSrc} />
        )}

        <audio
          ref={audioRef}
          src={audioSrc || undefined}
          preload="metadata"
          onPlay={() => setPlaying(true)}
          onPause={() => setPlaying(false)}
          onEnded={() => setPlaying(false)}
          onLoadedMetadata={(e) => setDuration(e.currentTarget.duration)}
          onError={() => setAudioError(true)}
        />
      </div>
    </section>
  )
}

function EmptyLyrics({ spotifyUrl }: { spotifyUrl?: string }) {
  return (
    <div className="border border-white/8 bg-white/[0.02] px-8 py-12 text-center">
      <p className="text-[13px] leading-[1.9] text-white/45 font-light max-w-[440px] mx-auto">
        Todavía no hay letra cargada. Es obra de terceros, así que hay que
        traerla de una fuente con licencia y pegarla en{' '}
        <code className="text-[#C9A84C] not-italic">src/lib/lyrics/kai.ts</code>{' '}
        en formato <code className="text-[#C9A84C]">.lrc</code>.
      </p>
      <p className="mt-6 text-[11px] leading-[1.9] text-white/28 font-light max-w-[440px] mx-auto">
        Si la tenés sin sincronizar: dale play, y con{' '}
        <span className="text-white/50">copiar tiempo</span> vas marcando el
        timestamp de cada línea.
      </p>
      {spotifyUrl && (
        <a
          href={spotifyUrl}
          target="_blank"
          rel="noreferrer"
          className="inline-block mt-8 text-[10px] tracking-[0.25em] uppercase text-[#C9A84C]/70 border-b border-[#C9A84C]/25 pb-1 hover:text-[#C9A84C] transition-colors"
        >
          Escuchar en Spotify ↗
        </a>
      )}
    </div>
  )
}

function SpotifyFallback({
  spotifyId,
  audioSrc,
}: {
  spotifyId?: string
  audioSrc: string
}) {
  return (
    <div className="mt-10">
      {spotifyId ? (
        <iframe
          title="KAI — MOSKA en Spotify"
          src={`https://open.spotify.com/embed/track/${spotifyId}?theme=0`}
          width="100%"
          height="152"
          frameBorder="0"
          loading="lazy"
          allow="encrypted-media"
          className="rounded"
        />
      ) : null}
      <p className="mt-4 text-center text-[10px] tracking-[0.18em] uppercase text-white/25">
        No se encontró <span className="text-white/45">{audioSrc}</span> — el
        karaoke sincronizado necesita el audio local
      </p>
    </div>
  )
}
