export default function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="py-12 section-padding border-t border-white/5">
      <div className="max-w-5xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="flex items-center gap-3">
          <div className="w-7 h-7 border border-gold/40 flex items-center justify-center">
            <span className="text-gold font-serif text-xs font-bold">受</span>
          </div>
          <span className="text-gray-500 text-sm">JUKEN COACH</span>
        </div>

        <nav className="flex flex-wrap justify-center gap-6 text-xs text-gray-600">
          <a href="#coaches" className="hover:text-gold transition-colors">コーチ紹介</a>
          <a href="#services" className="hover:text-gold transition-colors">料金プラン</a>
          <a href="#process" className="hover:text-gold transition-colors">コーチングの流れ</a>
          <a href="#faq" className="hover:text-gold transition-colors">FAQ</a>
          <a href="#contact" className="hover:text-gold transition-colors">無料相談</a>
          <a href="https://note.com/karashikashi" target="_blank" rel="noopener noreferrer" className="hover:text-gold transition-colors">
            note
          </a>
        </nav>

        <p className="text-gray-700 text-xs">
          © {year} JUKEN COACH. All rights reserved.
        </p>
      </div>
    </footer>
  );
}
