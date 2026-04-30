export default function Contact() {
  return (
    <section id="contact" className="py-32 section-padding bg-ink-soft relative overflow-hidden">
      {/* Background glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[300px] bg-gold/5 blur-[100px] rounded-full pointer-events-none" />

      <div className="max-w-2xl mx-auto text-center relative z-10">
        <div className="label-tag mb-4">Free Consultation</div>
        <h2 className="font-serif text-3xl md:text-5xl font-bold mb-6 leading-tight">
          まず、話してみてください。<br />
          <span className="shimmer-text">30分で、方向性が見えます。</span>
        </h2>
        <div className="divider" />
        <p className="text-gray-400 text-sm mt-6 mb-10 leading-relaxed">
          無料相談は完全無料・勧誘なし。<br />
          「相談だけ」でもOKです。現状をお聞かせください。
        </p>

        {/* Calendly placeholder */}
        <div className="gold-border p-8 bg-ink mb-8">
          <p className="text-gray-500 text-sm mb-6">
            ご希望の日時を選択して、Zoomリンクを受け取ってください。
          </p>

          {/* This would be replaced with actual Calendly embed */}
          <a
            href="https://calendly.com/"
            target="_blank"
            rel="noopener noreferrer"
            className="btn-primary block text-center"
          >
            無料相談の日程を選ぶ（Calendly）
          </a>
        </div>

        <p className="text-gray-600 text-xs">
          またはメールでのお問い合わせ：{' '}
          <a href="mailto:contact@juken-coach.jp" className="text-gold/70 hover:text-gold">
            contact@juken-coach.jp
          </a>
        </p>

        <div className="mt-12 grid grid-cols-3 gap-6 text-center border-t border-gold/10 pt-12">
          {[
            { icon: '🎯', text: '完全無料\n勧誘なし' },
            { icon: '⏱', text: 'Zoom 30分\n当日対応可' },
            { icon: '🔒', text: '秘密厳守\n個人情報保護' },
          ].map((item) => (
            <div key={item.text}>
              <div className="text-2xl mb-2">{item.icon}</div>
              <p className="text-gray-500 text-xs whitespace-pre-line leading-relaxed">
                {item.text}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
