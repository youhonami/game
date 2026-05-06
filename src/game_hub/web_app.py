import hmac
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


HOST = "127.0.0.1"
PORT = 8000
OWNER_ADDRESS = "admin@estra.jp"
OWNER_PASSWORD = "password"
BACKGROUND_IMAGE_PATH = Path(
    "/Users/honamiyuusuke/.cursor/projects/"
    "Users-honamiyuusuke-coachtech-game/assets/"
    "_______-5e35f2db-48bd-48a4-ae7b-476c8cda2f70.png"
)


STYLE = """
    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      min-height: 100vh;
      color: #f5f7fb;
      font-family: -apple-system, BlinkMacSystemFont, "Hiragino Sans", "Yu Gothic", sans-serif;
      background: #021329 url("/assets/background.png") center / cover no-repeat fixed;
    }

    .page {
      display: flex;
      min-height: 100vh;
      background: linear-gradient(90deg, rgba(0, 10, 25, 0.88), rgba(0, 32, 68, 0.28));
    }

    .sidebar {
      display: flex;
      flex-direction: column;
      width: 280px;
      min-height: 100vh;
      padding: 42px 28px;
      background: rgba(4, 18, 36, 0.88);
      border-right: 2px solid rgba(120, 225, 255, 0.45);
      box-shadow: 12px 0 36px rgba(0, 0, 0, 0.32);
    }

    .sidebar h1 {
      margin: 0 0 44px;
      font-size: 28px;
      letter-spacing: 0.05em;
    }

    .sidebar h1 a {
      color: inherit;
      text-decoration: none;
    }

    .menu {
      display: grid;
      gap: 18px;
    }

    .sidebar-footer {
      margin-top: auto;
      padding-top: 32px;
    }

    .menu a {
      display: block;
      padding: 18px 20px;
      color: #ffffff;
      text-decoration: none;
      font-size: 22px;
      font-weight: 700;
      background: rgba(14, 90, 140, 0.72);
      border: 1px solid rgba(150, 235, 255, 0.78);
      border-radius: 16px;
      transition: transform 0.18s ease, background 0.18s ease;
    }

    .menu a:hover,
    .menu a.active {
      transform: translateX(6px);
      background: rgba(28, 150, 205, 0.86);
    }

    main {
      display: grid;
      flex: 1;
      place-items: center;
      padding: 48px;
      text-align: center;
    }

    .hero {
      min-width: min(680px, 100%);
      padding: 44px 56px;
      border: 1px solid rgba(160, 235, 255, 0.28);
      border-radius: 28px;
      background: rgba(2, 22, 48, 0.44);
      backdrop-filter: blur(4px);
    }

    .hero h2 {
      margin: 0 0 18px;
      font-size: clamp(44px, 7vw, 78px);
      text-shadow: 0 8px 28px rgba(0, 0, 0, 0.45);
    }

    .hero p {
      margin: 0;
      color: #9feaff;
      font-size: 24px;
      font-weight: 700;
    }

    .login-form {
      display: grid;
      gap: 18px;
      margin: 30px auto 0;
      max-width: 420px;
      text-align: left;
    }

    .login-form label {
      display: grid;
      gap: 8px;
      color: #d8f7ff;
      font-size: 16px;
      font-weight: 700;
    }

    .login-form input {
      width: 100%;
      padding: 14px 16px;
      color: #ffffff;
      font-size: 18px;
      background: rgba(0, 18, 40, 0.72);
      border: 1px solid rgba(150, 235, 255, 0.78);
      border-radius: 12px;
      outline: none;
    }

    .login-form input:focus {
      border-color: #ffffff;
      box-shadow: 0 0 0 3px rgba(120, 225, 255, 0.22);
    }

    .login-form button {
      margin-top: 8px;
      padding: 15px 18px;
      color: #ffffff;
      font-size: 18px;
      font-weight: 700;
      cursor: pointer;
      background: rgba(28, 150, 205, 0.9);
      border: 1px solid rgba(190, 245, 255, 0.9);
      border-radius: 14px;
    }

    .helper-text {
      margin-top: 20px;
      color: #9feaff;
      font-size: 16px;
      font-weight: 700;
    }

    .error-message {
      margin: 24px auto 0;
      max-width: 420px;
      padding: 12px 14px;
      color: #ffffff;
      font-size: 15px;
      font-weight: 700;
      background: rgba(210, 60, 80, 0.82);
      border: 1px solid rgba(255, 190, 200, 0.9);
      border-radius: 12px;
    }

    .back-link {
      display: inline-block;
      margin-top: 28px;
      color: #ffffff;
      font-weight: 700;
      text-decoration: none;
      border-bottom: 1px solid rgba(255, 255, 255, 0.7);
    }
"""


