# content_pipeline.py 使い方マニュアル

収録1本 → YouTube / Podcast / note / X(Twitter) / LINE の5媒体コンテンツを自動生成する手順です。

---

## 事前準備（初回のみ）

### 1. Python パッケージのインストール

```bash
cd juken_coach/pipeline
pip install -r requirements.txt
```

requirements.txt の内容：
```
anthropic>=0.40.0
python-dotenv>=1.0.0
click>=8.1.7
rich>=13.7.0
```

### 2. Anthropic API キーの取得と設定

1. https://console.anthropic.com にアクセス
2. 「API Keys」→「Create Key」でキーを発行（`sk-ant-...` という形式）
3. 以下のいずれかの方法で設定する

**方法A：毎回ターミナルで設定（簡単）**
```bash
export ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
```

**方法B：.env ファイルに保存（推奨）**
```bash
# pipeline/.env ファイルを作成
echo "ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx" > .env
```

> `.env` ファイルは絶対に Git にコミットしないこと。`.gitignore` に追加済み。

---

## 収録後の手順（毎回）

### STEP 1：トランスクリプトを .txt ファイルとして保存

ZOOMの文字起こしを取得する方法は2通り：

**方法A：ZOOM自動文字起こし**
1. ZOOM > 設定 > 「クラウドレコーディング」をオン
2. 「オーディオトランスクリプト」をオン
3. 収録後、ZOOMポータル（zoom.us）の「レコーディング」から `.vtt` または `.txt` をダウンロード
4. `.vtt` の場合はタイムスタンプ行を削除してテキストだけにする

**方法B：手動で書き起こし**
- `pipeline/templates/sample_transcript.txt` の形式を参考にテキストを作成

保存場所の例：
```
pipeline/transcripts/ep001_transcript.txt
```

---

### STEP 2：スクリプトを実行

```bash
cd juken_coach/pipeline

python content_pipeline.py transcripts/ep001_transcript.txt \
  --episode 1 \
  --topic "東大京大に受かる方法" \
  --output-dir output/ep001
```

**オプション一覧：**

| オプション | 短縮形 | 説明 | 例 |
|---|---|---|---|
| `--episode` | `-e` | エピソード番号 | `-e 1` |
| `--topic` | `-t` | テーマ（タイトルに使用） | `-t "東大京大に受かる方法"` |
| `--platforms` | `-p` | 生成する媒体（カンマ区切り） | `-p youtube,note` |
| `--output-dir` | `-o` | 出力先ディレクトリ | `-o output/ep001` |

**特定の媒体だけ生成したい場合：**
```bash
# YouTubeとnoteだけ
python content_pipeline.py transcripts/ep001_transcript.txt \
  -e 1 -t "東大京大に受かる方法" \
  -p youtube,note
```

---

### STEP 3：生成ファイルを確認

実行後、`output/ep001/` に以下のファイルが生成されます：

```
output/ep001/
├── ep001_youtube_20260507_143022.txt    ← YouTubeタイトル・概要欄・タイムスタンプ
├── ep001_podcast_20260507_143022.txt    ← Podcastショーノート
├── ep001_note_20260507_143022.txt       ← note記事本文
├── ep001_twitter_20260507_143022.txt    ← Xポスト×5本
├── ep001_line_20260507_143022.txt       ← LINE配信メッセージ
└── ep001_bundle_20260507_143022.json    ← 全媒体まとめ（バックアップ用）
```

---

### STEP 4：各プラットフォームに投稿

#### YouTube
1. `ep001_youtube_*.txt` を開く
2. **タイトル**をコピーして YouTube Studio の「タイトル」欄に貼り付け
3. **概要欄テキスト**をコピーして「説明」欄に貼り付け
4. **タイムスタンプ**は概要欄の末尾に追加
5. **ハッシュタグ**はタグ欄またはタイトルの末尾に追加

#### Podcast（Spotify for Podcasters / Anchor）
1. `ep001_podcast_*.txt` を開く
2. **エピソードタイトル**と**エピソード概要**をそれぞれ貼り付け
3. 音声ファイル（ZOOM録音の .m4a）をアップロード

#### note
1. `ep001_note_*.txt` を開く
2. note の「新しい記事を書く」から記事を作成
3. 生成された**タイトル**・**本文**を貼り付け
4. 必要に応じてサムネイル画像を設定

#### X（Twitter）
1. `ep001_twitter_*.txt` を開く
2. 5本のポストが生成されているので、スケジュール投稿ツール（Buffer / Hootsuite）に設定
3. 推奨投稿タイミング：
   - 公開日当日 朝8時（告知ポスト）
   - 公開日当日 夜21時（学びポスト）
   - 翌日 朝8時（スレッド）
   - 3日後 夜21時（問いかけポスト）
   - 1週間後 土曜朝（まとめポスト）

#### LINE公式
1. `ep001_line_*.txt` を開く
2. LINE Official Account Manager にログイン
3. 「メッセージ配信」→「メッセージを作成」
4. タイトルと本文を貼り付け、アクションボタンに各プラットフォームのURLを設定
5. 推奨配信タイミング：公開日の夜20時

---

## 週次の運用フロー（まとめ）

```
水曜：ZOOM収録（40〜50分）
      ↓
水曜夜：ZOOMポータルからトランスクリプトをダウンロード
      ↓
木曜朝：python content_pipeline.py を実行（約5分）
      ↓
木曜：YouTube・Podcast に音声と概要欄をアップロード
      ↓
木曜：note 記事を公開（または予約投稿）
      ↓
木曜：X ポストをスケジュール設定
      ↓
木曜：LINE配信を予約（金曜夜 or 土曜朝）
```

**1本の収録から全媒体展開までの作業時間：約30分**

---

## よくあるエラーと対処法

| エラー | 原因 | 対処 |
|---|---|---|
| `ANTHROPIC_API_KEY が設定されていません` | 環境変数が未設定 | `export ANTHROPIC_API_KEY=sk-ant-...` を実行 |
| `No such file or directory` | トランスクリプトファイルのパスが間違っている | ファイルパスをフルパスで指定する |
| `ModuleNotFoundError: anthropic` | パッケージ未インストール | `pip install -r requirements.txt` を実行 |
| 生成内容が短すぎる | トランスクリプトが短い | 収録が15分以上あることを確認 |
| 文字化け | ファイルのエンコーディング問題 | トランスクリプトを UTF-8 で保存し直す |
