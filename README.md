# Game Hub

Python と pygame で作る、複数のミニゲームを遊べるアプリの雛形です。

## セットアップ

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 起動

ブラウザで確認する場合:

```bash
python -m src.game_hub.web_app
```

その後、ブラウザで `http://127.0.0.1:8000` を開きます。

ページ:

- `http://127.0.0.1:8000/tetris`
- `http://127.0.0.1:8000/shooting`
- `http://127.0.0.1:8000/puyopuyo`
- `http://127.0.0.1:8000/ranking`
- `http://127.0.0.1:8000/owner-login`

pygame のウィンドウで確認する場合:

```bash
python -m src.game_hub.main
```

## 操作

- トップページ: サイドバーの各項目をクリック
- キーボード操作: `1` でテトリス、`2` でシューティング、`Esc` で終了
- 準備中画面: `Esc` でトップページに戻る
