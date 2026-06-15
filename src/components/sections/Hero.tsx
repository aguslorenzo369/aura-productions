'use client'
import { useEffect, useRef } from 'react'
import Image from 'next/image'

export default function Hero() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    let animId: number
    let W = 0, H = 0

    const resize = () => {
      W = canvas.width = window.innerWidth
      H = canvas.height = window.innerHeight
    }
    resize()
    window.addEventListener('resize', resize)

    type Particle = {
      x: number; y: number; vx: number; vy: number
      alpha: number; size: number; gold: boolean
    }

    const pts: Particle[] = Array.from({ length: 90 }, () => ({
      x: Math.random() * W, y: Math.random() * H,
      vx: (Math.random() - 0.5) * 0.25, vy: (Math.random() - 0.5) * 0.25,
      alpha: Math.random() * 0.25 + 0.04,
      size: Math.random() * 1.2 + 0.4,
      gold: Math.random() > 0.65,
    }))

    const loop = () => {
      ctx.clearRect(0, 0, W, H)
      pts.forEach((p) => {
        p.x += p.vx; p.y += p.vy
        if (p.x < 0 || p.x > W || p.y < 0 || p.y > H) {
          p.x = Math.random() * W; p.y = Math.random() * H
        }
        ctx.beginPath()
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2)
        ctx.fillStyle = p.gold
          ? `rgba(201,168,76,${p.alpha})`
          : `rgba(255,255,255,${p.alpha * 0.4})`
        ctx.fill()
      })
      animId = requestAnimationFrame(loop)
    }
    loop()

    return () => {
      cancelAnimationFrame(animId)
      window.removeEventListener('resize', resize)
    }
  }, [])

  return (
    <section className="relative min-h-screen flex items-center overflow-hidden">

      {/* Particle canvas */}
      <canvas ref={canvasRef} className="fixed inset-0 pointer-events-none z-0" />

      <div className="relative z-10 max-w-7xl mx-auto px-8 md:px-10 w-full grid md:grid-cols-2 gap-12 items-center pt-16">

        {/* LEFT */}
        <div>
          {/* Live tag */}
          <div className="inline-flex items-center gap-2 text-[10px] tracking-[0.25em] uppercase text-[#C9A84C] border border-[#C9A84C]/25 px-3.5 py-1.5 mb-10">
            <span className="w-1.5 h-1.5 rounded-full bg-[#C9A84C] animate-pulse" />
            Buenos Aires · Argentina · Est. 2019
          </div>

          {/* Headline */}
          <h1 className="text-[58px] md:text-[68px] font-bold leading-[1.0] tracking-[-2px] mb-7">
            Diseñamos<br />
            <span className="text-[#C9A84C]">experiencias</span><br />
            <span className="text-outline">extraordinarias</span>
          </h1>

          <p className="text-[14px] leading-[1.78] text-white/38 font-light max-w-[400px] mb-11">
            No producimos eventos. Construimos arquitectura humana de alto impacto —
            donde tecnología, diseño y propósito se fusionan en algo único.
          </p>

          <div className="flex gap-3 items-center">
            <a
              href="#servicios"
              className="text-[11px] font-medium tracking-[0.1em] uppercase bg-[#C9A84C] text-black px-7 py-3.5 hover:opacity-85 transition-opacity"
            >
              Ver nuestro trabajo
            </a>
            <a
              href="#nosotros"
              className="text-[11px] font-medium tracking-[0.1em] uppercase text-white/40 border border-white/12 px-7 py-3.5 hover:border-[#C9A84C]/50 hover:text-[#C9A84C] transition-all"
            >
              Conocer más ↓
            </a>
          </div>
        </div>

        {/* RIGHT — Phoenix */}
        <div className="flex justify-center items-center">
          <div className="relative w-[340px] h-[340px] md:w-[400px] md:h-[400px]">

            {/* Glow */}
            <div className="absolute inset-0 m-auto w-[220px] h-[220px] rounded-full bg-[#C9A84C]/6 animate-[breathe_4s_ease-in-out_infinite]" />

            {/* Ring 1 */}
            <div className="absolute inset-0 rounded-full border border-[#C9A84C]/10 animate-[spin_50s_linear_infinite]">
              <div className="absolute -top-[3px] left-1/2 -translate-x-1/2 w-[5px] h-[5px] rounded-full bg-[#C9A84C] shadow-[0_0_8px_rgba(201,168,76,0.9)]" />
            </div>

            {/* Ring 2 */}
            <div className="absolute top-[12%] left-[12%] right-[12%] bottom-[12%] rounded-full border border-[#C9A84C]/16 animate-[spin_35s_linear_reverse_infinite]">
              <div className="absolute -top-[3px] left-1/2 -translate-x-1/2 w-[4px] h-[4px] rounded-full bg-[#C9A84C] shadow-[0_0_6px_rgba(201,168,76,0.8)]" />
            </div>

            {/* Ring 3 */}
            <div className="absolute top-[24%] left-[24%] right-[24%] bottom-[24%] rounded-full border border-[#C9A84C]/8 animate-[spin_22s_linear_infinite]">
              <div className="absolute -top-[2px] left-1/2 -translate-x-1/2 w-[3px] h-[3px] rounded-full bg-[#C9A84C]" />
            </div>

            {/* Phoenix logo */}
            <div className="absolute inset-0 flex items-center justify-center animate-[float_6s_ease-in-out_infinite]">
              <Image
                src="/images/logo.png"
                alt="Aura Productions — Phoenix"
                width={280}
                height={280}
                className="object-contain glow-gold"
                priority
              />
            </div>
          </div>
        </div>
      </div>

      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 z-10">
        <div className="w-px h-10 bg-gradient-to-b from-[#C9A84C] to-transparent animate-[scrollLine_2s_ease-in-out_infinite]" />
        <span className="text-[8px] tracking-[0.35em] uppercase text-[#C9A84C]/35">Scroll</span>
      </div>
    </section>
  )
}
