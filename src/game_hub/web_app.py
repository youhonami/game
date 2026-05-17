import hmac
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


HOST = "127.0.0.1"
PORT = 8000
OWNER_ADDRESS = "admin@estra.jp"
OWNER_PASSWORD = "password"
BACKGROUND_IMAGE_PATH = Path(
    "/Users/honamiyuusuke/.cursor/projects/"
    "Users-honamiyuusuke-coachtech-game/assets/"
    "_______-5e35f2db-48bd-48a4-ae7b-476c8cda2f70.png"
)


STYLE = """
    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      min-height: 100vh;
      color: #f5f7fb;
      font-family: -apple-system, BlinkMacSystemFont, "Hiragino Sans", "Yu Gothic", sans-serif;
      background: #021329 url("/assets/background.png") center / cover no-repeat fixed;
    }

    .page {
      display: flex;
      min-height: 100vh;
      background: linear-gradient(90deg, rgba(0, 10, 25, 0.88), rgba(0, 32, 68, 0.28));
    }

    .sidebar {
      display: flex;
      flex-direction: column;
      width: 280px;
      min-height: 100vh;
      padding: 42px 28px;
      background: rgba(4, 18, 36, 0.88);
      border-right: 2px solid rgba(120, 225, 255, 0.45);
      box-shadow: 12px 0 36px rgba(0, 0, 0, 0.32);
    }

    .sidebar h1 {
      margin: 0 0 44px;
      font-size: 28px;
      letter-spacing: 0.05em;
    }

    .sidebar h1 a {
      color: inherit;
      text-decoration: none;
    }

    .menu {
      display: grid;
      gap: 18px;
    }

    .sidebar-footer {
      margin-top: auto;
      padding-top: 32px;
    }

    .menu a {
      display: block;
      padding: 18px 20px;
      color: #ffffff;
      text-decoration: none;
      font-size: 22px;
      font-weight: 700;
      background: rgba(14, 90, 140, 0.72);
      border: 1px solid rgba(150, 235, 255, 0.78);
      border-radius: 16px;
      transition: transform 0.18s ease, background 0.18s ease;
    }

    .menu a:hover,
    .menu a.active {
      transform: translateX(6px);
      background: rgba(28, 150, 205, 0.86);
    }

    main {
      display: grid;
      flex: 1;
      place-items: center;
      padding: 48px;
      text-align: center;
    }

    .hero {
      min-width: min(680px, 100%);
      padding: 44px 56px;
      border: 1px solid rgba(160, 235, 255, 0.28);
      border-radius: 28px;
      background: rgba(2, 22, 48, 0.44);
      backdrop-filter: blur(4px);
    }

    .hero h2 {
      margin: 0 0 18px;
      font-size: clamp(44px, 7vw, 78px);
      text-shadow: 0 8px 28px rgba(0, 0, 0, 0.45);
    }

    .hero p {
      margin: 0;
      color: #9feaff;
      font-size: 24px;
      font-weight: 700;
    }

    .login-form {
      display: grid;
      gap: 18px;
      margin: 30px auto 0;
      max-width: 420px;
      text-align: left;
    }

    .login-form label {
      display: grid;
      gap: 8px;
      color: #d8f7ff;
      font-size: 16px;
      font-weight: 700;
    }

    .login-form input {
      width: 100%;
      padding: 14px 16px;
      color: #ffffff;
      font-size: 18px;
      background: rgba(0, 18, 40, 0.72);
      border: 1px solid rgba(150, 235, 255, 0.78);
      border-radius: 12px;
      outline: none;
    }

    .login-form input:focus {
      border-color: #ffffff;
      box-shadow: 0 0 0 3px rgba(120, 225, 255, 0.22);
    }

    .login-form button {
      margin-top: 8px;
      padding: 15px 18px;
      color: #ffffff;
      font-size: 18px;
      font-weight: 700;
      cursor: pointer;
      background: rgba(28, 150, 205, 0.9);
      border: 1px solid rgba(190, 245, 255, 0.9);
      border-radius: 14px;
    }

    .helper-text {
      margin-top: 20px;
      color: #9feaff;
      font-size: 16px;
      font-weight: 700;
    }

    .error-message {
      margin: 24px auto 0;
      max-width: 420px;
      padding: 12px 14px;
      color: #ffffff;
      font-size: 15px;
      font-weight: 700;
      background: rgba(210, 60, 80, 0.82);
      border: 1px solid rgba(255, 190, 200, 0.9);
      border-radius: 12px;
    }

    .game-panel {
      display: grid;
      grid-template-columns: auto 220px;
      gap: 28px;
      align-items: start;
      margin-top: 28px;
    }

    .game-board {
      width: 300px;
      height: 600px;
      background: rgba(0, 12, 28, 0.86);
      border: 2px solid rgba(150, 235, 255, 0.85);
      border-radius: 14px;
      box-shadow: 0 18px 38px rgba(0, 0, 0, 0.35);
    }

    .puyo-board {
      width: 240px;
      height: 480px;
    }

    .game-info {
      display: grid;
      gap: 14px;
      text-align: left;
    }

    .info-card {
      padding: 18px;
      background: rgba(0, 18, 40, 0.68);
      border: 1px solid rgba(150, 235, 255, 0.5);
      border-radius: 16px;
    }

    .info-card h3 {
      margin: 0 0 10px;
      color: #9feaff;
      font-size: 18px;
    }

    .info-card p,
    .info-card ul {
      margin: 0;
      color: #ffffff;
      font-size: 15px;
      line-height: 1.7;
    }

    .info-card ul {
      padding-left: 18px;
    }

    .primary-button {
      width: 100%;
      padding: 14px 16px;
      color: #ffffff;
      font-size: 17px;
      font-weight: 700;
      cursor: pointer;
      background: rgba(28, 150, 205, 0.9);
      border: 1px solid rgba(190, 245, 255, 0.9);
      border-radius: 14px;
    }

    .game-over-overlay {
      position: fixed;
      inset: 0;
      display: grid;
      place-items: center;
      padding: 24px;
      background: rgba(0, 8, 20, 0.72);
      z-index: 20;
    }

    .game-over-overlay[hidden] {
      display: none;
    }

    .game-over-dialog {
      width: min(430px, 100%);
      padding: 34px;
      text-align: center;
      background: rgba(3, 24, 52, 0.96);
      border: 1px solid rgba(150, 235, 255, 0.86);
      border-radius: 24px;
      box-shadow: 0 24px 70px rgba(0, 0, 0, 0.52);
    }

    .game-over-dialog h3 {
      margin: 0 0 14px;
      font-size: 34px;
    }

    .game-over-score {
      margin: 0 0 22px;
      color: #9feaff;
      font-size: 24px;
      font-weight: 700;
    }

    .score-name-form {
      display: grid;
      gap: 14px;
    }

    .score-name-form label {
      display: grid;
      gap: 8px;
      color: #d8f7ff;
      font-weight: 700;
      text-align: left;
    }

    .score-name-form input {
      width: 100%;
      padding: 14px 16px;
      color: #ffffff;
      font-size: 24px;
      font-weight: 700;
      letter-spacing: 0.3em;
      text-align: center;
      text-transform: uppercase;
      background: rgba(0, 18, 40, 0.78);
      border: 1px solid rgba(150, 235, 255, 0.78);
      border-radius: 12px;
      outline: none;
    }

    .score-save-message {
      min-height: 24px;
      margin: 0;
      color: #9feaff;
      font-size: 15px;
      font-weight: 700;
    }

    .ranking-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(190px, 1fr));
      gap: 18px;
      margin-top: 30px;
      text-align: left;
    }

    .ranking-card {
      padding: 20px;
      background: rgba(0, 18, 40, 0.68);
      border: 1px solid rgba(150, 235, 255, 0.5);
      border-radius: 18px;
    }

    .ranking-card h3 {
      margin: 0 0 14px;
      color: #9feaff;
      font-size: 22px;
      text-align: center;
    }

    .ranking-list {
      display: grid;
      gap: 10px;
      margin: 0;
      padding: 0;
      list-style: none;
    }

    .ranking-list li {
      display: grid;
      grid-template-columns: 32px 1fr auto;
      gap: 10px;
      align-items: center;
      padding: 10px 12px;
      color: #ffffff;
      font-size: 15px;
      font-weight: 700;
      background: rgba(4, 32, 64, 0.78);
      border: 1px solid rgba(150, 235, 255, 0.28);
      border-radius: 12px;
    }

    .ranking-empty {
      margin: 0;
      color: #d8f7ff;
      font-size: 15px;
      line-height: 1.7;
      text-align: center;
    }

    .back-link {
      display: inline-block;
      margin-top: 28px;
      color: #ffffff;
      font-weight: 700;
      text-decoration: none;
      border-bottom: 1px solid rgba(255, 255, 255, 0.7);
    }
"""


