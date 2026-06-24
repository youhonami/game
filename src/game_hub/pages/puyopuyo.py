from ..layout import render_page


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
              <a class="primary-button" href="/">別のゲームで遊ぶ</a>
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
            scoreForm.querySelector('button[type="submit"]').hidden = true;
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
