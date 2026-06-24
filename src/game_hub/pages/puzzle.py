from ..layout import render_page


PUZZLE_HTML = render_page(
    title="15パズル | Ocean Game Hub",
    heading="15パズル",
    active_page="puzzle",
    body_html="""<p>数字を並べ替えて、1から15まで順番にそろえましょう</p>
        <section class="fifteen-puzzle-table">
          <div class="info-card">
            <h3>状態</h3>
            <p id="fifteen-status">シャッフルして開始してください</p>
          </div>
          <div class="info-card">
            <h3>移動回数</h3>
            <p id="fifteen-moves">0</p>
          </div>
          <div class="info-card">
            <h3>ハイスコア</h3>
            <p>移動回数: <span id="fifteen-high-score">-</span> / <span id="fifteen-high-score-name">---</span></p>
            <p>クリアタイム: <span id="fifteen-high-score-time">-</span></p>
          </div>
          <div class="fifteen-puzzle-actions">
            <button class="primary-button" id="fifteen-shuffle" type="button">シャッフル</button>
            <button class="primary-button" id="fifteen-reset" type="button">リセット</button>
          </div>
          <div class="fifteen-puzzle-board" id="fifteen-board"></div>
          <div class="info-card">
            <h3>遊び方</h3>
            <p>空きマスの上下左右にある数字をクリックすると、その数字が空きマスへ移動します。</p>
          </div>
        </section>
        <div class="game-over-overlay" id="fifteen-score-modal" hidden>
          <div class="game-over-dialog" role="dialog" aria-modal="true" aria-labelledby="fifteen-score-title">
            <h3 id="fifteen-score-title">クリア</h3>
            <p class="game-over-score">移動回数: <span id="fifteen-final-moves">0</span></p>
            <p class="game-over-score">クリアタイム: <span id="fifteen-final-time">0秒</span></p>
            <form class="score-name-form" id="fifteen-score-form">
            <label>
              プレイヤー名（3文字）
              <input id="fifteen-player-name" name="player-name" maxlength="3" autocomplete="off" required>
            </label>
            <button class="primary-button" type="submit">登録</button>
            <p class="score-save-message" id="fifteen-score-save-message"></p>
            <button class="primary-button" id="fifteen-play-again" type="button">もう一度遊ぶ</button>
            <a class="primary-button" href="/ranking">ランキングを見る</a>
          </form>
          </div>
        </div>
        <script>
          const fifteenBoardElement = document.getElementById("fifteen-board");
          const fifteenStatusElement = document.getElementById("fifteen-status");
          const fifteenMovesElement = document.getElementById("fifteen-moves");
          const fifteenShuffleButton = document.getElementById("fifteen-shuffle");
          const fifteenResetButton = document.getElementById("fifteen-reset");
          const fifteenHighScoreElement = document.getElementById("fifteen-high-score");
          const fifteenHighScoreNameElement = document.getElementById("fifteen-high-score-name");
          const fifteenHighScoreTimeElement = document.getElementById("fifteen-high-score-time");
          const fifteenScoreModal = document.getElementById("fifteen-score-modal");
          const fifteenFinalMovesElement = document.getElementById("fifteen-final-moves");
          const fifteenFinalTimeElement = document.getElementById("fifteen-final-time");
          const fifteenScoreForm = document.getElementById("fifteen-score-form");
          const fifteenPlayerNameInput = document.getElementById("fifteen-player-name");
          const fifteenScoreSaveMessage = document.getElementById("fifteen-score-save-message");
          const fifteenPlayAgainButton = document.getElementById("fifteen-play-again");

          const fifteenHighScoreKey = "gameHubFifteenPuzzleHighScore";
          const fifteenHighScoreNameKey = "gameHubFifteenPuzzleHighScoreName";
          const fifteenHighScoreTimeKey = "gameHubFifteenPuzzleHighScoreTime";
          const fifteenRankingKey = "gameHubFifteenPuzzleRanking";
          const solvedFifteenTiles = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0];
          let fifteenTiles = [...solvedFifteenTiles];
          let fifteenMoves = 0;
          let fifteenIsSolved = true;
          let fifteenHasStarted = false;
          let fifteenCanRegisterScore = false;
          let fifteenStartedAt = 0;
          let fifteenClearTimeSeconds = 0;

          function getFifteenRow(index) {
            return Math.floor(index / 4);
          }

          function getFifteenColumn(index) {
            return index % 4;
          }

          function canMoveFifteenTile(tileIndex) {
            const emptyIndex = fifteenTiles.indexOf(0);
            return (
              Math.abs(getFifteenRow(tileIndex) - getFifteenRow(emptyIndex))
              + Math.abs(getFifteenColumn(tileIndex) - getFifteenColumn(emptyIndex))
            ) === 1;
          }

          function isFifteenSolved() {
            return fifteenTiles.every((tile, index) => tile === solvedFifteenTiles[index]);
          }

          function updateFifteenStatus(message) {
            fifteenMovesElement.textContent = String(fifteenMoves);
            fifteenStatusElement.textContent = message;
          }

          function formatFifteenTime(totalSeconds) {
            if (!Number.isFinite(totalSeconds) || totalSeconds <= 0) {
              return "-";
            }

            const minutes = Math.floor(totalSeconds / 60);
            const seconds = totalSeconds % 60;
            if (minutes === 0) {
              return `${seconds}秒`;
            }
            return `${minutes}分${String(seconds).padStart(2, "0")}秒`;
          }

          function loadFifteenRanking() {
            try {
              const ranking = JSON.parse(localStorage.getItem(fifteenRankingKey) || "[]");
              return Array.isArray(ranking) ? ranking : [];
            } catch {
              return [];
            }
          }

          function updateFifteenHighScoreDisplay() {
            const highScore = Number(localStorage.getItem(fifteenHighScoreKey) || 0);
            const highScoreName = localStorage.getItem(fifteenHighScoreNameKey) || "---";
            const highScoreTime = Number(localStorage.getItem(fifteenHighScoreTimeKey) || 0);
            fifteenHighScoreElement.textContent = highScore > 0 ? String(highScore) : "-";
            fifteenHighScoreNameElement.textContent = highScore > 0 ? highScoreName : "---";
            fifteenHighScoreTimeElement.textContent = highScore > 0 ? formatFifteenTime(highScoreTime) : "-";
          }

          function saveFifteenScoreEntry(playerName) {
            const ranking = loadFifteenRanking()
              .filter((entry) => entry && entry.name && Number.isFinite(Number(entry.score)));
            ranking.push({
              name: playerName.slice(0, 3),
              score: fifteenMoves,
              clearTime: fifteenClearTimeSeconds,
              playedAt: new Date().toISOString(),
            });
            ranking.sort((left, right) => (
              Number(left.score) - Number(right.score)
              || (Number(left.clearTime) || Number.MAX_SAFE_INTEGER) - (Number(right.clearTime) || Number.MAX_SAFE_INTEGER)
            ));
            localStorage.setItem(fifteenRankingKey, JSON.stringify(ranking.slice(0, 5)));

            const currentHighScore = Number(localStorage.getItem(fifteenHighScoreKey) || 0);
            const currentHighScoreTime = Number(localStorage.getItem(fifteenHighScoreTimeKey) || 0);
            if (
              currentHighScore === 0
              || fifteenMoves < currentHighScore
              || (fifteenMoves === currentHighScore && (currentHighScoreTime === 0 || fifteenClearTimeSeconds < currentHighScoreTime))
            ) {
              localStorage.setItem(fifteenHighScoreKey, String(fifteenMoves));
              localStorage.setItem(fifteenHighScoreNameKey, playerName.slice(0, 3));
              localStorage.setItem(fifteenHighScoreTimeKey, String(fifteenClearTimeSeconds));
            }
            updateFifteenHighScoreDisplay();
          }

          function resetFifteenScoreForm() {
            fifteenScoreModal.hidden = true;
            fifteenPlayerNameInput.value = "";
            fifteenScoreSaveMessage.textContent = "";
            fifteenScoreForm.querySelector('button[type="submit"]').hidden = false;
            fifteenCanRegisterScore = false;
          }

          function showFifteenScoreModal() {
            fifteenFinalMovesElement.textContent = String(fifteenMoves);
            fifteenFinalTimeElement.textContent = formatFifteenTime(fifteenClearTimeSeconds);
            fifteenScoreModal.hidden = false;
            fifteenScoreSaveMessage.textContent = "";
            fifteenPlayerNameInput.value = "";
            fifteenScoreForm.querySelector('button[type="submit"]').hidden = false;
            fifteenCanRegisterScore = true;
            fifteenPlayerNameInput.focus();
          }

          function renderFifteenBoard() {
            fifteenBoardElement.innerHTML = fifteenTiles
              .map((tile, index) => {
                if (tile === 0) {
                  return '<button class="fifteen-tile is-empty" type="button" aria-label="空きマス" disabled></button>';
                }
                return `<button class="fifteen-tile" type="button" data-tile-index="${index}">${tile}</button>`;
              })
              .join("");

            fifteenBoardElement.querySelectorAll("[data-tile-index]").forEach((button) => {
              button.addEventListener("click", () => {
                moveFifteenTile(Number(button.dataset.tileIndex), true);
              });
            });
          }

          function moveFifteenTile(tileIndex, countMove) {
            if (fifteenIsSolved && countMove) {
              return false;
            }

            if (!canMoveFifteenTile(tileIndex)) {
              return false;
            }

            const emptyIndex = fifteenTiles.indexOf(0);
            [fifteenTiles[tileIndex], fifteenTiles[emptyIndex]] = [fifteenTiles[emptyIndex], fifteenTiles[tileIndex]];

            if (countMove) {
              fifteenMoves += 1;
            }

            fifteenIsSolved = isFifteenSolved();
            renderFifteenBoard();
            if (fifteenIsSolved) {
              fifteenClearTimeSeconds = Math.max(1, Math.floor((Date.now() - fifteenStartedAt) / 1000));
              updateFifteenStatus(`完成です！ ${fifteenMoves} 回、${formatFifteenTime(fifteenClearTimeSeconds)}でクリアしました`);
              if (fifteenHasStarted && countMove) {
                showFifteenScoreModal();
              }
            } else {
              updateFifteenStatus("空きマスの隣の数字を動かしてください");
            }
            return true;
          }

          function shuffleFifteenPuzzle() {
            fifteenTiles = [...solvedFifteenTiles];
            fifteenMoves = 0;
            fifteenIsSolved = false;
            fifteenHasStarted = true;
            fifteenStartedAt = 0;
            fifteenClearTimeSeconds = 0;
            resetFifteenScoreForm();

            let lastEmptyIndex = fifteenTiles.indexOf(0);
            for (let step = 0; step < 180; step += 1) {
              const emptyIndex = fifteenTiles.indexOf(0);
              const movableIndexes = fifteenTiles
                .map((tile, index) => index)
                .filter((index) => index !== lastEmptyIndex && canMoveFifteenTile(index));
              const nextIndex = movableIndexes[Math.floor(Math.random() * movableIndexes.length)];
              lastEmptyIndex = emptyIndex;
              moveFifteenTile(nextIndex, false);
            }

            if (isFifteenSolved()) {
              shuffleFifteenPuzzle();
              return;
            }

            fifteenMoves = 0;
            fifteenIsSolved = false;
            fifteenHasStarted = true;
            fifteenStartedAt = Date.now();
            fifteenClearTimeSeconds = 0;
            renderFifteenBoard();
            updateFifteenStatus("ゲーム開始です。空きマスの隣をクリックしてください");
          }

          function resetFifteenPuzzle() {
            fifteenTiles = [...solvedFifteenTiles];
            fifteenMoves = 0;
            fifteenIsSolved = true;
            fifteenHasStarted = false;
            fifteenStartedAt = 0;
            fifteenClearTimeSeconds = 0;
            resetFifteenScoreForm();
            renderFifteenBoard();
            updateFifteenStatus("リセットしました。シャッフルして開始してください");
          }

          fifteenShuffleButton.addEventListener("click", shuffleFifteenPuzzle);
          fifteenResetButton.addEventListener("click", resetFifteenPuzzle);
          fifteenPlayAgainButton.addEventListener("click", shuffleFifteenPuzzle);
          fifteenPlayerNameInput.addEventListener("input", () => {
            fifteenPlayerNameInput.value = fifteenPlayerNameInput.value.slice(0, 3).toUpperCase();
          });
          fifteenScoreForm.addEventListener("submit", (event) => {
            event.preventDefault();
            const playerName = fifteenPlayerNameInput.value.trim().toUpperCase();
            if (!fifteenCanRegisterScore) {
              fifteenScoreSaveMessage.textContent = "このスコアは登録済みです";
              return;
            }
            if (!playerName) {
              fifteenScoreSaveMessage.textContent = "名前を入力してください";
              return;
            }

            saveFifteenScoreEntry(playerName);
            fifteenCanRegisterScore = false;
            fifteenScoreSaveMessage.textContent = "スコアを登録しました";
            fifteenScoreForm.querySelector('button[type="submit"]').hidden = true;
          });
          updateFifteenHighScoreDisplay();
          resetFifteenPuzzle();
        </script>""",
)
