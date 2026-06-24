from ..layout import render_page


BREAKOUT_HTML = render_page(
    title="ブロック崩し | Ocean Game Hub",
    heading="ブロック崩し",
    active_page="breakout",
    body_html="""<p>ボールを跳ね返して全てのブロックを壊しましょう</p>
        <div class="game-panel">
          <canvas class="game-board breakout-board" id="breakout-board" width="520" height="620"></canvas>
          <aside class="game-info">
            <div class="info-card">
              <h3>スコア</h3>
              <p id="breakout-score">0</p>
              <p>ステージ <span id="breakout-stage">1</span></p>
            </div>
            <div class="info-card">
              <h3>操作</h3>
              <ul>
                <li>← →: パドル移動</li>
                <li>Space: ボール発射</li>
                <li>P: 一時停止</li>
              </ul>
            </div>
            <div class="info-card">
              <h3>状態</h3>
              <p id="breakout-status">スタート待ち</p>
            </div>
            <button class="primary-button" id="breakout-restart" type="button">スタート</button>
            <div class="info-card">
              <h3>ハイスコア</h3>
              <p><span id="breakout-high-score">0</span> / <span id="breakout-high-score-name">---</span></p>
            </div>
          </aside>
        </div>
        <div class="game-over-overlay" id="breakout-game-over" hidden>
          <div class="game-over-dialog" role="dialog" aria-modal="true" aria-labelledby="breakout-game-over-title">
            <h3 id="breakout-game-over-title">ゲームオーバー</h3>
            <p class="game-over-score">達成スコア: <span id="breakout-final-score">0</span></p>
            <form class="score-name-form" id="breakout-score-form">
              <label>
                プレイヤー名（3文字）
                <input id="breakout-player-name" name="player-name" maxlength="3" autocomplete="off" required>
              </label>
              <button class="primary-button" type="submit">登録</button>
              <p class="score-save-message" id="breakout-score-save-message"></p>
              <button class="primary-button" id="breakout-play-again" type="button">もう一度遊ぶ</button>
              <a class="primary-button" href="/">別のゲームで遊ぶ</a>
            </form>
          </div>
        </div>
        <script>
          const canvas = document.getElementById("breakout-board");
          const context = canvas.getContext("2d");
          const scoreElement = document.getElementById("breakout-score");
          const stageElement = document.getElementById("breakout-stage");
          const highScoreElement = document.getElementById("breakout-high-score");
          const highScoreNameElement = document.getElementById("breakout-high-score-name");
          const statusElement = document.getElementById("breakout-status");
          const restartButton = document.getElementById("breakout-restart");
          const gameOverOverlay = document.getElementById("breakout-game-over");
          const finalScoreElement = document.getElementById("breakout-final-score");
          const scoreForm = document.getElementById("breakout-score-form");
          const playerNameInput = document.getElementById("breakout-player-name");
          const scoreSaveMessage = document.getElementById("breakout-score-save-message");
          const playAgainButton = document.getElementById("breakout-play-again");

          const highScoreKey = "gameHubBreakoutHighScore";
          const highScoreNameKey = "gameHubBreakoutHighScoreName";
          const rankingKey = "gameHubBreakoutRanking";
          const paddleWidth = 92;
          const paddleHeight = 16;
          const ballRadius = 8;
          const brickRows = 5;
          const brickColumns = 8;
          const brickWidth = 54;
          const brickHeight = 20;
          const brickGap = 8;
          const brickOffsetX = 22;
          const brickOffsetY = 70;
          const yellowBrickBonus = 120;
          const extendedPaddleWidth = 150;
          const paddleExtendDurationMs = 30000;

          let paddle;
          let balls;
          let bricks;
          let score;
          let highScore;
          let highScoreName;
          let stage;
          let hasStarted;
          let isPaused;
          let isGameOver;
          let keys;
          let paddleExtendUntil;

          function shouldPlaceBrick(row, column, pattern) {
            if (pattern === 1) {
              return row === 0 || (row + column) % 2 === 0;
            }
            if (pattern === 2) {
              return column === 0 || column === brickColumns - 1 || row % 2 === 0;
            }
            if (pattern === 3) {
              const center = (brickColumns - 1) / 2;
              return Math.abs(column - center) <= row + 1;
            }
            return true;
          }

          function getYellowBrickIndex(bricksForStage) {
            return (stage * 7 + 3) % bricksForStage.length;
          }

          function getGreenBrickIndex(bricksForStage, yellowIndex) {
            let greenIndex = (stage * 5 + 1) % bricksForStage.length;
            if (greenIndex === yellowIndex) {
              greenIndex = (greenIndex + 1) % bricksForStage.length;
            }
            return greenIndex;
          }

          function createBricks() {
            const createdBricks = [];
            const rowCount = Math.min(brickRows + 2, brickRows + Math.floor((stage - 1) / 2));
            const pattern = (stage - 1) % 4;
            const baseHits = 1 + Math.floor((stage - 1) / 3);

            for (let row = 0; row < rowCount; row += 1) {
              for (let column = 0; column < brickColumns; column += 1) {
                if (!shouldPlaceBrick(row, column, pattern)) {
                  continue;
                }

                const isReinforced = stage >= 3 && (row + column + stage) % 4 === 0;
                const hits = Math.min(4, baseHits + (isReinforced ? 1 : 0));
                createdBricks.push({
                  x: brickOffsetX + column * (brickWidth + brickGap),
                  y: brickOffsetY + row * (brickHeight + brickGap),
                  width: brickWidth,
                  height: brickHeight,
                  hits,
                  maxHits: hits,
                  points: (rowCount - row) * 10 * hits,
                  isYellow: false,
                  isGreen: false,
                });
              }
            }
            if (createdBricks.length > 0) {
              const yellowIndex = getYellowBrickIndex(createdBricks);
              const yellowBrick = createdBricks[yellowIndex];
              yellowBrick.isYellow = true;
              yellowBrick.hits = 1;
              yellowBrick.maxHits = 1;
              yellowBrick.points += yellowBrickBonus;

              if (createdBricks.length > 1) {
                const greenBrick = createdBricks[getGreenBrickIndex(createdBricks, yellowIndex)];
                greenBrick.isGreen = true;
                greenBrick.hits = 1;
                greenBrick.maxHits = 1;
              }
            }
            return createdBricks;
          }

          function rectsOverlap(left, right) {
            return (
              left.x < right.x + right.width &&
              left.x + left.width > right.x &&
              left.y < right.y + right.height &&
              left.y + left.height > right.y
            );
          }

          function createBall(launch = false, direction = 1) {
            return {
              x: paddle.x + paddle.width / 2,
              y: paddle.y - ballRadius - 2,
              radius: ballRadius,
              dx: launch ? direction * (3.4 + stage * 0.25) : 0,
              dy: launch ? -(4.2 + stage * 0.28) : 0,
              isLaunched: launch,
            };
          }

          function resetBall(launch = false) {
            balls = [createBall(launch)];
          }

          function doubleBalls() {
            balls = balls.flatMap((currentBall) => {
              if (!currentBall.isLaunched) {
                return [currentBall, createBall(false)];
              }

              return [
                currentBall,
                {
                  ...currentBall,
                  dx: currentBall.dx === 0 ? 3.2 : -currentBall.dx,
                  dy: currentBall.dy * 0.96,
                },
              ];
            });
            statusElement.textContent = "黄色ブロック: ボール倍増";
          }

          function extendPaddle() {
            const center = paddle.x + paddle.width / 2;
            paddle.width = extendedPaddleWidth;
            paddle.x = Math.max(0, Math.min(canvas.width - paddle.width, center - paddle.width / 2));
            paddleExtendUntil = performance.now() + paddleExtendDurationMs;
            statusElement.textContent = "緑ブロック: バー延長";
          }

          function updatePaddleExtension() {
            if (!paddleExtendUntil || performance.now() < paddleExtendUntil) {
              return;
            }

            const center = paddle.x + paddle.width / 2;
            paddle.width = paddleWidth;
            paddle.x = Math.max(0, Math.min(canvas.width - paddle.width, center - paddle.width / 2));
            paddleExtendUntil = 0;
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

          function finishGame(statusText) {
            if (isGameOver) {
              return;
            }

            isGameOver = true;
            statusElement.textContent = statusText;
            updateHighScore();
            showGameOverDialog();
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

          function launchBall() {
            if (balls.some((currentBall) => !currentBall.isLaunched)) {
              balls = balls.map((currentBall, index) => {
                if (currentBall.isLaunched) {
                  return currentBall;
                }

                return createBall(true, index % 2 === 0 ? 1 : -1);
              });
              statusElement.textContent = "プレイ中";
            }
          }

          function updatePaddle() {
            updatePaddleExtension();
            if (keys.ArrowLeft) {
              paddle.x -= paddle.speed;
            }
            if (keys.ArrowRight) {
              paddle.x += paddle.speed;
            }
            paddle.x = Math.max(0, Math.min(canvas.width - paddle.width, paddle.x));
          }

          function updateBall() {
            balls.forEach((ball) => {
              if (!ball.isLaunched) {
                ball.x = paddle.x + paddle.width / 2;
                ball.y = paddle.y - ball.radius - 2;
                return;
              }

              ball.x += ball.dx;
              ball.y += ball.dy;

              if (ball.x - ball.radius <= 0 || ball.x + ball.radius >= canvas.width) {
                ball.dx *= -1;
                ball.x = Math.max(ball.radius, Math.min(canvas.width - ball.radius, ball.x));
              }
              if (ball.y - ball.radius <= 0) {
                ball.dy *= -1;
                ball.y = ball.radius;
              }

              const ballRect = {
                x: ball.x - ball.radius,
                y: ball.y - ball.radius,
                width: ball.radius * 2,
                height: ball.radius * 2,
              };
              if (rectsOverlap(ballRect, paddle) && ball.dy > 0) {
                const hitPosition = (ball.x - (paddle.x + paddle.width / 2)) / (paddle.width / 2);
                ball.dx = hitPosition * (4 + stage * 0.35);
                ball.dy = -Math.abs(ball.dy);
                ball.y = paddle.y - ball.radius - 1;
              }

              const brickIndex = bricks.findIndex((brick) => rectsOverlap(ballRect, brick));
              if (brickIndex !== -1) {
                const brick = bricks[brickIndex];
                score += Math.ceil(brick.points / brick.maxHits);
                scoreElement.textContent = score;
                updateHighScore();
                brick.hits -= 1;
                if (brick.hits <= 0) {
                  if (brick.isYellow) {
                    doubleBalls();
                  }
                  if (brick.isGreen) {
                    extendPaddle();
                  }
                  bricks.splice(brickIndex, 1);
                }
                ball.dy *= -1;
              }
            });

            balls = balls.filter((ball) => ball.y - ball.radius <= canvas.height);
            if (balls.length === 0) {
              finishGame("ゲームオーバー");
              return;
            }

            if (bricks.length === 0) {
              stage += 1;
              stageElement.textContent = stage;
              score += 200 + (stage - 2) * 80;
              scoreElement.textContent = score;
              updateHighScore();
              bricks = createBricks();
              resetBall(false);
              statusElement.textContent = `ステージ ${stage}`;
            }
          }

          function draw() {
            context.fillStyle = "rgba(0, 12, 28, 0.96)";
            context.fillRect(0, 0, canvas.width, canvas.height);

            bricks.forEach((brick) => {
              const hue = 185 + Math.floor(brick.y / 10);
              const lightness = Math.max(42, 68 - brick.hits * 7);
              context.fillStyle = brick.isYellow
                ? "#ffe45c"
                : brick.isGreen
                  ? "#5cff9d"
                  : `hsl(${hue}, 85%, ${lightness}%)`;
              context.fillRect(brick.x, brick.y, brick.width, brick.height);
              context.strokeStyle = "rgba(255, 255, 255, 0.35)";
              context.strokeRect(brick.x + 1, brick.y + 1, brick.width - 2, brick.height - 2);
              if (brick.isYellow || brick.isGreen) {
                context.fillStyle = "rgba(0, 18, 40, 0.85)";
                context.font = "bold 13px sans-serif";
                context.textAlign = "center";
                context.textBaseline = "middle";
                context.fillText(brick.isYellow ? "x2" : "W", brick.x + brick.width / 2, brick.y + brick.height / 2);
                return;
              }
              if (brick.maxHits > 1) {
                context.fillStyle = "rgba(255, 255, 255, 0.86)";
                context.font = "bold 13px sans-serif";
                context.textAlign = "center";
                context.textBaseline = "middle";
                context.fillText(brick.hits, brick.x + brick.width / 2, brick.y + brick.height / 2);
              }
            });

            context.fillStyle = "#9feaff";
            context.fillRect(paddle.x, paddle.y, paddle.width, paddle.height);
            context.fillStyle = "#ffe45c";
            balls.forEach((ball) => {
              context.beginPath();
              context.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
              context.fill();
            });
          }

          function update() {
            if (hasStarted && !isPaused && !isGameOver) {
              updatePaddle();
              updateBall();
            }

            draw();
            requestAnimationFrame(update);
          }

          function startGame() {
            paddle = {
              x: canvas.width / 2 - paddleWidth / 2,
              y: canvas.height - 48,
              width: paddleWidth,
              height: paddleHeight,
              speed: 7,
            };
            stage = 1;
            score = 0;
            bricks = createBricks();
            hasStarted = true;
            isPaused = false;
            isGameOver = false;
            keys = {};
            paddleExtendUntil = 0;
            scoreElement.textContent = score;
            stageElement.textContent = stage;
            statusElement.textContent = "Spaceで発射";
            restartButton.textContent = "リスタート";
            resetBall(false);
            hideGameOverDialog();
          }

          document.addEventListener("keydown", (event) => {
            if (event.target.closest("#breakout-game-over")) {
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

            if (event.code === "Space") {
              launchBall();
              event.preventDefault();
            }

            if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
              keys[event.key] = true;
              event.preventDefault();
            }
          });

          document.addEventListener("keyup", (event) => {
            if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
              keys[event.key] = false;
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

          paddle = {
            x: canvas.width / 2 - paddleWidth / 2,
            y: canvas.height - 48,
            width: paddleWidth,
            height: paddleHeight,
            speed: 7,
          };
          stage = 1;
          score = 0;
          bricks = createBricks();
          highScore = Number(localStorage.getItem(highScoreKey) || 0);
          highScoreName = localStorage.getItem(highScoreNameKey) || findHighScoreName(highScore);
          hasStarted = false;
          isPaused = false;
          isGameOver = false;
          keys = {};
          paddleExtendUntil = 0;
          scoreElement.textContent = score;
          stageElement.textContent = stage;
          highScoreElement.textContent = highScore;
          highScoreNameElement.textContent = highScoreName || (highScore > 0 ? "登録待ち" : "---");
          resetBall(false);
          draw();
          update();
        </script>""",
)
