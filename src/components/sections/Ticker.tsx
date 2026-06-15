'use client'

const items = [
  'Producción integral',
  'Experiencias transformadoras',
  'Buenos Aires · Montevideo',
  '+120 eventos producidos',
  '50.000 vidas impactadas',
  'Diseño · Tecnología · Propósito',
]

export default function Ticker() {
  const doubled = [...items, ...items]
  return (
    <div className="overflow-hidden border-t border-b border-white/5 py-3">
      <style>{`@keyframes ticker { from { transform: translateX(0); } to { transform: translateX(-50%); } }`}</style>
      <div className="flex whitespace-nowrap" style={{ animation: 'ticker 30s linear infinite' }}>
        {doubled.map((item, i) => (
          <span key={i} className="inline-flex items-center gap-4 px-7 text-[10px] tracking-[0.22em] uppercase text-white/20">
            <span className="w-[3px] h-[3px] rounded-full bg-[#C9A84C] flex-shrink-0" />
            {item}
          </span>
        ))}
      </div>
    </div>
  )
}
