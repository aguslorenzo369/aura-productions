import type { Metadata } from 'next'
import Navbar from '@/components/layout/Navbar'
import Footer from '@/components/layout/Footer'
import LyricsPlayer from '@/components/sections/LyricsPlayer'
import { KAI_TRACK, kaiLyrics } from '@/lib/lyrics/kai'

export const metadata: Metadata = {
  title: 'KAI — MOSKA | Aura Productions',
  description: 'Reproductor con letra sincronizada.',
}

export default function KaiPage() {
  return (
    <main className="pt-16">
      <Navbar />
      <LyricsPlayer
        title={KAI_TRACK.title}
        artist={KAI_TRACK.artist}
        lines={kaiLyrics}
        audioSrc={KAI_TRACK.audioSrc}
        spotifyId={KAI_TRACK.spotifyId}
        spotifyUrl={KAI_TRACK.spotifyUrl}
      />
      <Footer />
    </main>
  )
}
