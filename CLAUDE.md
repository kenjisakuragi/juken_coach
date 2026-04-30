# JUKEN COACH プロジェクト ― Claude Code 制約事項

## API 使用禁止ルール

**このプロジェクト内で Claude Code 自身が ANTHROPIC_API_KEY を用いた API 呼び出しを行ってはならない。**

- `generate_sheet.py` や `content_pipeline.py` など、Anthropic SDK を内部で呼ぶスクリプトを Claude Code のセッション中に実行しないこと
- コンテンツ生成（台本・収録シート・マニュアル等）は Write ツールで直接ファイルに出力すること
- ユーザーが自分の環境で `ANTHROPIC_API_KEY` を設定してスクリプトを実行するのは問題ない

## コンテンツ出力のルール

- 台本・収録シート・設計書はすべて Write ツールで `radio/sheets/` または `radio/scripts/` に保存する
- 「書きます」と宣言した直後に必ず Write ツールを呼ぶこと。宣言だけでターンを終えない
