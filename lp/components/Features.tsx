const features = [
  {
    number: '01',
    title: '合格者本人が直接指導',
    description:
      '実際に東大・京大に合格したコーチが担当します。「なんとなく教えられる」講師ではなく、本番で使った戦略をそのまま伝えます。',
  },
  {
    number: '02',
    title: '完全オーダーメイドの学習設計',
    description:
      '入会時に詳細なヒアリングを実施。現在の偏差値・志望校・残り期間・科目の得意不得意をもとに、あなた専用の学習ロードマップを作成します。',
  },
  {
    number: '03',
    title: '模試・過去問の徹底分析',
    description:
      '点数だけを見るのではなく、どの問題でどう間違えたかを詳細に分析。「何をすれば点数が上がるか」を具体的に特定します。',
  },
  {
    number: '04',
    title: 'メンタルサポート',
    description:
      '受験は学力だけでなく精神力の戦いでもあります。浪人経験を持つコーチが、受験のプレッシャーや挫折からの立て直しを徹底サポートします。',
  },
  {
    number: '05',
    title: 'AIを活用した学習分析',
    description:
      'AIによる弱点分析・学習ログの可視化で、感覚ではなくデータに基づいた戦略修正を行います。毎週の改善サイクルを仕組み化します。',
  },
  {
    number: '06',
    title: '保護者との連携報告',
    description:
      '月次（プランによっては週次）で保護者への進捗報告を実施。家庭での勉強環境づくりのアドバイスも行い、家族全体で受験を乗り越えます。',
  },
];

export default function Features() {
  return (
    <section className="py-24 section-padding">
      <div className="max-w-5xl mx-auto">
        <div className="text-center mb-16">
          <div className="label-tag mb-4">Why Choose Us</div>
          <h2 className="font-serif text-3xl md:text-4xl font-bold mb-4">
            選ばれる6つの理由
          </h2>
          <div className="divider" />
        </div>

        <div className="grid md:grid-cols-2 gap-0">
          {features.map((f, i) => (
            <div
              key={i}
              className={`p-8 border-b border-r border-white/5 hover:bg-ink-soft transition-colors duration-300 ${
                i % 2 === 1 ? 'border-r-0' : ''
              } ${i >= features.length - 2 ? 'border-b-0' : ''}`}
            >
              <div className="text-gold/30 font-serif text-5xl font-bold mb-4 leading-none">
                {f.number}
              </div>
              <h3 className="font-bold text-lg mb-3">{f.title}</h3>
              <p className="text-gray-400 text-sm leading-relaxed">{f.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
