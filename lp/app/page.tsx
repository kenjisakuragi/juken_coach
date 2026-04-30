import Header from '@/components/Header';
import Hero from '@/components/Hero';
import Problems from '@/components/Problems';
import Coaches from '@/components/Coaches';
import Features from '@/components/Features';
import Services from '@/components/Services';
import Process from '@/components/Process';
import FAQ from '@/components/FAQ';
import Contact from '@/components/Contact';
import Footer from '@/components/Footer';

export default function Home() {
  return (
    <main>
      <Header />
      <Hero />
      <Problems />
      <Coaches />
      <Features />
      <Services />
      <Process />
      <FAQ />
      <Contact />
      <Footer />
    </main>
  );
}
