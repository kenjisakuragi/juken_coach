#!/usr/bin/env python3
"""
収録シート自動生成スクリプト
毎週月曜日に実行 → その週の収録シートをMarkdownで出力する
"""

import os
import sys
import anthropic
import click
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.panel import Panel

console = Console()

EPISODE_THEMES = {
    # シリーズA: 合格メソッド
    "A-01": "東大・京大に受かる人の勉強法、何が共通しているか",
    "A-02": "塾なし東大合格は再現可能か？私がやった勉強の全貌",
    "A-03": "浪人で伸びる人・伸びない人の決定的な違い",
    "A-04": "逆算思考と学習計画の立て方",
    "A-05": "暗記vs理解、どちらが正しいか？科目別に答える",
    "A-06": "模試・過去問の正しい使い方と間違った使い方",
    "A-07": "高1・高2の勉強は何をすべきか？",
    "A-08": "東大攻略・各科目別の勉強戦略",
    "A-09": "「勉強法本」は読む価値があるか？名著を検証する",
    "A-10": "睡眠・食事・運動と受験〜コンディション管理論",
    "A-11": "各科目への興味はどうやって見つけるか？",
    "A-12": "勉強が好きはいつからタスクになるのか？",
    # シリーズB: 教育答え合わせ音声版
    "B-01": "公文はやるべきか？難関大学合格者19人のデータで答える",
    "B-02": "親の「放任」の正体〜放任は無関心ではなかった",
    "B-03": "勉強覚醒はいつどこで起きるか？",
    "B-04": "素直さは最強の受験資質か？",
    "B-05": "地方出身者が東大京大に受かる条件",
    "B-06": "中高一貫出身者と公立出身者、大学でどう変わるか",
    "B-07": "読書習慣は高学歴と関係するか？",
    "B-08": "高学歴者の親はどんな人か？出身・職業・教育方針を分析",
    "B-09": "お金をかければ受かるは本当か？教育費の真実",
    "B-10": "逆転合格した人のパターン〜5浪東大理三の話",
    "B-11": "なぜ公立出身の親は子どもに中学受験をさせたがらないのか",
    "B-12": "受験失敗が後で活きたケース・活きなかったケース",
    # シリーズC: 受験戦略論
    "C-01": "小学受験・中学受験・高校受験、どれを選ぶべきか？",
    "C-02": "コスパで考える受験〜教育費と生涯年収の試算",
    "C-03": "有名進学校を徹底解説（灘・開成・聖光・西大和）",
    "C-04": "東大大学院という学歴ロンダリングの現実",
    "C-05": "学歴と就活の相関〜実際どれほど効くのか",
    "C-06": "塾の選び方・費用・使い方ガイド",
    "C-07": "塾で覚醒させる最適タイミングとは何か",
    # シリーズD: AI・現代教育論
    "D-01": "AI時代に学歴は意味があるか？本音で語る",
    "D-02": "ChatGPTで受験はどう変わるか？使い方と危険性",
    "D-03": "知的好奇心はどうやって育てるか？",
    "D-04": "地頭がいい以外に受験に必要な資質とは何か",
    "D-05": "学力は遺伝するのか？科学的に答える",
    # シリーズE: 人物・書籍特集
    "E-01": "山口真由の天才の勉強法を東大×京大視点で検証する",
    "E-02": "藤沢数希の学歴論・教育論を語る",
    "E-03": "受験必読書ランキング〜実際に役立った本を本音で評価",
    "E-04": "ドラゴン桜はどこまで正しいか？受験プロが検証",
    # シリーズF: メンタル・資質編
    "F-01": "受験とメンタル〜潰れる人・強くなる人の違い",
    "F-02": "子どものメンタルケアで親がやるべきこと",
    "F-03": "受験時代の思い出に闇がある人・ない人の差",
    "F-04": "好きを受験に活かす方法",
    "F-05": "受験で親子関係が壊れるとき〜距離感の取り方",
    "F-06": "浪人のメンタル管理〜からしかし自身の経験から",
}

