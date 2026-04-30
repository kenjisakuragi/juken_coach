export default function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background grid */}
      <div
        className="absolute inset-0 opacity-[0.03]"
        style={{
          backgroundImage:
            'linear-gradient(#C9A84C 1px, transparent 1px), linear-gradient(90deg, #C9A84C 1px, transparent 1px)',
          backgroundSize: '60px 60px',
        }}
      />

      {/* Radial glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full bg-gold/5 blur-[120px] pointer-events-none" />

      <div className="relative z-10 text-center section-padding py-40 max-w-5xl mx-auto">
        <div className="label-tag mb-6 animate-fade-in">
          Premium Exam Coaching
        </div>

        <h1 className="font-serif text-4xl md:text-6xl lg:text-7xl font-bold leading-tight mb-6">
          <span className="shimmer-text">東大・京大合格者</span>が、<br />
          あなたの子どもを導く。
        </h1>

        <p className="text-gray-400 text-lg md:text-xl max-w-2xl mx-auto leading-relaxed mb-4">
          塾なし東大現役合格 × 公立高校から京大合格。<br />
          2人の実績者が伝える、本物の受験戦略。
        </p>

        <p className="text-gray-500 text-sm tracking-wider mb-12">
          完全オーダーメイド ｜ 週1〜毎日サポート ｜ 月額5万円〜
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <a href="#contact" className="btn-primary">
            無料相談（30分）を申し込む
          </a>
          <a href="#coaches" className="btn-outline">
            コーチを見る
          </a>
        </div>

        <p className="text-gray-600 text-xs mt-8 tracking-wider">
          ※ 無料相談は完全無料・勧誘なし。現在の学習状況をお聞かせください。
        </p>

        {/* Stats */}
        <div className="mt-20 grid grid-cols-3 gap-8 max-w-xl mx-auto border-t border-gold/10 pt-12">
          {[
            { num: '2', label: '東大・京大\n合格コーチ' },
            { num: '100%', label: '完全\nオーダーメイド' },
            { num: '30分', label: '無料相談\n実施中' },
          ].map((stat) => (
            <div key={stat.label} className="text-center">
              <div className="text-gold text-2xl md:text-3xl font-bold font-serif">{stat.num}</div>
              <div className="text-gray-500 text-xs mt-1 whitespace-pre-line leading-relaxed">
                {stat.label}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 text-gray-600">
        <span className="text-xs tracking-widest">SCROLL</span>
        <div className="w-px h-10 bg-gradient-to-b from-gold/40 to-transparent animate-pulse" />
      </div>
    </section>
  );
}
