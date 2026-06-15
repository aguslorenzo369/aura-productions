'use client'
import { useState, useEffect } from 'react'
import Image from 'next/image'
import Link from 'next/link'

const links = [
  { label: 'Nosotros', href: '#nosotros' },
  { label: 'Servicios', href: '#servicios' },
  { label: 'Proyectos', href: '#proyectos' },
  { label: 'Contacto', href: '#contacto' },
]

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const handler = () => setScrolled(window.scrollY > 40)
    window.addEventListener('scroll', handler)
    return () => window.removeEventListener('scroll', handler)
  }, [])

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 glass-nav ${
        scrolled ? 'border-b border-white/5' : ''
      }`}
    >
      <div className="max-w-7xl mx-auto px-8 md:px-10 h-16 flex items-center justify-between">

        {/* Logo */}
        <Link href="/" className="flex items-center gap-3 group">
          <Image
            src="/images/logo.png"
            alt="Aura Productions"
            width={38}
            height={38}
            className="object-contain"
          />
          <span className="text-[11px] font-medium tracking-[0.25em] uppercase text-[#C9A84C]">
            Aura Productions
          </span>
        </Link>

        {/* Links — desktop */}
        <ul className="hidden md:flex items-center gap-8">
          {links.map((l) => (
            <li key={l.href}>
              <Link
                href={l.href}
                className="text-[10px] tracking-[0.15em] uppercase text-white/35 hover:text-[#C9A84C] transition-colors duration-200"
              >
                {l.label}
              </Link>
            </li>
          ))}
        </ul>

        {/* CTA */}
        <a
          href="#contacto"
          className="text-[10px] font-medium tracking-[0.18em] uppercase bg-[#C9A84C] text-black px-5 py-2.5 hover:opacity-85 transition-opacity"
        >
          Iniciar proyecto
        </a>
      </div>
    </nav>
  )
}
