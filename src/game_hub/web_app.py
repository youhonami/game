import hmac
import json
from datetime import datetime
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .layout import render_page
from .pages.breakout import BREAKOUT_HTML
from .pages.chat_room import CHAT_ROOM_HTML
from .pages.home import HOME_HTML
from .pages.ludo import LUDO_HTML
from .pages.memory import MEMORY_HTML
from .pages.minesweeper import MINESWEEPER_HTML
from .pages.old_maid import OLD_MAID_HTML
from .pages.puzzle import PUZZLE_HTML
from .pages.puyopuyo import PUYOPUYO_HTML
from .pages.ranking import RANKING_HTML
from .pages.sevens import SEVENS_HTML
from .pages.shooting import SHOOTING_HTML
from .pages.tetris import TETRIS_HTML
from .pages.trump import TRUMP_HTML
from .pages.uno import UNO_HTML


HOST = "127.0.0.1"
PORT = 8000
OWNER_ADDRESS = "admin@estra.jp"
OWNER_PASSWORD = "password"
CONTACT_MESSAGES_PATH = Path(__file__).with_name("contact_messages.json")
CHAT_ROOM_MESSAGES_PATH = Path(__file__).with_name("chat_room_messages.json")
BACKGROUND_IMAGE_PATH = Path(
    "/Users/honamiyuusuke/.cursor/projects/"
    "Users-honamiyuusuke-coachtech-game/assets/"
    "_______-5e35f2db-48bd-48a4-ae7b-476c8cda2f70.png"
)

