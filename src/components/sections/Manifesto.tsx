export default function Manifesto() {
  return (
    <section className="relative px-8 md:px-10 py-28 text-center overflow-hidden"
      style={{ borderTop: '1px solid rgba(255,255,255,0.06)' }}
    >
      {/* Radial glow */}
      <div className="absolute inset-0 pointer-events-none"
        style={{ background: 'radial-gradient(ellipse 70% 60% at 50% 50%, rgba(201,168,76,0.05) 0%, transparent 70%)' }}
      />

      <div className="relative max-w-2xl mx-auto">
        <span
          className="block text-[80px] leading-[0.4] text-[#C9A84C]/12 mb-7"
          style={{ fontFamily: 'Playfair Display, serif' }}
        >
          "
        </span>

        <p
          className="text-[30px] md:text-[36px] leading-[1.5] text-white/80 font-light"
          style={{ fontFamily: 'Playfair Display, serif', fontStyle: 'italic' }}
        >
          El fénix no es un símbolo decorativo.<br />
          Es una{' '}
          <strong className="not-italic text-[#C9A84C] font-normal">
            promesa operativa
          </strong>
          :<br />
          cada evento que tocamos se transforma<br />
          en algo que no existía antes.
        </p>

        <p className="mt-9 text-[10px] tracking-[0.28em] uppercase text-[#C9A84C]/35">
          — Filosofía Aura Productions
        </p>
      </div>
    </section>
  )
}
