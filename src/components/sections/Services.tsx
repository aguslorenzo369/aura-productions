const services = [
  {
    num: '01',
    title: 'Producción integral',
    desc: 'Diseño, logística y ejecución de eventos de alta complejidad. Desde 500 hasta 10.000 personas en cualquier escala y geografía.',
  },
  {
    num: '02',
    title: 'Experiencias inmersivas',
    desc: 'Tecnología, escenografía y storytelling integrados. Producción cinematográfica en vivo que transforma a cada participante.',
  },
  {
    num: '03',
    title: 'Coordinación de staff',
    desc: 'Equipos entrenados para operar bajo presión máxima. Protocolos de excelencia en cada punto de contacto con el participante.',
  },
]

export default function Services() {
  return (
    <section id="servicios" className="px-8 md:px-10 py-24 pb-14">
      <div className="max-w-7xl mx-auto">

        <div className="flex items-center gap-3 mb-5">
          <span className="w-6 h-px bg-[#C9A84C]" />
          <span className="text-[10px] tracking-[0.28em] uppercase text-[#C9A84C]">Capacidades</span>
        </div>

        <h2 className="text-[44px] md:text-[52px] font-bold leading-[1.08] tracking-[-1.5px]">
          Todo lo que tu evento<br />
          necesita para ser{' '}
          <em className="font-light not-italic" style={{ fontFamily: 'Playfair Display, serif', color: '#C9A84C' }}>
            legendario
          </em>
        </h2>

        <div
          className="mt-14 grid grid-cols-1 md:grid-cols-3"
          style={{ gap: '1px', background: 'rgba(255,255,255,0.06)' }}
        >
          {services.map((s) => (
            <div
              key={s.num}
              className="bg-black p-10 relative overflow-hidden group cursor-default transition-colors duration-300 hover:bg-[#C9A84C]/[0.04]"
            >
              {/* Top accent line on hover */}
              <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-[#C9A84C] to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

              <div className="text-[10px] tracking-[0.2em] text-[#C9A84C]/30 mb-4">{s.num}</div>
              <h3 className="text-[15px] font-medium mb-3">{s.title}</h3>
              <p className="text-[12px] leading-[1.78] text-white/32 font-light">{s.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
