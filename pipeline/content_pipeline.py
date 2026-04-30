#!/usr/bin/env python3
"""
JUKEN COACH コンテンツ自動化パイプライン
ZOOM収録トランスクリプト → YouTube / Podcast / note / X(Twitter) / LINE 同時展開
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime

import anthropic
import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich import print as rprint

console = Console()

BRAND = {
    "show_name": "受験ラジオ by JUKEN COACH",
    "hosts": "コーチA（東大）× からしかし（京大）",
    "tagline": "塾なし東大現役合格 × 公立高校から京大合格",
    "cta": "無料相談はプロフィールリンクから → https://juken-coach.jp",
    "note_url": "https://note.com/karashikashi",
    "hashtags": "#受験 #大学受験 #東大 #京大 #受験コーチング #勉強法 #受験生",
}

SYSTEM_PROMPT = f"""あなたは「{BRAND['show_name']}」のコンテンツディレクターです。
番組の特徴：
- ホスト：{BRAND['hosts']}
- コンセプト：{BRAND['tagline']}
- ブランドトーン：知的・親しみやすい・具体的・エビデンスベース
- ターゲット：受験生（高1〜浪人）とその保護者

コンテンツは常に：
1. 具体的で実践可能なアドバイスを含む
2. コーチの実体験（東大・京大合格経験）に基づく権威性を示す
3. 読者/視聴者が「次のアクション」を取りたくなる構成にする
4. 高圧的な売り込みではなく、価値提供ファーストのトーン
"""


def get_client() -> anthropic.Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        console.print("[red]ERROR: ANTHROPIC_API_KEY が設定されていません[/red]")
        console.print("  export ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)
    return anthropic.Anthropic(api_key=api_key)


def generate_content(client: anthropic.Anthropic, platform: str, transcript: str, episode_num: int, topic: str) -> str:
    prompts = {
        "youtube": f"""以下の収録トランスクリプトをもとに、YouTubeの動画説明文を作成してください。

トランスクリプト:
{transcript}

出力フォーマット（日本語）：
1. タイトル（40字以内、検索キーワードを含む、数字や「〇〇する方法」形式）
2. 概要欄（冒頭150字は特に重要：何が学べるかを明確に）
3. タイムスタンプ（00:00 形式、最低5個）
4. ハッシュタグ（15個、受験関連）
5. 関連動画テキスト（視聴継続率を上げる誘導文）

エピソード番号: #{episode_num}
テーマ: {topic}
""",

        "podcast": f"""以下の収録トランスクリプトをもとに、Podcastのshow notesを作成してください。

トランスクリプト:
{transcript}

出力フォーマット（日本語）：
1. エピソードタイトル（60字以内）
2. 1行サマリー（ポッドキャストアプリで表示される）
3. エピソード概要（300字、SEOを意識）
4. 今回のポイント（箇条書き5〜7項目）
5. 本編で紹介した参考文献・ツール・書籍リスト
6. 次回予告（聴き続けてもらう引きを作る）
7. ホストプロフィール（固定テキスト）

エピソード番号: #{episode_num}
テーマ: {topic}
""",

        "note": f"""以下の収録トランスクリプトをもとに、noteの記事を作成してください。

トランスクリプト:
{transcript}

出力フォーマット（日本語）：
1. タイトル（32字以内、SEO・クリック率最適化）
2. リード文（200字、有料記事の場合でも無料で読める冒頭）
3. 見出し構成（H2 x 4〜5個の提案）
4. 本文（各H2セクション400〜600字、合計2000〜3000字）
   - 具体的な体験談を含める
   - 「なぜ多くの受験生が失敗するか」→「解決策」の構成
   - コーチの実体験エピソードを1〜2個挿入
5. まとめ（行動を促すCTA込み）
6. プロフィール + 無料相談への誘導

エピソード番号: #{episode_num}
テーマ: {topic}
""",

        "twitter": f"""以下の収録トランスクリプトをもとに、X(Twitter)への投稿文を5本作成してください。

トランスクリプト:
{transcript}

