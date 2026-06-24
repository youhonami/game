from ..layout import render_page


TRUMP_HTML = render_page(
    title="トランプ | Ocean Game Hub",
    heading="トランプ",
    active_page="trump",
    body_html="""<p>遊びたいトランプゲームを選んでください</p>
        <div class="game-select-grid">
          <a class="game-select-button" href="/trump/old-maid">ババ抜き</a>
          <a class="game-select-button" href="/trump/sevens">七並べ</a>
          <a class="game-select-button" href="/trump/memory">神経衰弱</a>
        </div>""",
)
