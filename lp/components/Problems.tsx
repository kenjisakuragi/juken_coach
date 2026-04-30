const problems = [
  {
    icon: '📉',
    text: '塾や予備校に通わせているのに、成績が上がらない',
  },
  {
    icon: '🤷',
    text: '子どもが自分で勉強計画を立てられず、何から始めたらいいかわからない',
  },
  {
    icon: '💸',
    text: '大手塾の費用が高いわりに、個別対応が薄くて不満がある',
  },
  {
    icon: '😰',
    text: '東大・京大志望だが、周りに実際に合格した人がおらず、具体的な戦略が見えない',
  },
  {
    icon: '📆',
    text: '受験まで残り時間が少なく、効率的な逆算学習計画が必要',
  },
  {
    icon: '🧠',
    text: 'メンタル面でのサポートがなく、受験プレッシャーに押しつぶされそう',
  },
];

export default function Problems() {
  return (
    <section className="py-24 section-padding bg-ink-soft">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-16">
          <div className="label-tag mb-4">The Problem</div>
          <h2 className="font-serif text-3xl md:text-4xl font-bold mb-4">
            こんな悩み、ありませんか？
          </h2>
          <div className="divider" />
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          {problems.map((p, i) => (
            <div
              key={i}
              className="flex items-start gap-4 p-5 border border-white/5 bg-ink hover:border-gold/20 transition-all duration-300"
            >
              <span className="text-2xl flex-shrink-0">{p.icon}</span>
              <p className="text-gray-300 text-sm leading-relaxed">{p.text}</p>
            </div>
          ))}
        </div>

        <div className="mt-12 text-center p-8 border border-gold/20 bg-gold/5">
          <p className="text-gold font-serif text-xl font-bold mb-2">
            その悩み、私たちが解決できます。
          </p>
          <p className="text-gray-400 text-sm">
            東大・京大に合格した私たちが、あなたの子どもに合わせた戦略を直接設計します。
          </p>
        </div>
      </div>
    </section>
  );
}