SYSTEM_PROMPT = """あなたは「受験ラジオ by JUKEN COACH」の番組ディレクターです。
ホストは2人：
- コーチA：聖光学院→塾・予備校なし東大現役合格。得意：理系科目・逆算学習・自己管理
- からしかし：公立高校→一浪で京大合格。得意：メンタル管理・逆転戦略・文系科目。noteで「私の教育答え合わせ」を96本以上公開。

番組のトーン：知的・親しみやすい・本音・具体的エピソードあり・売り込まない
"""


def generate_recording_sheet(episode_id: str, theme: str, episode_num: int, record_date: str) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    prompt = f"""以下の条件で、ZOOMラジオ収録用の「収録シート」を作成してください。

エピソード番号: #{episode_num:03d}
テーマID: {episode_id}
テーマ: {theme}
収録予定日: {record_date}

以下の形式で出力してください：

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
受験ラジオ 収録シート
EP番号: #{episode_num:03d}  |  収録日: {record_date}  |  テーマ: {theme}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【オープニングフック（冒頭30秒で聴衆を掴む一言）】
（具体的な問いかけ・共感フレーズを1〜2文で）

【トーク流れ】

① 問題提起（2分）
   - リスナーが感じているであろう悩み・疑問を言語化

② コーチA視点（5分）
   - 東大受験・塾なし経験に関連するエピソード・気づき
   - 具体的な体験談のメモ（ふせんレベルでOK）

③ からしかし視点（5分）
   - 浪人経験・公立出身・教育答え合わせ取材経験からの知見
   - 具体的な体験談・取材事例

④ 対話・深掘りポイント（8分）
   - 2人で意見が分かれそうなポイント
   - 「なぜ？」「それって本当に？」と突っ込める箇所
   - リスナーが「そうそう！」と思いやすい視点

⑤ まとめ・リスナーへのアクション（3分）
   - 今日聞いたことを受けて、明日から何をするか
   - 1つの具体的なアクション提案

【受験相談コーナー Q案（2問）】
Q1: （このテーマに関連した、リスナーが持ちやすいリアルな質問）
回答メモ:

Q2: （保護者視点の質問）
回答メモ:

【キーワード・名言候補】
（SNS・note切り抜きに使えそうな名言・一言まとめを3つ）
1.
2.
3.

【関連する「私の教育答え合わせ」記事・エピソード事例】
（このテーマに関連しそうなnote記事のエピソードを2〜3個引用メモ）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
収録後チェック：
□ 冒頭フックは30秒以内に言えたか
□ お互いの話を遮らず引き出せたか
□ CTAはエンディングで読んだか
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


@click.command()
@click.argument("episode_id")
@click.option("--episode-num", "-n", default=1, help="エピソード通し番号")
@click.option("--date", "-d", default=None, help="収録予定日（YYYY-MM-DD）、省略時は来週水曜")
@click.option("--output-dir", "-o", default="sheets", help="出力ディレクトリ")
def main(episode_id: str, episode_num: int, date: str, output_dir: str):
    """
    収録シート自動生成

    EPISODE_ID: A-01〜G-06 のいずれか

    使用例:
        python generate_sheet.py A-02 -n 1
        python generate_sheet.py B-01 -n 6 -d 2024-10-16
    """
    if episode_id not in EPISODE_THEMES:
        console.print(f"[red]ERROR: {episode_id} は存在しません[/red]")
        console.print("利用可能なID: " + ", ".join(sorted(EPISODE_THEMES.keys())))
        sys.exit(1)

    if not os.environ.get("ANTHROPIC_API_KEY"):
        console.print("[red]ERROR: ANTHROPIC_API_KEY が未設定です[/red]")
        sys.exit(1)

    theme = EPISODE_THEMES[episode_id]
    record_date = date or "（収録日を記入）"

    console.print(
        Panel.fit(
            f"収録シート生成中...\n[gold1]EP#{episode_num:03d}[/gold1]  {theme}",
            border_style="yellow",
        )
    )

    sheet = generate_recording_sheet(episode_id, theme, episode_num, record_date)

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"ep{episode_num:03d}_{episode_id}_sheet.md"
    out_path.write_text(sheet, encoding="utf-8")

    console.print(f"\n[green]✓ 収録シートを生成しました:[/green] {out_path}")
    console.print("\n" + sheet)


if __name__ == "__main__":
    main()
