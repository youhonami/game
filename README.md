# Game Hub

ブラウザで複数のミニゲームを遊べる Python 製のゲームハブです。`http.server` でローカルサーバーを起動し、各ゲームは HTML / CSS / JavaScript を Python から配信します。

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

起動後、ブラウザで `http://127.0.0.1:8000` を開きます。

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
- `/ranking` - ランキング
- `/contact` - お問い合わせ
- `/owner-login` - オーナーログイン

## 主な機能

- サイドバーから各ゲームへ遷移できます。
- テトリス、シューティング、ぷよぷよ、ブロック崩し、15パズル、マインスイーパーはランキング表示に対応しています。
- 15パズルは移動回数が少ない順でスコア登録できます。
- マインスイーパーは初級・中級・上級の難易度別にクリアタイムを登録できます。
- お問い合わせフォームからメッセージを送信でき、オーナーログイン後に確認・削除できます。
- オーナー画面では登録済みスコアの確認・削除ができます。

## ファイル構成

```text
src/game_hub/
  web_app.py          # ルーティング、問い合わせ、管理機能
  layout.py           # 共通CSSと共通レイアウト
  pages/              # 各ページ・各ゲームのHTML/JavaScript
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
    ranking.py
```

## 管理機能

オーナーログイン:

- URL: `http://127.0.0.1:8000/owner-login`
- アドレス: `admin@estra.jp`
- パスワード: `password`

ログイン後、スコア削除ページとメッセージ確認ページへ移動できます。

## 補足

`src/game_hub/main.py` には pygame 版の簡易メニューも残っていますが、現在の開発・確認はブラウザ版の `src.game_hub.web_app` が中心です。