def render_page(
    title: str,
    heading: str,
    message: str = "",
    active_page: str = "",
    body_html: str | None = None,
) -> str:
    tetris_class = "active" if active_page == "tetris" else ""
    shooting_class = "active" if active_page == "shooting" else ""
    puyopuyo_class = "active" if active_page == "puyopuyo" else ""
    breakout_class = "active" if active_page == "breakout" else ""
    ranking_class = "active" if active_page == "ranking" else ""
    owner_login_class = "active" if active_page == "owner-login" else ""
    back_link = "" if not active_page else '<a class="back-link" href="/">トップページに戻る</a>'
    body = body_html if body_html is not None else f"<p>{message}</p>"

    return f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
{STYLE}
  </style>
</head>
<body>
  <div class="page">
    <aside class="sidebar">
      <h1><a href="/">Game Menu</a></h1>
      <nav class="menu" aria-label="ゲームメニュー">
        <a class="{tetris_class}" href="/tetris">テトリス</a>
        <a class="{shooting_class}" href="/shooting">シューティング</a>
        <a class="{puyopuyo_class}" href="/puyopuyo">ぷよぷよ</a>
        <a class="{breakout_class}" href="/breakout">ブロック崩し</a>
        <a class="{ranking_class}" href="/ranking">ランキング</a>
      </nav>
      <nav class="menu sidebar-footer" aria-label="オーナーメニュー">
        <a class="{owner_login_class}" href="/owner-login">オーナーログイン</a>
      </nav>
    </aside>
    <main>
      <section class="hero">
        <h2>{heading}</h2>
        {body}
        {back_link}
      </section>
    </main>
  </div>
