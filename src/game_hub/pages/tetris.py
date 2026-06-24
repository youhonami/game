from ..layout import render_page


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
              <a class="primary-button" href="/">別のゲームで遊ぶ</a>
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
            scoreForm.querySelector('button[type="submit"]').hidden = false;
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
            scoreForm.querySelector('button[type="submit"]').hidden = true;
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