def render_page(
    title: str,
    heading: str,
    message: str = "",
    active_page: str = "",
    body_html: str | None = None,
) -> str:
    tetris_class = "active" if active_page == "tetris" else ""
    shooting_class = "active" if active_page == "shooting" else ""
    puyopuyo_class = "active" if active_page == "puyopuyo" else ""
    score_class = "active" if active_page == "score" else ""
    owner_login_class = "active" if active_page == "owner-login" else ""
    back_link = "" if not active_page else '<a class="back-link" href="/">トップページに戻る</a>'
    body = body_html if body_html is not None else f"<p>{message}</p>"

    return f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
{STYLE}
  </style>
</head>
<body>
  <div class="page">
    <aside class="sidebar">
      <h1><a href="/">Game Menu</a></h1>
      <nav class="menu" aria-label="ゲームメニュー">
        <a class="{tetris_class}" href="/tetris">テトリス</a>
        <a class="{shooting_class}" href="/shooting">シューティング</a>
        <a class="{puyopuyo_class}" href="/puyopuyo">ぷよぷよ</a>
        <a class="{score_class}" href="/score">スコア</a>
      </nav>
      <nav class="menu sidebar-footer" aria-label="オーナーメニュー">
        <a class="{owner_login_class}" href="/owner-login">オーナーログイン</a>
      </nav>
    </aside>
    <main>
      <section class="hero">
        <h2>{heading}</h2>
        {body}
        {back_link}
      </section>
    </main>
  </div>
</body>
</html>
"""


HOME_HTML = render_page(
    title="Ocean Game Hub",
    heading="Ocean Game Hub",
    message="サイドバーからゲームを選択",
)
TETRIS_HTML = render_page(
    title="テトリス | Ocean Game Hub",
    heading="テトリス",
    message="このページの内容は後で作成します",
    active_page="tetris",
)
SHOOTING_HTML = render_page(
    title="シューティング | Ocean Game Hub",
    heading="シューティング",
    message="このページの内容は後で作成します",
    active_page="shooting",
)
PUYOPUYO_HTML = render_page(
    title="ぷよぷよ | Ocean Game Hub",
    heading="ぷよぷよ",
    message="このページの内容は後で作成します",
    active_page="puyopuyo",
)
SCORE_HTML = render_page(
    title="スコア | Ocean Game Hub",
    heading="スコア",
    message="このページの内容は後で作成します",
    active_page="score",
)


def render_owner_login_page(error_message: str = "") -> str:
    error_html = f'<div class="error-message">{error_message}</div>' if error_message else ""

    return render_page(
        title="オーナーログイン | Ocean Game Hub",
        heading="オーナーログイン",
        active_page="owner-login",
        body_html=f"""<p>管理機能へ進むにはログインしてください</p>
        <form class="login-form" action="/owner-dashboard" method="post">
          <label>
            アドレス
            <input type="email" name="address" autocomplete="email" required>
          </label>
          <label>
            パスワード
            <input type="password" name="password" autocomplete="current-password" required>
          </label>
          <button type="submit">ログイン</button>
        </form>
        {error_html}
        <div class="helper-text">管理画面の内容は後日作成します</div>""",
    )


OWNER_LOGIN_HTML = render_owner_login_page()
OWNER_DASHBOARD_HTML = render_page(
    title="管理ページ | Ocean Game Hub",
    heading="管理ページ",
    message="スコアデータ削除などの管理機能は後日作成します",
    active_page="owner-login",
)


class GameHubHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        path = urlparse(self.path).path

        if path in {"/", "/index.html"}:
            self._send_html(HOME_HTML)
            return

        if path == "/tetris":
            self._send_html(TETRIS_HTML)
            return

        if path == "/shooting":
            self._send_html(SHOOTING_HTML)
            return

        if path == "/puyopuyo":
            self._send_html(PUYOPUYO_HTML)
            return

        if path == "/score":
            self._send_html(SCORE_HTML)
            return

        if path == "/owner-login":
            self._send_html(OWNER_LOGIN_HTML)
            return

        if path == "/owner-dashboard":
            self._send_html(OWNER_LOGIN_HTML)
            return

        if path == "/assets/background.png":
            self._send_background()
            return

        self.send_error(404)

    def do_POST(self) -> None:
        path = urlparse(self.path).path

        if path == "/owner-dashboard":
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length).decode("utf-8") if content_length else ""
            form = parse_qs(raw_body)
            address = form.get("address", [""])[0]
            password = form.get("password", [""])[0]

            if is_owner_login(address, password):
                self._send_html(OWNER_DASHBOARD_HTML)
                return

            self._send_html(render_owner_login_page("アドレスまたはパスワードが違います"))
            return

        self.send_error(404)

    def log_message(self, format: str, *args: object) -> None:
        return

    def _send_html(self, html: str) -> None:
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_background(self) -> None:
        if not BACKGROUND_IMAGE_PATH.exists():
            self.send_error(404, "Background image not found")
            return

        body = BACKGROUND_IMAGE_PATH.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "image/png")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def is_owner_login(address: str, password: str) -> bool:
    return hmac.compare_digest(address, OWNER_ADDRESS) and hmac.compare_digest(
        password,
        OWNER_PASSWORD,
    )


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), GameHubHandler)
    print(f"Open http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