</body>
</html>
"""


HOME_HTML = render_page(
    title="Ocean Game Hub",
    heading="Ocean Game Hub",
    message="サイドバーからゲームを選択",
)
TETRIS_HTML = render_page(
    title="テトリス | Ocean Game Hub",
    heading="テトリス",
    active_page="tetris",
    body_html="""<p>ラインをそろえてスコアを伸ばしましょう</p>
        <div class="game-panel">
          <canvas class="game-board" id="tetris-board" width="300" height="600"></canvas>
          <aside class="game-info">
            <div class="info-card">
              <h3>スコア</h3>
              <p id="tetris-score">0</p>
            </div>
            <div class="info-card">
              <h3>操作</h3>
              <ul>
                <li>← →: 移動</li>
                <li>↓: 早く落とす</li>
                <li>Space: 回転</li>
                <li>↑: 一気に落とす</li>
                <li>P: 一時停止</li>
              </ul>
            </div>
            <div class="info-card">
              <h3>状態</h3>
              <p id="tetris-status">スタート待ち</p>
            </div>
            <button class="primary-button" id="tetris-restart" type="button">スタート</button>
            <div class="info-card">
              <h3>ハイスコア</h3>
              <p><span id="tetris-high-score">0</span> / <span id="tetris-high-score-name">---</span></p>
            </div>
          </aside>
        </div>
        <div class="game-over-overlay" id="tetris-game-over" hidden>
          <div class="game-over-dialog" role="dialog" aria-modal="true" aria-labelledby="game-over-title">
            <h3 id="game-over-title">ゲームオーバー</h3>
            <p class="game-over-score">達成スコア: <span id="tetris-final-score">0</span></p>
            <form class="score-name-form" id="tetris-score-form">
              <label>
                プレイヤー名（3文字）
                <input id="tetris-player-name" name="player-name" maxlength="3" autocomplete="off" required>
              </label>
              <button class="primary-button" type="submit">登録</button>
              <p class="score-save-message" id="tetris-score-save-message"></p>
              <button class="primary-button" id="tetris-play-again" type="button">もう一度遊ぶ</button>
            </form>
          </div>
        </div>
        <script>
          const canvas = document.getElementById("tetris-board");
          const context = canvas.getContext("2d");
          const scoreElement = document.getElementById("tetris-score");
          const highScoreElement = document.getElementById("tetris-high-score");
          const highScoreNameElement = document.getElementById("tetris-high-score-name");
          const statusElement = document.getElementById("tetris-status");
          const restartButton = document.getElementById("tetris-restart");
          const gameOverOverlay = document.getElementById("tetris-game-over");
          const finalScoreElement = document.getElementById("tetris-final-score");
          const scoreForm = document.getElementById("tetris-score-form");
          const playerNameInput = document.getElementById("tetris-player-name");
          const scoreSaveMessage = document.getElementById("tetris-score-save-message");
          const playAgainButton = document.getElementById("tetris-play-again");

          const highScoreKey = "gameHubTetrisHighScore";
          const highScoreNameKey = "gameHubTetrisHighScoreName";
          const rankingKey = "gameHubTetrisRanking";
          const columns = 10;
          const rows = 20;
          const blockSize = 30;
          const baseDropInterval = 800;
          const minDropInterval = 120;
          const speedUpScoreStep = 500;
          const dropIntervalStep = 100;
          const colors = {
            I: "#60e7ff",
            J: "#5c8cff",
            L: "#ffb347",
            O: "#ffe45c",
            S: "#5cff9d",
            T: "#c77dff",
            Z: "#ff5c7a",
          };
          const shapes = {
            I: [[1, 1, 1, 1]],
            J: [[1, 0, 0], [1, 1, 1]],
            L: [[0, 0, 1], [1, 1, 1]],
            O: [[1, 1], [1, 1]],
            S: [[0, 1, 1], [1, 1, 0]],
            T: [[0, 1, 0], [1, 1, 1]],
            Z: [[1, 1, 0], [0, 1, 1]],
          };

          let board;
          let piece;
          let score;
          let highScore;
          let highScoreName;
          let dropCounter;
          let dropInterval;
          let lastTime;
          let hasStarted;
          let isPaused;
          let isGameOver;

          function createBoard() {
            return Array.from({ length: rows }, () => Array(columns).fill(""));
          }

          function createPiece() {
            const names = Object.keys(shapes);
            const name = names[Math.floor(Math.random() * names.length)];
            const matrix = shapes[name].map((row) => [...row]);
            return {
              name,
              matrix,
              x: Math.floor(columns / 2) - Math.ceil(matrix[0].length / 2),
              y: 0,
            };
          }

          function rotate(matrix) {
            return matrix[0].map((_, index) => matrix.map((row) => row[index]).reverse());
          }

          function hasCollision(target = piece) {
            return target.matrix.some((row, y) =>
              row.some((cell, x) => {
                if (!cell) {
                  return false;
                }
                const nextX = target.x + x;
                const nextY = target.y + y;
                return (
                  nextX < 0 ||
                  nextX >= columns ||
                  nextY >= rows ||
                  (nextY >= 0 && board[nextY][nextX])
                );
              })
            );
          }

          function mergePiece() {
            piece.matrix.forEach((row, y) => {
              row.forEach((cell, x) => {
                if (cell && piece.y + y >= 0) {
                  board[piece.y + y][piece.x + x] = piece.name;
                }
              });
            });
          }

          function clearLines() {
            let cleared = 0;
            for (let y = rows - 1; y >= 0; y -= 1) {
              if (board[y].every(Boolean)) {
                board.splice(y, 1);
                board.unshift(Array(columns).fill(""));
                cleared += 1;
                y += 1;
              }
            }

            if (cleared > 0) {
              score += [0, 100, 250, 380, 500][cleared];
              scoreElement.textContent = score;
              updateHighScore();
              updateDropSpeed();
            }
          }

          function updateDropSpeed() {
            const speedLevel = Math.floor(score / speedUpScoreStep);
            dropInterval = Math.max(
              minDropInterval,
              baseDropInterval - speedLevel * dropIntervalStep,
            );
          }

          function movePiece(offsetX) {
            piece.x += offsetX;
            if (hasCollision()) {
              piece.x -= offsetX;
            }
          }

          function dropPiece() {
            piece.y += 1;
            if (hasCollision()) {
              piece.y -= 1;
              mergePiece();
              clearLines();
              piece = createPiece();
              if (hasCollision()) {
                isGameOver = true;
                statusElement.textContent = "ゲームオーバー";
                updateHighScore();
                showGameOverDialog();
              }
            }
            dropCounter = 0;
          }

          function updateHighScore() {
            if (score <= highScore) {
              return;
            }

            highScore = score;
            highScoreName = "";
            highScoreElement.textContent = highScore;
            highScoreNameElement.textContent = "登録待ち";
            localStorage.setItem(highScoreKey, String(highScore));
            localStorage.removeItem(highScoreNameKey);
          }

          function showGameOverDialog() {
            finalScoreElement.textContent = score;
            scoreSaveMessage.textContent = "";
            playerNameInput.value = "";
            gameOverOverlay.hidden = false;
            playerNameInput.focus();
          }

          function hideGameOverDialog() {
            gameOverOverlay.hidden = true;
          }

          function saveScoreEntry(playerName) {
            const ranking = JSON.parse(localStorage.getItem(rankingKey) || "[]");
            ranking.push({
              name: playerName,
              score,
              playedAt: new Date().toISOString(),
            });
            ranking.sort((left, right) => right.score - left.score);
            localStorage.setItem(rankingKey, JSON.stringify(ranking.slice(0, 50)));

            if (score >= highScore && score > 0) {
              highScore = score;
              highScoreName = playerName;
              highScoreElement.textContent = highScore;
              highScoreNameElement.textContent = highScoreName;
              localStorage.setItem(highScoreKey, String(highScore));
              localStorage.setItem(highScoreNameKey, highScoreName);
            }
          }

          function findHighScoreName(targetScore) {
            const ranking = JSON.parse(localStorage.getItem(rankingKey) || "[]");
            const matchedEntry = ranking.find((entry) => entry.score === targetScore);
            return matchedEntry ? matchedEntry.name : "";
          }

          function rotatePiece() {
            const originalMatrix = piece.matrix;
            const originalX = piece.x;
            piece.matrix = rotate(piece.matrix);

            for (const offset of [0, -1, 1, -2, 2]) {
              piece.x = originalX + offset;
              if (!hasCollision()) {
                return;
              }
            }

            piece.matrix = originalMatrix;
            piece.x = originalX;
          }

          function hardDrop() {
            while (!hasCollision({ ...piece, y: piece.y + 1 })) {
              piece.y += 1;
            }
            dropPiece();
          }

          function drawCell(x, y, color) {
            context.fillStyle = color;
            context.fillRect(x * blockSize, y * blockSize, blockSize, blockSize);
            context.strokeStyle = "rgba(255, 255, 255, 0.18)";
            context.lineWidth = 2;
            context.strokeRect(x * blockSize + 1, y * blockSize + 1, blockSize - 2, blockSize - 2);
          }

          function draw() {
            context.fillStyle = "rgba(0, 12, 28, 0.96)";
            context.fillRect(0, 0, canvas.width, canvas.height);

            board.forEach((row, y) => {
              row.forEach((cell, x) => {
                if (cell) {
                  drawCell(x, y, colors[cell]);
                }
              });
            });

            if (piece) {
              piece.matrix.forEach((row, y) => {
                row.forEach((cell, x) => {
                  if (cell) {
                    drawCell(piece.x + x, piece.y + y, colors[piece.name]);
                  }
                });
              });
            }
          }

          function update(time = 0) {
            const deltaTime = time - lastTime;
            lastTime = time;

            if (hasStarted && !isPaused && !isGameOver) {
              dropCounter += deltaTime;
              if (dropCounter > dropInterval) {
                dropPiece();
              }
            }

            draw();
            requestAnimationFrame(update);
          }

          function startGame() {
            board = createBoard();
            piece = createPiece();
            score = 0;
            dropCounter = 0;
            dropInterval = baseDropInterval;
            lastTime = 0;
            hasStarted = true;
            isPaused = false;
            isGameOver = false;
            scoreElement.textContent = score;
            statusElement.textContent = "プレイ中";
            restartButton.textContent = "リスタート";
            hideGameOverDialog();
          }

          document.addEventListener("keydown", (event) => {
            if (event.target.closest("#tetris-game-over")) {
              return;
            }

            if (!hasStarted) {
              if (event.key === "Enter") {
                startGame();
              }
              return;
            }

            if (isGameOver) {
              return;
            }

            if (event.key === "p" || event.key === "P") {
              isPaused = !isPaused;
              statusElement.textContent = isPaused ? "一時停止中" : "プレイ中";
              return;
            }

            if (isPaused) {
              return;
            }

            if (event.key === "ArrowLeft") {
              movePiece(-1);
              event.preventDefault();
            } else if (event.key === "ArrowRight") {
              movePiece(1);
              event.preventDefault();
            } else if (event.key === "ArrowDown") {
              dropPiece();
              event.preventDefault();
            } else if (event.key === "ArrowUp") {
              hardDrop();
              event.preventDefault();
            } else if (event.code === "Space") {
              rotatePiece();
              event.preventDefault();
            } else if (event.key === "Enter") {
              startGame();
            }
          });

          restartButton.addEventListener("click", startGame);
          playAgainButton.addEventListener("click", startGame);
          playerNameInput.addEventListener("input", () => {
            playerNameInput.value = playerNameInput.value.slice(0, 3).toUpperCase();
          });
          scoreForm.addEventListener("submit", (event) => {
            event.preventDefault();
            const playerName = playerNameInput.value.trim().toUpperCase();
            if (!playerName) {
              scoreSaveMessage.textContent = "名前を入力してください";
              return;
            }

            saveScoreEntry(playerName);
            scoreSaveMessage.textContent = "スコアを登録しました";
          });

          board = createBoard();
          piece = null;
          score = 0;
          highScore = Number(localStorage.getItem(highScoreKey) || 0);
          highScoreName = localStorage.getItem(highScoreNameKey) || findHighScoreName(highScore);
          dropCounter = 0;
          dropInterval = baseDropInterval;
          lastTime = 0;
          hasStarted = false;
          isPaused = false;
          isGameOver = false;
          scoreElement.textContent = score;
          highScoreElement.textContent = highScore;
          highScoreNameElement.textContent = highScoreName || (highScore > 0 ? "登録待ち" : "---");
          draw();
          update();
        </script>""",
)
SHOOTING_HTML = render_page(
    title="シューティング | Ocean Game Hub",
    heading="シューティング",
    message="このページの内容は後で作成します",
    active_page="shooting",
)
PUYOPUYO_HTML = render_page(
    title="ぷよぷよ | Ocean Game Hub",
    heading="ぷよぷよ",
    active_page="puyopuyo",
    body_html="""<p>同じ色を4つ以上つなげて消しましょう</p>
        <div class="game-panel">
          <canvas class="game-board puyo-board" id="puyo-board" width="240" height="480"></canvas>
          <aside class="game-info">
            <div class="info-card">
              <h3>スコア</h3>
              <p id="puyo-score">0</p>
              <p id="puyo-chain">0連鎖</p>
            </div>
            <div class="info-card">
              <h3>操作</h3>
              <ul>
                <li>← →: 移動</li>
                <li>↓: 早く落とす</li>
                <li>Space: 回転</li>
                <li>↑: 一気に落とす</li>
                <li>P: 一時停止</li>
              </ul>
            </div>
            <div class="info-card">
              <h3>状態</h3>
              <p id="puyo-status">スタート待ち</p>
            </div>
            <button class="primary-button" id="puyo-restart" type="button">スタート</button>
            <div class="info-card">
              <h3>ハイスコア</h3>
              <p><span id="puyo-high-score">0</span> / <span id="puyo-high-score-name">---</span></p>
            </div>
          </aside>
        </div>
        <div class="game-over-overlay" id="puyo-game-over" hidden>
          <div class="game-over-dialog" role="dialog" aria-modal="true" aria-labelledby="puyo-game-over-title">
            <h3 id="puyo-game-over-title">ゲームオーバー</h3>
            <p class="game-over-score">達成スコア: <span id="puyo-final-score">0</span></p>
            <form class="score-name-form" id="puyo-score-form">
              <label>
                プレイヤー名（3文字）
                <input id="puyo-player-name" name="player-name" maxlength="3" autocomplete="off" required>
              </label>
              <button class="primary-button" type="submit">登録</button>
              <p class="score-save-message" id="puyo-score-save-message"></p>
              <button class="primary-button" id="puyo-play-again" type="button">もう一度遊ぶ</button>
            </form>
          </div>
        </div>
        <script>
          const canvas = document.getElementById("puyo-board");
          const context = canvas.getContext("2d");
          const scoreElement = document.getElementById("puyo-score");
          const highScoreElement = document.getElementById("puyo-high-score");
          const highScoreNameElement = document.getElementById("puyo-high-score-name");
          const statusElement = document.getElementById("puyo-status");
          const chainElement = document.getElementById("puyo-chain");
          const restartButton = document.getElementById("puyo-restart");
          const gameOverOverlay = document.getElementById("puyo-game-over");
          const finalScoreElement = document.getElementById("puyo-final-score");
          const scoreForm = document.getElementById("puyo-score-form");
          const playerNameInput = document.getElementById("puyo-player-name");
          const scoreSaveMessage = document.getElementById("puyo-score-save-message");
          const playAgainButton = document.getElementById("puyo-play-again");

          const highScoreKey = "gameHubPuyopuyoHighScore";
          const highScoreNameKey = "gameHubPuyopuyoHighScoreName";
          const rankingKey = "gameHubPuyopuyoRanking";
          const columns = 6;
          const rows = 12;
          const cellSize = 40;
          const baseDropInterval = 820;
          const minDropInterval = 160;
          const speedUpScoreStep = 500;
          const dropIntervalStep = 70;
          const chainScoreTable = [0, 20, 50, 90, 140, 200, 270, 350, 440, 540, 650];
          const colors = ["red", "green", "blue", "yellow", "purple"];
          const colorMap = {
            red: "#ff5c7a",
            green: "#5cff9d",
            blue: "#60e7ff",
            yellow: "#ffe45c",
            purple: "#c77dff",
          };

          let board;
          let pair;
          let score;
          let highScore;
          let highScoreName;
          let dropCounter;
          let dropInterval;
          let lastTime;
          let hasStarted;
          let isPaused;
          let isGameOver;
          let isResolving;
          let clearingCells;

          function createBoard() {
            return Array.from({ length: rows }, () => Array(columns).fill(""));
          }

          function delay(milliseconds) {
            return new Promise((resolve) => {
              setTimeout(resolve, milliseconds);
            });
          }

          function flattenGroups(groups) {
            return groups.flatMap((group) => group);
          }

          function randomColor() {
            return colors[Math.floor(Math.random() * colors.length)];
          }

          function createPair() {
            return {
              x: Math.floor(columns / 2),
              y: 1,
              rotation: 0,
              colors: [randomColor(), randomColor()],
            };
          }

          function getPairCells(target = pair) {
            const offsets = [
              { x: 0, y: -1 },
              { x: 1, y: 0 },
              { x: 0, y: 1 },
              { x: -1, y: 0 },
            ];
            const offset = offsets[target.rotation];
            return [
              { x: target.x, y: target.y, color: target.colors[0] },
              { x: target.x + offset.x, y: target.y + offset.y, color: target.colors[1] },
            ];
          }

          function hasCollision(target = pair) {
            return getPairCells(target).some((cell) => (
              cell.x < 0 ||
              cell.x >= columns ||
              cell.y >= rows ||
              (cell.y >= 0 && board[cell.y][cell.x])
            ));
          }

          function movePair(offsetX) {
            const nextPair = { ...pair, x: pair.x + offsetX };
            if (!hasCollision(nextPair)) {
              pair = nextPair;
            }
          }

          function rotatePair() {
            for (const offsetX of [0, -1, 1, -2, 2]) {
              const nextPair = {
                ...pair,
                x: pair.x + offsetX,
                rotation: (pair.rotation + 1) % 4,
              };
              if (!hasCollision(nextPair)) {
                pair = nextPair;
                return;
              }
            }
          }

          function mergePair() {
            getPairCells().forEach((cell) => {
              if (cell.y >= 0) {
                board[cell.y][cell.x] = cell.color;
              }
            });
          }

          function applyGravity() {
            for (let x = 0; x < columns; x += 1) {
              const stack = [];
              for (let y = rows - 1; y >= 0; y -= 1) {
                if (board[y][x]) {
                  stack.push(board[y][x]);
                }
              }
              for (let y = rows - 1; y >= 0; y -= 1) {
                board[y][x] = stack[rows - 1 - y] || "";
              }
            }
          }

          function findGroups() {
            const visited = Array.from({ length: rows }, () => Array(columns).fill(false));
            const groups = [];

            for (let y = 0; y < rows; y += 1) {
              for (let x = 0; x < columns; x += 1) {
                const color = board[y][x];
                if (!color || visited[y][x]) {
                  continue;
                }

                const group = [];
                const queue = [{ x, y }];
                visited[y][x] = true;

                while (queue.length > 0) {
                  const current = queue.shift();
                  group.push(current);

                  for (const direction of [{ x: 1, y: 0 }, { x: -1, y: 0 }, { x: 0, y: 1 }, { x: 0, y: -1 }]) {
                    const nextX = current.x + direction.x;
                    const nextY = current.y + direction.y;
                    if (
                      nextX < 0 ||
                      nextX >= columns ||
                      nextY < 0 ||
                      nextY >= rows ||
                      visited[nextY][nextX] ||
                      board[nextY][nextX] !== color
                    ) {
                      continue;
                    }
                    visited[nextY][nextX] = true;
                    queue.push({ x: nextX, y: nextY });
                  }
                }

                if (group.length >= 4) {
                  groups.push(group);
                }
              }
            }

            return groups;
          }

          async function clearGroups() {
            let chain = 0;
            let clearedAny = false;

            while (true) {
              const groups = findGroups();
              if (groups.length === 0) {
                break;
              }

              chain += 1;
              clearedAny = true;
              statusElement.textContent = `${chain}連鎖`;
              chainElement.textContent = `${chain}連鎖`;
              await animateClearing(flattenGroups(groups));

              groups.forEach((group) => {
                group.forEach((cell) => {
                  board[cell.y][cell.x] = "";
                });
              });
              score += chainScoreTable[Math.min(chain, 10)];
              scoreElement.textContent = score;
              updateHighScore();
              await delay(250);
              applyGravity();
              await delay(350);
            }

            if (clearedAny) {
              updateDropSpeed();
              statusElement.textContent = "プレイ中";
            } else {
              chainElement.textContent = "0連鎖";
            }

            return clearedAny;
          }

          function updateDropSpeed() {
            const speedLevel = Math.floor(score / speedUpScoreStep);
            dropInterval = Math.max(
              minDropInterval,
              baseDropInterval - speedLevel * dropIntervalStep,
            );
          }

          async function dropPair() {
            if (isResolving) {
              return;
            }

            const nextPair = { ...pair, y: pair.y + 1 };
            if (!hasCollision(nextPair)) {
              pair = nextPair;
              dropCounter = 0;
              return;
            }

            mergePair();
            pair = null;
            applyGravity();
            isResolving = true;
            const clearedAny = await clearGroups();
            isResolving = false;
            if (!clearedAny) {
              chainElement.textContent = "0連鎖";
            }
            pair = createPair();
            if (hasCollision()) {
              isGameOver = true;
              statusElement.textContent = "ゲームオーバー";
              updateHighScore();
              showGameOverDialog();
            }
            dropCounter = 0;
          }

          async function hardDrop() {
            if (isResolving) {
              return;
            }

            while (!hasCollision({ ...pair, y: pair.y + 1 })) {
              pair = { ...pair, y: pair.y + 1 };
            }
            await dropPair();
          }

          function updateHighScore() {
            if (score <= highScore) {
              return;
            }

            highScore = score;
            highScoreName = "";
            highScoreElement.textContent = highScore;
            highScoreNameElement.textContent = "登録待ち";
            localStorage.setItem(highScoreKey, String(highScore));
            localStorage.removeItem(highScoreNameKey);
          }

          function showGameOverDialog() {
            finalScoreElement.textContent = score;
            scoreSaveMessage.textContent = "";
            playerNameInput.value = "";
            gameOverOverlay.hidden = false;
            playerNameInput.focus();
          }

          function hideGameOverDialog() {
            gameOverOverlay.hidden = true;
          }

          function saveScoreEntry(playerName) {
            const ranking = JSON.parse(localStorage.getItem(rankingKey) || "[]");
            ranking.push({
              name: playerName,
              score,
              playedAt: new Date().toISOString(),
            });
            ranking.sort((left, right) => right.score - left.score);
            localStorage.setItem(rankingKey, JSON.stringify(ranking.slice(0, 50)));

            if (score >= highScore && score > 0) {
              highScore = score;
              highScoreName = playerName;
              highScoreElement.textContent = highScore;
              highScoreNameElement.textContent = highScoreName;
              localStorage.setItem(highScoreKey, String(highScore));
              localStorage.setItem(highScoreNameKey, highScoreName);
            }
          }

          function findHighScoreName(targetScore) {
            const ranking = JSON.parse(localStorage.getItem(rankingKey) || "[]");
            const matchedEntry = ranking.find((entry) => entry.score === targetScore);
            return matchedEntry ? matchedEntry.name : "";
          }

          async function animateClearing(cells) {
            for (let frame = 0; frame < 6; frame += 1) {
              clearingCells = cells.map((cell) => ({
                ...cell,
                scale: frame % 2 === 0 ? 1.18 : 0.72,
                alpha: frame % 2 === 0 ? 1 : 0.45,
              }));
              draw();
              await delay(90);
            }

            clearingCells = [];
            draw();
          }

          function drawPuyo(x, y, color, scale = 1, alpha = 1) {
            const centerX = x * cellSize + cellSize / 2;
            const centerY = y * cellSize + cellSize / 2;
            context.save();
            context.globalAlpha = alpha;
            context.fillStyle = colorMap[color];
            context.beginPath();
            context.arc(centerX, centerY, cellSize * 0.42 * scale, 0, Math.PI * 2);
            context.fill();
            context.fillStyle = "rgba(255, 255, 255, 0.45)";
            context.beginPath();
            context.arc(centerX - 7 * scale, centerY - 8 * scale, cellSize * 0.12 * scale, 0, Math.PI * 2);
            context.fill();
            context.restore();
          }

          function draw() {
            context.fillStyle = "rgba(0, 12, 28, 0.96)";
            context.fillRect(0, 0, canvas.width, canvas.height);

            context.strokeStyle = "rgba(150, 235, 255, 0.12)";
            for (let x = 1; x < columns; x += 1) {
              context.beginPath();
              context.moveTo(x * cellSize, 0);
              context.lineTo(x * cellSize, canvas.height);
              context.stroke();
            }
            for (let y = 1; y < rows; y += 1) {
              context.beginPath();
              context.moveTo(0, y * cellSize);
              context.lineTo(canvas.width, y * cellSize);
              context.stroke();
            }

            board.forEach((row, y) => {
              row.forEach((color, x) => {
                if (color) {
                  const clearingCell = clearingCells.find((cell) => cell.x === x && cell.y === y);
                  if (clearingCell) {
                    drawPuyo(x, y, color, clearingCell.scale, clearingCell.alpha);
                    return;
                  }
                  drawPuyo(x, y, color);
                }
              });
            });

            if (pair) {
              getPairCells().forEach((cell) => {
                if (cell.y >= 0) {
                  drawPuyo(cell.x, cell.y, cell.color);
                }
              });
            }
          }

          function update(time = 0) {
            const deltaTime = time - lastTime;
            lastTime = time;

            if (hasStarted && !isPaused && !isGameOver && !isResolving) {
              dropCounter += deltaTime;
              if (dropCounter > dropInterval) {
                dropPair();
              }
            }

            draw();
            requestAnimationFrame(update);
          }

          function startGame() {
            board = createBoard();
            pair = createPair();
            score = 0;
            dropCounter = 0;
            dropInterval = baseDropInterval;
            lastTime = 0;
            hasStarted = true;
            isPaused = false;
            isGameOver = false;
            isResolving = false;
            clearingCells = [];
            scoreElement.textContent = score;
            chainElement.textContent = "0連鎖";
            statusElement.textContent = "プレイ中";
            restartButton.textContent = "リスタート";
            hideGameOverDialog();
          }

          document.addEventListener("keydown", (event) => {
            if (event.target.closest("#puyo-game-over")) {
              return;
            }

            if (!hasStarted) {
              if (event.key === "Enter") {
                startGame();
              }
              return;
            }

            if (isGameOver || isResolving) {
              return;
            }

            if (event.key === "p" || event.key === "P") {
              isPaused = !isPaused;
              statusElement.textContent = isPaused ? "一時停止中" : "プレイ中";
              return;
            }

            if (isPaused) {
              return;
            }

            if (event.key === "ArrowLeft") {
              movePair(-1);
              event.preventDefault();
            } else if (event.key === "ArrowRight") {
              movePair(1);
              event.preventDefault();
            } else if (event.key === "ArrowDown") {
              dropPair();
              event.preventDefault();
            } else if (event.key === "ArrowUp") {
              hardDrop();
              event.preventDefault();
            } else if (event.code === "Space") {
              rotatePair();
              event.preventDefault();
            } else if (event.key === "Enter") {
              startGame();
            }
          });

          restartButton.addEventListener("click", startGame);
          playAgainButton.addEventListener("click", startGame);
          playerNameInput.addEventListener("input", () => {
            playerNameInput.value = playerNameInput.value.slice(0, 3).toUpperCase();
          });
          scoreForm.addEventListener("submit", (event) => {
            event.preventDefault();
            const playerName = playerNameInput.value.trim().toUpperCase();
            if (!playerName) {
              scoreSaveMessage.textContent = "名前を入力してください";
              return;
            }

            saveScoreEntry(playerName);
            scoreSaveMessage.textContent = "スコアを登録しました";
          });

          board = createBoard();
          pair = null;
          score = 0;
          highScore = Number(localStorage.getItem(highScoreKey) || 0);
          highScoreName = localStorage.getItem(highScoreNameKey) || findHighScoreName(highScore);
          dropCounter = 0;
          dropInterval = baseDropInterval;
          lastTime = 0;
          hasStarted = false;
          isPaused = false;
          isGameOver = false;
          isResolving = false;
          clearingCells = [];
          scoreElement.textContent = score;
          chainElement.textContent = "0連鎖";
          highScoreElement.textContent = highScore;
          highScoreNameElement.textContent = highScoreName || (highScore > 0 ? "登録待ち" : "---");
          draw();
          update();
        </script>""",
)
BREAKOUT_HTML = render_page(
    title="ブロック崩し | Ocean Game Hub",
    heading="ブロック崩し",
    message="このページの内容は後で作成します",
    active_page="breakout",
)
RANKING_HTML = render_page(
    title="ランキング | Ocean Game Hub",
    heading="ランキング",
    active_page="ranking",
    body_html="""<p>各ゲームのランキングトップ5を表示します</p>
        <div class="ranking-grid">
          <section class="ranking-card">
            <h3>テトリス</h3>
            <ol class="ranking-list" id="ranking-tetris"></ol>
          </section>
          <section class="ranking-card">
            <h3>シューティング</h3>
            <ol class="ranking-list" id="ranking-shooting"></ol>
          </section>
          <section class="ranking-card">
            <h3>ぷよぷよ</h3>
            <ol class="ranking-list" id="ranking-puyopuyo"></ol>
          </section>
        </div>
        <script>
          const rankingSources = [
            { elementId: "ranking-tetris", storageKey: "gameHubTetrisRanking" },
            { elementId: "ranking-shooting", storageKey: "gameHubShootingRanking" },
            { elementId: "ranking-puyopuyo", storageKey: "gameHubPuyopuyoRanking" },
          ];

          function loadRanking(storageKey) {
            try {
              const ranking = JSON.parse(localStorage.getItem(storageKey) || "[]");
              return Array.isArray(ranking) ? ranking : [];
            } catch {
              return [];
            }
          }

          function renderRanking({ elementId, storageKey }) {
            const listElement = document.getElementById(elementId);
            const topScores = loadRanking(storageKey)
              .filter((entry) => entry && entry.name && Number.isFinite(Number(entry.score)))
              .sort((left, right) => Number(right.score) - Number(left.score))
              .slice(0, 5);

            if (topScores.length === 0) {
              listElement.outerHTML = '<p class="ranking-empty">まだ記録がありません</p>';
              return;
            }

            listElement.innerHTML = topScores
              .map((entry, index) => `
                <li>
                  <span>${index + 1}位</span>
                  <span>${String(entry.name).slice(0, 3)}</span>
                  <span>${Number(entry.score)}</span>
                </li>
              `)
              .join("");
          }

          rankingSources.forEach(renderRanking);
        </script>""",
)


def render_owner_login_page(error_message: str = "") -> str:
    error_html = f'<div class="error-message">{error_message}</div>' if error_message else ""

    return render_page(
        title="オーナーログイン | Ocean Game Hub",
        heading="オーナーログイン",
        active_page="owner-login",
        body_html=f"""<p>管理機能へ進むにはログインしてください</p>
        <form class="login-form" action="/owner-dashboard" method="post">
          <label>
            アドレス
            <input type="email" name="address" autocomplete="email" required>
          </label>
          <label>
            パスワード
            <input type="password" name="password" autocomplete="current-password" required>
          </label>
          <button type="submit">ログイン</button>
        </form>
        {error_html}
        <div class="helper-text">管理画面の内容は後日作成します</div>""",
    )


OWNER_LOGIN_HTML = render_owner_login_page()
OWNER_DASHBOARD_HTML = render_page(
    title="管理ページ | Ocean Game Hub",
    heading="管理ページ",
    message="スコアデータ削除などの管理機能は後日作成します",
    active_page="owner-login",
)


class GameHubHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        path = urlparse(self.path).path

        if path in {"/", "/index.html"}:
            self._send_html(HOME_HTML)
            return

        if path == "/tetris":
            self._send_html(TETRIS_HTML)
            return

        if path == "/shooting":
            self._send_html(SHOOTING_HTML)
            return

        if path == "/puyopuyo":
            self._send_html(PUYOPUYO_HTML)
            return

        if path == "/breakout":
            self._send_html(BREAKOUT_HTML)
            return

        if path in {"/ranking", "/score"}:
            self._send_html(RANKING_HTML)
            return

        if path == "/owner-login":
            self._send_html(OWNER_LOGIN_HTML)
            return

        if path == "/owner-dashboard":
            self._send_html(OWNER_LOGIN_HTML)
            return

        if path == "/assets/background.png":
            self._send_background()
            return

        self.send_error(404)

    def do_POST(self) -> None:
        path = urlparse(self.path).path

        if path == "/owner-dashboard":
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length).decode("utf-8") if content_length else ""
            form = parse_qs(raw_body)
            address = form.get("address", [""])[0]
            password = form.get("password", [""])[0]

            if is_owner_login(address, password):
                self._send_html(OWNER_DASHBOARD_HTML)
                return

            self._send_html(render_owner_login_page("アドレスまたはパスワードが違います"))
            return

        self.send_error(404)

    def log_message(self, format: str, *args: object) -> None:
        return

    def _send_html(self, html: str) -> None:
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_background(self) -> None:
        if not BACKGROUND_IMAGE_PATH.exists():
            self.send_error(404, "Background image not found")
            return

        body = BACKGROUND_IMAGE_PATH.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "image/png")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def is_owner_login(address: str, password: str) -> bool:
    return hmac.compare_digest(address, OWNER_ADDRESS) and hmac.compare_digest(
        password,
        OWNER_PASSWORD,
    )


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), GameHubHandler)
    print(f"Open http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
