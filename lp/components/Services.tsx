const plans = [
  {
    name: 'スタンダード',
    price: '50,000',
    unit: '月額',
    tag: null,
    features: [
      'オンラインセッション 週1回（60分）',
      '入会時 学習カルテ作成',
      '月次 進捗レポート',
      '模試分析サポート',
      'LINEでの質問（平日 返信）',
    ],
    cta: '無料相談を申し込む',
    highlight: false,
    target: '高1〜高2、初めてコーチングを受ける方',
  },
  {
    name: 'プレミアム',
    price: '100,000',
    unit: '月額',
    tag: '人気 No.1',
    features: [
      'オンラインセッション 週2回（60分）',
      '完全オーダーメイド 学習計画',
      '週次 進捗チェック',
      '模試・過去問 深掘り分析',
      'LINEでの質問（毎日 当日返信）',
      '保護者への月次報告',
    ],
    cta: '無料相談を申し込む',
    highlight: true,
    target: '高3・受験本番まで1年以内の方',
  },
  {
    name: 'VIP',
    price: '200,000',
    unit: '月額',
    tag: '最上位',
    features: [
      'オンラインセッション 週3〜4回',
      'パーソナライズ 学習計画（毎月更新）',
      '毎日チェックイン（LINE / Zoom）',
      '模試・過去問 全科目フルサポート',
      '24時間 質問対応専用LINE',
      '保護者との週次報告 + 緊急相談',
      '東大・京大OB ネットワーク活用',
    ],
    cta: '無料相談を申し込む',
    highlight: false,
    target: '最難関志望・短期逆転・本気の方のみ',
  },
];

export default function Services() {
  return (
    <section id="services" className="py-24 section-padding bg-ink-soft">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <div className="label-tag mb-4">Pricing Plans</div>
          <h2 className="font-serif text-3xl md:text-4xl font-bold mb-4">
            料金プラン
          </h2>
          <div className="divider" />
          <p className="text-gray-400 text-sm mt-6 max-w-xl mx-auto">
            すべてのプランに無料相談（30分）が含まれます。
            入会後はいつでもプランの変更が可能です。
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          {plans.map((plan, i) => (
            <div
              key={i}
              className={`relative p-8 flex flex-col transition-all duration-300 ${
                plan.highlight
                  ? 'bg-gold/10 border-2 border-gold shadow-[0_0_40px_rgba(201,168,76,0.15)] -mt-4 md:-mt-6'
                  : 'bg-ink border border-white/5 hover:border-gold/30'
              }`}
            >
              {plan.tag && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-gold text-ink text-xs font-bold px-4 py-1 tracking-wider">
                  {plan.tag}
                </div>
              )}

              <div className="mb-6">
                <h3 className="font-bold text-lg mb-3">{plan.name}</h3>
                <div className="flex items-end gap-1">
                  <span className="text-gray-500 text-sm">{plan.unit}</span>
                  <span className={`font-serif text-4xl font-bold ${plan.highlight ? 'text-gold' : 'text-white'}`}>
                    ¥{plan.price}
                  </span>
                </div>
                <p className="text-gray-600 text-xs mt-2">{plan.target}</p>
              </div>

              <ul className="space-y-3 mb-8 flex-1">
                {plan.features.map((f) => (
                  <li key={f} className="flex items-start gap-2 text-sm text-gray-300">
                    <span className="text-gold mt-0.5 flex-shrink-0">✓</span>
                    {f}
                  </li>
                ))}
              </ul>

              <a
                href="#contact"
                className={plan.highlight ? 'btn-primary text-center' : 'btn-outline text-center'}
              >
                {plan.cta}
              </a>
            </div>
          ))}
        </div>

        <p className="text-center text-gray-600 text-xs mt-8">
          ※ 半年一括払いは5%割引。消費税別途。初月は日割り計算。
        </p>
      </div>
    </section>
  );
}