def load_contact_messages() -> list[dict[str, str]]:
    if not CONTACT_MESSAGES_PATH.exists():
        return []

    try:
        data = json.loads(CONTACT_MESSAGES_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(data, list):
        return []

    messages: list[dict[str, str]] = []
    for item in data:
        if not isinstance(item, dict):
            continue

        messages.append(
            {
                "name": str(item.get("name", "")),
                "email": str(item.get("email", "")),
                "message": str(item.get("message", "")),
                "sent_at": str(item.get("sent_at", "")),
            }
        )

    return messages


def save_contact_messages(messages: list[dict[str, str]]) -> None:
    CONTACT_MESSAGES_PATH.write_text(
        json.dumps(messages, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def add_contact_message(name: str, email: str, message: str) -> None:
    messages = load_contact_messages()
    messages.append(
        {
            "name": name,
            "email": email,
            "message": message,
            "sent_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
    )
    save_contact_messages(messages)


def delete_contact_message(message_index: int) -> bool:
    messages = load_contact_messages()
    if message_index < 0 or message_index >= len(messages):
        return False

    messages.pop(message_index)
    save_contact_messages(messages)
    return True


def load_chat_room_messages() -> list[dict[str, str]]:
    if not CHAT_ROOM_MESSAGES_PATH.exists():
        return []

    try:
        data = json.loads(CHAT_ROOM_MESSAGES_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(data, list):
        return []

    messages: list[dict[str, str]] = []
    for item in data:
        if not isinstance(item, dict):
            continue

        messages.append(
            {
                "name": str(item.get("name", "")),
                "text": str(item.get("text", "")),
                "sent_at": str(item.get("sent_at", "")),
            }
        )

    return messages


def save_chat_room_messages(messages: list[dict[str, str]]) -> None:
    CHAT_ROOM_MESSAGES_PATH.write_text(
        json.dumps(messages[-100:], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def add_chat_room_message(name: str, text: str) -> dict[str, str]:
    message = {
        "name": name[:12],
        "text": text[:500],
        "sent_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    messages = load_chat_room_messages()
    messages.append(message)
    save_chat_room_messages(messages)
    return message


def render_contact_page(
    status_message: str = "",
    is_error: bool = False,
    name: str = "",
    email: str = "",
    message: str = "",
) -> str:
    status_html = ""
    if status_message:
        status_class = "error-message" if is_error else "success-message"
        status_html = f'<div class="{status_class}">{escape(status_message)}</div>'

    return render_page(
        title="お問い合わせ | Ocean Game Hub",
        heading="お問い合わせ",
        active_page="contact",
        body_html=f"""<p>オーナーへメッセージを送れます</p>
        <form class="contact-form" action="/contact" method="post">
          <label>
            お名前
            <input type="text" name="name" value="{escape(name, quote=True)}" autocomplete="name" required>
          </label>
          <label>
            メールアドレス
            <input type="email" name="email" value="{escape(email, quote=True)}" autocomplete="email" required>
          </label>
          <label>
            メッセージ
            <textarea name="message" required>{escape(message)}</textarea>
          </label>
          <button type="submit">送信する</button>
        </form>
        {status_html}""",
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


def render_contact_messages(messages: list[dict[str, str]]) -> str:
    if not messages:
        return '<p class="empty-contact-message">お問い合わせはまだ届いていません</p>'

    items = []
    for message_index, contact_message in reversed(list(enumerate(messages))):
        name = escape(contact_message["name"])
        email = escape(contact_message["email"])
        sent_at = escape(contact_message["sent_at"])
        body = escape(contact_message["message"])
        items.append(
            f"""<li>
              <strong>{name}</strong>
              <small>{email} / {sent_at}</small>
              <p>{body}</p>
              <form class="contact-delete-form" action="/owner-messages/delete" method="post">
                <input type="hidden" name="message_index" value="{message_index}">
                <button type="submit">削除</button>
              </form>
            </li>"""
        )

    return f'<ul class="contact-message-list">{"".join(items)}</ul>'


def render_owner_dashboard_page() -> str:
    return render_page(
        title="管理ページ | Ocean Game Hub",
        heading="管理ページ",
        active_page="owner-login",
        body_html="""<p>確認したい管理機能を選択してください</p>
        <div class="owner-menu-grid">
          <a class="owner-menu-button" href="/owner-scores">スコア削除</a>
          <a class="owner-menu-button" href="/owner-messages">メッセージ確認</a>
        </div>
        <a class="back-link" href="/">トップページに戻る</a>""",
    )


def render_owner_messages_page(status_message: str = "") -> str:
    contact_messages_html = render_contact_messages(load_contact_messages())
    status_html = (
        f'<div class="success-message">{escape(status_message)}</div>'
        if status_message
        else ""
    )

    return render_page(
        title="メッセージ確認 | Ocean Game Hub",
        heading="メッセージ確認",
        active_page="owner-login",
        body_html=f"""<p>お問い合わせから届いたメッセージを確認できます</p>
        <section class="owner-contact-panel">
          <h3>お問い合わせ</h3>
          {contact_messages_html}
        </section>
        {status_html}
        <a class="back-link" href="/owner-dashboard">管理ページに戻る</a>""",
    )


def render_owner_scores_page() -> str:
    dashboard_body = """<p>登録されたスコアデータを削除できます</p>
        <div class="admin-grid">
          <section class="admin-card">
            <button class="admin-toggle" type="button" data-toggle-score="tetris" aria-expanded="false">
              テトリス<span>開く</span>
            </button>
            <div class="admin-score-detail" id="admin-tetris-detail" hidden>
              <p id="admin-tetris-count">読み込み中...</p>
              <ul class="score-entry-list" id="admin-tetris-list"></ul>
            </div>
          </section>
          <section class="admin-card">
            <button class="admin-toggle" type="button" data-toggle-score="shooting" aria-expanded="false">
              シューティング<span>開く</span>
            </button>
            <div class="admin-score-detail" id="admin-shooting-detail" hidden>
              <p id="admin-shooting-count">読み込み中...</p>
              <ul class="score-entry-list" id="admin-shooting-list"></ul>
            </div>
          </section>
          <section class="admin-card">
            <button class="admin-toggle" type="button" data-toggle-score="puyopuyo" aria-expanded="false">
              ぷよぷよ<span>開く</span>
            </button>
            <div class="admin-score-detail" id="admin-puyopuyo-detail" hidden>
              <p id="admin-puyopuyo-count">読み込み中...</p>
              <ul class="score-entry-list" id="admin-puyopuyo-list"></ul>
            </div>
          </section>
          <section class="admin-card">
            <button class="admin-toggle" type="button" data-toggle-score="breakout" aria-expanded="false">
              ブロック崩し<span>開く</span>
            </button>
            <div class="admin-score-detail" id="admin-breakout-detail" hidden>
              <p id="admin-breakout-count">読み込み中...</p>
              <ul class="score-entry-list" id="admin-breakout-list"></ul>
            </div>
          </section>
          <section class="admin-card">
            <button class="admin-toggle" type="button" data-toggle-score="fifteenPuzzle" aria-expanded="false">
              15パズル<span>開く</span>
            </button>
            <div class="admin-score-detail" id="admin-fifteen-puzzle-detail" hidden>
              <p id="admin-fifteen-puzzle-count">読み込み中...</p>
              <ul class="score-entry-list" id="admin-fifteen-puzzle-list"></ul>
            </div>
          </section>
        </div>
        <div class="admin-actions">
          <button class="danger-button" id="delete-selected-game-scores" type="button" disabled>選択中ゲームのスコアを削除</button>
          <button class="danger-button" id="delete-all-scores" type="button">全ゲームのスコアを削除</button>
        </div>
        <p class="admin-message" id="admin-score-message"></p>
        <a class="back-link" href="/owner-dashboard">管理ページに戻る</a>
        <script>
          const scoreStores = {
            tetris: {
              label: "テトリス",
              countId: "admin-tetris-count",
              detailId: "admin-tetris-detail",
              listId: "admin-tetris-list",
              keys: ["gameHubTetrisRanking", "gameHubTetrisHighScore", "gameHubTetrisHighScoreName"],
            },
            shooting: {
              label: "シューティング",
              countId: "admin-shooting-count",
              detailId: "admin-shooting-detail",
              listId: "admin-shooting-list",
              keys: ["gameHubShootingRanking", "gameHubShootingHighScore", "gameHubShootingHighScoreName"],
            },
            puyopuyo: {
              label: "ぷよぷよ",
              countId: "admin-puyopuyo-count",
              detailId: "admin-puyopuyo-detail",
              listId: "admin-puyopuyo-list",
              keys: ["gameHubPuyopuyoRanking", "gameHubPuyopuyoHighScore", "gameHubPuyopuyoHighScoreName"],
            },
            breakout: {
              label: "ブロック崩し",
              countId: "admin-breakout-count",
              detailId: "admin-breakout-detail",
              listId: "admin-breakout-list",
              keys: ["gameHubBreakoutRanking", "gameHubBreakoutHighScore", "gameHubBreakoutHighScoreName"],
              order: "desc",
            },
            fifteenPuzzle: {
              label: "15パズル",
              countId: "admin-fifteen-puzzle-count",
              detailId: "admin-fifteen-puzzle-detail",
              listId: "admin-fifteen-puzzle-list",
              keys: ["gameHubFifteenPuzzleRanking", "gameHubFifteenPuzzleHighScore", "gameHubFifteenPuzzleHighScoreName", "gameHubFifteenPuzzleHighScoreTime"],
              order: "asc",
            },
          };

          const messageElement = document.getElementById("admin-score-message");
          const deleteSelectedGameButton = document.getElementById("delete-selected-game-scores");
          let activeStoreKey = null;

          function updateDeleteGameButton() {
            if (!activeStoreKey) {
              deleteSelectedGameButton.disabled = true;
              deleteSelectedGameButton.textContent = "選択中ゲームのスコアを削除";
              return;
            }

            deleteSelectedGameButton.disabled = false;
            deleteSelectedGameButton.textContent = `${scoreStores[activeStoreKey].label}のスコアをすべて削除`;
          }

          function getRankingCount(storageKey) {
            try {
              const ranking = JSON.parse(localStorage.getItem(storageKey) || "[]");
              return Array.isArray(ranking) ? ranking.length : 0;
            } catch {
              return 0;
            }
          }

          function loadRanking(storageKey) {
            try {
              const ranking = JSON.parse(localStorage.getItem(storageKey) || "[]");
              return Array.isArray(ranking) ? ranking : [];
            } catch {
              return [];
            }
          }

          function saveRanking(store, ranking) {
            localStorage.setItem(store.keys[0], JSON.stringify(ranking));
          }

          function updateHighScoreFromRanking(store) {
            const ranking = loadRanking(store.keys[0])
              .filter((entry) => entry && entry.name && Number.isFinite(Number(entry.score)))
              .sort((left, right) => (
                store.order === "asc"
                  ? Number(left.score) - Number(right.score)
                  : Number(right.score) - Number(left.score)
              ));
            const topEntry = ranking[0];

            if (!topEntry) {
              localStorage.removeItem(store.keys[1]);
              localStorage.removeItem(store.keys[2]);
              return;
            }

            localStorage.setItem(store.keys[1], String(Number(topEntry.score)));
            localStorage.setItem(store.keys[2], String(topEntry.name).slice(0, 3));
          }

          function renderScoreEntries(storeKey) {
            const store = scoreStores[storeKey];
            const listElement = document.getElementById(store.listId);
            const ranking = loadRanking(store.keys[0])
              .filter((entry) => entry && entry.name && Number.isFinite(Number(entry.score)))
              .sort((left, right) => (
                store.order === "asc"
                  ? Number(left.score) - Number(right.score)
                  : Number(right.score) - Number(left.score)
              ));

            if (ranking.length === 0) {
              listElement.classList.remove("is-scrollable");
              listElement.innerHTML = '<li><span>-</span><span>登録なし</span><span></span><span></span></li>';
              return;
            }

            listElement.classList.toggle("is-scrollable", ranking.length >= 5);
            listElement.innerHTML = ranking
              .map((entry, index) => `
                <li>
                  <span>${index + 1}位</span>
                  <span>${String(entry.name).slice(0, 3)}</span>
                  <span>${Number(entry.score)}</span>
                  <button type="button" data-delete-entry="${storeKey}" data-entry-index="${index}">削除</button>
                </li>
              `)
              .join("");
          }

          function refreshScoreCounts() {
            Object.entries(scoreStores).forEach(([storeKey, store]) => {
              const rankingCount = getRankingCount(store.keys[0]);
              const highScore = Number(localStorage.getItem(store.keys[1]) || 0);
              document.getElementById(store.countId).textContent =
                `登録数: ${rankingCount}件 / ハイスコア: ${highScore}`;
              renderScoreEntries(storeKey);
            });
          }

          function deleteScoreStore(storeKey) {
            const store = scoreStores[storeKey];
            store.keys.forEach((key) => localStorage.removeItem(key));
            refreshScoreCounts();
            messageElement.textContent = `${store.label}のスコアを削除しました`;
          }

          function closeScoreDetail(storeKey) {
            const store = scoreStores[storeKey];
            const toggleButton = document.querySelector(`[data-toggle-score="${storeKey}"]`);
            const detailElement = document.getElementById(store.detailId);
            toggleButton.setAttribute("aria-expanded", "false");
            toggleButton.querySelector("span").textContent = "開く";
            detailElement.hidden = true;
            if (activeStoreKey === storeKey) {
              activeStoreKey = null;
              updateDeleteGameButton();
            }
          }

          function openScoreDetail(storeKey) {
            Object.keys(scoreStores).forEach((otherStoreKey) => {
              if (otherStoreKey !== storeKey) {
                closeScoreDetail(otherStoreKey);
              }
            });

            const store = scoreStores[storeKey];
            const toggleButton = document.querySelector(`[data-toggle-score="${storeKey}"]`);
            const detailElement = document.getElementById(store.detailId);
            toggleButton.setAttribute("aria-expanded", "true");
            toggleButton.querySelector("span").textContent = "閉じる";
            detailElement.hidden = false;
            activeStoreKey = storeKey;
            updateDeleteGameButton();
          }

          document.addEventListener("click", (event) => {
            const toggleButton = event.target.closest("[data-toggle-score]");
            if (toggleButton) {
              const storeKey = toggleButton.dataset.toggleScore;
              const isOpen = toggleButton.getAttribute("aria-expanded") === "true";
              if (isOpen) {
                closeScoreDetail(storeKey);
              } else {
                openScoreDetail(storeKey);
              }
              return;
            }

            const deleteButton = event.target.closest("[data-delete-entry]");
            if (!deleteButton) {
              return;
            }

            const storeKey = deleteButton.dataset.deleteEntry;
            const entryIndex = Number(deleteButton.dataset.entryIndex);
            const store = scoreStores[storeKey];
            const ranking = loadRanking(store.keys[0])
              .filter((entry) => entry && entry.name && Number.isFinite(Number(entry.score)))
              .sort((left, right) => Number(right.score) - Number(left.score));
            const entry = ranking[entryIndex];

            if (!entry) {
              return;
            }

            if (!confirm(`${store.label}の ${entry.name} / ${entry.score} 点を削除しますか？`)) {
                return;
            }

            ranking.splice(entryIndex, 1);
            saveRanking(store, ranking);
            updateHighScoreFromRanking(store);
            refreshScoreCounts();
            messageElement.textContent = `${store.label}のスコアを1件削除しました`;
          });

          deleteSelectedGameButton.addEventListener("click", () => {
            if (!activeStoreKey) {
              return;
            }

            const store = scoreStores[activeStoreKey];
            if (!confirm(`${store.label}のスコアをすべて削除しますか？`)) {
              return;
            }

            deleteScoreStore(activeStoreKey);
          });

          document.getElementById("delete-all-scores").addEventListener("click", () => {
            if (!confirm("全ゲームのスコアを削除しますか？")) {
              return;
            }

            Object.keys(scoreStores).forEach(deleteScoreStore);
            messageElement.textContent = "全ゲームのスコアを削除しました";
          });

          refreshScoreCounts();
          updateDeleteGameButton();
        </script>"""

    return render_page(
        title="スコア削除 | Ocean Game Hub",
        heading="スコア削除",
        active_page="owner-login",
        body_html=dashboard_body,
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

        if path == "/breakout":
            self._send_html(BREAKOUT_HTML)
            return

        if path == "/ludo":
            self._send_html(LUDO_HTML)
            return

        if path == "/trump":
            self._send_html(TRUMP_HTML)
            return

        if path == "/trump/old-maid":
            self._send_html(OLD_MAID_HTML)
            return

        if path == "/trump/sevens":
            self._send_html(SEVENS_HTML)
            return

        if path == "/trump/memory":
            self._send_html(MEMORY_HTML)
            return

        if path == "/puzzle":
            self._send_html(PUZZLE_HTML)
            return

        if path == "/minesweeper":
            self._send_html(MINESWEEPER_HTML)
            return

        if path == "/uno":
            self._send_html(UNO_HTML)
            return

        if path == "/chat-room":
            self._send_html(CHAT_ROOM_HTML)
            return

        if path == "/chat-room/messages":
            self._send_json({"messages": load_chat_room_messages()})
            return

        if path in {"/ranking", "/score"}:
            self._send_html(RANKING_HTML)
            return

        if path == "/contact":
            self._send_html(render_contact_page())
            return

        if path == "/owner-login":
            self._send_html(OWNER_LOGIN_HTML)
            return

        if path == "/owner-dashboard":
            self._send_html(render_owner_dashboard_page())
            return

        if path == "/owner-scores":
            self._send_html(render_owner_scores_page())
            return

        if path == "/owner-messages":
            self._send_html(render_owner_messages_page())
            return

        if path == "/assets/background.png":
            self._send_background()
            return

        self.send_error(404)

    def do_POST(self) -> None:
        path = urlparse(self.path).path

        if path == "/contact":
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length).decode("utf-8") if content_length else ""
            form = parse_qs(raw_body)
            name = form.get("name", [""])[0].strip()
            email = form.get("email", [""])[0].strip()
            message = form.get("message", [""])[0].strip()

            if not name or not email or not message:
                self._send_html(
                    render_contact_page(
                        "お名前、メールアドレス、メッセージを入力してください",
                        is_error=True,
                        name=name,
                        email=email,
                        message=message,
                    )
                )
                return

            add_contact_message(name, email, message)
            self._send_html(render_contact_page("メッセージを送信しました"))
            return

        if path == "/chat-room/messages":
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length).decode("utf-8") if content_length else ""
            try:
                payload = json.loads(raw_body or "{}")
            except json.JSONDecodeError:
                payload = {}

            name = str(payload.get("name", "")).strip()
            text = str(payload.get("text", "")).strip()
            if not name or not text:
                self._send_json({"error": "お名前とメッセージを入力してください"}, status=400)
                return

            message = add_chat_room_message(name, text)
            self._send_json({"message": message, "messages": load_chat_room_messages()})
            return

        if path == "/owner-dashboard":
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length).decode("utf-8") if content_length else ""
            form = parse_qs(raw_body)
            address = form.get("address", [""])[0]
            password = form.get("password", [""])[0]

            if is_owner_login(address, password):
                self._send_html(render_owner_dashboard_page())
                return

            self._send_html(render_owner_login_page("アドレスまたはパスワードが違います"))
            return

        if path == "/owner-messages/delete":
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length).decode("utf-8") if content_length else ""
            form = parse_qs(raw_body)

            try:
                message_index = int(form.get("message_index", ["-1"])[0])
            except ValueError:
                message_index = -1

            if delete_contact_message(message_index):
                self._send_html(render_owner_messages_page("メッセージを削除しました"))
                return

            self._send_html(render_owner_messages_page("削除するメッセージが見つかりませんでした"))
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

    def _send_json(self, data: object, status: int = 200) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
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
