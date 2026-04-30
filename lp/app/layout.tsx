import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: '高級受験コーチング | 東大・京大合格者が直接教える',
  description:
    '塾なし東大現役合格 × 公立高校から京大合格。2人の実績者が直接指導する、完全オーダーメイドの高級受験コーチングサービス。月額5万円〜。無料相談受付中。',
  keywords: '受験コーチング, 東大, 京大, 塾なし, 受験指導, オンライン家庭教師, 難関大学',
  openGraph: {
    title: '高級受験コーチング | 東大・京大合格者が直接教える',
    description: '塾なし東大現役合格 × 公立高校から京大合格。2人の実績者が完全オーダーメイドで指導。',
    type: 'website',
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  );
}
