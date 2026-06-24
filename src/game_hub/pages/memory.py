from ..layout import render_page


MEMORY_HTML = render_page(
    title="神経衰弱 | Ocean Game Hub",
    heading="神経衰弱",
    active_page="trump",
    body_html="""<p>プレイヤー人数を選んで神経衰弱を始めましょう</p>
        <section class="memory-setup" id="memory-setup">
          <label>
            プレイヤー人数
            <select id="memory-player-count">
              <option value="2">2人</option>
              <option value="3">3人</option>
              <option value="4" selected>4人</option>
            </select>
          </label>
          <label>
            CPUの強さ
            <select id="memory-cpu-level">
              <option value="easy">やさしい</option>
              <option value="normal" selected>ふつう</option>
              <option value="hard">つよい</option>
            </select>
          </label>
          <label>
            揃える枚数
            <select id="memory-match-mode">
              <option value="2" selected>2枚ペア</option>
              <option value="4">4枚セット</option>
            </select>
          </label>
          <button class="primary-button" id="memory-start" type="button">ゲーム開始</button>
        </section>
        <section class="memory-table" id="memory-table" hidden>
          <div class="info-card">
            <h3>状態</h3>
            <p id="memory-status">人数を選んでゲームを開始してください</p>
          </div>
          <div class="memory-actions">
            <button class="primary-button" id="memory-reset" type="button">人数設定に戻る</button>
            <a class="primary-button" href="/trump">トランプ選択に戻る</a>
          </div>
          <div class="memory-board" id="memory-board"></div>
          <div class="memory-players" id="memory-players"></div>
        </section>
        <script>
          const memorySetupElement = document.getElementById("memory-setup");
          const memoryTableElement = document.getElementById("memory-table");
          const memoryPlayerCountSelect = document.getElementById("memory-player-count");
          const memoryCpuLevelSelect = document.getElementById("memory-cpu-level");
          const memoryMatchModeSelect = document.getElementById("memory-match-mode");
          const memoryStartButton = document.getElementById("memory-start");
          const memoryResetButton = document.getElementById("memory-reset");
          const memoryStatusElement = document.getElementById("memory-status");
          const memoryBoardElement = document.getElementById("memory-board");
          const memoryPlayersElement = document.getElementById("memory-players");

          const memoryPairs = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10"];
          let memoryPlayers = [];
          let memoryCards = [];
          let memoryCurrentPlayerIndex = 0;
          let memorySelectedIndexes = [];
          let memoryIsLocked = false;
          let memoryIsGameOver = false;
          let memoryCpuTimer = null;
          let memoryCpuLevel = "normal";
          let memoryGroupSize = 2;
          let memoryKnownCards = new Map();

          function createMemoryPlayers(playerCount) {
            return Array.from({ length: playerCount }, (_, index) => ({
              name: index === 0 ? "あなた" : `CPU ${index}`,
              score: 0,
            }));
          }

          function shuffleMemoryCards(cards) {
            for (let index = cards.length - 1; index > 0; index -= 1) {
              const swapIndex = Math.floor(Math.random() * (index + 1));
              [cards[index], cards[swapIndex]] = [cards[swapIndex], cards[index]];
            }
            return cards;
          }

          function createMemoryCards() {
            const activeRanks = memoryGroupSize === 4 ? memoryPairs.slice(0, 5) : memoryPairs;
            return shuffleMemoryCards(
              activeRanks.flatMap((rank) =>
                Array.from({ length: memoryGroupSize }, () => ({
                  rank,
                  isOpen: false,
                  isMatched: false,
                }))
              )
            );
          }

          function getCurrentMemoryPlayer() {
            return memoryPlayers[memoryCurrentPlayerIndex];
          }

          function getRemainingMemoryIndexes() {
            return memoryCards
              .map((card, index) => ({ card, index }))
              .filter(({ card }) => !card.isMatched && !card.isOpen)
              .map(({ index }) => index);
          }

          function rememberMemoryCard(cardIndex) {
            const card = memoryCards[cardIndex];
            if (!card) {
              return;
            }
            memoryKnownCards.set(cardIndex, card.rank);
          }

          function getKnownMemorySet(requiredCount = memoryGroupSize) {
            const knownByRank = new Map();
            memoryKnownCards.forEach((rank, cardIndex) => {
              const card = memoryCards[cardIndex];
              if (!card || card.isMatched || card.isOpen) {
                return;
              }

              const indexes = knownByRank.get(rank) || [];
              indexes.push(cardIndex);
              knownByRank.set(rank, indexes);
            });

            for (const indexes of knownByRank.values()) {
              if (indexes.length >= requiredCount) {
                return indexes.slice(0, requiredCount);
              }
            }
            return null;
          }

          function shouldUseMemory(chance) {
            if (memoryCpuLevel === "hard") {
              return true;
            }
            if (memoryCpuLevel === "normal") {
              return Math.random() < chance;
            }
            return false;
          }

          function chooseCpuFirstMemoryIndex(availableIndexes) {
            const knownSet = getKnownMemorySet();
            if (knownSet && shouldUseMemory(0.6)) {
              return knownSet[0];
            }
            return availableIndexes[Math.floor(Math.random() * availableIndexes.length)];
          }

          function chooseCpuNextMemoryIndex(selectedIndexes, availableIndexes) {
            const firstIndex = selectedIndexes[0];
            const firstRank = memoryCards[firstIndex].rank;
            const knownMatchIndex = availableIndexes.find((cardIndex) => {
              const card = memoryCards[cardIndex];
              return (
                memoryKnownCards.get(cardIndex) === firstRank
                && card
                && !card.isMatched
                && !card.isOpen
                && !selectedIndexes.includes(cardIndex)
              );
            });

            if (knownMatchIndex !== undefined && shouldUseMemory(0.75)) {
              return knownMatchIndex;
            }
            return availableIndexes[Math.floor(Math.random() * availableIndexes.length)];
          }

          function advanceMemoryTurn(message = "") {
            if (checkMemoryGameOver()) {
              return;
            }

            memoryCurrentPlayerIndex = (memoryCurrentPlayerIndex + 1) % memoryPlayers.length;
            const currentPlayer = getCurrentMemoryPlayer();
            memoryStatusElement.textContent = message
              ? `${message} ${currentPlayer.name} の番です`
              : `${currentPlayer.name} の番です`;
            renderMemory();
            scheduleMemoryCpuTurn();
          }

          function checkMemoryGameOver() {
            if (!memoryCards.length || memoryCards.some((card) => !card.isMatched)) {
              return false;
            }

            memoryIsGameOver = true;
            clearTimeout(memoryCpuTimer);
            memoryCpuTimer = null;
            const highScore = Math.max(...memoryPlayers.map((player) => player.score));
            const winners = memoryPlayers
              .filter((player) => player.score === highScore)
              .map((player) => player.name)
              .join("、");
            memoryStatusElement.textContent = `ゲーム終了。勝者: ${winners}（${highScore}組）`;
            renderMemory();
            return true;
          }

          function resolveMemorySelection() {
            const selectedCards = memorySelectedIndexes.map((cardIndex) => memoryCards[cardIndex]);
            const firstCard = selectedCards[0];
            const currentPlayer = getCurrentMemoryPlayer();

            if (selectedCards.every((card) => card.rank === firstCard.rank)) {
              selectedCards.forEach((card) => {
                card.isMatched = true;
              });
              currentPlayer.score += 1;
              memorySelectedIndexes = [];
              memoryIsLocked = false;
              memoryStatusElement.textContent = `${currentPlayer.name} が ${firstCard.rank} を${memoryGroupSize}枚揃えました。もう一度めくれます`;
              renderMemory();
              if (!checkMemoryGameOver()) {
                scheduleMemoryCpuTurn();
              }
              return;
            }

            setTimeout(() => {
              selectedCards.forEach((card) => {
                card.isOpen = false;
              });
              memorySelectedIndexes = [];
              memoryIsLocked = false;
              advanceMemoryTurn(`${currentPlayer.name} は揃えられませんでした。`);
            }, 1000);
          }

          function flipMemoryCard(cardIndex) {
            if (memoryIsLocked || memoryIsGameOver || memorySelectedIndexes.includes(cardIndex)) {
              return;
            }

            const card = memoryCards[cardIndex];
            if (!card || card.isOpen || card.isMatched) {
              return;
            }

            card.isOpen = true;
            rememberMemoryCard(cardIndex);
            memorySelectedIndexes.push(cardIndex);
            renderMemory();

            if (memorySelectedIndexes.length === memoryGroupSize) {
              memoryIsLocked = true;
              resolveMemorySelection();
            }
          }

          function flipMemoryIndexesSequentially(indexes, delay = 650) {
            const [firstIndex, ...restIndexes] = indexes;
            flipMemoryCard(firstIndex);
            if (restIndexes.length === 0) {
              return;
            }

            setTimeout(() => {
              flipMemoryIndexesSequentially(restIndexes, delay);
            }, delay);
          }

          function cpuMemoryTurn() {
            if (memoryIsGameOver || memoryCurrentPlayerIndex === 0 || memoryIsLocked) {
              return;
            }

            const availableIndexes = getRemainingMemoryIndexes();
            if (availableIndexes.length < memoryGroupSize) {
              checkMemoryGameOver();
              return;
            }

            const knownSet = getKnownMemorySet();
            if (knownSet && shouldUseMemory(0.6)) {
              flipMemoryIndexesSequentially(knownSet);
              return;
            }

            const selectedIndexes = [chooseCpuFirstMemoryIndex(availableIndexes)];
            flipMemoryCard(selectedIndexes[0]);

            function chooseNextCard() {
              const nextIndexes = getRemainingMemoryIndexes();
              if (nextIndexes.length === 0 || selectedIndexes.length >= memoryGroupSize) {
                checkMemoryGameOver();
                return;
              }

              const nextIndex = chooseCpuNextMemoryIndex(selectedIndexes, nextIndexes);
              selectedIndexes.push(nextIndex);
              flipMemoryCard(nextIndex);
              if (selectedIndexes.length < memoryGroupSize) {
                setTimeout(chooseNextCard, 650);
              }
            }

            setTimeout(chooseNextCard, 650);
          }

          function scheduleMemoryCpuTurn() {
            if (memoryCpuTimer || memoryIsGameOver || memoryCurrentPlayerIndex === 0 || memoryIsLocked) {
              return;
            }

            memoryCpuTimer = setTimeout(() => {
              memoryCpuTimer = null;
              cpuMemoryTurn();
            }, 800);
          }

          function renderMemoryBoard() {
            memoryBoardElement.innerHTML = memoryCards.map((card, cardIndex) => {
              const visible = card.isOpen || card.isMatched || memoryIsGameOver;
              const classes = [
                "memory-card",
                card.isOpen ? "is-open" : "",
                card.isMatched ? "is-matched" : "",
              ].filter(Boolean).join(" ");
              return `<button class="${classes}" type="button" data-card-index="${cardIndex}">${visible ? card.rank : "?"}</button>`;
            }).join("");

            memoryBoardElement.querySelectorAll("[data-card-index]").forEach((button) => {
              button.addEventListener("click", () => {
                if (memoryCurrentPlayerIndex !== 0) {
                  return;
                }
                flipMemoryCard(Number(button.dataset.cardIndex));
              });
            });
          }

          function renderMemoryPlayers() {
            memoryPlayersElement.innerHTML = memoryPlayers.map((player, playerIndex) => {
              const activeClass = playerIndex === memoryCurrentPlayerIndex && !memoryIsGameOver ? " is-active" : "";
              return `<section class="memory-player${activeClass}">
                <h3>${player.name}</h3>
                <p>獲得: ${player.score}組</p>
              </section>`;
            }).join("");
          }

          function renderMemory() {
            renderMemoryBoard();
            renderMemoryPlayers();
          }

          function startMemoryGame() {
            const playerCount = Number(memoryPlayerCountSelect.value);
            memoryCpuLevel = memoryCpuLevelSelect.value;
            memoryGroupSize = Number(memoryMatchModeSelect.value);
            memoryPlayers = createMemoryPlayers(playerCount);
            memoryCards = createMemoryCards();
            memoryCurrentPlayerIndex = 0;
            memorySelectedIndexes = [];
            memoryIsLocked = false;
            memoryIsGameOver = false;
            clearTimeout(memoryCpuTimer);
            memoryCpuTimer = null;
            memoryKnownCards = new Map();

            memorySetupElement.hidden = true;
            memoryTableElement.hidden = false;
            const levelLabel = memoryCpuLevelSelect.options[memoryCpuLevelSelect.selectedIndex].textContent;
            const modeLabel = memoryMatchModeSelect.options[memoryMatchModeSelect.selectedIndex].textContent;
            memoryStatusElement.textContent = `あなたの番です。カードを${memoryGroupSize}枚めくってください（CPU: ${levelLabel} / ${modeLabel}）`;
            renderMemory();
          }

          function resetMemoryGame() {
            clearTimeout(memoryCpuTimer);
            memoryPlayers = [];
            memoryCards = [];
            memoryCurrentPlayerIndex = 0;
            memorySelectedIndexes = [];
            memoryIsLocked = false;
            memoryIsGameOver = false;
            memoryCpuTimer = null;
            memoryCpuLevel = "normal";
            memoryGroupSize = 2;
            memoryKnownCards = new Map();
            memorySetupElement.hidden = false;
            memoryTableElement.hidden = true;
            memoryStatusElement.textContent = "人数を選んでゲームを開始してください";
            memoryBoardElement.innerHTML = "";
            memoryPlayersElement.innerHTML = "";
          }

          memoryStartButton.addEventListener("click", startMemoryGame);
          memoryResetButton.addEventListener("click", resetMemoryGame);
        </script>""",
)
