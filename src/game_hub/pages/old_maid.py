from ..layout import render_page


OLD_MAID_HTML = render_page(
    title="ババ抜き | Ocean Game Hub",
    heading="ババ抜き",
    active_page="trump",
    body_html="""<p>プレイヤー人数を選んでババ抜きを始めましょう</p>
        <section class="old-maid-setup" id="old-maid-setup">
          <label>
            プレイヤー人数
            <select id="old-maid-player-count">
              <option value="2">2人</option>
              <option value="3">3人</option>
              <option value="4" selected>4人</option>
              <option value="5">5人</option>
              <option value="6">6人</option>
            </select>
          </label>
          <button class="primary-button" id="old-maid-start" type="button">ゲーム開始</button>
        </section>
        <section class="old-maid-table" id="old-maid-table" hidden>
          <div class="info-card">
            <h3>状態</h3>
            <p id="old-maid-status">人数を選んでゲームを開始してください</p>
          </div>
          <div class="old-maid-actions">
            <button class="primary-button" id="old-maid-next" type="button" hidden>CPUのターンを進める</button>
            <button class="primary-button" id="old-maid-reset" type="button">人数設定に戻る</button>
          </div>
          <div class="old-maid-players" id="old-maid-players"></div>
        </section>
        <script>
          const setupElement = document.getElementById("old-maid-setup");
          const tableElement = document.getElementById("old-maid-table");
          const playerCountSelect = document.getElementById("old-maid-player-count");
          const startButton = document.getElementById("old-maid-start");
          const resetButton = document.getElementById("old-maid-reset");
          const nextButton = document.getElementById("old-maid-next");
          const statusElement = document.getElementById("old-maid-status");
          const playersElement = document.getElementById("old-maid-players");

          const ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"];
          const suits = ["♠", "♥", "♦", "♣"];
          let players = [];
          let currentPlayerIndex = 0;
          let finishedOrder = [];
          let cpuTimer = null;
          let isGameOver = false;

          function createDeck() {
            const deck = [];
            ranks.forEach((rank) => {
              suits.forEach((suit) => {
                deck.push({
                  rank,
                  suit,
                  label: `${rank}${suit}`,
                  isJoker: false,
                });
              });
            });
            deck.push({
              rank: "JOKER",
              suit: "",
              label: "Joker",
              isJoker: true,
            });
            return deck;
          }

          function shuffle(cards) {
            for (let index = cards.length - 1; index > 0; index -= 1) {
              const swapIndex = Math.floor(Math.random() * (index + 1));
              [cards[index], cards[swapIndex]] = [cards[swapIndex], cards[index]];
            }
            return cards;
          }

          function createPlayers(playerCount) {
            return Array.from({ length: playerCount }, (_, index) => ({
              name: index === 0 ? "あなた" : `CPU ${index}`,
              hand: [],
              isOut: false,
              finishedRank: null,
            }));
          }

          function dealCards(deck) {
            deck.forEach((card, index) => {
              players[index % players.length].hand.push(card);
            });
          }

          function markPlayerOut(player) {
            if (player.hand.length > 0 || player.finishedRank !== null) {
              return;
            }

            finishedOrder.push(player.name);
            player.isOut = true;
            player.finishedRank = finishedOrder.length;
          }

          function removePairs(player) {
            const rankCounts = new Map();
            player.hand.forEach((card) => {
              if (card.isJoker) {
                return;
              }
              rankCounts.set(card.rank, (rankCounts.get(card.rank) || 0) + 1);
            });

            const removeByRank = new Map();
            rankCounts.forEach((count, rank) => {
              removeByRank.set(rank, count - (count % 2));
            });

            player.hand = player.hand.filter((card) => {
              const removableCount = removeByRank.get(card.rank) || 0;
              if (card.isJoker || removableCount <= 0) {
                return true;
              }
              removeByRank.set(card.rank, removableCount - 1);
              return false;
            });

            markPlayerOut(player);
          }

          function removeAllPairs() {
            players.forEach(removePairs);
          }

          function getActivePlayers() {
            return players.filter((player) => !player.isOut);
          }

          function normalizeCurrentPlayer() {
            if (getActivePlayers().length <= 1) {
              return;
            }

            while (players[currentPlayerIndex].isOut) {
              currentPlayerIndex = (currentPlayerIndex + 1) % players.length;
            }
          }

          function findNextOpponentIndex(playerIndex) {
            for (let offset = 1; offset < players.length; offset += 1) {
              const nextIndex = (playerIndex + offset) % players.length;
              if (!players[nextIndex].isOut && players[nextIndex].hand.length > 0) {
                return nextIndex;
              }
            }
            return -1;
          }

          function getGameResult() {
            const activePlayers = getActivePlayers();
            if (activePlayers.length > 1) {
              return "";
            }

            const loser = activePlayers[0];
            if (!loser) {
              return "全員あがりました";
            }
            const loserRank = players.length;
            return `${loser.name} がババを持って負けです。最終順位: ${loserRank}位`;
          }

          function checkGameOver() {
            if (getActivePlayers().length > 1) {
              return false;
            }

            const loser = getActivePlayers()[0];
            if (loser && loser.finishedRank === null) {
              loser.finishedRank = players.length;
            }

            isGameOver = true;
            nextButton.hidden = true;
            statusElement.textContent = getGameResult();
            render();
            return true;
          }

          function advanceTurn(extraMessage = "") {
            if (checkGameOver()) {
              return;
            }

            currentPlayerIndex = (currentPlayerIndex + 1) % players.length;
            normalizeCurrentPlayer();

            const currentPlayer = players[currentPlayerIndex];
            const opponentIndex = findNextOpponentIndex(currentPlayerIndex);
            const opponent = players[opponentIndex];
            const turnMessage = `${currentPlayer.name} の番です。${opponent.name} からカードを引きます`;
            statusElement.textContent = extraMessage ? `${extraMessage} ${turnMessage}` : turnMessage;
            nextButton.hidden = true;
            render();
            scheduleCpuDraw();
          }

          function drawCard(playerIndex, opponentIndex, cardIndex) {
            const player = players[playerIndex];
            const opponent = players[opponentIndex];
            const [card] = opponent.hand.splice(cardIndex, 1);
            player.hand.push(card);
            removePairs(player);
            removePairs(opponent);
            advanceTurn(`${player.name} が1枚引きました。`);
          }

          function cpuDraw() {
            if (isGameOver || currentPlayerIndex === 0) {
              return;
            }

            const opponentIndex = findNextOpponentIndex(currentPlayerIndex);
            if (opponentIndex < 0) {
              checkGameOver();
              return;
            }

            const opponent = players[opponentIndex];
            const cardIndex = Math.floor(Math.random() * opponent.hand.length);
            drawCard(currentPlayerIndex, opponentIndex, cardIndex);
          }

          function scheduleCpuDraw() {
            if (cpuTimer || isGameOver || currentPlayerIndex === 0) {
              return;
            }

            cpuTimer = setTimeout(() => {
              cpuTimer = null;
              cpuDraw();
            }, 750);
          }

          function renderPlayer(player, playerIndex) {
            const isCurrentPlayer = playerIndex === currentPlayerIndex && !isGameOver;
            const opponentIndex = findNextOpponentIndex(currentPlayerIndex);
            const isDrawableOpponent = currentPlayerIndex === 0 && playerIndex === opponentIndex && !isGameOver;
            const rankLabel = player.finishedRank
              ? `<span class="old-maid-rank">${player.finishedRank}位であがり</span>`
              : player.isOut
                ? '<span class="old-maid-rank">あがり</span>'
                : `残り ${player.hand.length} 枚`;
            const handContent = player.hand.map((card, cardIndex) => {
              if (playerIndex === 0 || isGameOver) {
                const jokerClass = card.isJoker ? " is-joker" : "";
                return `<span class="old-maid-card${jokerClass}">${card.label}</span>`;
              }

              if (isDrawableOpponent) {
                return `<button class="old-maid-card-back" type="button" data-card-index="${cardIndex}">?</button>`;
              }

              return '<span class="old-maid-card-back">?</span>';
            }).join("");

            return `<section class="old-maid-player${isCurrentPlayer ? " is-active" : ""}">
              <h3>${player.name}</h3>
              <p>${rankLabel}</p>
              <div class="old-maid-card-row">${handContent || "<p>手札なし</p>"}</div>
            </section>`;
          }

          function render() {
            playersElement.innerHTML = players.map(renderPlayer).join("");
            playersElement.querySelectorAll("[data-card-index]").forEach((button) => {
              button.addEventListener("click", () => {
                if (currentPlayerIndex !== 0 || isGameOver) {
                  return;
                }

                const opponentIndex = findNextOpponentIndex(0);
                drawCard(0, opponentIndex, Number(button.dataset.cardIndex));
              });
            });
          }

          function startGame() {
            const playerCount = Number(playerCountSelect.value);
            players = createPlayers(playerCount);
            currentPlayerIndex = 0;
            finishedOrder = [];
            clearTimeout(cpuTimer);
            cpuTimer = null;
            isGameOver = false;

            dealCards(shuffle(createDeck()));
            removeAllPairs();
            normalizeCurrentPlayer();

            setupElement.hidden = true;
            tableElement.hidden = false;
            nextButton.hidden = true;
            statusElement.textContent = "あなたの番です。右隣の相手からカードを1枚選んでください";
            render();
            if (!checkGameOver()) {
              scheduleCpuDraw();
            }
          }

          function resetGame() {
            clearTimeout(cpuTimer);
            players = [];
            currentPlayerIndex = 0;
            finishedOrder = [];
            cpuTimer = null;
            isGameOver = false;
            setupElement.hidden = false;
            tableElement.hidden = true;
            nextButton.hidden = true;
            statusElement.textContent = "人数を選んでゲームを開始してください";
            playersElement.innerHTML = "";
          }

          startButton.addEventListener("click", startGame);
          resetButton.addEventListener("click", resetGame);
          nextButton.addEventListener("click", cpuDraw);
        </script>""",
)
