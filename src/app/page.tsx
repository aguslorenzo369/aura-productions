import Navbar from '@/components/layout/Navbar'
import Footer from '@/components/layout/Footer'
import Hero from '@/components/sections/Hero'
import Ticker from '@/components/sections/Ticker'
import Services from '@/components/sections/Services'
import Numbers from '@/components/sections/Numbers'
import Manifesto from '@/components/sections/Manifesto'
import CtaFinal from '@/components/sections/CtaFinal'

export default function Home() {
  return (
    <main>
      <Navbar />
      <Hero />
      <Ticker />
      <Services />
      <Numbers />
      <Manifesto />
      <CtaFinal />
      <Footer />
    </main>
  )
}