出力フォーマット（各140字以内）：
1. 【告知ポスト】動画/音声公開の告知（エンゲージメント最大化）
2. 【学びポスト】番組の核心的な気づきを1つ（保存・シェアされやすい）
3. 【スレッド冒頭】「3つのこと（1/4）」形式のスレッド開始文
4. 【問いかけポスト】フォロワーとのエンゲージメントを生む質問
5. 【エピソードリンク付き締め】週末の振り返り用まとめポスト

各ポストに適切なハッシュタグを含めること。
エピソード番号: #{episode_num}
テーマ: {topic}
""",

        "line": f"""以下の収録トランスクリプトをもとに、LINE公式アカウントへの配信メッセージを作成してください。

トランスクリプト:
{transcript}

出力フォーマット（日本語）：
1. タイトルメッセージ（30字以内、絵文字1個）
2. 本文メッセージ（200字以内、改行多め・読みやすく）
3. アクションボタン用テキスト（「動画を見る」「音声を聴く」「記事を読む」の3つ）
4. 配信タイミング推奨（曜日・時間帯）

エピソード番号: #{episode_num}
テーマ: {topic}
""",
    }

    prompt = prompts.get(platform)
    if not prompt:
        raise ValueError(f"Unknown platform: {platform}")

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text


def save_outputs(outputs: dict, episode_num: int, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for platform, content in outputs.items():
        filename = output_dir / f"ep{episode_num:03d}_{platform}_{timestamp}.txt"
        filename.write_text(content, encoding="utf-8")

    bundle_path = output_dir / f"ep{episode_num:03d}_bundle_{timestamp}.json"
    bundle_path.write_text(
        json.dumps(
            {
                "episode": episode_num,
                "timestamp": timestamp,
                "brand": BRAND,
                "outputs": outputs,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return bundle_path


@click.command()
@click.argument("transcript_file", type=click.Path(exists=True))
@click.option("--episode", "-e", default=1, help="エピソード番号")
@click.option("--topic", "-t", default="受験攻略", help="エピソードのテーマ")
@click.option(
    "--platforms",
    "-p",
    default="youtube,podcast,note,twitter,line",
    help="生成するプラットフォーム（カンマ区切り）",
)
@click.option("--output-dir", "-o", default="output", help="出力ディレクトリ")
def main(transcript_file: str, episode: int, topic: str, platforms: str, output_dir: str):
    """
    JUKEN COACH コンテンツ自動化パイプライン

    TRANSCRIPT_FILE: トランスクリプトファイル（.txt）のパス

    使用例:
        python content_pipeline.py transcript.txt -e 1 -t "東大塾なし合格の秘密"
    """
    console.print(
        Panel.fit(
            f"[gold1]JUKEN COACH[/gold1] コンテンツ自動化パイプライン\n"
            f"エピソード #{episode} | テーマ: {topic}",
            border_style="yellow",
        )
    )

    transcript = Path(transcript_file).read_text(encoding="utf-8")
    console.print(f"[dim]トランスクリプト読み込み完了: {len(transcript)}文字[/dim]")

    target_platforms = [p.strip() for p in platforms.split(",")]

    client = get_client()
    outputs = {}

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        for platform in target_platforms:
            task = progress.add_task(f"[yellow]{platform}[/yellow] コンテンツ生成中...", total=None)
            try:
                outputs[platform] = generate_content(client, platform, transcript, episode, topic)
                progress.update(task, description=f"[green]✓ {platform}[/green] 完了")
            except Exception as e:
                progress.update(task, description=f"[red]✗ {platform}[/red] エラー: {e}")
                console.print(f"[red]{platform} エラー詳細: {e}[/red]")

    bundle_path = save_outputs(outputs, episode, Path(output_dir))

    table = Table(title="生成完了", border_style="yellow")
    table.add_column("プラットフォーム", style="cyan")
    table.add_column("文字数", justify="right")
    table.add_column("ステータス", justify="center")

    for platform, content in outputs.items():
        table.add_row(platform, str(len(content)), "[green]✓[/green]")

    console.print(table)
    console.print(f"\n[dim]バンドルファイル: {bundle_path}[/dim]")
    console.print("\n[gold1]全プラットフォームへの展開準備が完了しました。[/gold1]")


if __name__ == "__main__":
    main()
