import type { Metadata } from 'next'
import '../styles/globals.css'

export const metadata: Metadata = {
  title: 'Aura Productions — Experiencias que transforman vidas',
  description: 'Producción de eventos de alto impacto. Diseñamos experiencias transformadoras donde tecnología, diseño y propósito convergen.',
  keywords: 'producción de eventos, eventos corporativos, experiencias inmersivas, Buenos Aires, Argentina',
  openGraph: {
    title: 'Aura Productions',
    description: 'Experiencias que transforman vidas',
    url: 'https://auraproductions.com.ar',
    siteName: 'Aura Productions',
    locale: 'es_AR',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  )
}
