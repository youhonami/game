# Game Hub

ブラウザで複数のミニゲームを遊べる Python 製のゲームハブです。`http.server` ベースのローカルサーバーから、各ゲームの HTML / CSS / JavaScript を配信します。

## セットアップ

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 起動

ブラウザ版を起動します。

```bash
python -m src.game_hub.web_app
```

起動後、ブラウザで `http://127.0.0.1:8000` を開きます。デフォルトのホストとポートは `src/game_hub/web_app.py` の `HOST` / `PORT` で管理しています。

## 実装済みページ

- `/` - トップページ
- `/tetris` - テトリス
- `/shooting` - シューティング
- `/puyopuyo` - ぷよぷよ
- `/breakout` - ブロック崩し
- `/ludo` - ルドー
- `/trump` - トランプゲーム選択
- `/trump/old-maid` - ババ抜き
- `/trump/sevens` - 七並べ
- `/trump/memory` - 神経衰弱
- `/puzzle` - 15パズル
- `/minesweeper` - マインスイーパー
- `/uno` - UNO
- `/chat-room` - チャットルーム
- `/ranking` - ランキング
- `/contact` - お問い合わせ
- `/owner-login` - オーナーログイン

## 主な機能

- サイドバーから各ゲーム、ランキング、チャットルーム、お問い合わせへ遷移できます。
- テトリス、シューティング、ぷよぷよ、ブロック崩し、15パズル、マインスイーパーはランキング表示に対応しています。
- 15パズルはクリア時にモーダルでスコア登録でき、移動回数が少ない順、同点時はクリアタイムが短い順で表示します。
- マインスイーパーは初級・中級・上級の難易度を選択でき、難易度別にクリアタイムを登録・表示します。
- UNO は 2〜4 人で遊べ、CPU プレイヤーと対戦できます。山札と捨て札を中央に置き、プレイヤーを周囲に配置する UI です。
- チャットルームは投稿メッセージをサーバー側の JSON ファイルに保存し、誰でも閲覧できます。
- お問い合わせフォームからオーナーへメッセージを送信できます。
- テトリス、シューティング、ぷよぷよ、ブロック崩し、15パズルは縦スクロールなしで収まりやすいようにページ専用 CSS を調整しています。

## ランキング

ランキングはブラウザの `localStorage` に保存されます。`/ranking` では各ゲームのトップ 5 を表示します。

- テトリス、シューティング、ぷよぷよ、ブロック崩し: スコアが高い順
- 15パズル: 移動回数が少ない順、同点時はクリアタイムが短い順
- マインスイーパー: 難易度別にクリアタイムが短い順

## チャットと管理データ

サーバー側で永続化するデータは `src/game_hub/` 配下の JSON ファイルに保存されます。

- `contact_messages.json` - お問い合わせメッセージ
- `chat_room_messages.json` - チャットルームの投稿メッセージ

これらのファイルは投稿があると自動作成されます。

## ファイル構成

```text
src/game_hub/
  web_app.py                 # ルーティング、API、問い合わせ、管理機能
  layout.py                  # 共通CSS、サイドバー、共通レイアウト
  main.py                    # pygame版の簡易メニュー
  pages/                     # 各ページ・各ゲームのHTML/JavaScript
    home.py
    tetris.py
    shooting.py
    puyopuyo.py
    breakout.py
    ludo.py
    trump.py
    old_maid.py
    sevens.py
    memory.py
    puzzle.py
    minesweeper.py
    uno.py
    chat_room.py
    ranking.py
```

## 管理機能

オーナーログイン:

- URL: `http://127.0.0.1:8000/owner-login`
- アドレス: `admin@estra.jp`
- パスワード: `password`

ログイン後、以下の管理ページへ移動できます。

- `/owner-scores` - 登録済みスコアの確認・削除
- `/owner-messages` - お問い合わせメッセージの確認・削除
- `/owner-chat-messages` - チャットメッセージの確認・削除

## 補足

現在の開発・確認はブラウザ版の `src.game_hub.web_app` が中心です。`requirements.txt` には pygame 版で使用する `pygame` も含まれています。
