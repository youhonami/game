from ..layout import render_page


SEVENS_HTML = render_page(
    title="七並べ | Ocean Game Hub",
    heading="七並べ",
    active_page="trump",
    body_html="""<p>プレイヤー人数を選んで七並べを始めましょう</p>
        <section class="sevens-setup" id="sevens-setup">
          <label>
            プレイヤー人数
            <select id="sevens-player-count">
              <option value="2">2人</option>
              <option value="3">3人</option>
              <option value="4" selected>4人</option>
              <option value="5">5人</option>
              <option value="6">6人</option>
            </select>
          </label>
          <button class="primary-button" id="sevens-start" type="button">ゲーム開始</button>
        </section>
        <section class="sevens-table" id="sevens-table" hidden>
          <div class="info-card">
            <h3>状態</h3>
            <p id="sevens-status">人数を選んでゲームを開始してください</p>
          </div>
          <div class="sevens-actions">
            <button class="primary-button" id="sevens-pass" type="button">パス</button>
            <button class="primary-button" id="sevens-next" type="button" hidden>CPUのターンを進める</button>
            <button class="primary-button" id="sevens-reset" type="button">人数設定に戻る</button>
          </div>
          <div class="sevens-board" id="sevens-board"></div>
          <div>
            <div class="info-card">
              <h3>あなたの手札</h3>
              <p>出せるカードは光ります。クリックして場に出してください。</p>
            </div>
            <div class="sevens-hand" id="sevens-hand"></div>
          </div>
          <div class="sevens-players" id="sevens-players"></div>
        </section>
        <script>
          const sevensSetupElement = document.getElementById("sevens-setup");
          const sevensTableElement = document.getElementById("sevens-table");
          const sevensPlayerCountSelect = document.getElementById("sevens-player-count");
          const sevensStartButton = document.getElementById("sevens-start");
          const sevensResetButton = document.getElementById("sevens-reset");
          const sevensPassButton = document.getElementById("sevens-pass");
          const sevensNextButton = document.getElementById("sevens-next");
          const sevensStatusElement = document.getElementById("sevens-status");
          const sevensBoardElement = document.getElementById("sevens-board");
          const sevensHandElement = document.getElementById("sevens-hand");
          const sevensPlayersElement = document.getElementById("sevens-players");

          const sevensRanks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"];
          const sevensSuits = ["♠", "♥", "♦", "♣"];
          let sevensPlayers = [];
          let sevensBoard = {};
          let sevensCurrentPlayerIndex = 0;
          let sevensFinishedOrder = [];
          let sevensCpuTimer = null;
          let sevensIsGameOver = false;

          function createSevensDeck() {
            const deck = [];
            sevensSuits.forEach((suit) => {
              sevensRanks.forEach((rank, rankIndex) => {
                deck.push({
                  suit,
                  rank,
                  rankIndex,
                  label: `${rank}${suit}`,
                });
              });
            });
            return deck;
          }

          function shuffleSevensCards(cards) {
            for (let index = cards.length - 1; index > 0; index -= 1) {
              const swapIndex = Math.floor(Math.random() * (index + 1));
              [cards[index], cards[swapIndex]] = [cards[swapIndex], cards[index]];
            }
            return cards;
          }

          function createSevensPlayers(playerCount) {
            return Array.from({ length: playerCount }, (_, index) => ({
              name: index === 0 ? "あなた" : `CPU ${index}`,
              hand: [],
              isOut: false,
              finishedRank: null,
              passCount: 0,
            }));
          }

          function createSevensBoard() {
            return Object.fromEntries(
              sevensSuits.map((suit) => [
                suit,
                { low: 6, high: 6, cards: new Set([6]) },
              ])
            );
          }

          function dealSevensCards(deck) {
            deck.forEach((card, index) => {
              if (card.rankIndex === 6) {
                return;
              }
              sevensPlayers[index % sevensPlayers.length].hand.push(card);
            });
            sevensPlayers.forEach(sortSevensHand);
          }

          function sortSevensHand(player) {
            player.hand.sort((left, right) => {
              const suitDiff = sevensSuits.indexOf(left.suit) - sevensSuits.indexOf(right.suit);
              return suitDiff || left.rankIndex - right.rankIndex;
            });
          }

          function isSevensRed(cardOrSuit) {
            const suit = typeof cardOrSuit === "string" ? cardOrSuit : cardOrSuit.suit;
            return suit === "♥" || suit === "♦";
          }

          function canPlaySevensCard(card) {
            const suitBoard = sevensBoard[card.suit];
            return card.rankIndex === suitBoard.low - 1 || card.rankIndex === suitBoard.high + 1;
          }

          function getPlayableSevensCards(player) {
            if (player.isOut) {
              return [];
            }
            return player.hand.filter(canPlaySevensCard);
          }

          function markSevensPlayerOut(player) {
            if (player.hand.length > 0 || player.finishedRank !== null) {
              return;
            }
            sevensFinishedOrder.push(player.name);
            player.isOut = true;
            player.finishedRank = sevensFinishedOrder.length;
          }

          function getActiveSevensPlayers() {
            return sevensPlayers.filter((player) => !player.isOut);
          }

          function normalizeSevensCurrentPlayer() {
            if (getActiveSevensPlayers().length === 0) {
              return;
            }
            while (sevensPlayers[sevensCurrentPlayerIndex].isOut) {
              sevensCurrentPlayerIndex = (sevensCurrentPlayerIndex + 1) % sevensPlayers.length;
            }
          }

          function getSevensResult() {
            const loserNames = sevensPlayers
              .filter((player) => !player.isOut)
              .map((player) => player.name);
            if (loserNames.length === 0) {
              return "全員があがりました";
            }
            return `ゲーム終了。未完了: ${loserNames.join("、")}`;
          }

          function checkSevensGameOver() {
            if (sevensPlayers.every((player) => player.isOut)) {
              sevensIsGameOver = true;
            }

            const playableExists = sevensPlayers.some((player) => getPlayableSevensCards(player).length > 0);
            if (!playableExists && getActiveSevensPlayers().length > 0) {
              sevensIsGameOver = true;
            }

            if (!sevensIsGameOver) {
              return false;
            }

            sevensPassButton.hidden = true;
            sevensNextButton.hidden = true;
            sevensStatusElement.textContent = getSevensResult();
            renderSevens();
            return true;
          }

          function advanceSevensTurn(message = "") {
            if (checkSevensGameOver()) {
              return;
            }

            sevensCurrentPlayerIndex = (sevensCurrentPlayerIndex + 1) % sevensPlayers.length;
            normalizeSevensCurrentPlayer();
            const player = sevensPlayers[sevensCurrentPlayerIndex];
            const playableCards = getPlayableSevensCards(player);
            const turnMessage = playableCards.length > 0
              ? `${player.name} の番です。出せるカードがあります`
              : `${player.name} の番です。出せるカードがないためパスします`;
            sevensStatusElement.textContent = message ? `${message} ${turnMessage}` : turnMessage;
            renderSevens();
            scheduleSevensCpuTurn();
          }

          function playSevensCard(playerIndex, handIndex) {
            if (sevensIsGameOver) {
              return;
            }

            const player = sevensPlayers[playerIndex];
            const card = player.hand[handIndex];
            if (!card || !canPlaySevensCard(card)) {
              return;
            }

            player.hand.splice(handIndex, 1);
            const suitBoard = sevensBoard[card.suit];
            suitBoard.cards.add(card.rankIndex);
            suitBoard.low = Math.min(suitBoard.low, card.rankIndex);
            suitBoard.high = Math.max(suitBoard.high, card.rankIndex);
            player.passCount = 0;
            markSevensPlayerOut(player);
            advanceSevensTurn(`${player.name} が ${card.label} を出しました。`);
          }

          function passSevensTurn() {
            if (sevensIsGameOver) {
              return;
            }

            const player = sevensPlayers[sevensCurrentPlayerIndex];
            const playableCards = getPlayableSevensCards(player);
            if (playableCards.length > 0 && sevensCurrentPlayerIndex === 0) {
              sevensStatusElement.textContent = "出せるカードがあります。カードを出してください";
              renderSevens();
              return;
            }

            player.passCount += 1;
            advanceSevensTurn(`${player.name} がパスしました。`);
          }

          function cpuPlaySevensTurn() {
            if (sevensIsGameOver || sevensCurrentPlayerIndex === 0) {
              return;
            }

            const player = sevensPlayers[sevensCurrentPlayerIndex];
            const playableCards = getPlayableSevensCards(player);
            if (playableCards.length === 0) {
              passSevensTurn();
              return;
            }

            const selectedCard = playableCards
              .slice()
              .sort((left, right) => Math.abs(left.rankIndex - 6) - Math.abs(right.rankIndex - 6))[0];
            playSevensCard(sevensCurrentPlayerIndex, player.hand.indexOf(selectedCard));
          }

          function scheduleSevensCpuTurn() {
            if (sevensCpuTimer || sevensIsGameOver || sevensCurrentPlayerIndex === 0) {
              return;
            }

            sevensCpuTimer = setTimeout(() => {
              sevensCpuTimer = null;
              cpuPlaySevensTurn();
            }, 750);
          }

          function renderSevensBoard() {
            sevensBoardElement.innerHTML = sevensSuits.map((suit) => {
              const suitBoard = sevensBoard[suit];
              const rowCards = sevensRanks.map((rank, rankIndex) => {
                if (!suitBoard.cards.has(rankIndex)) {
                  return '<span class="sevens-slot"></span>';
                }
                const redClass = isSevensRed(suit) ? " is-red" : "";
                return `<span class="sevens-card${redClass}">${rank}${suit}</span>`;
              }).join("");
              return `<div class="sevens-row"><span class="sevens-suit">${suit}</span>${rowCards}</div>`;
            }).join("");
          }

          function renderSevensHand() {
            const player = sevensPlayers[0];
            const playableCards = getPlayableSevensCards(player);
            sevensHandElement.innerHTML = player.hand.map((card, handIndex) => {
              const redClass = isSevensRed(card) ? " is-red" : "";
              const playableClass = playableCards.includes(card) && sevensCurrentPlayerIndex === 0 && !sevensIsGameOver
                ? " is-playable"
                : "";
              return `<button class="sevens-card${redClass}${playableClass}" type="button" data-hand-index="${handIndex}">${card.label}</button>`;
            }).join("") || "<p>手札なし</p>";

            sevensHandElement.querySelectorAll("[data-hand-index]").forEach((button) => {
              button.addEventListener("click", () => {
                if (sevensCurrentPlayerIndex !== 0 || sevensIsGameOver) {
                  return;
                }
                playSevensCard(0, Number(button.dataset.handIndex));
              });
            });
          }

          function renderSevensPlayers() {
            sevensPlayersElement.innerHTML = sevensPlayers.map((player, playerIndex) => {
              const isActive = playerIndex === sevensCurrentPlayerIndex && !sevensIsGameOver;
              const rankLabel = player.finishedRank ? `${player.finishedRank}位であがり` : `残り ${player.hand.length} 枚`;
              return `<section class="sevens-player${isActive ? " is-active" : ""}">
                <h3>${player.name}</h3>
                <p>${rankLabel}</p>
                <p>パス: ${player.passCount}回</p>
              </section>`;
            }).join("");
          }

          function renderSevens() {
            renderSevensBoard();
            renderSevensHand();
            renderSevensPlayers();
            sevensPassButton.hidden = sevensIsGameOver || sevensCurrentPlayerIndex !== 0;
            sevensNextButton.hidden = true;
          }

          function startSevensGame() {
            const playerCount = Number(sevensPlayerCountSelect.value);
            sevensPlayers = createSevensPlayers(playerCount);
            sevensBoard = createSevensBoard();
            sevensCurrentPlayerIndex = 0;
            sevensFinishedOrder = [];
            sevensCpuTimer = null;
            sevensIsGameOver = false;

            dealSevensCards(shuffleSevensCards(createSevensDeck()));
            normalizeSevensCurrentPlayer();
            sevensSetupElement.hidden = true;
            sevensTableElement.hidden = false;
            sevensStatusElement.textContent = "あなたの番です。出せるカードをクリックしてください";
            renderSevens();
            if (!checkSevensGameOver()) {
              scheduleSevensCpuTurn();
            }
          }

          function resetSevensGame() {
            clearTimeout(sevensCpuTimer);
            sevensPlayers = [];
            sevensBoard = {};
            sevensCurrentPlayerIndex = 0;
            sevensFinishedOrder = [];
            sevensCpuTimer = null;
            sevensIsGameOver = false;
            sevensSetupElement.hidden = false;
            sevensTableElement.hidden = true;
            sevensStatusElement.textContent = "人数を選んでゲームを開始してください";
            sevensBoardElement.innerHTML = "";
            sevensHandElement.innerHTML = "";
            sevensPlayersElement.innerHTML = "";
          }

          sevensStartButton.addEventListener("click", startSevensGame);
          sevensResetButton.addEventListener("click", resetSevensGame);
          sevensPassButton.addEventListener("click", passSevensTurn);
          sevensNextButton.addEventListener("click", cpuPlaySevensTurn);
        </script>""",
)
