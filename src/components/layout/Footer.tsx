export default function Footer() {
  return (
    <footer className="border-t border-white/5 px-8 md:px-10 py-6">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        <span className="text-[11px] tracking-[0.25em] uppercase text-[#C9A84C]/45">
          Aura Productions
        </span>
        <div className="flex gap-6">
          {['Instagram', 'LinkedIn', 'WhatsApp'].map((s) => (
            <a
              key={s}
              href="#"
              className="text-[10px] tracking-wide text-white/18 hover:text-[#C9A84C] transition-colors"
            >
              {s}
            </a>
          ))}
        </div>
        <span className="text-[10px] text-white/12">
          © 2026 — Experiencias que transforman vidas
        </span>
      </div>
    </footer>
  )
}
