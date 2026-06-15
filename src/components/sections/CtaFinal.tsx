export default function CtaFinal() {
  return (
    <section
      id="contacto"
      className="px-8 md:px-10 py-24 flex flex-col md:flex-row items-start md:items-center justify-between gap-10"
      style={{ borderTop: '1px solid rgba(255,255,255,0.06)' }}
    >
      <div>
        <h2
          className="text-[44px] md:text-[52px] font-bold tracking-[-1.5px] leading-[1.05] mb-3"
        >
          ¿Listo para crear algo<br />
          <em
            className="font-light not-italic text-[#C9A84C]"
            style={{ fontFamily: 'Playfair Display, serif' }}
          >
            que no se olvide?
          </em>
        </h2>
        <p className="text-[13px] text-white/30 font-light">
          Contanos tu proyecto. Te respondemos en 24hs.
        </p>
      </div>

      <div className="flex gap-3 flex-shrink-0">
        <a
          href="mailto:hola@auraproductions.com.ar"
          className="text-[11px] font-medium tracking-[0.1em] uppercase bg-[#C9A84C] text-black px-7 py-3.5 hover:opacity-85 transition-opacity"
        >
          Iniciar proyecto →
        </a>
        <a
          href="#servicios"
          className="text-[11px] font-medium tracking-[0.1em] uppercase text-white/40 border border-white/12 px-7 py-3.5 hover:border-[#C9A84C]/50 hover:text-[#C9A84C] transition-all"
        >
          Ver portfolio
        </a>
      </div>
    </section>
  )
}
