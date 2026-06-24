from ..layout import render_page


RANKING_HTML = render_page(
    title="ランキング | Ocean Game Hub",
    heading="ランキング",
    active_page="ranking",
    body_html="""<p>各ゲームのランキングトップ5を表示します</p>
        <div class="ranking-grid">
          <section class="ranking-card">
            <h3>テトリス</h3>
            <ol class="ranking-list" id="ranking-tetris"></ol>
          </section>
          <section class="ranking-card">
            <h3>シューティング</h3>
            <ol class="ranking-list" id="ranking-shooting"></ol>
          </section>
          <section class="ranking-card">
            <h3>ぷよぷよ</h3>
            <ol class="ranking-list" id="ranking-puyopuyo"></ol>
          </section>
          <section class="ranking-card">
            <h3>ブロック崩し</h3>
            <ol class="ranking-list" id="ranking-breakout"></ol>
          </section>
          <section class="ranking-card">
            <h3>15パズル</h3>
            <ol class="ranking-list" id="ranking-fifteen-puzzle"></ol>
          </section>
        </div>
        <script>
          const rankingSources = [
            { elementId: "ranking-tetris", storageKey: "gameHubTetrisRanking", order: "desc" },
            { elementId: "ranking-shooting", storageKey: "gameHubShootingRanking", order: "desc" },
            { elementId: "ranking-puyopuyo", storageKey: "gameHubPuyopuyoRanking", order: "desc" },
            { elementId: "ranking-breakout", storageKey: "gameHubBreakoutRanking", order: "desc" },
            { elementId: "ranking-fifteen-puzzle", storageKey: "gameHubFifteenPuzzleRanking", order: "asc" },
          ];

          function loadRanking(storageKey) {
            try {
              const ranking = JSON.parse(localStorage.getItem(storageKey) || "[]");
              return Array.isArray(ranking) ? ranking : [];
            } catch {
              return [];
            }
          }

          function renderRanking({ elementId, storageKey, order }) {
            const listElement = document.getElementById(elementId);
            const topScores = loadRanking(storageKey)
              .filter((entry) => entry && entry.name && Number.isFinite(Number(entry.score)))
              .sort((left, right) => (
                order === "asc"
                  ? Number(left.score) - Number(right.score)
                    || (Number(left.clearTime) || Number.MAX_SAFE_INTEGER) - (Number(right.clearTime) || Number.MAX_SAFE_INTEGER)
                  : Number(right.score) - Number(left.score)
              ))
              .slice(0, 5);

            if (topScores.length === 0) {
              listElement.outerHTML = '<p class="ranking-empty">まだ記録がありません</p>';
              return;
            }

            listElement.innerHTML = topScores
              .map((entry, index) => `
                <li>
                  <span>${index + 1}位</span>
                  <span>${String(entry.name).slice(0, 3)}</span>
                  <span>${Number(entry.score)}</span>
                </li>
              `)
              .join("");
          }

          rankingSources.forEach(renderRanking);
        </script>""",
)
