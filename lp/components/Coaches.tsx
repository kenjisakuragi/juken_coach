const coaches = [
  {
    name: 'コーチ A',
    title: '塾・予備校なし 東京大学 現役合格',
    school: '聖光学院高校 → 東京大学',
    description:
      '高校3年間、一切の塾・予備校を使わず独学で東大現役合格。「勉強の仕組み化」と「自己分析型学習」を徹底することで、効率的に偏差値を伸ばす方法論を確立。特に理系科目の論理的アプローチと、現代文・英語の得点最大化戦略が得意。',
    strengths: ['独学戦略の設計', '理系科目（数学・物理・化学）', '自己管理システム構築'],
    badge: '東大',
    badgeColor: 'bg-blue-900/50 border-blue-500/30 text-blue-300',
  },
  {
    name: 'からしかし',
    title: '公立高校から 一浪で京都大学 合格',
    school: '公立高校 → 浪人 → 京都大学',
    description:
      '環境的に不利な公立高校から、一浪で京大合格を勝ち取る。浪人という「失敗からの逆転」経験を持つため、メンタル管理と立て直し戦略に強みがある。「最短ルートへの軌道修正」と「モチベーション維持の仕組み化」が専門。note（@karashikashi）でも受験論を発信中。',
    strengths: ['メンタルサポート', '浪人・逆転戦略', '国語・文系科目'],
    badge: '京大',
    badgeColor: 'bg-red-900/50 border-red-500/30 text-red-300',
  },
];

export default function Coaches() {
  return (
    <section id="coaches" className="py-24 section-padding">
      <div className="max-w-5xl mx-auto">
        <div className="text-center mb-16">
          <div className="label-tag mb-4">Our Coaches</div>
          <h2 className="font-serif text-3xl md:text-4xl font-bold mb-4">
            合格した本人が、あなたを教える。
          </h2>
          <div className="divider" />
          <p className="text-gray-400 text-sm mt-6 max-w-xl mx-auto">
            「有名大学卒」の看板だけで教えるコーチとは違います。
            私たちは受験本番で勝った戦略を、そのまま伝えます。
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {coaches.map((coach, i) => (
            <div
              key={i}
              className="gold-border p-8 card-hover bg-ink-soft"
            >
              {/* Badge */}
              <div className={`inline-block px-3 py-1 text-xs font-bold border rounded-full mb-6 ${coach.badgeColor}`}>
                {coach.badge}合格
              </div>

              {/* Avatar placeholder */}
              <div className="w-20 h-20 rounded-full border-2 border-gold/40 flex items-center justify-center bg-ink mb-4">
                <span className="text-gold text-3xl font-serif font-bold">
                  {coach.badge}
                </span>
              </div>

              <h3 className="font-bold text-xl mb-1">{coach.name}</h3>
              <p className="text-gold text-sm mb-1">{coach.title}</p>
              <p className="text-gray-500 text-xs mb-4 tracking-wider">{coach.school}</p>

              <p className="text-gray-300 text-sm leading-relaxed mb-6">
                {coach.description}
              </p>

              <div>
                <p className="text-xs text-gold/70 tracking-widest uppercase mb-2">得意分野</p>
                <div className="flex flex-wrap gap-2">
                  {coach.strengths.map((s) => (
                    <span
                      key={s}
                      className="text-xs px-3 py-1 border border-gold/20 text-gray-400"
                    >
                      {s}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-10 text-center">
          <p className="text-gray-500 text-sm">
            ※ 担当コーチは受験科目・志望校・性格に合わせてマッチングします。
          </p>
        </div>
      </div>
    </section>
  );
}
