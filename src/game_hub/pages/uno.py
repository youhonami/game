from ..layout import render_page


UNO_HTML = render_page(
    title="UNO | Ocean Game Hub",
    heading="UNO",
    active_page="uno",
    body_html="""<p>プレイヤー人数を選んでUNOを始めましょう。あなた以外はCPUが自動で進みます。</p>
        <section class="uno-setup" id="uno-setup">
          <label>
            プレイヤー人数
            <select id="uno-player-count">
              <option value="2">2人</option>
              <option value="3" selected>3人</option>
              <option value="4">4人</option>
            </select>
          </label>
          <button class="primary-button" id="uno-start" type="button">ゲーム開始</button>
        </section>
        <section class="uno-table" id="uno-table" hidden>
          <div class="info-card">
            <h3>状態</h3>
            <p id="uno-status">人数を選んでゲームを開始してください</p>
          </div>
          <div class="uno-actions">
            <button class="primary-button" id="uno-draw" type="button">山札から引く</button>
            <label>
              ワイルドの色
              <select class="uno-color-select" id="uno-color-choice">
                <option value="red">赤</option>
                <option value="blue">青</option>
                <option value="green">緑</option>
                <option value="yellow">黄</option>
              </select>
            </label>
            <button class="primary-button" id="uno-reset" type="button">人数設定に戻る</button>
            <button class="primary-button" id="uno-new-game" type="button">同じ人数でもう一度</button>
          </div>
          <div class="uno-board">
            <div class="uno-seat uno-seat-top" id="uno-seat-top"></div>
            <div class="uno-seat uno-seat-left" id="uno-seat-left"></div>
            <div class="uno-center">
              <div class="uno-deck-area">
                <h3>山札</h3>
                <p id="uno-deck-count">0枚</p>
                <div class="uno-card-back">UNO</div>
              </div>
              <div class="uno-discard">
                <h3>場札</h3>
                <div id="uno-discard"></div>
                <p>現在の色: <span id="uno-current-color">-</span></p>
              </div>
            </div>
            <div class="uno-seat uno-seat-right" id="uno-seat-right"></div>
            <div class="uno-seat uno-seat-bottom" id="uno-seat-bottom">
              <div class="uno-player">
                <h3>あなた</h3>
                <p>手札: 0枚</p>
              </div>
              <div class="uno-hand" id="uno-hand"></div>
            </div>
          </div>
          <div class="info-card">
            <h3>遊び方</h3>
            <p>中央の山札からカードを引けます。下があなた、CPUは上・左・右に配置されます。出せるカードをクリックしてください。</p>
          </div>
        </section>
        <script>
          const unoSetupElement = document.getElementById("uno-setup");
          const unoTableElement = document.getElementById("uno-table");
          const unoPlayerCountSelect = document.getElementById("uno-player-count");
          const unoStartButton = document.getElementById("uno-start");
          const unoResetButton = document.getElementById("uno-reset");
          const unoNewGameButton = document.getElementById("uno-new-game");
          const unoDrawButton = document.getElementById("uno-draw");
          const unoColorChoiceSelect = document.getElementById("uno-color-choice");
          const unoStatusElement = document.getElementById("uno-status");
          const unoDeckCountElement = document.getElementById("uno-deck-count");
          const unoDiscardElement = document.getElementById("uno-discard");
          const unoCurrentColorElement = document.getElementById("uno-current-color");
          const unoHandElement = document.getElementById("uno-hand");
          const unoSeatTopElement = document.getElementById("uno-seat-top");
          const unoSeatLeftElement = document.getElementById("uno-seat-left");
          const unoSeatRightElement = document.getElementById("uno-seat-right");
          const unoSeatBottomElement = document.getElementById("uno-seat-bottom");

          const unoColors = ["red", "blue", "green", "yellow"];
          const unoColorLabels = {
            red: "赤",
            blue: "青",
            green: "緑",
            yellow: "黄",
            wild: "ワイルド",
          };
          let unoPlayers = [];
          let unoDeck = [];
          let unoDiscardPile = [];
          let unoCurrentColor = "red";
          let unoCurrentPlayerIndex = 0;
          let unoDirection = 1;
          let unoCpuTimer = null;
          let unoIsGameOver = false;

          function createUnoCard(color, value) {
            return {
              color,
              value,
              label: value,
              id: `${color}-${value}-${Math.random().toString(36).slice(2)}`,
            };
          }

          function createUnoDeck() {
            const deck = [];
            unoColors.forEach((color) => {
              deck.push(createUnoCard(color, "0"));
              for (let number = 1; number <= 9; number += 1) {
                deck.push(createUnoCard(color, String(number)));
                deck.push(createUnoCard(color, String(number)));
              }
              ["Skip", "Reverse", "+2"].forEach((action) => {
                deck.push(createUnoCard(color, action));
                deck.push(createUnoCard(color, action));
              });
            });
            for (let index = 0; index < 4; index += 1) {
              deck.push(createUnoCard("wild", "Wild"));
              deck.push(createUnoCard("wild", "+4"));
            }
            return shuffleUnoCards(deck);
          }

          function shuffleUnoCards(cards) {
            for (let index = cards.length - 1; index > 0; index -= 1) {
              const swapIndex = Math.floor(Math.random() * (index + 1));
              [cards[index], cards[swapIndex]] = [cards[swapIndex], cards[index]];
            }
            return cards;
          }

          function createUnoPlayers(playerCount) {
            return Array.from({ length: playerCount }, (_, index) => ({
              name: index === 0 ? "あなた" : `CPU ${index}`,
              hand: [],
            }));
          }

          function drawUnoCard(player, count = 1) {
            for (let drawIndex = 0; drawIndex < count; drawIndex += 1) {
              if (unoDeck.length === 0) {
                rebuildUnoDeck();
              }
              const card = unoDeck.pop();
              if (card) {
                player.hand.push(card);
              }
            }
          }

          function rebuildUnoDeck() {
            if (unoDiscardPile.length <= 1) {
              return;
            }
            const topCard = unoDiscardPile.pop();
            unoDeck = shuffleUnoCards(unoDiscardPile.splice(0));
            unoDiscardPile = [topCard];
          }

          function getUnoTopCard() {
            return unoDiscardPile[unoDiscardPile.length - 1];
          }

          function isUnoPlayable(card) {
            const topCard = getUnoTopCard();
            return (
              card.color === "wild"
              || card.color === unoCurrentColor
              || card.value === topCard.value
            );
          }

          function getNextUnoPlayerIndex(fromIndex = unoCurrentPlayerIndex, steps = 1) {
            const playerCount = unoPlayers.length;
            return (fromIndex + unoDirection * steps + playerCount * 4) % playerCount;
          }

          function getUnoCardClass(card) {
            return card.color === "wild" ? "is-wild" : `is-${card.color}`;
          }

          function chooseUnoCpuColor(player) {
            const colorCounts = { red: 0, blue: 0, green: 0, yellow: 0 };
            player.hand.forEach((card) => {
              if (colorCounts[card.color] !== undefined) {
                colorCounts[card.color] += 1;
              }
            });
            return Object.entries(colorCounts).sort((left, right) => right[1] - left[1])[0][0];
          }

          function renderUnoCard(card, options = {}) {
            const disabledClass = options.disabled ? " is-disabled" : "";
            return `<button class="uno-card ${getUnoCardClass(card)}${disabledClass}" type="button" data-card-index="${options.index ?? ""}" ${options.disabled ? "disabled" : ""}>
              <span>${card.label}</span>
            </button>`;
          }

          function getUnoSeatName(playerIndex) {
            if (playerIndex === 0) {
              return "bottom";
            }

            if (unoPlayers.length === 2) {
              return "top";
            }

            if (unoPlayers.length === 3) {
              return playerIndex === 1 ? "top" : "right";
            }

            return ["bottom", "left", "top", "right"][playerIndex];
          }

          function renderUnoPlayerCard(player, index) {
            return `
              <section class="uno-player ${index === unoCurrentPlayerIndex && !unoIsGameOver ? "is-active" : ""}">
                <h3>${player.name}</h3>
                <p>手札: ${player.hand.length}枚</p>
                <p>${index === 0 ? "あなたの席" : "CPUが自動で進めます"}</p>
              </section>
            `;
          }

          function renderUno() {
            const topCard = getUnoTopCard();
            unoDeckCountElement.textContent = `${unoDeck.length}枚`;
            unoDiscardElement.innerHTML = topCard ? renderUnoCard(topCard, { disabled: true }) : "";
            unoCurrentColorElement.textContent = unoColorLabels[unoCurrentColor];

            const human = unoPlayers[0];
            const isHumanTurn = unoCurrentPlayerIndex === 0 && !unoIsGameOver;
            unoDrawButton.disabled = !isHumanTurn;
            unoColorChoiceSelect.disabled = !isHumanTurn;
            unoHandElement.innerHTML = human.hand
              .map((card, index) => renderUnoCard(card, {
                index,
                disabled: !isHumanTurn || !isUnoPlayable(card),
              }))
              .join("");

            unoHandElement.querySelectorAll("[data-card-index]").forEach((button) => {
              button.addEventListener("click", () => {
                playUnoCard(0, Number(button.dataset.cardIndex), unoColorChoiceSelect.value);
              });
            });

            unoSeatTopElement.innerHTML = "";
            unoSeatLeftElement.innerHTML = "";
            unoSeatRightElement.innerHTML = "";
            unoSeatBottomElement.querySelector(".uno-player").outerHTML = renderUnoPlayerCard(human, 0);

            unoPlayers.forEach((player, index) => {
              if (index === 0) {
                return;
              }

              const seatName = getUnoSeatName(index);
              const seatElement = {
                top: unoSeatTopElement,
                left: unoSeatLeftElement,
                right: unoSeatRightElement,
              }[seatName];
              if (seatElement) {
                seatElement.innerHTML = renderUnoPlayerCard(player, index);
              }
            });
          }

          function applyUnoCardEffect(card) {
            let nextIndex = getNextUnoPlayerIndex();
            if (card.value === "Reverse") {
              unoDirection *= -1;
              if (unoPlayers.length === 2) {
                nextIndex = getNextUnoPlayerIndex(unoCurrentPlayerIndex, 2);
              } else {
                nextIndex = getNextUnoPlayerIndex();
              }
            } else if (card.value === "Skip") {
              nextIndex = getNextUnoPlayerIndex(unoCurrentPlayerIndex, 2);
            } else if (card.value === "+2") {
              const targetIndex = getNextUnoPlayerIndex();
              drawUnoCard(unoPlayers[targetIndex], 2);
              nextIndex = getNextUnoPlayerIndex(unoCurrentPlayerIndex, 2);
            } else if (card.value === "+4") {
              const targetIndex = getNextUnoPlayerIndex();
              drawUnoCard(unoPlayers[targetIndex], 4);
              nextIndex = getNextUnoPlayerIndex(unoCurrentPlayerIndex, 2);
            }
            unoCurrentPlayerIndex = nextIndex;
          }

          function playUnoCard(playerIndex, cardIndex, selectedColor) {
            if (unoIsGameOver || playerIndex !== unoCurrentPlayerIndex) {
              return false;
            }

            const player = unoPlayers[playerIndex];
            const card = player.hand[cardIndex];
            if (!card || !isUnoPlayable(card)) {
              return false;
            }

            player.hand.splice(cardIndex, 1);
            unoDiscardPile.push(card);
            unoCurrentColor = card.color === "wild" ? selectedColor : card.color;

            if (player.hand.length === 0) {
              unoIsGameOver = true;
              clearTimeout(unoCpuTimer);
              unoStatusElement.textContent = `${player.name}の勝ちです！`;
              renderUno();
              return true;
            }

            applyUnoCardEffect(card);
            unoStatusElement.textContent = `${player.name}が ${card.label} を出しました`;
            renderUno();
            scheduleUnoCpuTurn();
            return true;
          }

          function drawForCurrentUnoPlayer() {
            if (unoIsGameOver) {
              return;
            }

            const player = unoPlayers[unoCurrentPlayerIndex];
            drawUnoCard(player, 1);
            const drawnCardIndex = player.hand.length - 1;
            const drawnCard = player.hand[drawnCardIndex];
            if (drawnCard && isUnoPlayable(drawnCard)) {
              const color = player === unoPlayers[0] ? unoColorChoiceSelect.value : chooseUnoCpuColor(player);
              playUnoCard(unoCurrentPlayerIndex, drawnCardIndex, color);
              return;
            }

            unoStatusElement.textContent = `${player.name}が山札から1枚引きました`;
            unoCurrentPlayerIndex = getNextUnoPlayerIndex();
            renderUno();
            scheduleUnoCpuTurn();
          }

          function runUnoCpuTurn() {
            if (unoIsGameOver || unoCurrentPlayerIndex === 0) {
              return;
            }

            const player = unoPlayers[unoCurrentPlayerIndex];
            const playableIndex = player.hand.findIndex(isUnoPlayable);
            if (playableIndex >= 0) {
              playUnoCard(unoCurrentPlayerIndex, playableIndex, chooseUnoCpuColor(player));
              return;
            }

            drawForCurrentUnoPlayer();
          }

          function scheduleUnoCpuTurn() {
            clearTimeout(unoCpuTimer);
            if (!unoIsGameOver && unoCurrentPlayerIndex !== 0) {
              unoCpuTimer = setTimeout(runUnoCpuTurn, 800);
            }
          }

          function startUnoGame() {
            clearTimeout(unoCpuTimer);
            const playerCount = Number(unoPlayerCountSelect.value);
            unoPlayers = createUnoPlayers(playerCount);
            unoDeck = createUnoDeck();
            unoDiscardPile = [];
            unoCurrentPlayerIndex = 0;
            unoDirection = 1;
            unoIsGameOver = false;

            for (let drawRound = 0; drawRound < 7; drawRound += 1) {
              unoPlayers.forEach((player) => drawUnoCard(player, 1));
            }

            let firstCard = unoDeck.pop();
            while (firstCard && firstCard.color === "wild") {
              unoDeck.unshift(firstCard);
              shuffleUnoCards(unoDeck);
              firstCard = unoDeck.pop();
            }
            unoDiscardPile.push(firstCard);
            unoCurrentColor = firstCard.color;

            unoSetupElement.hidden = true;
            unoTableElement.hidden = false;
            unoStatusElement.textContent = "あなたの番です。出せるカードを選ぶか、山札から引いてください";
            renderUno();
          }

          function resetUnoGame() {
            clearTimeout(unoCpuTimer);
            unoPlayers = [];
            unoDeck = [];
            unoDiscardPile = [];
            unoCurrentPlayerIndex = 0;
            unoDirection = 1;
            unoIsGameOver = false;
            unoSetupElement.hidden = false;
            unoTableElement.hidden = true;
            unoStatusElement.textContent = "人数を選んでゲームを開始してください";
            unoHandElement.innerHTML = "";
            unoSeatTopElement.innerHTML = "";
            unoSeatLeftElement.innerHTML = "";
            unoSeatRightElement.innerHTML = "";
            unoSeatBottomElement.querySelector(".uno-player").outerHTML = `
              <div class="uno-player">
                <h3>あなた</h3>
                <p>手札: 0枚</p>
              </div>
            `;
          }

          unoStartButton.addEventListener("click", startUnoGame);
          unoNewGameButton.addEventListener("click", startUnoGame);
          unoResetButton.addEventListener("click", resetUnoGame);
          unoDrawButton.addEventListener("click", () => {
            if (unoCurrentPlayerIndex === 0) {
              drawForCurrentUnoPlayer();
            }
          });
        </script>""",
)
