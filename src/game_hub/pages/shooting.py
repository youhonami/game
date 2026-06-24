from ..layout import render_page


SHOOTING_HTML = render_page(
    title="シューティング | Ocean Game Hub",
    heading="シューティング",
    active_page="shooting",
    body_html="""<p>敵を撃ち落として地球を守りましょう</p>
        <div class="game-panel">
          <canvas class="game-board shooting-board" id="shooting-board" width="520" height="620"></canvas>
          <aside class="game-info">
            <div class="info-card">
              <h3>スコア</h3>
              <p id="shooting-score">0</p>
              <p>ステージ <span id="shooting-stage">1</span></p>
            </div>
            <div class="info-card">
              <h3>操作</h3>
              <ul>
                <li>← →: 移動</li>
                <li>Space: 弾を撃つ</li>
                <li>P: 一時停止</li>
              </ul>
            </div>
            <div class="info-card">
              <h3>状態</h3>
              <p id="shooting-status">スタート待ち</p>
            </div>
            <button class="primary-button" id="shooting-restart" type="button">スタート</button>
            <div class="info-card">
              <h3>ハイスコア</h3>
              <p><span id="shooting-high-score">0</span> / <span id="shooting-high-score-name">---</span></p>
            </div>
          </aside>
        </div>
        <div class="game-over-overlay" id="shooting-game-over" hidden>
          <div class="game-over-dialog" role="dialog" aria-modal="true" aria-labelledby="shooting-game-over-title">
            <h3 id="shooting-game-over-title">ゲームオーバー</h3>
            <p class="game-over-score">達成スコア: <span id="shooting-final-score">0</span></p>
            <form class="score-name-form" id="shooting-score-form">
              <label>
                プレイヤー名（3文字）
                <input id="shooting-player-name" name="player-name" maxlength="3" autocomplete="off" required>
              </label>
              <button class="primary-button" type="submit">登録</button>
              <p class="score-save-message" id="shooting-score-save-message"></p>
              <button class="primary-button" id="shooting-play-again" type="button">もう一度遊ぶ</button>
              <a class="primary-button" href="/">別のゲームで遊ぶ</a>
            </form>
          </div>
        </div>
        <script>
          const canvas = document.getElementById("shooting-board");
          const context = canvas.getContext("2d");
          const scoreElement = document.getElementById("shooting-score");
          const stageElement = document.getElementById("shooting-stage");
          const highScoreElement = document.getElementById("shooting-high-score");
          const highScoreNameElement = document.getElementById("shooting-high-score-name");
          const statusElement = document.getElementById("shooting-status");
          const restartButton = document.getElementById("shooting-restart");
          const gameOverOverlay = document.getElementById("shooting-game-over");
          const finalScoreElement = document.getElementById("shooting-final-score");
          const scoreForm = document.getElementById("shooting-score-form");
          const playerNameInput = document.getElementById("shooting-player-name");
          const scoreSaveMessage = document.getElementById("shooting-score-save-message");
          const playAgainButton = document.getElementById("shooting-play-again");

          const highScoreKey = "gameHubShootingHighScore";
          const highScoreNameKey = "gameHubShootingHighScoreName";
          const rankingKey = "gameHubShootingRanking";
          const playerWidth = 46;
          const playerHeight = 22;
          const bulletSpeed = 7;
          const baseEnemyBulletSpeed = 3.2;
          const baseEnemyFireInterval = 52;
          const enemyWidth = 32;
          const enemyHeight = 24;
          const enemyRows = 4;
          const enemyColumns = 9;
          const rareEnemySpawnFrames = 60 * 60;

          let player;
          let bullets;
          let enemyBullets;
          let enemies;
          let rareEnemy;
          let rareEnemyTimer;
          let enemyDirection;
          let enemyMoveTimer;
          let enemyMoveInterval;
          let enemyFireTimer;
          let stage;
          let score;
          let highScore;
          let highScoreName;
          let hasStarted;
          let isPaused;
          let isGameOver;
          let keys;

          function createEnemies() {
            const startX = 56;
            const startY = 70;
            const gapX = 42;
            const gapY = 36;
            const createdEnemies = [];

            for (let row = 0; row < enemyRows; row += 1) {
              for (let column = 0; column < enemyColumns; column += 1) {
                createdEnemies.push({
                  x: startX + column * gapX,
                  y: startY + row * gapY,
                  width: enemyWidth,
                  height: enemyHeight,
                  points: (enemyRows - row) * 10,
                });
              }
            }

            return createdEnemies;
          }

          function createRareEnemy() {
            const startsFromLeft = Math.random() > 0.5;
            return {
              x: startsFromLeft ? -70 : canvas.width + 10,
              y: 28,
              width: 58,
              height: 24,
              speed: startsFromLeft ? 2.4 : -2.4,
              points: 1000,
            };
          }

          function rectsOverlap(left, right) {
            return (
              left.x < right.x + right.width &&
              left.x + left.width > right.x &&
              left.y < right.y + right.height &&
              left.y + left.height > right.y
            );
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

          function shoot() {
            const now = performance.now();
            if (now - player.lastShotAt < 280) {
              return;
            }

            bullets.push({
              x: player.x + player.width / 2 - 2,
              y: player.y - 12,
              width: 4,
              height: 12,
            });
            player.lastShotAt = now;
          }

          function updatePlayer() {
            if (keys.ArrowLeft) {
              player.x -= player.speed;
            }
            if (keys.ArrowRight) {
              player.x += player.speed;
            }
            player.x = Math.max(0, Math.min(canvas.width - player.width, player.x));
          }

          function updateBullets() {
            bullets.forEach((bullet) => {
              bullet.y -= bulletSpeed;
            });
            bullets = bullets.filter((bullet) => bullet.y + bullet.height > 0);

            enemyBullets.forEach((bullet) => {
              bullet.y += bullet.speed;
            });
            enemyBullets = enemyBullets.filter((bullet) => bullet.y < canvas.height);
          }

          function getEnemyMoveInterval() {
            return Math.max(6, 34 - (stage - 1) * 4);
          }

          function getEnemyMoveDistance() {
            return Math.min(22, 12 + (stage - 1) * 2);
          }

          function updateEnemies() {
            enemyMoveTimer += 1;
            if (enemyMoveTimer < enemyMoveInterval) {
              return;
            }
            enemyMoveTimer = 0;

            let shouldDrop = false;
            const moveDistance = getEnemyMoveDistance();
            enemies.forEach((enemy) => {
              enemy.x += enemyDirection * moveDistance;
              if (enemy.x <= 16 || enemy.x + enemy.width >= canvas.width - 16) {
                shouldDrop = true;
              }
            });

            if (shouldDrop) {
              enemyDirection *= -1;
              enemies.forEach((enemy) => {
                enemy.y += 18;
              });
            }

            enemyMoveInterval = getEnemyMoveInterval();
          }

          function updateRareEnemy() {
            if (rareEnemy) {
              rareEnemy.x += rareEnemy.speed;
              if (rareEnemy.x + rareEnemy.width < -20 || rareEnemy.x > canvas.width + 20) {
                rareEnemy = null;
              }
              return;
            }

            rareEnemyTimer += 1;
            if (rareEnemyTimer >= rareEnemySpawnFrames) {
              rareEnemy = createRareEnemy();
              rareEnemyTimer = 0;
            }
          }

          function updateEnemyFire() {
            enemyFireTimer += 1;
            const enemyFireInterval = Math.max(
              16,
              baseEnemyFireInterval - (stage - 1) * 6,
            );
            if (enemyFireTimer < enemyFireInterval || enemies.length === 0) {
              return;
            }
            enemyFireTimer = 0;

            const shooter = enemies[Math.floor(Math.random() * enemies.length)];
            enemyBullets.push({
              x: shooter.x + shooter.width / 2 - 3,
              y: shooter.y + shooter.height,
              width: 6,
              height: 12,
              speed: baseEnemyBulletSpeed + (stage - 1) * 0.45,
            });
          }

          function advanceStage() {
            stage += 1;
            stageElement.textContent = stage;
            statusElement.textContent = `ステージ ${stage}`;
            enemies = createEnemies();
            enemyBullets = [];
            enemyDirection = stage % 2 === 0 ? -1 : 1;
            enemyMoveTimer = 0;
            enemyFireTimer = 0;
            enemyMoveInterval = getEnemyMoveInterval();
          }

          function resolveCollisions() {
            bullets = bullets.filter((bullet) => {
              if (rareEnemy && rectsOverlap(bullet, rareEnemy)) {
                score += rareEnemy.points;
                scoreElement.textContent = score;
                statusElement.textContent = "レア敵撃破 +1000";
                updateHighScore();
                rareEnemy = null;
                return false;
              }

              const enemyIndex = enemies.findIndex((enemy) => rectsOverlap(bullet, enemy));
              if (enemyIndex === -1) {
                return true;
              }

              score += enemies[enemyIndex].points;
              scoreElement.textContent = score;
              updateHighScore();
              enemies.splice(enemyIndex, 1);
              return false;
            });

            if (enemyBullets.some((bullet) => rectsOverlap(bullet, player))) {
              finishGame("ゲームオーバー");
              return;
            }

            if (enemies.some((enemy) => enemy.y + enemy.height >= player.y)) {
              finishGame("侵略されました");
              return;
            }

            if (enemies.length === 0) {
              score += 200 + (stage - 1) * 50;
              scoreElement.textContent = score;
              updateHighScore();
              advanceStage();
            }
          }

          function drawPlayer() {
            context.fillStyle = "#9feaff";
            context.fillRect(player.x, player.y + 10, player.width, player.height - 10);
            context.fillRect(player.x + player.width / 2 - 5, player.y, 10, 14);
          }

          function drawEnemy(enemy) {
            context.fillStyle = "#5cff9d";
            context.fillRect(enemy.x, enemy.y + 6, enemy.width, enemy.height - 6);
            context.fillStyle = "#021329";
            context.fillRect(enemy.x + 7, enemy.y + 12, 5, 5);
            context.fillRect(enemy.x + enemy.width - 12, enemy.y + 12, 5, 5);
            context.fillStyle = "#5cff9d";
            context.fillRect(enemy.x + 4, enemy.y, 6, 8);
            context.fillRect(enemy.x + enemy.width - 10, enemy.y, 6, 8);
          }

          function drawRareEnemy() {
            if (!rareEnemy) {
              return;
            }

            context.fillStyle = "#ffe45c";
            context.fillRect(rareEnemy.x, rareEnemy.y + 8, rareEnemy.width, rareEnemy.height - 8);
            context.fillStyle = "#ff5c7a";
            context.fillRect(rareEnemy.x + 10, rareEnemy.y, rareEnemy.width - 20, 10);
            context.fillStyle = "#021329";
            context.fillRect(rareEnemy.x + 14, rareEnemy.y + 14, 7, 5);
            context.fillRect(rareEnemy.x + rareEnemy.width - 21, rareEnemy.y + 14, 7, 5);
          }

          function draw() {
            context.fillStyle = "rgba(0, 12, 28, 0.96)";
            context.fillRect(0, 0, canvas.width, canvas.height);

            context.fillStyle = "rgba(159, 234, 255, 0.35)";
            for (let i = 0; i < 60; i += 1) {
              const x = (i * 83) % canvas.width;
              const y = (i * 47) % canvas.height;
              context.fillRect(x, y, 2, 2);
            }

            drawRareEnemy();
            enemies.forEach(drawEnemy);

            context.fillStyle = "#ffe45c";
            bullets.forEach((bullet) => {
              context.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
            });

            context.fillStyle = "#ff5c7a";
            enemyBullets.forEach((bullet) => {
              context.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
            });

            drawPlayer();
          }

          function update() {
            if (hasStarted && !isPaused && !isGameOver) {
              updatePlayer();
              updateBullets();
              updateEnemies();
              updateRareEnemy();
              updateEnemyFire();
              resolveCollisions();
            }

            draw();
            requestAnimationFrame(update);
          }

          function startGame() {
            player = {
              x: canvas.width / 2 - playerWidth / 2,
              y: canvas.height - 58,
              width: playerWidth,
              height: playerHeight,
              speed: 5,
              lastShotAt: 0,
            };
            bullets = [];
            enemyBullets = [];
            enemies = createEnemies();
            rareEnemy = null;
            rareEnemyTimer = 0;
            enemyDirection = 1;
            enemyMoveTimer = 0;
            enemyFireTimer = 0;
            stage = 1;
            enemyMoveInterval = getEnemyMoveInterval();
            score = 0;
            hasStarted = true;
            isPaused = false;
            isGameOver = false;
            scoreElement.textContent = score;
            stageElement.textContent = stage;
            statusElement.textContent = "プレイ中";
            restartButton.textContent = "リスタート";
            hideGameOverDialog();
          }

          document.addEventListener("keydown", (event) => {
            if (event.target.closest("#shooting-game-over")) {
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
              shoot();
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

          player = {
            x: canvas.width / 2 - playerWidth / 2,
            y: canvas.height - 58,
            width: playerWidth,
            height: playerHeight,
            speed: 5,
            lastShotAt: 0,
          };
          bullets = [];
          enemyBullets = [];
          enemies = createEnemies();
          rareEnemy = null;
          rareEnemyTimer = 0;
          enemyDirection = 1;
          enemyMoveTimer = 0;
          enemyFireTimer = 0;
          stage = 1;
          enemyMoveInterval = getEnemyMoveInterval();
          score = 0;
          highScore = Number(localStorage.getItem(highScoreKey) || 0);
          highScoreName = localStorage.getItem(highScoreNameKey) || findHighScoreName(highScore);
          hasStarted = false;
          isPaused = false;
          isGameOver = false;
          keys = {};
          scoreElement.textContent = score;
          stageElement.textContent = stage;
          highScoreElement.textContent = highScore;
          highScoreNameElement.textContent = highScoreName || (highScore > 0 ? "登録待ち" : "---");
          draw();
          update();
        </script>""",
)
