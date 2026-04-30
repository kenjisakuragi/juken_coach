const steps = [
  {
    step: 'STEP 1',
    title: '無料相談（30分）',
    description:
      'Zoomで現在の状況をヒアリング。志望校・現偏差値・学習環境・悩みを詳しく聞かせてください。この時点での入会プッシュは一切しません。',
    duration: '30分',
  },
  {
    step: 'STEP 2',
    title: '学習カルテの作成',
    description:
      '入会後、詳細なアセスメントを実施。模試の結果・得意不得意・残り期間をもとに、あなた専用の学習カルテと3ヶ月ロードマップを作成します。',
    duration: '入会後 3日以内',
  },
  {
    step: 'STEP 3',
    title: '週次セッション開始',
    description:
      '週1〜4回のオンラインセッションで、進捗確認・課題の深掘り・次週の計画を設定。毎回終了後にサマリーと宿題リストを送ります。',
    duration: '毎週継続',
  },
  {
    step: 'STEP 4',
    title: '月次レビューと計画修正',
    description:
      '月に1度、模試結果・学習ログ・体調・メンタルを総合的にレビュー。必要に応じてロードマップを修正し、常に最適な状態を維持します。',
    duration: '月1回',
  },
];

export default function Process() {
  return (
    <section id="process" className="py-24 section-padding bg-ink-soft">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-16">
          <div className="label-tag mb-4">How It Works</div>
          <h2 className="font-serif text-3xl md:text-4xl font-bold mb-4">
            コーチングの流れ
          </h2>
          <div className="divider" />
        </div>

        <div className="relative">
          {/* Vertical line */}
          <div className="absolute left-6 top-8 bottom-8 w-px bg-gold/20 hidden md:block" />

          <div className="space-y-0">
            {steps.map((s, i) => (
              <div key={i} className="relative flex gap-8 group">
                {/* Step number circle */}
                <div className="flex-shrink-0 w-12 h-12 rounded-full border-2 border-gold/40 bg-ink flex items-center justify-center z-10 group-hover:border-gold group-hover:bg-gold/10 transition-all">
                  <span className="text-gold text-xs font-bold">{i + 1}</span>
                </div>

                <div className="pb-12 flex-1">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <div className="text-gold/60 text-xs tracking-widest mb-1">{s.step}</div>
                      <h3 className="font-bold text-lg">{s.title}</h3>
                    </div>
                    <span className="text-gray-600 text-xs border border-white/5 px-3 py-1 flex-shrink-0 ml-4">
                      {s.duration}
                    </span>
                  </div>
                  <p className="text-gray-400 text-sm leading-relaxed">{s.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="text-center mt-8">
          <a href="#contact" className="btn-primary">
            まず無料相談から始める
          </a>
        </div>
      </div>
    </section>
  );
}
