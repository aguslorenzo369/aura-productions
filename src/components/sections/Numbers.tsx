const stats = [
  { val: '+120', suffix: '.', label: 'Eventos producidos' },
  { val: '2', suffix: '×', label: 'Países operados' },
  { val: '50', suffix: 'k', label: 'Vidas impactadas' },
  { val: '100', suffix: '%', label: 'Entregas cumplidas' },
]

export default function Numbers() {
  return (
    <div
      className="grid grid-cols-2 md:grid-cols-4"
      style={{ borderTop: '1px solid rgba(255,255,255,0.06)', borderBottom: '1px solid rgba(255,255,255,0.06)' }}
    >
      {stats.map((s, i) => (
        <div
          key={i}
          className="px-8 py-12 md:px-10"
          style={{ borderRight: i < stats.length - 1 ? '1px solid rgba(255,255,255,0.06)' : 'none' }}
        >
          <div className="text-[50px] md:text-[58px] font-bold tracking-[-2px] leading-none mb-2">
            {s.val}
            <span className="text-[#C9A84C]">{s.suffix}</span>
          </div>
          <div className="text-[10px] tracking-[0.2em] uppercase text-white/22">{s.label}</div>
        </div>
      ))}
    </div>
  )
}
