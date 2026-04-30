'use client';
import { useState } from 'react';

const faqs = [
  {
    q: '無料相談で何を話しますか？',
    a: '現在の学習状況（偏差値・模試結果）、志望校、受験までの残り期間、現在の学習環境、お悩みをヒアリングします。コーチングの内容説明も行いますが、入会を勧誘することはありません。30分で「今後の方向性」が見えることを目指しています。',
  },
  {
    q: '高1・高2でも入会できますか？',
    a: 'もちろんです。早めに正しい勉強法と戦略を身につけることで、高3での追い込みが格段に楽になります。高1からの入会も大歓迎です。',
  },
  {
    q: '浪人生・既卒生でも対応できますか？',
    a: 'はい。コーチの一人が浪人経験者のため、浪人特有のメンタル管理・計画修正・モチベーション維持を専門的にサポートできます。',
  },
  {
    q: '担当コーチは選べますか？',
    a: '無料相談時に志望校・科目・性格・希望をヒアリングし、最適なコーチをご提案します。複数回の相談を経てから決定するため、ミスマッチが起きにくい仕組みです。',
  },
  {
    q: 'オンラインのみですか？対面での指導はありますか？',
    a: '基本はZoomを使ったオンライン指導です。画面共有・ホワイトボードを活用した実践的な授業が可能です。一部エリアでは対面対応も相談可能です。',
  },
  {
    q: '途中解約はできますか？',
    a: 'はい。月末に解約の意思をお伝えいただければ、翌月からのご請求はありません。契約期間の縛りはございません（半年一括払いの場合は残余分を返金します）。',
  },
  {
    q: '受験科目が特殊（医学部・芸術系など）でも対応できますか？',
    a: '理系科目・文系科目ともに対応可能です。医学部志望の場合は別途ご相談ください。専門性の高い科目については、コーチングの範囲と外部リソースの組み合わせを提案することがあります。',
  },
  {
    q: 'どうやって支払いますか？',
    a: 'クレジットカード（Visa・Mastercard・AMEX）または銀行振込に対応しています。月初に前月分を請求します。',
  },
];

export default function FAQ() {
  const [open, setOpen] = useState<number | null>(null);

  return (
    <section id="faq" className="py-24 section-padding">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-16">
          <div className="label-tag mb-4">FAQ</div>
          <h2 className="font-serif text-3xl md:text-4xl font-bold mb-4">
            よくある質問
          </h2>
          <div className="divider" />
        </div>

        <div className="space-y-0">
          {faqs.map((faq, i) => (
            <div key={i} className="border-b border-white/5">
              <button
                className="w-full text-left py-6 flex items-center justify-between gap-4 group"
                onClick={() => setOpen(open === i ? null : i)}
              >
                <span className="text-sm font-medium group-hover:text-gold transition-colors leading-relaxed">
                  {faq.q}
                </span>
                <span
                  className={`text-gold text-xl flex-shrink-0 transition-transform duration-300 ${
                    open === i ? 'rotate-45' : ''
                  }`}
                >
                  +
                </span>
              </button>

              {open === i && (
                <div className="pb-6">
                  <p className="text-gray-400 text-sm leading-relaxed border-l-2 border-gold/30 pl-4">
                    {faq.a}
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>

        <p className="text-center text-gray-500 text-sm mt-10">
          その他のご質問は{' '}
          <a href="#contact" className="text-gold hover:underline">
            無料相談
          </a>{' '}
          でお気軽にどうぞ。
        </p>
      </div>
    </section>
  );
}
