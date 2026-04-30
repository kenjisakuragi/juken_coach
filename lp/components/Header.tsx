'use client';
import { useState, useEffect } from 'react';

export default function Header() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40);
    window.addEventListener('scroll', onScroll);
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled ? 'bg-ink/95 backdrop-blur-sm border-b border-gold/10' : 'bg-transparent'
      }`}
    >
      <div className="section-padding py-5 flex items-center justify-between">
        <a href="#" className="flex items-center gap-3">
          <div className="w-8 h-8 border border-gold flex items-center justify-center">
            <span className="text-gold font-serif text-sm font-bold">受</span>
          </div>
          <span className="text-white font-bold tracking-wider text-sm hidden sm:block">
            JUKEN COACH
          </span>
        </a>

        <nav className="hidden md:flex items-center gap-8 text-xs tracking-widest text-gray-400">
          <a href="#coaches" className="hover:text-gold transition-colors">コーチ</a>
          <a href="#services" className="hover:text-gold transition-colors">料金</a>
          <a href="#process" className="hover:text-gold transition-colors">プロセス</a>
          <a href="#faq" className="hover:text-gold transition-colors">FAQ</a>
        </nav>

        <a href="#contact" className="btn-primary text-xs py-3 px-6">
          無料相談を申し込む
        </a>
      </div>
    </header>
  );
}
