# Game Hub

Python と pygame で作る、複数のミニゲームを遊べるアプリの雛形です。

## セットアップ

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 起動

```bash
python -m src.game_hub.main
```

## 操作

- メニュー: `1` または `2` でゲーム選択、`Esc` で終了
- Dodge Game: 矢印キーで移動、落ちてくるブロックを避ける
- Click Target: マウスクリックでターゲットを取る
- 各ゲーム中: `Esc` でメニューに戻る
# game
