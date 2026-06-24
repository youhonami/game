from ..layout import render_page


LUDO_HTML = render_page(
    title="ルドー | Ocean Game Hub",
    heading="ルドー",
    active_page="ludo",
    body_html="""<p>サイコロを振って、4つのコマをすべてゴールへ進めましょう</p>
        <div class="game-panel">
          <canvas class="game-board ludo-board" id="ludo-board" width="520" height="520"></canvas>
          <aside class="game-info">
            <div class="info-card">
              <h3>手番</h3>
              <p id="ludo-turn">プレイヤー</p>
            </div>
            <div class="info-card">
              <h3>サイコロ</h3>
              <p id="ludo-dice">-</p>
            </div>
            <div class="info-card">
              <h3>状態</h3>
              <p id="ludo-status">サイコロを振ってください</p>
            </div>
            <button class="primary-button" id="ludo-roll" type="button">サイコロを振る</button>
            <button class="primary-button" id="ludo-restart" type="button">最初から</button>
            <div class="info-card">
              <h3>遊び方</h3>
              <ul>
                <li>6が出ると待機中のコマをスタートできます</li>
                <li>サイコロ後に動かすコマをクリックします</li>
                <li>相手のコマに止まると相手は待機に戻ります</li>
                <li>4つのコマを先にゴールさせると勝ちです</li>
              </ul>
            </div>
          </aside>
        </div>
        <script>
          const canvas = document.getElementById("ludo-board");
          const context = canvas.getContext("2d");
          const turnElement = document.getElementById("ludo-turn");
          const diceElement = document.getElementById("ludo-dice");
          const statusElement = document.getElementById("ludo-status");
          const rollButton = document.getElementById("ludo-roll");
          const restartButton = document.getElementById("ludo-restart");

          const players = [
            {
              name: "プレイヤー",
              color: "#3fe0ff",
              home: { x: 84, y: 84 },
              startIndex: 0,
              goal: { x: 260, y: 176 },
            },
            {
              name: "CPU",
              color: "#ff6b8b",
              home: { x: 436, y: 436 },
              startIndex: 14,
              goal: { x: 260, y: 344 },
            },
          ];

          const track = [
            { x: 260, y: 60 }, { x: 320, y: 80 }, { x: 376, y: 116 }, { x: 420, y: 164 },
            { x: 452, y: 224 }, { x: 452, y: 296 }, { x: 420, y: 356 }, { x: 376, y: 404 },
            { x: 320, y: 440 }, { x: 260, y: 460 }, { x: 200, y: 440 }, { x: 144, y: 404 },
            { x: 100, y: 356 }, { x: 68, y: 296 }, { x: 68, y: 224 }, { x: 100, y: 164 },
            { x: 144, y: 116 }, { x: 200, y: 80 },
          ];

          const homeOffsets = [
            { x: -24, y: -24 },
            { x: 24, y: -24 },
            { x: -24, y: 24 },
            { x: 24, y: 24 },
          ];

          let pieces = [];
          let currentPlayerIndex = 0;
          let diceValue = 0;
          let hasRolled = false;
          let isGameOver = false;

          function createPieces() {
            return players.flatMap((player, playerIndex) =>
              Array.from({ length: 4 }, (_, pieceIndex) => ({
                playerIndex,
                pieceIndex,
                steps: -1,
              }))
            );
          }

          function getPiecePosition(piece) {
            const player = players[piece.playerIndex];
            const offset = homeOffsets[piece.pieceIndex];

            if (piece.steps < 0) {
              return {
                x: player.home.x + offset.x,
                y: player.home.y + offset.y,
              };
            }

            if (piece.steps >= track.length) {
              return {
                x: player.goal.x + offset.x * 0.48,
                y: player.goal.y + offset.y * 0.48,
              };
            }

            return track[(player.startIndex + piece.steps) % track.length];
          }

          function getMovablePieces(playerIndex, roll) {
            return pieces.filter((piece) => {
              if (piece.playerIndex !== playerIndex || piece.steps >= track.length) {
                return false;
              }

              if (piece.steps < 0) {
                return roll === 6;
              }

              return piece.steps + roll <= track.length;
            });
          }

          function updateInfo(message) {
            const currentPlayer = players[currentPlayerIndex];
            turnElement.textContent = currentPlayer.name;
            diceElement.textContent = diceValue || "-";
            statusElement.textContent = message;
          }

          function drawPath() {
            context.strokeStyle = "rgba(150, 235, 255, 0.62)";
            context.lineWidth = 4;
            context.beginPath();
            track.forEach((point, index) => {
              if (index === 0) {
                context.moveTo(point.x, point.y);
              } else {
                context.lineTo(point.x, point.y);
              }
            });
            context.closePath();
            context.stroke();

            track.forEach((point, index) => {
              context.fillStyle = index === players[0].startIndex
                ? "rgba(63, 224, 255, 0.4)"
                : index === players[1].startIndex
                  ? "rgba(255, 107, 139, 0.4)"
                  : "rgba(4, 32, 64, 0.95)";
              context.strokeStyle = "rgba(190, 245, 255, 0.75)";
              context.lineWidth = 2;
              context.beginPath();
              context.arc(point.x, point.y, 18, 0, Math.PI * 2);
              context.fill();
              context.stroke();
            });
          }

          function drawHome(player) {
            context.fillStyle = `${player.color}22`;
            context.strokeStyle = player.color;
            context.lineWidth = 3;
            context.beginPath();
            context.roundRect(player.home.x - 58, player.home.y - 58, 116, 116, 22);
            context.fill();
            context.stroke();
          }

          function drawGoal(player) {
            context.fillStyle = `${player.color}30`;
            context.strokeStyle = player.color;
            context.lineWidth = 3;
            context.beginPath();
            context.arc(player.goal.x, player.goal.y, 34, 0, Math.PI * 2);
            context.fill();
            context.stroke();
          }

          function drawPiece(piece) {
            const player = players[piece.playerIndex];
            const position = getPiecePosition(piece);
            const movablePieces = hasRolled ? getMovablePieces(currentPlayerIndex, diceValue) : [];
            const isMovable = movablePieces.includes(piece) && !isGameOver;

            context.fillStyle = player.color;
            context.strokeStyle = isMovable ? "#ffffff" : "rgba(0, 8, 20, 0.9)";
            context.lineWidth = isMovable ? 4 : 2;
            context.beginPath();
            context.arc(position.x, position.y, 14, 0, Math.PI * 2);
            context.fill();
            context.stroke();

            context.fillStyle = "#021329";
            context.font = "bold 12px sans-serif";
            context.textAlign = "center";
            context.textBaseline = "middle";
            context.fillText(String(piece.pieceIndex + 1), position.x, position.y + 1);
          }

          function draw() {
            context.clearRect(0, 0, canvas.width, canvas.height);
            context.fillStyle = "rgba(0, 12, 28, 0.86)";
            context.fillRect(0, 0, canvas.width, canvas.height);

            drawPath();
            players.forEach(drawHome);
            players.forEach(drawGoal);

            context.fillStyle = "rgba(255, 255, 255, 0.86)";
            context.font = "bold 18px sans-serif";
            context.textAlign = "center";
            context.fillText("START", 260, 34);
            context.fillText("GOAL", 260, 262);

            pieces.forEach(drawPiece);
          }

          function sendPieceHome(piece) {
            piece.steps = -1;
          }

          function capturePieces(movedPiece) {
            if (movedPiece.steps < 0 || movedPiece.steps >= track.length) {
              return;
            }

            const movedPosition = getPiecePosition(movedPiece);
            pieces.forEach((piece) => {
              if (piece.playerIndex === movedPiece.playerIndex || piece.steps < 0 || piece.steps >= track.length) {
                return;
              }

              const position = getPiecePosition(piece);
              if (position.x === movedPosition.x && position.y === movedPosition.y) {
                sendPieceHome(piece);
              }
            });
          }

          function hasWon(playerIndex) {
            return pieces
              .filter((piece) => piece.playerIndex === playerIndex)
              .every((piece) => piece.steps >= track.length);
          }

          function endTurn(extraTurn) {
            hasRolled = false;
            diceValue = 0;

            if (!extraTurn) {
              currentPlayerIndex = currentPlayerIndex === 0 ? 1 : 0;
            }

            rollButton.disabled = isGameOver || currentPlayerIndex !== 0;
            updateInfo(currentPlayerIndex === 0 ? "サイコロを振ってください" : "CPUが考えています");
            draw();

            if (!isGameOver && currentPlayerIndex === 1) {
              setTimeout(cpuTurn, 700);
            }
          }

          function movePiece(piece) {
            if (!hasRolled || isGameOver) {
              return false;
            }

            if (!getMovablePieces(currentPlayerIndex, diceValue).includes(piece)) {
              return false;
            }

            if (piece.steps < 0) {
              piece.steps = 0;
            } else {
              piece.steps += diceValue;
            }

            capturePieces(piece);

            if (hasWon(piece.playerIndex)) {
              isGameOver = true;
              rollButton.disabled = true;
              updateInfo(`${players[piece.playerIndex].name}の勝ちです！`);
              draw();
              return true;
            }

            endTurn(diceValue === 6);
            return true;
          }

          function rollDice() {
            if (hasRolled || isGameOver) {
              return;
            }

            diceValue = Math.floor(Math.random() * 6) + 1;
            hasRolled = true;
            const movablePieces = getMovablePieces(currentPlayerIndex, diceValue);

            if (movablePieces.length === 0) {
              updateInfo(`${diceValue} が出ました。動かせるコマがありません`);
              draw();
              setTimeout(() => endTurn(false), 900);
              return;
            }

            updateInfo(`${diceValue} が出ました。動かすコマを選んでください`);
            draw();
          }

          function cpuTurn() {
            if (isGameOver || currentPlayerIndex !== 1) {
              return;
            }

            rollDice();
            const movablePieces = getMovablePieces(1, diceValue);
            if (movablePieces.length === 0) {
              return;
            }

            const selectedPiece = movablePieces
              .slice()
              .sort((left, right) => right.steps - left.steps)[0];
            setTimeout(() => movePiece(selectedPiece), 700);
          }

          function findClickedPiece(x, y) {
            return pieces.find((piece) => {
              const position = getPiecePosition(piece);
              return Math.hypot(position.x - x, position.y - y) <= 18;
            });
          }

          function startGame() {
            pieces = createPieces();
            currentPlayerIndex = 0;
            diceValue = 0;
            hasRolled = false;
            isGameOver = false;
            rollButton.disabled = false;
            updateInfo("サイコロを振ってください");
            draw();
          }

          canvas.addEventListener("click", (event) => {
            if (currentPlayerIndex !== 0 || !hasRolled || isGameOver) {
              return;
            }

            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            const piece = findClickedPiece(
              (event.clientX - rect.left) * scaleX,
              (event.clientY - rect.top) * scaleY
            );

            if (piece) {
              movePiece(piece);
            }
          });

          rollButton.addEventListener("click", rollDice);
          restartButton.addEventListener("click", startGame);
          startGame();
        </script>""",
)
