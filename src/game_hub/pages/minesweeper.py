from ..layout import render_page


MINESWEEPER_HTML = render_page(
    title="マインスイーパー | Ocean Game Hub",
    heading="マインスイーパー",
    active_page="minesweeper",
    body_html="""<p>地雷を避けながらすべての安全なマスを開きましょう。右クリックで旗を立てられます。</p>
        <section class="minesweeper-table">
          <div class="minesweeper-status-grid">
            <div class="info-card">
              <h3>状態</h3>
              <p id="minesweeper-status">新しいゲームを開始してください</p>
            </div>
            <div class="info-card">
              <h3>難易度</h3>
              <p id="minesweeper-difficulty-label">初級 9x9</p>
            </div>
            <div class="info-card">
              <h3>地雷</h3>
              <p><span id="minesweeper-mines-left">10</span> 個</p>
            </div>
            <div class="info-card">
              <h3>タイム</h3>
              <p><span id="minesweeper-time">0</span> 秒</p>
            </div>
          </div>
          <div class="minesweeper-actions">
            <label class="score-name-form">
              難易度
              <select id="minesweeper-difficulty">
                <option value="beginner">初級（9x9 / 地雷10個）</option>
                <option value="intermediate">中級（12x12 / 地雷20個）</option>
                <option value="advanced">上級（16x16 / 地雷40個）</option>
              </select>
            </label>
            <button class="primary-button" id="minesweeper-new-game" type="button">新しいゲーム</button>
            <button class="primary-button" id="minesweeper-reveal" type="button">答えを見る</button>
          </div>
          <div class="minesweeper-board" id="minesweeper-board" aria-label="マインスイーパー盤面"></div>
          <div class="info-card">
            <h3>遊び方</h3>
            <p>左クリックでマスを開きます。数字は周囲8マスにある地雷の数です。右クリックで旗を立てて地雷の候補をメモできます。</p>
          </div>
        </section>
        <div class="game-over-overlay" id="minesweeper-clear-modal" hidden>
          <div class="game-over-dialog" role="dialog" aria-modal="true" aria-labelledby="minesweeper-clear-title">
            <h3 id="minesweeper-clear-title">クリア</h3>
            <p class="game-over-score"><span id="minesweeper-clear-difficulty">初級</span> / <span id="minesweeper-final-time">0</span> 秒</p>
            <form class="score-name-form" id="minesweeper-score-form">
              <label>
                プレイヤー名（3文字）
                <input id="minesweeper-player-name" name="player-name" maxlength="3" autocomplete="off" required>
              </label>
              <button class="primary-button" type="submit">登録</button>
              <p class="score-save-message" id="minesweeper-score-save-message"></p>
              <button class="primary-button" id="minesweeper-play-again" type="button">もう一度遊ぶ</button>
              <a class="primary-button" href="/ranking">ランキングを見る</a>
            </form>
          </div>
        </div>
        <script>
          const minesweeperBoardElement = document.getElementById("minesweeper-board");
          const minesweeperStatusElement = document.getElementById("minesweeper-status");
          const minesweeperDifficultyLabelElement = document.getElementById("minesweeper-difficulty-label");
          const minesweeperMinesLeftElement = document.getElementById("minesweeper-mines-left");
          const minesweeperTimeElement = document.getElementById("minesweeper-time");
          const minesweeperDifficultySelect = document.getElementById("minesweeper-difficulty");
          const minesweeperNewGameButton = document.getElementById("minesweeper-new-game");
          const minesweeperRevealButton = document.getElementById("minesweeper-reveal");
          const minesweeperClearModal = document.getElementById("minesweeper-clear-modal");
          const minesweeperClearDifficultyElement = document.getElementById("minesweeper-clear-difficulty");
          const minesweeperFinalTimeElement = document.getElementById("minesweeper-final-time");
          const minesweeperScoreForm = document.getElementById("minesweeper-score-form");
          const minesweeperPlayerNameInput = document.getElementById("minesweeper-player-name");
          const minesweeperScoreSaveMessage = document.getElementById("minesweeper-score-save-message");
          const minesweeperPlayAgainButton = document.getElementById("minesweeper-play-again");

          const minesweeperDifficulties = {
            beginner: { label: "初級", size: 9, mines: 10, rankingKey: "gameHubMinesweeperBeginnerRanking" },
            intermediate: { label: "中級", size: 12, mines: 20, rankingKey: "gameHubMinesweeperIntermediateRanking" },
            advanced: { label: "上級", size: 16, mines: 40, rankingKey: "gameHubMinesweeperAdvancedRanking" },
          };
          let minesweeperDifficulty = minesweeperDifficulties.beginner;
          let minesweeperSize = minesweeperDifficulty.size;
          let minesweeperMineCount = minesweeperDifficulty.mines;
          let minesweeperCells = [];
          let minesweeperIsStarted = false;
          let minesweeperIsGameOver = false;
          let minesweeperOpenedCount = 0;
          let minesweeperTimer = null;
          let minesweeperSeconds = 0;
          let minesweeperFinalTime = 0;
          let minesweeperCompletedDifficultyKey = "beginner";
          let minesweeperCanRegisterScore = false;

          function createMinesweeperCells() {
            return Array.from({ length: minesweeperSize * minesweeperSize }, (_, index) => ({
              index,
              isMine: false,
              isOpen: false,
              isFlagged: false,
              adjacentMines: 0,
            }));
          }

          function applyMinesweeperDifficulty() {
            minesweeperDifficulty = minesweeperDifficulties[minesweeperDifficultySelect.value] || minesweeperDifficulties.beginner;
            minesweeperSize = minesweeperDifficulty.size;
            minesweeperMineCount = minesweeperDifficulty.mines;
            minesweeperDifficultyLabelElement.textContent =
              `${minesweeperDifficulty.label} ${minesweeperSize}x${minesweeperSize}`;
            minesweeperBoardElement.style.gridTemplateColumns = `repeat(${minesweeperSize}, 1fr)`;
          }

          function getMinesweeperRow(index) {
            return Math.floor(index / minesweeperSize);
          }

          function getMinesweeperColumn(index) {
            return index % minesweeperSize;
          }

          function getMinesweeperNeighbors(index) {
            const row = getMinesweeperRow(index);
            const column = getMinesweeperColumn(index);
            const neighbors = [];

            for (let rowOffset = -1; rowOffset <= 1; rowOffset += 1) {
              for (let columnOffset = -1; columnOffset <= 1; columnOffset += 1) {
                if (rowOffset === 0 && columnOffset === 0) {
                  continue;
                }

                const nextRow = row + rowOffset;
                const nextColumn = column + columnOffset;
                if (
                  nextRow >= 0
                  && nextRow < minesweeperSize
                  && nextColumn >= 0
                  && nextColumn < minesweeperSize
                ) {
                  neighbors.push(nextRow * minesweeperSize + nextColumn);
                }
              }
            }

            return neighbors;
          }

          function startMinesweeperTimer() {
            clearInterval(minesweeperTimer);
            minesweeperTimer = setInterval(() => {
              minesweeperSeconds += 1;
              minesweeperTimeElement.textContent = String(minesweeperSeconds);
            }, 1000);
          }

          function stopMinesweeperTimer() {
            clearInterval(minesweeperTimer);
            minesweeperTimer = null;
          }

          function loadMinesweeperRanking(rankingKey) {
            try {
              const ranking = JSON.parse(localStorage.getItem(rankingKey) || "[]");
              return Array.isArray(ranking) ? ranking : [];
            } catch {
              return [];
            }
          }

          function saveMinesweeperScore(playerName) {
            const completedDifficulty = minesweeperDifficulties[minesweeperCompletedDifficultyKey];
            const ranking = loadMinesweeperRanking(completedDifficulty.rankingKey)
              .filter((entry) => entry && entry.name && Number.isFinite(Number(entry.time)));

            ranking.push({
              name: playerName.slice(0, 3),
              time: minesweeperFinalTime,
              difficulty: minesweeperCompletedDifficultyKey,
              playedAt: new Date().toISOString(),
            });
            ranking.sort((left, right) => Number(left.time) - Number(right.time));
            localStorage.setItem(completedDifficulty.rankingKey, JSON.stringify(ranking.slice(0, 10)));
          }

          function resetMinesweeperScoreForm() {
            minesweeperClearModal.hidden = true;
            minesweeperPlayerNameInput.value = "";
            minesweeperScoreSaveMessage.textContent = "";
            minesweeperScoreForm.querySelector('button[type="submit"]').hidden = false;
            minesweeperCanRegisterScore = false;
          }

          function showMinesweeperClearModal() {
            const completedDifficulty = minesweeperDifficulties[minesweeperCompletedDifficultyKey];
            minesweeperClearDifficultyElement.textContent = completedDifficulty.label;
            minesweeperFinalTimeElement.textContent = String(minesweeperFinalTime);
            minesweeperClearModal.hidden = false;
            minesweeperPlayerNameInput.value = "";
            minesweeperScoreSaveMessage.textContent = "";
            minesweeperScoreForm.querySelector('button[type="submit"]').hidden = false;
            minesweeperCanRegisterScore = true;
            minesweeperPlayerNameInput.focus();
          }

          function placeMinesweeperMines(firstOpenIndex) {
            const blockedIndexes = new Set([firstOpenIndex, ...getMinesweeperNeighbors(firstOpenIndex)]);
            const candidates = minesweeperCells
              .map((cell) => cell.index)
              .filter((index) => !blockedIndexes.has(index));

            for (let mineIndex = 0; mineIndex < minesweeperMineCount; mineIndex += 1) {
              const candidateIndex = Math.floor(Math.random() * candidates.length);
              const cellIndex = candidates.splice(candidateIndex, 1)[0];
              minesweeperCells[cellIndex].isMine = true;
            }

            minesweeperCells.forEach((cell) => {
              cell.adjacentMines = getMinesweeperNeighbors(cell.index)
                .filter((neighborIndex) => minesweeperCells[neighborIndex].isMine)
                .length;
            });
          }

          function updateMinesweeperStats() {
            const flaggedCount = minesweeperCells.filter((cell) => cell.isFlagged).length;
            minesweeperMinesLeftElement.textContent = String(Math.max(0, minesweeperMineCount - flaggedCount));
          }

          function renderMinesweeperBoard() {
            minesweeperBoardElement.style.gridTemplateColumns = `repeat(${minesweeperSize}, 1fr)`;
            minesweeperBoardElement.innerHTML = minesweeperCells
              .map((cell) => {
                const classes = ["minesweeper-cell"];
                if (cell.isOpen) {
                  classes.push("is-open");
                }
                if (cell.isFlagged) {
                  classes.push("is-flagged");
                }
                if (cell.isMine && cell.isOpen) {
                  classes.push("is-mine");
                }

                let label = "";
                if (cell.isFlagged && !cell.isOpen) {
                  label = "旗";
                } else if (cell.isOpen && cell.isMine) {
                  label = "地雷";
                } else if (cell.isOpen && cell.adjacentMines > 0) {
                  label = String(cell.adjacentMines);
                } else if (cell.isOpen) {
                  label = "空きマス";
                } else {
                  label = "未開封";
                }

                let content = "";
                if (cell.isFlagged && !cell.isOpen) {
                  content = "F";
                } else if (cell.isOpen && cell.isMine) {
                  content = "*";
                } else if (cell.isOpen && cell.adjacentMines > 0) {
                  content = String(cell.adjacentMines);
                }

                return `<button class="${classes.join(" ")}" type="button" data-cell-index="${cell.index}" aria-label="${label}">${content}</button>`;
              })
              .join("");

            minesweeperBoardElement.querySelectorAll("[data-cell-index]").forEach((button) => {
              button.addEventListener("click", () => {
                openMinesweeperCell(Number(button.dataset.cellIndex));
              });
              button.addEventListener("contextmenu", (event) => {
                event.preventDefault();
                toggleMinesweeperFlag(Number(button.dataset.cellIndex));
              });
            });

            updateMinesweeperStats();
          }

          function openMinesweeperCell(index) {
            if (minesweeperIsGameOver) {
              return;
            }

            const cell = minesweeperCells[index];
            if (cell.isOpen || cell.isFlagged) {
              return;
            }

            if (!minesweeperIsStarted) {
              minesweeperIsStarted = true;
              placeMinesweeperMines(index);
              startMinesweeperTimer();
              minesweeperStatusElement.textContent = "地雷を避けてマスを開いてください";
            }

            cell.isOpen = true;
            minesweeperOpenedCount += 1;

            if (cell.isMine) {
              finishMinesweeperGame(false);
              return;
            }

            if (cell.adjacentMines === 0) {
              getMinesweeperNeighbors(index).forEach(openMinesweeperCell);
            }

            if (minesweeperOpenedCount === minesweeperCells.length - minesweeperMineCount) {
              finishMinesweeperGame(true);
              return;
            }

            renderMinesweeperBoard();
          }

          function toggleMinesweeperFlag(index) {
            if (minesweeperIsGameOver) {
              return;
            }

            const cell = minesweeperCells[index];
            if (cell.isOpen) {
              return;
            }

            cell.isFlagged = !cell.isFlagged;
            renderMinesweeperBoard();
          }

          function finishMinesweeperGame(isWin) {
            minesweeperIsGameOver = true;
            stopMinesweeperTimer();
            if (isWin) {
              minesweeperFinalTime = Math.max(1, minesweeperSeconds);
              minesweeperCompletedDifficultyKey = minesweeperDifficultySelect.value;
            }
            minesweeperCells.forEach((cell) => {
              if (cell.isMine) {
                cell.isOpen = true;
              }
              if (isWin && cell.isMine) {
                cell.isFlagged = true;
              }
            });
            minesweeperStatusElement.textContent = isWin
              ? `クリアです！ ${minesweeperFinalTime} 秒で成功しました`
              : "地雷を踏みました。もう一度挑戦してください";
            renderMinesweeperBoard();
            if (isWin) {
              showMinesweeperClearModal();
            }
          }

          function revealMinesweeperAnswer() {
            if (!minesweeperIsStarted) {
              minesweeperIsStarted = true;
              placeMinesweeperMines(Math.floor(minesweeperCells.length / 2));
            }
            minesweeperIsGameOver = true;
            stopMinesweeperTimer();
            minesweeperCells.forEach((cell) => {
              cell.isOpen = true;
            });
            minesweeperStatusElement.textContent = "答えを表示しました";
            renderMinesweeperBoard();
          }

          function resetMinesweeperGame() {
            stopMinesweeperTimer();
            applyMinesweeperDifficulty();
            resetMinesweeperScoreForm();
            minesweeperCells = createMinesweeperCells();
            minesweeperIsStarted = false;
            minesweeperIsGameOver = false;
            minesweeperOpenedCount = 0;
            minesweeperSeconds = 0;
            minesweeperFinalTime = 0;
            minesweeperTimeElement.textContent = "0";
            minesweeperStatusElement.textContent = "最初のマスをクリックして開始してください";
            renderMinesweeperBoard();
          }

          minesweeperDifficultySelect.addEventListener("change", resetMinesweeperGame);
          minesweeperNewGameButton.addEventListener("click", resetMinesweeperGame);
          minesweeperRevealButton.addEventListener("click", revealMinesweeperAnswer);
          minesweeperPlayAgainButton.addEventListener("click", resetMinesweeperGame);
          minesweeperPlayerNameInput.addEventListener("input", () => {
            minesweeperPlayerNameInput.value = minesweeperPlayerNameInput.value.slice(0, 3).toUpperCase();
          });
          minesweeperScoreForm.addEventListener("submit", (event) => {
            event.preventDefault();
            const playerName = minesweeperPlayerNameInput.value.trim().toUpperCase();
            if (!minesweeperCanRegisterScore) {
              minesweeperScoreSaveMessage.textContent = "このタイムは登録済みです";
              return;
            }
            if (!playerName) {
              minesweeperScoreSaveMessage.textContent = "名前を入力してください";
              return;
            }

            saveMinesweeperScore(playerName);
            minesweeperCanRegisterScore = false;
            minesweeperScoreSaveMessage.textContent = "クリアタイムを登録しました";
            minesweeperScoreForm.querySelector('button[type="submit"]').hidden = true;
          });
          resetMinesweeperGame();
        </script>""",
)
