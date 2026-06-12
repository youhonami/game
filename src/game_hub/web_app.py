import hmac
import json
from datetime import datetime
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


HOST = "127.0.0.1"
PORT = 8000
OWNER_ADDRESS = "admin@estra.jp"
OWNER_PASSWORD = "password"
CONTACT_MESSAGES_PATH = Path(__file__).with_name("contact_messages.json")
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

    .login-form,
    .contact-form {
      display: grid;
      gap: 18px;
      margin: 30px auto 0;
      max-width: 420px;
      text-align: left;
    }

    .login-form label,
    .contact-form label {
      display: grid;
      gap: 8px;
      color: #d8f7ff;
      font-size: 16px;
      font-weight: 700;
    }

    .login-form input,
    .contact-form input,
    .contact-form textarea {
      width: 100%;
      padding: 14px 16px;
      color: #ffffff;
      font-size: 18px;
      background: rgba(0, 18, 40, 0.72);
      border: 1px solid rgba(150, 235, 255, 0.78);
      border-radius: 12px;
      outline: none;
    }

    .contact-form textarea {
      min-height: 160px;
      resize: vertical;
      line-height: 1.6;
    }

    .login-form input:focus,
    .contact-form input:focus,
    .contact-form textarea:focus {
      border-color: #ffffff;
      box-shadow: 0 0 0 3px rgba(120, 225, 255, 0.22);
    }

    .login-form button,
    .contact-form button {
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

    .success-message {
      margin: 24px auto 0;
      max-width: 420px;
      padding: 12px 14px;
      color: #ffffff;
      font-size: 15px;
      font-weight: 700;
      background: rgba(28, 150, 105, 0.82);
      border: 1px solid rgba(175, 255, 220, 0.9);
      border-radius: 12px;
    }

    .game-panel {
      display: grid;
      grid-template-columns: auto 220px;
      gap: 28px;
      align-items: start;
      margin-top: 28px;
    }

    .game-board {
      width: 300px;
      height: 600px;
      background: rgba(0, 12, 28, 0.86);
      border: 2px solid rgba(150, 235, 255, 0.85);
      border-radius: 14px;
      box-shadow: 0 18px 38px rgba(0, 0, 0, 0.35);
    }

    .puyo-board {
      width: 240px;
      height: 480px;
    }

    .shooting-board {
      width: 520px;
      height: 620px;
    }

    .breakout-board {
      width: 520px;
      height: 620px;
    }

    .ludo-board {
      width: 520px;
      height: 520px;
    }

    .game-info {
      display: grid;
      gap: 14px;
      text-align: left;
    }

    .info-card {
      padding: 18px;
      background: rgba(0, 18, 40, 0.68);
      border: 1px solid rgba(150, 235, 255, 0.5);
      border-radius: 16px;
    }

    .info-card h3 {
      margin: 0 0 10px;
      color: #9feaff;
      font-size: 18px;
    }

    .info-card p,
    .info-card ul {
      margin: 0;
      color: #ffffff;
      font-size: 15px;
      line-height: 1.7;
    }

    .info-card ul {
      padding-left: 18px;
    }

    .primary-button {
      display: block;
      width: 100%;
      padding: 14px 16px;
      color: #ffffff;
      font-size: 17px;
      font-weight: 700;
      text-align: center;
      text-decoration: none;
      cursor: pointer;
      background: rgba(28, 150, 205, 0.9);
      border: 1px solid rgba(190, 245, 255, 0.9);
      border-radius: 14px;
    }

    .game-over-overlay {
      position: fixed;
      inset: 0;
      display: grid;
      place-items: center;
      padding: 24px;
      background: rgba(0, 8, 20, 0.72);
      z-index: 20;
    }

    .game-over-overlay[hidden] {
      display: none;
    }

    .game-over-dialog {
      width: min(430px, 100%);
      padding: 34px;
      text-align: center;
      background: rgba(3, 24, 52, 0.96);
      border: 1px solid rgba(150, 235, 255, 0.86);
      border-radius: 24px;
      box-shadow: 0 24px 70px rgba(0, 0, 0, 0.52);
    }

    .game-over-dialog h3 {
      margin: 0 0 14px;
      font-size: 34px;
    }

    .game-over-score {
      margin: 0 0 22px;
      color: #9feaff;
      font-size: 24px;
      font-weight: 700;
    }

    .score-name-form {
      display: grid;
      gap: 14px;
    }

    .score-name-form label {
      display: grid;
      gap: 8px;
      color: #d8f7ff;
      font-weight: 700;
      text-align: left;
    }

    .score-name-form input {
      width: 100%;
      padding: 14px 16px;
      color: #ffffff;
      font-size: 24px;
      font-weight: 700;
      letter-spacing: 0.3em;
      text-align: center;
      text-transform: uppercase;
      background: rgba(0, 18, 40, 0.78);
      border: 1px solid rgba(150, 235, 255, 0.78);
      border-radius: 12px;
      outline: none;
    }

    .score-save-message {
      min-height: 24px;
      margin: 0;
      color: #9feaff;
      font-size: 15px;
      font-weight: 700;
    }

    .ranking-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(190px, 1fr));
      gap: 18px;
      margin-top: 30px;
      text-align: left;
    }

    .ranking-card {
      padding: 20px;
      background: rgba(0, 18, 40, 0.68);
      border: 1px solid rgba(150, 235, 255, 0.5);
      border-radius: 18px;
    }

    .ranking-card h3 {
      margin: 0 0 14px;
      color: #9feaff;
      font-size: 22px;
      text-align: center;
    }

    .ranking-list {
      display: grid;
      gap: 10px;
      margin: 0;
      padding: 0;
      list-style: none;
    }

    .ranking-list li {
      display: grid;
      grid-template-columns: 32px 1fr auto;
      gap: 10px;
      align-items: center;
      padding: 10px 12px;
      color: #ffffff;
      font-size: 15px;
      font-weight: 700;
      background: rgba(4, 32, 64, 0.78);
      border: 1px solid rgba(150, 235, 255, 0.28);
      border-radius: 12px;
    }

    .ranking-empty {
      margin: 0;
      color: #d8f7ff;
      font-size: 15px;
      line-height: 1.7;
      text-align: center;
    }

    .admin-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(220px, 1fr));
      gap: 18px;
      margin-top: 30px;
      text-align: left;
    }

    .admin-card {
      padding: 20px;
      background: rgba(0, 18, 40, 0.68);
      border: 1px solid rgba(150, 235, 255, 0.5);
      border-radius: 18px;
    }

    .admin-toggle {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      padding: 0;
      color: #9feaff;
      font-size: 22px;
      font-weight: 700;
      cursor: pointer;
      background: transparent;
      border: 0;
    }

    .admin-toggle span {
      color: #d8f7ff;
      font-size: 13px;
    }

    .admin-score-detail {
      margin-top: 14px;
    }

    .admin-score-detail[hidden] {
      display: none;
    }

    .admin-score-detail p {
      margin: 0 0 16px;
      color: #ffffff;
      font-size: 15px;
      line-height: 1.7;
      text-align: center;
    }

    .danger-button {
      display: block;
      width: 100%;
      padding: 14px 16px;
      color: #ffffff;
      font-size: 17px;
      font-weight: 700;
      text-align: center;
      cursor: pointer;
      background: rgba(210, 60, 80, 0.9);
      border: 1px solid rgba(255, 190, 200, 0.9);
      border-radius: 14px;
    }

    .danger-button:disabled {
      cursor: not-allowed;
      opacity: 0.45;
    }

    .admin-actions {
      display: grid;
      grid-template-columns: repeat(2, minmax(220px, 1fr));
      gap: 14px;
      margin-top: 22px;
    }

    .score-entry-list {
      display: grid;
      gap: 10px;
      margin: 14px 0 0;
      padding: 0;
      list-style: none;
    }

    .score-entry-list.is-scrollable {
      max-height: 280px;
      padding-right: 6px;
      overflow-y: auto;
    }

    .score-entry-list li {
      display: grid;
      grid-template-columns: 40px 1fr auto auto;
      gap: 10px;
      align-items: center;
      padding: 10px 12px;
      color: #ffffff;
      font-size: 14px;
      font-weight: 700;
      background: rgba(4, 32, 64, 0.78);
      border: 1px solid rgba(150, 235, 255, 0.28);
      border-radius: 12px;
    }

    .score-entry-list button {
      padding: 8px 10px;
      color: #ffffff;
      font-weight: 700;
      cursor: pointer;
      background: rgba(210, 60, 80, 0.9);
      border: 1px solid rgba(255, 190, 200, 0.8);
      border-radius: 10px;
    }

    .admin-message {
      min-height: 24px;
      margin: 22px 0 0;
      color: #9feaff;
      font-size: 16px;
      font-weight: 700;
    }

    .owner-menu-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(220px, 1fr));
      gap: 18px;
      margin-top: 30px;
    }

    .owner-menu-button {
      display: grid;
      place-items: center;
      min-height: 110px;
      padding: 20px;
      color: #ffffff;
      font-size: 22px;
      font-weight: 700;
      text-align: center;
      text-decoration: none;
      background: rgba(28, 150, 205, 0.9);
      border: 1px solid rgba(190, 245, 255, 0.9);
      border-radius: 18px;
      transition: transform 0.18s ease, background 0.18s ease;
    }

    .owner-menu-button:hover {
      transform: translateY(-4px);
      background: rgba(45, 170, 220, 0.95);
    }

    .game-select-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(160px, 1fr));
      gap: 18px;
      margin-top: 30px;
    }

    .game-select-button {
      display: grid;
      place-items: center;
      min-height: 120px;
      padding: 20px;
      color: #ffffff;
      font-size: 24px;
      font-weight: 700;
      text-align: center;
      text-decoration: none;
      background: rgba(28, 150, 205, 0.9);
      border: 1px solid rgba(190, 245, 255, 0.9);
      border-radius: 18px;
      transition: transform 0.18s ease, background 0.18s ease;
    }

    .game-select-button:hover {
      transform: translateY(-4px);
      background: rgba(45, 170, 220, 0.95);
    }

    .old-maid-setup {
      display: grid;
      gap: 18px;
      max-width: 420px;
      margin: 30px auto 0;
      text-align: left;
    }

    .old-maid-setup label {
      display: grid;
      gap: 8px;
      color: #d8f7ff;
      font-size: 16px;
      font-weight: 700;
    }

    .old-maid-setup select {
      width: 100%;
      padding: 14px 16px;
      color: #ffffff;
      font-size: 18px;
      background: rgba(0, 18, 40, 0.72);
      border: 1px solid rgba(150, 235, 255, 0.78);
      border-radius: 12px;
      outline: none;
    }

    .old-maid-table {
      display: grid;
      gap: 18px;
      width: 900px;
      max-width: calc(100vw - 420px);
      margin-top: 30px;
      text-align: left;
    }

    .old-maid-table[hidden] {
      display: none;
    }

    .old-maid-players {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
      align-items: stretch;
    }

    .old-maid-player {
      display: grid;
      grid-template-rows: auto auto 1fr;
      min-width: 0;
      min-height: 250px;
      padding: 16px;
      background: rgba(0, 18, 40, 0.68);
      border: 1px solid rgba(150, 235, 255, 0.5);
      border-radius: 16px;
    }

    .old-maid-player.is-active {
      border-color: #ffffff;
      box-shadow: 0 0 0 3px rgba(120, 225, 255, 0.22);
    }

    .old-maid-player h3 {
      margin: 0 0 10px;
      color: #9feaff;
      font-size: 18px;
    }

    .old-maid-player p {
      margin: 0;
      color: #ffffff;
      font-size: 15px;
      line-height: 1.7;
    }

    .old-maid-rank {
      color: #9feaff;
      font-weight: 700;
    }

    .old-maid-card-row {
      display: flex;
      flex-wrap: wrap;
      align-content: flex-start;
      gap: 8px;
      height: 150px;
      margin-top: 10px;
      padding-right: 6px;
      min-width: 0;
      overflow-y: auto;
    }

    .old-maid-card,
    .old-maid-card-back {
      display: grid;
      place-items: center;
      width: 48px;
      height: 66px;
      color: #ffffff;
      font-size: 15px;
      font-weight: 700;
      background: rgba(4, 32, 64, 0.9);
      border: 1px solid rgba(150, 235, 255, 0.6);
      border-radius: 10px;
    }

    .old-maid-card.is-joker {
      color: #ffdce5;
      background: rgba(130, 22, 58, 0.9);
      border-color: rgba(255, 190, 210, 0.82);
    }

    .old-maid-card-back {
      cursor: pointer;
      background: rgba(28, 150, 205, 0.88);
    }

    .old-maid-card-back:hover {
      transform: translateY(-3px);
      background: rgba(45, 170, 220, 0.95);
    }

    .old-maid-actions {
      display: grid;
      grid-template-columns: repeat(2, minmax(180px, 1fr));
      gap: 14px;
    }

    .sevens-setup {
      display: grid;
      gap: 18px;
      max-width: 420px;
      margin: 30px auto 0;
      text-align: left;
    }

    .sevens-setup label {
      display: grid;
      gap: 8px;
      color: #d8f7ff;
      font-size: 16px;
      font-weight: 700;
    }

    .sevens-setup select {
      width: 100%;
      padding: 14px 16px;
      color: #ffffff;
      font-size: 18px;
      background: rgba(0, 18, 40, 0.72);
      border: 1px solid rgba(150, 235, 255, 0.78);
      border-radius: 12px;
      outline: none;
    }

    .sevens-table {
      display: grid;
      gap: 18px;
      width: 980px;
      max-width: calc(100vw - 420px);
      margin-top: 30px;
      text-align: left;
    }

    .sevens-table[hidden] {
      display: none;
    }

    .sevens-actions {
      display: grid;
      grid-template-columns: repeat(3, minmax(160px, 1fr));
      gap: 14px;
    }

    .sevens-board {
      display: grid;
      gap: 10px;
      padding: 16px;
      background: rgba(0, 18, 40, 0.68);
      border: 1px solid rgba(150, 235, 255, 0.5);
      border-radius: 18px;
    }

    .sevens-row {
      display: grid;
      grid-template-columns: 36px repeat(13, minmax(0, 1fr));
      gap: 6px;
      align-items: center;
    }

    .sevens-suit {
      color: #9feaff;
      font-size: 20px;
      font-weight: 700;
      text-align: center;
    }

    .sevens-slot,
    .sevens-card {
      display: grid;
      place-items: center;
      min-width: 44px;
      height: 58px;
      color: #ffffff;
      font-size: 14px;
      font-weight: 700;
      background: rgba(4, 32, 64, 0.72);
      border: 1px dashed rgba(150, 235, 255, 0.32);
      border-radius: 10px;
    }

    .sevens-card {
      cursor: default;
      background: rgba(4, 32, 64, 0.92);
      border-style: solid;
      border-color: rgba(150, 235, 255, 0.62);
    }

    .sevens-card.is-red {
      color: #ffdce5;
      border-color: rgba(255, 190, 210, 0.76);
    }

    .sevens-card.is-playable {
      cursor: pointer;
      box-shadow: 0 0 0 3px rgba(120, 225, 255, 0.22);
    }

    .sevens-card.is-playable:hover {
      transform: translateY(-3px);
      background: rgba(28, 150, 205, 0.9);
    }

    .sevens-hand {
      display: flex;
      flex-wrap: wrap;
      align-content: flex-start;
      gap: 8px;
      height: 146px;
      padding: 12px;
      overflow-y: auto;
      background: rgba(0, 18, 40, 0.68);
      border: 1px solid rgba(150, 235, 255, 0.5);
      border-radius: 16px;
    }

    .sevens-players {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
    }

    .sevens-player {
      min-width: 0;
      padding: 14px;
      background: rgba(0, 18, 40, 0.68);
      border: 1px solid rgba(150, 235, 255, 0.5);
      border-radius: 16px;
    }

    .sevens-player.is-active {
      border-color: #ffffff;
      box-shadow: 0 0 0 3px rgba(120, 225, 255, 0.22);
    }

    .sevens-player h3 {
      margin: 0 0 8px;
      color: #9feaff;
      font-size: 18px;
    }

    .sevens-player p {
      margin: 0;
      color: #ffffff;
      font-size: 15px;
      line-height: 1.7;
    }

    .owner-contact-panel {
      margin-top: 30px;
      padding: 20px;
      text-align: left;
      background: rgba(0, 18, 40, 0.68);
      border: 1px solid rgba(150, 235, 255, 0.5);
      border-radius: 18px;
    }

    .owner-contact-panel h3 {
      margin: 0 0 14px;
      color: #9feaff;
      font-size: 22px;
      text-align: center;
    }

    .contact-message-list {
      display: grid;
      gap: 12px;
      max-height: 360px;
      margin: 0;
      padding: 0;
      overflow-y: auto;
      list-style: none;
    }

    .contact-message-list li {
      padding: 14px;
      color: #ffffff;
      background: rgba(4, 32, 64, 0.78);
      border: 1px solid rgba(150, 235, 255, 0.28);
      border-radius: 12px;
    }

    .contact-message-list strong {
      display: block;
      margin-bottom: 6px;
      color: #ffffff;
      font-size: 16px;
    }

    .contact-message-list small {
      display: block;
      margin-bottom: 10px;
      color: #9feaff;
      font-size: 13px;
      font-weight: 700;
    }

    .contact-message-list p,
    .empty-contact-message {
      margin: 0;
      color: #d8f7ff;
      font-size: 15px;
      line-height: 1.7;
      white-space: pre-wrap;
    }

    .contact-delete-form {
      margin-top: 12px;
      text-align: right;
    }

    .contact-delete-form button {
      padding: 8px 12px;
      color: #ffffff;
      font-size: 14px;
      font-weight: 700;
      cursor: pointer;
      background: rgba(210, 60, 80, 0.9);
      border: 1px solid rgba(255, 190, 200, 0.8);
      border-radius: 10px;
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
    breakout_class = "active" if active_page == "breakout" else ""
    ludo_class = "active" if active_page == "ludo" else ""
    trump_class = "active" if active_page == "trump" else ""
    ranking_class = "active" if active_page == "ranking" else ""
    contact_class = "active" if active_page == "contact" else ""
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
        <a class="{breakout_class}" href="/breakout">ブロック崩し</a>
        <a class="{ludo_class}" href="/ludo">ルドー</a>
        <a class="{trump_class}" href="/trump">トランプ</a>
        <a class="{ranking_class}" href="/ranking">ランキング</a>
        <a class="{contact_class}" href="/contact">お問い合わせ</a>
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


HOME_HTML = render_page(
    title="Ocean Game Hub",
    heading="Ocean Game Hub",
    message="サイドバーからゲームを選択",
)
TETRIS_HTML = render_page(
    title="テトリス | Ocean Game Hub",
    heading="テトリス",
    active_page="tetris",
    body_html="""<p>ラインをそろえてスコアを伸ばしましょう</p>
        <div class="game-panel">
          <canvas class="game-board" id="tetris-board" width="300" height="600"></canvas>
          <aside class="game-info">
            <div class="info-card">
              <h3>スコア</h3>
              <p id="tetris-score">0</p>
            </div>
            <div class="info-card">
              <h3>操作</h3>
              <ul>
                <li>← →: 移動</li>
                <li>↓: 早く落とす</li>
                <li>Space: 回転</li>
                <li>↑: 一気に落とす</li>
                <li>P: 一時停止</li>
              </ul>
            </div>
            <div class="info-card">
              <h3>状態</h3>
              <p id="tetris-status">スタート待ち</p>
            </div>
            <button class="primary-button" id="tetris-restart" type="button">スタート</button>
            <div class="info-card">
              <h3>ハイスコア</h3>
              <p><span id="tetris-high-score">0</span> / <span id="tetris-high-score-name">---</span></p>
            </div>
          </aside>
        </div>
        <div class="game-over-overlay" id="tetris-game-over" hidden>
          <div class="game-over-dialog" role="dialog" aria-modal="true" aria-labelledby="game-over-title">
            <h3 id="game-over-title">ゲームオーバー</h3>
            <p class="game-over-score">達成スコア: <span id="tetris-final-score">0</span></p>
            <form class="score-name-form" id="tetris-score-form">
              <label>
                プレイヤー名（3文字）
                <input id="tetris-player-name" name="player-name" maxlength="3" autocomplete="off" required>
              </label>
              <button class="primary-button" type="submit">登録</button>
              <p class="score-save-message" id="tetris-score-save-message"></p>
              <button class="primary-button" id="tetris-play-again" type="button">もう一度遊ぶ</button>
              <a class="primary-button" href="/">別のゲームで遊ぶ</a>
            </form>
          </div>
        </div>
        <script>
          const canvas = document.getElementById("tetris-board");
          const context = canvas.getContext("2d");
          const scoreElement = document.getElementById("tetris-score");
          const highScoreElement = document.getElementById("tetris-high-score");
          const highScoreNameElement = document.getElementById("tetris-high-score-name");
          const statusElement = document.getElementById("tetris-status");
          const restartButton = document.getElementById("tetris-restart");
          const gameOverOverlay = document.getElementById("tetris-game-over");
          const finalScoreElement = document.getElementById("tetris-final-score");
          const scoreForm = document.getElementById("tetris-score-form");
          const playerNameInput = document.getElementById("tetris-player-name");
          const scoreSaveMessage = document.getElementById("tetris-score-save-message");
          const playAgainButton = document.getElementById("tetris-play-again");

          const highScoreKey = "gameHubTetrisHighScore";
          const highScoreNameKey = "gameHubTetrisHighScoreName";
          const rankingKey = "gameHubTetrisRanking";
          const columns = 10;
          const rows = 20;
          const blockSize = 30;
          const baseDropInterval = 800;
          const minDropInterval = 120;
          const speedUpScoreStep = 500;
          const dropIntervalStep = 100;
          const colors = {
            I: "#60e7ff",
            J: "#5c8cff",
            L: "#ffb347",
            O: "#ffe45c",
            S: "#5cff9d",
            T: "#c77dff",
            Z: "#ff5c7a",
          };
          const shapes = {
            I: [[1, 1, 1, 1]],
            J: [[1, 0, 0], [1, 1, 1]],
            L: [[0, 0, 1], [1, 1, 1]],
            O: [[1, 1], [1, 1]],
            S: [[0, 1, 1], [1, 1, 0]],
            T: [[0, 1, 0], [1, 1, 1]],
            Z: [[1, 1, 0], [0, 1, 1]],
          };

          let board;
          let piece;
          let score;
          let highScore;
          let highScoreName;
          let dropCounter;
          let dropInterval;
          let lastTime;
          let hasStarted;
          let isPaused;
          let isGameOver;

          function createBoard() {
            return Array.from({ length: rows }, () => Array(columns).fill(""));
          }

          function createPiece() {
            const names = Object.keys(shapes);
            const name = names[Math.floor(Math.random() * names.length)];
            const matrix = shapes[name].map((row) => [...row]);
            return {
              name,
              matrix,
              x: Math.floor(columns / 2) - Math.ceil(matrix[0].length / 2),
              y: 0,
            };
          }

          function rotate(matrix) {
            return matrix[0].map((_, index) => matrix.map((row) => row[index]).reverse());
          }

          function hasCollision(target = piece) {
            return target.matrix.some((row, y) =>
              row.some((cell, x) => {
                if (!cell) {
                  return false;
                }
                const nextX = target.x + x;
                const nextY = target.y + y;
                return (
                  nextX < 0 ||
                  nextX >= columns ||
                  nextY >= rows ||
                  (nextY >= 0 && board[nextY][nextX])
                );
              })
            );
          }

          function mergePiece() {
            piece.matrix.forEach((row, y) => {
              row.forEach((cell, x) => {
                if (cell && piece.y + y >= 0) {
                  board[piece.y + y][piece.x + x] = piece.name;
                }
              });
            });
          }

          function clearLines() {
            let cleared = 0;
            for (let y = rows - 1; y >= 0; y -= 1) {
              if (board[y].every(Boolean)) {
                board.splice(y, 1);
                board.unshift(Array(columns).fill(""));
                cleared += 1;
                y += 1;
              }
            }

            if (cleared > 0) {
              score += [0, 100, 250, 380, 500][cleared];
              scoreElement.textContent = score;
              updateHighScore();
              updateDropSpeed();
            }
          }

          function updateDropSpeed() {
            const speedLevel = Math.floor(score / speedUpScoreStep);
            dropInterval = Math.max(
              minDropInterval,
              baseDropInterval - speedLevel * dropIntervalStep,
            );
          }

          function movePiece(offsetX) {
            piece.x += offsetX;
            if (hasCollision()) {
              piece.x -= offsetX;
            }
          }

          function dropPiece() {
            piece.y += 1;
            if (hasCollision()) {
              piece.y -= 1;
              mergePiece();
              clearLines();
              piece = createPiece();
              if (hasCollision()) {
                isGameOver = true;
                statusElement.textContent = "ゲームオーバー";
                updateHighScore();
                showGameOverDialog();
              }
            }
            dropCounter = 0;
          }

          function updateHighScore() {
            if (score <= highScore) {
              return;
            }

            highScore = score;
            highScoreName = "";
            highScoreElement.textContent = highScore;
            highScoreNameElement.textContent = "登録待ち";
            localStorage.setItem(highScoreKey, String(highScore));
            localStorage.removeItem(highScoreNameKey);
          }

          function showGameOverDialog() {
            finalScoreElement.textContent = score;
            scoreSaveMessage.textContent = "";
            playerNameInput.value = "";
            scoreForm.querySelector('button[type="submit"]').hidden = false;
            gameOverOverlay.hidden = false;
            playerNameInput.focus();
          }

          function hideGameOverDialog() {
            gameOverOverlay.hidden = true;
          }

          function saveScoreEntry(playerName) {
            const ranking = JSON.parse(localStorage.getItem(rankingKey) || "[]");
            ranking.push({
              name: playerName,
              score,
              playedAt: new Date().toISOString(),
            });
            ranking.sort((left, right) => right.score - left.score);
            localStorage.setItem(rankingKey, JSON.stringify(ranking.slice(0, 50)));

            if (score >= highScore && score > 0) {
              highScore = score;
              highScoreName = playerName;
              highScoreElement.textContent = highScore;
              highScoreNameElement.textContent = highScoreName;
              localStorage.setItem(highScoreKey, String(highScore));
              localStorage.setItem(highScoreNameKey, highScoreName);
            }
          }

          function findHighScoreName(targetScore) {
            const ranking = JSON.parse(localStorage.getItem(rankingKey) || "[]");
            const matchedEntry = ranking.find((entry) => entry.score === targetScore);
            return matchedEntry ? matchedEntry.name : "";
          }

          function rotatePiece() {
            const originalMatrix = piece.matrix;
            const originalX = piece.x;
            piece.matrix = rotate(piece.matrix);

            for (const offset of [0, -1, 1, -2, 2]) {
              piece.x = originalX + offset;
              if (!hasCollision()) {
                return;
              }
            }

            piece.matrix = originalMatrix;
            piece.x = originalX;
          }

          function hardDrop() {
            while (!hasCollision({ ...piece, y: piece.y + 1 })) {
              piece.y += 1;
            }
            dropPiece();
          }

          function drawCell(x, y, color) {
            context.fillStyle = color;
            context.fillRect(x * blockSize, y * blockSize, blockSize, blockSize);
            context.strokeStyle = "rgba(255, 255, 255, 0.18)";
            context.lineWidth = 2;
            context.strokeRect(x * blockSize + 1, y * blockSize + 1, blockSize - 2, blockSize - 2);
          }

          function draw() {
            context.fillStyle = "rgba(0, 12, 28, 0.96)";
            context.fillRect(0, 0, canvas.width, canvas.height);

            board.forEach((row, y) => {
              row.forEach((cell, x) => {
                if (cell) {
                  drawCell(x, y, colors[cell]);
                }
              });
            });

            if (piece) {
              piece.matrix.forEach((row, y) => {
                row.forEach((cell, x) => {
                  if (cell) {
                    drawCell(piece.x + x, piece.y + y, colors[piece.name]);
                  }
                });
              });
            }
          }

          function update(time = 0) {
            const deltaTime = time - lastTime;
            lastTime = time;

            if (hasStarted && !isPaused && !isGameOver) {
              dropCounter += deltaTime;
              if (dropCounter > dropInterval) {
                dropPiece();
              }
            }

            draw();
            requestAnimationFrame(update);
          }

          function startGame() {
            board = createBoard();
            piece = createPiece();
            score = 0;
            dropCounter = 0;
            dropInterval = baseDropInterval;
            lastTime = 0;
            hasStarted = true;
            isPaused = false;
            isGameOver = false;
            scoreElement.textContent = score;
            statusElement.textContent = "プレイ中";
            restartButton.textContent = "リスタート";
            hideGameOverDialog();
          }

          document.addEventListener("keydown", (event) => {
            if (event.target.closest("#tetris-game-over")) {
              return;
            }

            if (!hasStarted) {
              if (event.key === "Enter") {
                startGame();
              }
              return;
            }

            if (isGameOver) {
              return;
            }

            if (event.key === "p" || event.key === "P") {
              isPaused = !isPaused;
              statusElement.textContent = isPaused ? "一時停止中" : "プレイ中";
              return;
            }

            if (isPaused) {
              return;
            }

            if (event.key === "ArrowLeft") {
              movePiece(-1);
              event.preventDefault();
            } else if (event.key === "ArrowRight") {
              movePiece(1);
              event.preventDefault();
            } else if (event.key === "ArrowDown") {
              dropPiece();
              event.preventDefault();
            } else if (event.key === "ArrowUp") {
              hardDrop();
              event.preventDefault();
            } else if (event.code === "Space") {
              rotatePiece();
              event.preventDefault();
            } else if (event.key === "Enter") {
              startGame();
            }
          });

          restartButton.addEventListener("click", startGame);
          playAgainButton.addEventListener("click", startGame);
          playerNameInput.addEventListener("input", () => {
            playerNameInput.value = playerNameInput.value.slice(0, 3).toUpperCase();
          });
          scoreForm.addEventListener("submit", (event) => {
            event.preventDefault();
            const playerName = playerNameInput.value.trim().toUpperCase();
            if (!playerName) {
              scoreSaveMessage.textContent = "名前を入力してください";
              return;
            }

            saveScoreEntry(playerName);
            scoreSaveMessage.textContent = "スコアを登録しました";
            scoreForm.querySelector('button[type="submit"]').hidden = true;
          });

          board = createBoard();
          piece = null;
          score = 0;
          highScore = Number(localStorage.getItem(highScoreKey) || 0);
          highScoreName = localStorage.getItem(highScoreNameKey) || findHighScoreName(highScore);
          dropCounter = 0;
          dropInterval = baseDropInterval;
          lastTime = 0;
          hasStarted = false;
          isPaused = false;
          isGameOver = false;
          scoreElement.textContent = score;
          highScoreElement.textContent = highScore;
          highScoreNameElement.textContent = highScoreName || (highScore > 0 ? "登録待ち" : "---");
          draw();
          update();
        </script>""",
)
SHOOTING_HTML = render_page(
    title="シューティング | Ocean Game Hub",
    heading="シューティング",
    active_page="shooting",
    body_html="""<p>敵を撃ち落として地球を守りましょう</p>
        <div class="game-panel">
          <canvas class="game-board shooting-board" id="shooting-board" width="520" height="620"></canvas>
          <aside class="game-info">
            <div class="info-card">
              <h3>スコア</h3>
              <p id="shooting-score">0</p>
              <p>ステージ <span id="shooting-stage">1</span></p>
            </div>
            <div class="info-card">
              <h3>操作</h3>
              <ul>
                <li>← →: 移動</li>
                <li>Space: 弾を撃つ</li>
                <li>P: 一時停止</li>
              </ul>
            </div>
            <div class="info-card">
              <h3>状態</h3>
              <p id="shooting-status">スタート待ち</p>
            </div>
            <button class="primary-button" id="shooting-restart" type="button">スタート</button>
            <div class="info-card">
              <h3>ハイスコア</h3>
              <p><span id="shooting-high-score">0</span> / <span id="shooting-high-score-name">---</span></p>
            </div>
          </aside>
        </div>
        <div class="game-over-overlay" id="shooting-game-over" hidden>
          <div class="game-over-dialog" role="dialog" aria-modal="true" aria-labelledby="shooting-game-over-title">
            <h3 id="shooting-game-over-title">ゲームオーバー</h3>
            <p class="game-over-score">達成スコア: <span id="shooting-final-score">0</span></p>
            <form class="score-name-form" id="shooting-score-form">
              <label>
                プレイヤー名（3文字）
                <input id="shooting-player-name" name="player-name" maxlength="3" autocomplete="off" required>
              </label>
              <button class="primary-button" type="submit">登録</button>
              <p class="score-save-message" id="shooting-score-save-message"></p>
              <button class="primary-button" id="shooting-play-again" type="button">もう一度遊ぶ</button>
              <a class="primary-button" href="/">別のゲームで遊ぶ</a>
            </form>
          </div>
        </div>
        <script>
          const canvas = document.getElementById("shooting-board");
          const context = canvas.getContext("2d");
          const scoreElement = document.getElementById("shooting-score");
          const stageElement = document.getElementById("shooting-stage");
          const highScoreElement = document.getElementById("shooting-high-score");
          const highScoreNameElement = document.getElementById("shooting-high-score-name");
          const statusElement = document.getElementById("shooting-status");
          const restartButton = document.getElementById("shooting-restart");
          const gameOverOverlay = document.getElementById("shooting-game-over");
          const finalScoreElement = document.getElementById("shooting-final-score");
          const scoreForm = document.getElementById("shooting-score-form");
          const playerNameInput = document.getElementById("shooting-player-name");
          const scoreSaveMessage = document.getElementById("shooting-score-save-message");
          const playAgainButton = document.getElementById("shooting-play-again");

          const highScoreKey = "gameHubShootingHighScore";
          const highScoreNameKey = "gameHubShootingHighScoreName";
          const rankingKey = "gameHubShootingRanking";
          const playerWidth = 46;
          const playerHeight = 22;
          const bulletSpeed = 7;
          const baseEnemyBulletSpeed = 3.2;
          const baseEnemyFireInterval = 52;
          const enemyWidth = 32;
          const enemyHeight = 24;
          const enemyRows = 4;
          const enemyColumns = 9;
          const rareEnemySpawnFrames = 60 * 60;

          let player;
          let bullets;
          let enemyBullets;
          let enemies;
          let rareEnemy;
          let rareEnemyTimer;
          let enemyDirection;
          let enemyMoveTimer;
          let enemyMoveInterval;
          let enemyFireTimer;
          let stage;
          let score;
          let highScore;
          let highScoreName;
          let hasStarted;
          let isPaused;
          let isGameOver;
          let keys;

          function createEnemies() {
            const startX = 56;
            const startY = 70;
            const gapX = 42;
            const gapY = 36;
            const createdEnemies = [];

            for (let row = 0; row < enemyRows; row += 1) {
              for (let column = 0; column < enemyColumns; column += 1) {
                createdEnemies.push({
                  x: startX + column * gapX,
                  y: startY + row * gapY,
                  width: enemyWidth,
                  height: enemyHeight,
                  points: (enemyRows - row) * 10,
                });
              }
            }

            return createdEnemies;
          }

          function createRareEnemy() {
            const startsFromLeft = Math.random() > 0.5;
            return {
              x: startsFromLeft ? -70 : canvas.width + 10,
              y: 28,
              width: 58,
              height: 24,
              speed: startsFromLeft ? 2.4 : -2.4,
              points: 1000,
            };
          }

          function rectsOverlap(left, right) {
            return (
              left.x < right.x + right.width &&
              left.x + left.width > right.x &&
              left.y < right.y + right.height &&
              left.y + left.height > right.y
            );
          }

          function updateHighScore() {
            if (score <= highScore) {
              return;
            }

            highScore = score;
            highScoreName = "";
            highScoreElement.textContent = highScore;
            highScoreNameElement.textContent = "登録待ち";
            localStorage.setItem(highScoreKey, String(highScore));
            localStorage.removeItem(highScoreNameKey);
          }

          function showGameOverDialog() {
            finalScoreElement.textContent = score;
            scoreSaveMessage.textContent = "";
            playerNameInput.value = "";
            scoreForm.querySelector('button[type="submit"]').hidden = false;
            gameOverOverlay.hidden = false;
            playerNameInput.focus();
          }

          function hideGameOverDialog() {
            gameOverOverlay.hidden = true;
          }

          function finishGame(statusText) {
            if (isGameOver) {
              return;
            }

            isGameOver = true;
            statusElement.textContent = statusText;
            updateHighScore();
            showGameOverDialog();
          }

          function saveScoreEntry(playerName) {
            const ranking = JSON.parse(localStorage.getItem(rankingKey) || "[]");
            ranking.push({
              name: playerName,
              score,
              playedAt: new Date().toISOString(),
            });
            ranking.sort((left, right) => right.score - left.score);
            localStorage.setItem(rankingKey, JSON.stringify(ranking.slice(0, 50)));

            if (score >= highScore && score > 0) {
              highScore = score;
              highScoreName = playerName;
              highScoreElement.textContent = highScore;
              highScoreNameElement.textContent = highScoreName;
              localStorage.setItem(highScoreKey, String(highScore));
              localStorage.setItem(highScoreNameKey, highScoreName);
            }
          }

          function findHighScoreName(targetScore) {
            const ranking = JSON.parse(localStorage.getItem(rankingKey) || "[]");
            const matchedEntry = ranking.find((entry) => entry.score === targetScore);
            return matchedEntry ? matchedEntry.name : "";
          }

          function shoot() {
            const now = performance.now();
            if (now - player.lastShotAt < 280) {
              return;
            }

            bullets.push({
              x: player.x + player.width / 2 - 2,
              y: player.y - 12,
              width: 4,
              height: 12,
            });
            player.lastShotAt = now;
          }

          function updatePlayer() {
            if (keys.ArrowLeft) {
              player.x -= player.speed;
            }
            if (keys.ArrowRight) {
              player.x += player.speed;
            }
            player.x = Math.max(0, Math.min(canvas.width - player.width, player.x));
          }

          function updateBullets() {
            bullets.forEach((bullet) => {
              bullet.y -= bulletSpeed;
            });
            bullets = bullets.filter((bullet) => bullet.y + bullet.height > 0);

            enemyBullets.forEach((bullet) => {
              bullet.y += bullet.speed;
            });
            enemyBullets = enemyBullets.filter((bullet) => bullet.y < canvas.height);
          }

          function getEnemyMoveInterval() {
            return Math.max(6, 34 - (stage - 1) * 4);
          }

          function getEnemyMoveDistance() {
            return Math.min(22, 12 + (stage - 1) * 2);
          }

          function updateEnemies() {
            enemyMoveTimer += 1;
            if (enemyMoveTimer < enemyMoveInterval) {
              return;
            }
            enemyMoveTimer = 0;

            let shouldDrop = false;
            const moveDistance = getEnemyMoveDistance();
            enemies.forEach((enemy) => {
              enemy.x += enemyDirection * moveDistance;
              if (enemy.x <= 16 || enemy.x + enemy.width >= canvas.width - 16) {
                shouldDrop = true;
              }
            });

            if (shouldDrop) {
              enemyDirection *= -1;
              enemies.forEach((enemy) => {
                enemy.y += 18;
              });
            }

            enemyMoveInterval = getEnemyMoveInterval();
          }

          function updateRareEnemy() {
            if (rareEnemy) {
              rareEnemy.x += rareEnemy.speed;
              if (rareEnemy.x + rareEnemy.width < -20 || rareEnemy.x > canvas.width + 20) {
                rareEnemy = null;
              }
              return;
            }

            rareEnemyTimer += 1;
            if (rareEnemyTimer >= rareEnemySpawnFrames) {
              rareEnemy = createRareEnemy();
              rareEnemyTimer = 0;
            }
          }

          function updateEnemyFire() {
            enemyFireTimer += 1;
            const enemyFireInterval = Math.max(
              16,
              baseEnemyFireInterval - (stage - 1) * 6,
            );
            if (enemyFireTimer < enemyFireInterval || enemies.length === 0) {
              return;
            }
            enemyFireTimer = 0;

            const shooter = enemies[Math.floor(Math.random() * enemies.length)];
            enemyBullets.push({
              x: shooter.x + shooter.width / 2 - 3,
              y: shooter.y + shooter.height,
              width: 6,
              height: 12,
              speed: baseEnemyBulletSpeed + (stage - 1) * 0.45,
            });
          }

          function advanceStage() {
            stage += 1;
            stageElement.textContent = stage;
            statusElement.textContent = `ステージ ${stage}`;
            enemies = createEnemies();
            enemyBullets = [];
            enemyDirection = stage % 2 === 0 ? -1 : 1;
            enemyMoveTimer = 0;
            enemyFireTimer = 0;
            enemyMoveInterval = getEnemyMoveInterval();
          }

          function resolveCollisions() {
            bullets = bullets.filter((bullet) => {
              if (rareEnemy && rectsOverlap(bullet, rareEnemy)) {
                score += rareEnemy.points;
                scoreElement.textContent = score;
                statusElement.textContent = "レア敵撃破 +1000";
                updateHighScore();
                rareEnemy = null;
                return false;
              }

              const enemyIndex = enemies.findIndex((enemy) => rectsOverlap(bullet, enemy));
              if (enemyIndex === -1) {
                return true;
              }

              score += enemies[enemyIndex].points;
              scoreElement.textContent = score;
              updateHighScore();
              enemies.splice(enemyIndex, 1);
              return false;
            });

            if (enemyBullets.some((bullet) => rectsOverlap(bullet, player))) {
              finishGame("ゲームオーバー");
              return;
            }

            if (enemies.some((enemy) => enemy.y + enemy.height >= player.y)) {
              finishGame("侵略されました");
              return;
            }

            if (enemies.length === 0) {
              score += 200 + (stage - 1) * 50;
              scoreElement.textContent = score;
              updateHighScore();
              advanceStage();
            }
          }

          function drawPlayer() {
            context.fillStyle = "#9feaff";
            context.fillRect(player.x, player.y + 10, player.width, player.height - 10);
            context.fillRect(player.x + player.width / 2 - 5, player.y, 10, 14);
          }

          function drawEnemy(enemy) {
            context.fillStyle = "#5cff9d";
            context.fillRect(enemy.x, enemy.y + 6, enemy.width, enemy.height - 6);
            context.fillStyle = "#021329";
            context.fillRect(enemy.x + 7, enemy.y + 12, 5, 5);
            context.fillRect(enemy.x + enemy.width - 12, enemy.y + 12, 5, 5);
            context.fillStyle = "#5cff9d";
            context.fillRect(enemy.x + 4, enemy.y, 6, 8);
            context.fillRect(enemy.x + enemy.width - 10, enemy.y, 6, 8);
          }

          function drawRareEnemy() {
            if (!rareEnemy) {
              return;
            }

            context.fillStyle = "#ffe45c";
            context.fillRect(rareEnemy.x, rareEnemy.y + 8, rareEnemy.width, rareEnemy.height - 8);
            context.fillStyle = "#ff5c7a";
            context.fillRect(rareEnemy.x + 10, rareEnemy.y, rareEnemy.width - 20, 10);
            context.fillStyle = "#021329";
            context.fillRect(rareEnemy.x + 14, rareEnemy.y + 14, 7, 5);
            context.fillRect(rareEnemy.x + rareEnemy.width - 21, rareEnemy.y + 14, 7, 5);
          }

          function draw() {
            context.fillStyle = "rgba(0, 12, 28, 0.96)";
            context.fillRect(0, 0, canvas.width, canvas.height);

            context.fillStyle = "rgba(159, 234, 255, 0.35)";
            for (let i = 0; i < 60; i += 1) {
              const x = (i * 83) % canvas.width;
              const y = (i * 47) % canvas.height;
              context.fillRect(x, y, 2, 2);
            }

            drawRareEnemy();
            enemies.forEach(drawEnemy);

            context.fillStyle = "#ffe45c";
            bullets.forEach((bullet) => {
              context.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
            });

            context.fillStyle = "#ff5c7a";
            enemyBullets.forEach((bullet) => {
              context.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
            });

            drawPlayer();
          }

          function update() {
            if (hasStarted && !isPaused && !isGameOver) {
              updatePlayer();
              updateBullets();
              updateEnemies();
              updateRareEnemy();
              updateEnemyFire();
              resolveCollisions();
            }

            draw();
            requestAnimationFrame(update);
          }

          function startGame() {
            player = {
              x: canvas.width / 2 - playerWidth / 2,
              y: canvas.height - 58,
              width: playerWidth,
              height: playerHeight,
              speed: 5,
              lastShotAt: 0,
            };
            bullets = [];
            enemyBullets = [];
            enemies = createEnemies();
            rareEnemy = null;
            rareEnemyTimer = 0;
            enemyDirection = 1;
            enemyMoveTimer = 0;
            enemyFireTimer = 0;
            stage = 1;
            enemyMoveInterval = getEnemyMoveInterval();
            score = 0;
            hasStarted = true;
            isPaused = false;
            isGameOver = false;
            scoreElement.textContent = score;
            stageElement.textContent = stage;
            statusElement.textContent = "プレイ中";
            restartButton.textContent = "リスタート";
            hideGameOverDialog();
          }

          document.addEventListener("keydown", (event) => {
            if (event.target.closest("#shooting-game-over")) {
              return;
            }

            if (!hasStarted) {
              if (event.key === "Enter") {
                startGame();
              }
              return;
            }

            if (isGameOver) {
              return;
            }

            if (event.key === "p" || event.key === "P") {
              isPaused = !isPaused;
              statusElement.textContent = isPaused ? "一時停止中" : "プレイ中";
              return;
            }

            if (event.code === "Space") {
              shoot();
              event.preventDefault();
            }

            if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
              keys[event.key] = true;
              event.preventDefault();
            }
          });

          document.addEventListener("keyup", (event) => {
            if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
              keys[event.key] = false;
            }
          });

          restartButton.addEventListener("click", startGame);
          playAgainButton.addEventListener("click", startGame);
          playerNameInput.addEventListener("input", () => {
            playerNameInput.value = playerNameInput.value.slice(0, 3).toUpperCase();
          });
          scoreForm.addEventListener("submit", (event) => {
            event.preventDefault();
            const playerName = playerNameInput.value.trim().toUpperCase();
            if (!playerName) {
              scoreSaveMessage.textContent = "名前を入力してください";
              return;
            }

            saveScoreEntry(playerName);
            scoreSaveMessage.textContent = "スコアを登録しました";
            scoreForm.querySelector('button[type="submit"]').hidden = true;
          });

          player = {
            x: canvas.width / 2 - playerWidth / 2,
            y: canvas.height - 58,
            width: playerWidth,
            height: playerHeight,
            speed: 5,
            lastShotAt: 0,
          };
          bullets = [];
          enemyBullets = [];
          enemies = createEnemies();
          rareEnemy = null;
          rareEnemyTimer = 0;
          enemyDirection = 1;
          enemyMoveTimer = 0;
          enemyFireTimer = 0;
          stage = 1;
          enemyMoveInterval = getEnemyMoveInterval();
          score = 0;
          highScore = Number(localStorage.getItem(highScoreKey) || 0);
          highScoreName = localStorage.getItem(highScoreNameKey) || findHighScoreName(highScore);
          hasStarted = false;
          isPaused = false;
          isGameOver = false;
          keys = {};
          scoreElement.textContent = score;
          stageElement.textContent = stage;
          highScoreElement.textContent = highScore;
          highScoreNameElement.textContent = highScoreName || (highScore > 0 ? "登録待ち" : "---");
          draw();
          update();
        </script>""",
)
PUYOPUYO_HTML = render_page(
    title="ぷよぷよ | Ocean Game Hub",
    heading="ぷよぷよ",
    active_page="puyopuyo",
    body_html="""<p>同じ色を4つ以上つなげて消しましょう</p>
        <div class="game-panel">
          <canvas class="game-board puyo-board" id="puyo-board" width="240" height="480"></canvas>
          <aside class="game-info">
            <div class="info-card">
              <h3>スコア</h3>
              <p id="puyo-score">0</p>
              <p id="puyo-chain">0連鎖</p>
            </div>
            <div class="info-card">
              <h3>操作</h3>
              <ul>
                <li>← →: 移動</li>
                <li>↓: 早く落とす</li>
                <li>Space: 回転</li>
                <li>↑: 一気に落とす</li>
                <li>P: 一時停止</li>
              </ul>
            </div>
            <div class="info-card">
              <h3>状態</h3>
              <p id="puyo-status">スタート待ち</p>
            </div>
            <button class="primary-button" id="puyo-restart" type="button">スタート</button>
            <div class="info-card">
              <h3>ハイスコア</h3>
              <p><span id="puyo-high-score">0</span> / <span id="puyo-high-score-name">---</span></p>
            </div>
          </aside>
        </div>
        <div class="game-over-overlay" id="puyo-game-over" hidden>
          <div class="game-over-dialog" role="dialog" aria-modal="true" aria-labelledby="puyo-game-over-title">
            <h3 id="puyo-game-over-title">ゲームオーバー</h3>
            <p class="game-over-score">達成スコア: <span id="puyo-final-score">0</span></p>
            <form class="score-name-form" id="puyo-score-form">
              <label>
                プレイヤー名（3文字）
                <input id="puyo-player-name" name="player-name" maxlength="3" autocomplete="off" required>
              </label>
              <button class="primary-button" type="submit">登録</button>
              <p class="score-save-message" id="puyo-score-save-message"></p>
              <button class="primary-button" id="puyo-play-again" type="button">もう一度遊ぶ</button>
              <a class="primary-button" href="/">別のゲームで遊ぶ</a>
            </form>
          </div>
        </div>
        <script>
          const canvas = document.getElementById("puyo-board");
          const context = canvas.getContext("2d");
          const scoreElement = document.getElementById("puyo-score");
          const highScoreElement = document.getElementById("puyo-high-score");
          const highScoreNameElement = document.getElementById("puyo-high-score-name");
          const statusElement = document.getElementById("puyo-status");
          const chainElement = document.getElementById("puyo-chain");
          const restartButton = document.getElementById("puyo-restart");
          const gameOverOverlay = document.getElementById("puyo-game-over");
          const finalScoreElement = document.getElementById("puyo-final-score");
          const scoreForm = document.getElementById("puyo-score-form");
          const playerNameInput = document.getElementById("puyo-player-name");
          const scoreSaveMessage = document.getElementById("puyo-score-save-message");
          const playAgainButton = document.getElementById("puyo-play-again");

          const highScoreKey = "gameHubPuyopuyoHighScore";
          const highScoreNameKey = "gameHubPuyopuyoHighScoreName";
          const rankingKey = "gameHubPuyopuyoRanking";
          const columns = 6;
          const rows = 12;
          const cellSize = 40;
          const baseDropInterval = 820;
          const minDropInterval = 160;
          const speedUpScoreStep = 500;
          const dropIntervalStep = 70;
          const chainScoreTable = [0, 20, 50, 90, 140, 200, 270, 350, 440, 540, 650];
          const colors = ["red", "green", "blue", "yellow", "purple"];
          const colorMap = {
            red: "#ff5c7a",
            green: "#5cff9d",
            blue: "#60e7ff",
            yellow: "#ffe45c",
            purple: "#c77dff",
          };

          let board;
          let pair;
          let score;
          let highScore;
          let highScoreName;
          let dropCounter;
          let dropInterval;
          let lastTime;
          let hasStarted;
          let isPaused;
          let isGameOver;
          let isResolving;
          let clearingCells;

          function createBoard() {
            return Array.from({ length: rows }, () => Array(columns).fill(""));
          }

          function delay(milliseconds) {
            return new Promise((resolve) => {
              setTimeout(resolve, milliseconds);
            });
          }

          function flattenGroups(groups) {
            return groups.flatMap((group) => group);
          }

          function randomColor() {
            return colors[Math.floor(Math.random() * colors.length)];
          }

          function createPair() {
            return {
              x: Math.floor(columns / 2),
              y: 1,
              rotation: 0,
              colors: [randomColor(), randomColor()],
            };
          }

          function getPairCells(target = pair) {
            const offsets = [
              { x: 0, y: -1 },
              { x: 1, y: 0 },
              { x: 0, y: 1 },
              { x: -1, y: 0 },
            ];
            const offset = offsets[target.rotation];
            return [
              { x: target.x, y: target.y, color: target.colors[0] },
              { x: target.x + offset.x, y: target.y + offset.y, color: target.colors[1] },
            ];
          }

          function hasCollision(target = pair) {
            return getPairCells(target).some((cell) => (
              cell.x < 0 ||
              cell.x >= columns ||
              cell.y >= rows ||
              (cell.y >= 0 && board[cell.y][cell.x])
            ));
          }

          function movePair(offsetX) {
            const nextPair = { ...pair, x: pair.x + offsetX };
            if (!hasCollision(nextPair)) {
              pair = nextPair;
            }
          }

          function rotatePair() {
            for (const offsetX of [0, -1, 1, -2, 2]) {
              const nextPair = {
                ...pair,
                x: pair.x + offsetX,
                rotation: (pair.rotation + 1) % 4,
              };
              if (!hasCollision(nextPair)) {
                pair = nextPair;
                return;
              }
            }
          }

          function mergePair() {
            getPairCells().forEach((cell) => {
              if (cell.y >= 0) {
                board[cell.y][cell.x] = cell.color;
              }
            });
          }

          function applyGravity() {
            for (let x = 0; x < columns; x += 1) {
              const stack = [];
              for (let y = rows - 1; y >= 0; y -= 1) {
                if (board[y][x]) {
                  stack.push(board[y][x]);
                }
              }
              for (let y = rows - 1; y >= 0; y -= 1) {
                board[y][x] = stack[rows - 1 - y] || "";
              }
            }
          }

          function findGroups() {
            const visited = Array.from({ length: rows }, () => Array(columns).fill(false));
            const groups = [];

            for (let y = 0; y < rows; y += 1) {
              for (let x = 0; x < columns; x += 1) {
                const color = board[y][x];
                if (!color || visited[y][x]) {
                  continue;
                }

                const group = [];
                const queue = [{ x, y }];
                visited[y][x] = true;

                while (queue.length > 0) {
                  const current = queue.shift();
                  group.push(current);

                  for (const direction of [{ x: 1, y: 0 }, { x: -1, y: 0 }, { x: 0, y: 1 }, { x: 0, y: -1 }]) {
                    const nextX = current.x + direction.x;
                    const nextY = current.y + direction.y;
                    if (
                      nextX < 0 ||
                      nextX >= columns ||
                      nextY < 0 ||
                      nextY >= rows ||
                      visited[nextY][nextX] ||
                      board[nextY][nextX] !== color
                    ) {
                      continue;
                    }
                    visited[nextY][nextX] = true;
                    queue.push({ x: nextX, y: nextY });
                  }
                }

                if (group.length >= 4) {
                  groups.push(group);
                }
              }
            }

            return groups;
          }

          async function clearGroups() {
            let chain = 0;
            let clearedAny = false;

            while (true) {
              const groups = findGroups();
              if (groups.length === 0) {
                break;
              }

              chain += 1;
              clearedAny = true;
              statusElement.textContent = `${chain}連鎖`;
              chainElement.textContent = `${chain}連鎖`;
              await animateClearing(flattenGroups(groups));

              groups.forEach((group) => {
                group.forEach((cell) => {
                  board[cell.y][cell.x] = "";
                });
              });
              score += chainScoreTable[Math.min(chain, 10)];
              scoreElement.textContent = score;
              updateHighScore();
              await delay(250);
              applyGravity();
              await delay(350);
            }

            if (clearedAny) {
              updateDropSpeed();
              statusElement.textContent = "プレイ中";
            } else {
              chainElement.textContent = "0連鎖";
            }

            return clearedAny;
          }

          function updateDropSpeed() {
            const speedLevel = Math.floor(score / speedUpScoreStep);
            dropInterval = Math.max(
              minDropInterval,
              baseDropInterval - speedLevel * dropIntervalStep,
            );
          }

          async function dropPair() {
            if (isResolving) {
              return;
            }

            const nextPair = { ...pair, y: pair.y + 1 };
            if (!hasCollision(nextPair)) {
              pair = nextPair;
              dropCounter = 0;
              return;
            }

            mergePair();
            pair = null;
            applyGravity();
            isResolving = true;
            const clearedAny = await clearGroups();
            isResolving = false;
            if (!clearedAny) {
              chainElement.textContent = "0連鎖";
            }
            pair = createPair();
            if (hasCollision()) {
              isGameOver = true;
              statusElement.textContent = "ゲームオーバー";
              updateHighScore();
              showGameOverDialog();
            }
            dropCounter = 0;
          }

          async function hardDrop() {
            if (isResolving) {
              return;
            }

            while (!hasCollision({ ...pair, y: pair.y + 1 })) {
              pair = { ...pair, y: pair.y + 1 };
            }
            await dropPair();
          }

          function updateHighScore() {
            if (score <= highScore) {
              return;
            }

            highScore = score;
            highScoreName = "";
            highScoreElement.textContent = highScore;
            highScoreNameElement.textContent = "登録待ち";
            localStorage.setItem(highScoreKey, String(highScore));
            localStorage.removeItem(highScoreNameKey);
          }

          function showGameOverDialog() {
            finalScoreElement.textContent = score;
            scoreSaveMessage.textContent = "";
            playerNameInput.value = "";
            scoreForm.querySelector('button[type="submit"]').hidden = false;
            gameOverOverlay.hidden = false;
            playerNameInput.focus();
          }

          function hideGameOverDialog() {
            gameOverOverlay.hidden = true;
          }

          function saveScoreEntry(playerName) {
            const ranking = JSON.parse(localStorage.getItem(rankingKey) || "[]");
            ranking.push({
              name: playerName,
              score,
              playedAt: new Date().toISOString(),
            });
            ranking.sort((left, right) => right.score - left.score);
            localStorage.setItem(rankingKey, JSON.stringify(ranking.slice(0, 50)));

            if (score >= highScore && score > 0) {
              highScore = score;
              highScoreName = playerName;
              highScoreElement.textContent = highScore;
              highScoreNameElement.textContent = highScoreName;
              localStorage.setItem(highScoreKey, String(highScore));
              localStorage.setItem(highScoreNameKey, highScoreName);
            }
          }

          function findHighScoreName(targetScore) {
            const ranking = JSON.parse(localStorage.getItem(rankingKey) || "[]");
            const matchedEntry = ranking.find((entry) => entry.score === targetScore);
            return matchedEntry ? matchedEntry.name : "";
          }

          async function animateClearing(cells) {
            for (let frame = 0; frame < 6; frame += 1) {
              clearingCells = cells.map((cell) => ({
                ...cell,
                scale: frame % 2 === 0 ? 1.18 : 0.72,
                alpha: frame % 2 === 0 ? 1 : 0.45,
              }));
              draw();
              await delay(90);
            }

            clearingCells = [];
            draw();
          }

          function drawPuyo(x, y, color, scale = 1, alpha = 1) {
            const centerX = x * cellSize + cellSize / 2;
            const centerY = y * cellSize + cellSize / 2;
            context.save();
            context.globalAlpha = alpha;
            context.fillStyle = colorMap[color];
            context.beginPath();
            context.arc(centerX, centerY, cellSize * 0.42 * scale, 0, Math.PI * 2);
            context.fill();
            context.fillStyle = "rgba(255, 255, 255, 0.45)";
            context.beginPath();
            context.arc(centerX - 7 * scale, centerY - 8 * scale, cellSize * 0.12 * scale, 0, Math.PI * 2);
            context.fill();
            context.restore();
          }

          function draw() {
            context.fillStyle = "rgba(0, 12, 28, 0.96)";
            context.fillRect(0, 0, canvas.width, canvas.height);

            context.strokeStyle = "rgba(150, 235, 255, 0.12)";
            for (let x = 1; x < columns; x += 1) {
              context.beginPath();
              context.moveTo(x * cellSize, 0);
              context.lineTo(x * cellSize, canvas.height);
              context.stroke();
            }
            for (let y = 1; y < rows; y += 1) {
              context.beginPath();
              context.moveTo(0, y * cellSize);
              context.lineTo(canvas.width, y * cellSize);
              context.stroke();
            }

            board.forEach((row, y) => {
              row.forEach((color, x) => {
                if (color) {
                  const clearingCell = clearingCells.find((cell) => cell.x === x && cell.y === y);
                  if (clearingCell) {
                    drawPuyo(x, y, color, clearingCell.scale, clearingCell.alpha);
                    return;
                  }
                  drawPuyo(x, y, color);
                }
              });
            });

            if (pair) {
              getPairCells().forEach((cell) => {
                if (cell.y >= 0) {
                  drawPuyo(cell.x, cell.y, cell.color);
                }
              });
            }
          }

          function update(time = 0) {
            const deltaTime = time - lastTime;
            lastTime = time;

            if (hasStarted && !isPaused && !isGameOver && !isResolving) {
              dropCounter += deltaTime;
              if (dropCounter > dropInterval) {
                dropPair();
              }
            }

            draw();
            requestAnimationFrame(update);
          }

          function startGame() {
            board = createBoard();
            pair = createPair();
            score = 0;
            dropCounter = 0;
            dropInterval = baseDropInterval;
            lastTime = 0;
            hasStarted = true;
            isPaused = false;
            isGameOver = false;
            isResolving = false;
            clearingCells = [];
            scoreElement.textContent = score;
            chainElement.textContent = "0連鎖";
            statusElement.textContent = "プレイ中";
            restartButton.textContent = "リスタート";
            hideGameOverDialog();
          }

          document.addEventListener("keydown", (event) => {
            if (event.target.closest("#puyo-game-over")) {
              return;
            }

            if (!hasStarted) {
              if (event.key === "Enter") {
                startGame();
              }
              return;
            }

            if (isGameOver || isResolving) {
              return;
            }

            if (event.key === "p" || event.key === "P") {
              isPaused = !isPaused;
              statusElement.textContent = isPaused ? "一時停止中" : "プレイ中";
              return;
            }

            if (isPaused) {
              return;
            }

            if (event.key === "ArrowLeft") {
              movePair(-1);
              event.preventDefault();
            } else if (event.key === "ArrowRight") {
              movePair(1);
              event.preventDefault();
            } else if (event.key === "ArrowDown") {
              dropPair();
              event.preventDefault();
            } else if (event.key === "ArrowUp") {
              hardDrop();
              event.preventDefault();
            } else if (event.code === "Space") {
              rotatePair();
              event.preventDefault();
            } else if (event.key === "Enter") {
              startGame();
            }
          });

          restartButton.addEventListener("click", startGame);
          playAgainButton.addEventListener("click", startGame);
          playerNameInput.addEventListener("input", () => {
            playerNameInput.value = playerNameInput.value.slice(0, 3).toUpperCase();
          });
          scoreForm.addEventListener("submit", (event) => {
            event.preventDefault();
            const playerName = playerNameInput.value.trim().toUpperCase();
            if (!playerName) {
              scoreSaveMessage.textContent = "名前を入力してください";
              return;
            }

            saveScoreEntry(playerName);
            scoreSaveMessage.textContent = "スコアを登録しました";
            scoreForm.querySelector('button[type="submit"]').hidden = true;
          });

          board = createBoard();
          pair = null;
          score = 0;
          highScore = Number(localStorage.getItem(highScoreKey) || 0);
          highScoreName = localStorage.getItem(highScoreNameKey) || findHighScoreName(highScore);
          dropCounter = 0;
          dropInterval = baseDropInterval;
          lastTime = 0;
          hasStarted = false;
          isPaused = false;
          isGameOver = false;
          isResolving = false;
          clearingCells = [];
          scoreElement.textContent = score;
          chainElement.textContent = "0連鎖";
          highScoreElement.textContent = highScore;
          highScoreNameElement.textContent = highScoreName || (highScore > 0 ? "登録待ち" : "---");
          draw();
          update();
        </script>""",
)
BREAKOUT_HTML = render_page(
    title="ブロック崩し | Ocean Game Hub",
    heading="ブロック崩し",
    active_page="breakout",
    body_html="""<p>ボールを跳ね返して全てのブロックを壊しましょう</p>
        <div class="game-panel">
          <canvas class="game-board breakout-board" id="breakout-board" width="520" height="620"></canvas>
          <aside class="game-info">
            <div class="info-card">
              <h3>スコア</h3>
              <p id="breakout-score">0</p>
              <p>ステージ <span id="breakout-stage">1</span></p>
            </div>
            <div class="info-card">
              <h3>操作</h3>
              <ul>
                <li>← →: パドル移動</li>
                <li>Space: ボール発射</li>
                <li>P: 一時停止</li>
              </ul>
            </div>
            <div class="info-card">
              <h3>状態</h3>
              <p id="breakout-status">スタート待ち</p>
            </div>
            <button class="primary-button" id="breakout-restart" type="button">スタート</button>
            <div class="info-card">
              <h3>ハイスコア</h3>
              <p><span id="breakout-high-score">0</span> / <span id="breakout-high-score-name">---</span></p>
            </div>
          </aside>
        </div>
        <div class="game-over-overlay" id="breakout-game-over" hidden>
          <div class="game-over-dialog" role="dialog" aria-modal="true" aria-labelledby="breakout-game-over-title">
            <h3 id="breakout-game-over-title">ゲームオーバー</h3>
            <p class="game-over-score">達成スコア: <span id="breakout-final-score">0</span></p>
            <form class="score-name-form" id="breakout-score-form">
              <label>
                プレイヤー名（3文字）
                <input id="breakout-player-name" name="player-name" maxlength="3" autocomplete="off" required>
              </label>
              <button class="primary-button" type="submit">登録</button>
              <p class="score-save-message" id="breakout-score-save-message"></p>
              <button class="primary-button" id="breakout-play-again" type="button">もう一度遊ぶ</button>
              <a class="primary-button" href="/">別のゲームで遊ぶ</a>
            </form>
          </div>
        </div>
        <script>
          const canvas = document.getElementById("breakout-board");
          const context = canvas.getContext("2d");
          const scoreElement = document.getElementById("breakout-score");
          const stageElement = document.getElementById("breakout-stage");
          const highScoreElement = document.getElementById("breakout-high-score");
          const highScoreNameElement = document.getElementById("breakout-high-score-name");
          const statusElement = document.getElementById("breakout-status");
          const restartButton = document.getElementById("breakout-restart");
          const gameOverOverlay = document.getElementById("breakout-game-over");
          const finalScoreElement = document.getElementById("breakout-final-score");
          const scoreForm = document.getElementById("breakout-score-form");
          const playerNameInput = document.getElementById("breakout-player-name");
          const scoreSaveMessage = document.getElementById("breakout-score-save-message");
          const playAgainButton = document.getElementById("breakout-play-again");

          const highScoreKey = "gameHubBreakoutHighScore";
          const highScoreNameKey = "gameHubBreakoutHighScoreName";
          const rankingKey = "gameHubBreakoutRanking";
          const paddleWidth = 92;
          const paddleHeight = 16;
          const ballRadius = 8;
          const brickRows = 5;
          const brickColumns = 8;
          const brickWidth = 54;
          const brickHeight = 20;
          const brickGap = 8;
          const brickOffsetX = 22;
          const brickOffsetY = 70;
          const yellowBrickBonus = 120;
          const extendedPaddleWidth = 150;
          const paddleExtendDurationMs = 30000;

          let paddle;
          let balls;
          let bricks;
          let score;
          let highScore;
          let highScoreName;
          let stage;
          let hasStarted;
          let isPaused;
          let isGameOver;
          let keys;
          let paddleExtendUntil;

          function shouldPlaceBrick(row, column, pattern) {
            if (pattern === 1) {
              return row === 0 || (row + column) % 2 === 0;
            }
            if (pattern === 2) {
              return column === 0 || column === brickColumns - 1 || row % 2 === 0;
            }
            if (pattern === 3) {
              const center = (brickColumns - 1) / 2;
              return Math.abs(column - center) <= row + 1;
            }
            return true;
          }

          function getYellowBrickIndex(bricksForStage) {
            return (stage * 7 + 3) % bricksForStage.length;
          }

          function getGreenBrickIndex(bricksForStage, yellowIndex) {
            let greenIndex = (stage * 5 + 1) % bricksForStage.length;
            if (greenIndex === yellowIndex) {
              greenIndex = (greenIndex + 1) % bricksForStage.length;
            }
            return greenIndex;
          }

          function createBricks() {
            const createdBricks = [];
            const rowCount = Math.min(brickRows + 2, brickRows + Math.floor((stage - 1) / 2));
            const pattern = (stage - 1) % 4;
            const baseHits = 1 + Math.floor((stage - 1) / 3);

            for (let row = 0; row < rowCount; row += 1) {
              for (let column = 0; column < brickColumns; column += 1) {
                if (!shouldPlaceBrick(row, column, pattern)) {
                  continue;
                }

                const isReinforced = stage >= 3 && (row + column + stage) % 4 === 0;
                const hits = Math.min(4, baseHits + (isReinforced ? 1 : 0));
                createdBricks.push({
                  x: brickOffsetX + column * (brickWidth + brickGap),
                  y: brickOffsetY + row * (brickHeight + brickGap),
                  width: brickWidth,
                  height: brickHeight,
                  hits,
                  maxHits: hits,
                  points: (rowCount - row) * 10 * hits,
                  isYellow: false,
                  isGreen: false,
                });
              }
            }
            if (createdBricks.length > 0) {
              const yellowIndex = getYellowBrickIndex(createdBricks);
              const yellowBrick = createdBricks[yellowIndex];
              yellowBrick.isYellow = true;
              yellowBrick.hits = 1;
              yellowBrick.maxHits = 1;
              yellowBrick.points += yellowBrickBonus;

              if (createdBricks.length > 1) {
                const greenBrick = createdBricks[getGreenBrickIndex(createdBricks, yellowIndex)];
                greenBrick.isGreen = true;
                greenBrick.hits = 1;
                greenBrick.maxHits = 1;
              }
            }
            return createdBricks;
          }

          function rectsOverlap(left, right) {
            return (
              left.x < right.x + right.width &&
              left.x + left.width > right.x &&
              left.y < right.y + right.height &&
              left.y + left.height > right.y
            );
          }

          function createBall(launch = false, direction = 1) {
            return {
              x: paddle.x + paddle.width / 2,
              y: paddle.y - ballRadius - 2,
              radius: ballRadius,
              dx: launch ? direction * (3.4 + stage * 0.25) : 0,
              dy: launch ? -(4.2 + stage * 0.28) : 0,
              isLaunched: launch,
            };
          }

          function resetBall(launch = false) {
            balls = [createBall(launch)];
          }

          function doubleBalls() {
            balls = balls.flatMap((currentBall) => {
              if (!currentBall.isLaunched) {
                return [currentBall, createBall(false)];
              }

              return [
                currentBall,
                {
                  ...currentBall,
                  dx: currentBall.dx === 0 ? 3.2 : -currentBall.dx,
                  dy: currentBall.dy * 0.96,
                },
              ];
            });
            statusElement.textContent = "黄色ブロック: ボール倍増";
          }

          function extendPaddle() {
            const center = paddle.x + paddle.width / 2;
            paddle.width = extendedPaddleWidth;
            paddle.x = Math.max(0, Math.min(canvas.width - paddle.width, center - paddle.width / 2));
            paddleExtendUntil = performance.now() + paddleExtendDurationMs;
            statusElement.textContent = "緑ブロック: バー延長";
          }

          function updatePaddleExtension() {
            if (!paddleExtendUntil || performance.now() < paddleExtendUntil) {
              return;
            }

            const center = paddle.x + paddle.width / 2;
            paddle.width = paddleWidth;
            paddle.x = Math.max(0, Math.min(canvas.width - paddle.width, center - paddle.width / 2));
            paddleExtendUntil = 0;
          }

          function updateHighScore() {
            if (score <= highScore) {
              return;
            }

            highScore = score;
            highScoreName = "";
            highScoreElement.textContent = highScore;
            highScoreNameElement.textContent = "登録待ち";
            localStorage.setItem(highScoreKey, String(highScore));
            localStorage.removeItem(highScoreNameKey);
          }

          function showGameOverDialog() {
            finalScoreElement.textContent = score;
            scoreSaveMessage.textContent = "";
            playerNameInput.value = "";
            scoreForm.querySelector('button[type="submit"]').hidden = false;
            gameOverOverlay.hidden = false;
            playerNameInput.focus();
          }

          function hideGameOverDialog() {
            gameOverOverlay.hidden = true;
          }

          function finishGame(statusText) {
            if (isGameOver) {
              return;
            }

            isGameOver = true;
            statusElement.textContent = statusText;
            updateHighScore();
            showGameOverDialog();
          }

          function saveScoreEntry(playerName) {
            const ranking = JSON.parse(localStorage.getItem(rankingKey) || "[]");
            ranking.push({
              name: playerName,
              score,
              playedAt: new Date().toISOString(),
            });
            ranking.sort((left, right) => right.score - left.score);
            localStorage.setItem(rankingKey, JSON.stringify(ranking.slice(0, 50)));

            if (score >= highScore && score > 0) {
              highScore = score;
              highScoreName = playerName;
              highScoreElement.textContent = highScore;
              highScoreNameElement.textContent = highScoreName;
              localStorage.setItem(highScoreKey, String(highScore));
              localStorage.setItem(highScoreNameKey, highScoreName);
            }
          }

          function findHighScoreName(targetScore) {
            const ranking = JSON.parse(localStorage.getItem(rankingKey) || "[]");
            const matchedEntry = ranking.find((entry) => entry.score === targetScore);
            return matchedEntry ? matchedEntry.name : "";
          }

          function launchBall() {
            if (balls.some((currentBall) => !currentBall.isLaunched)) {
              balls = balls.map((currentBall, index) => {
                if (currentBall.isLaunched) {
                  return currentBall;
                }

                return createBall(true, index % 2 === 0 ? 1 : -1);
              });
              statusElement.textContent = "プレイ中";
            }
          }

          function updatePaddle() {
            updatePaddleExtension();
            if (keys.ArrowLeft) {
              paddle.x -= paddle.speed;
            }
            if (keys.ArrowRight) {
              paddle.x += paddle.speed;
            }
            paddle.x = Math.max(0, Math.min(canvas.width - paddle.width, paddle.x));
          }

          function updateBall() {
            balls.forEach((ball) => {
              if (!ball.isLaunched) {
                ball.x = paddle.x + paddle.width / 2;
                ball.y = paddle.y - ball.radius - 2;
                return;
              }

              ball.x += ball.dx;
              ball.y += ball.dy;

              if (ball.x - ball.radius <= 0 || ball.x + ball.radius >= canvas.width) {
                ball.dx *= -1;
                ball.x = Math.max(ball.radius, Math.min(canvas.width - ball.radius, ball.x));
              }
              if (ball.y - ball.radius <= 0) {
                ball.dy *= -1;
                ball.y = ball.radius;
              }

              const ballRect = {
                x: ball.x - ball.radius,
                y: ball.y - ball.radius,
                width: ball.radius * 2,
                height: ball.radius * 2,
              };
              if (rectsOverlap(ballRect, paddle) && ball.dy > 0) {
                const hitPosition = (ball.x - (paddle.x + paddle.width / 2)) / (paddle.width / 2);
                ball.dx = hitPosition * (4 + stage * 0.35);
                ball.dy = -Math.abs(ball.dy);
                ball.y = paddle.y - ball.radius - 1;
              }

              const brickIndex = bricks.findIndex((brick) => rectsOverlap(ballRect, brick));
              if (brickIndex !== -1) {
                const brick = bricks[brickIndex];
                score += Math.ceil(brick.points / brick.maxHits);
                scoreElement.textContent = score;
                updateHighScore();
                brick.hits -= 1;
                if (brick.hits <= 0) {
                  if (brick.isYellow) {
                    doubleBalls();
                  }
                  if (brick.isGreen) {
                    extendPaddle();
                  }
                  bricks.splice(brickIndex, 1);
                }
                ball.dy *= -1;
              }
            });

            balls = balls.filter((ball) => ball.y - ball.radius <= canvas.height);
            if (balls.length === 0) {
              finishGame("ゲームオーバー");
              return;
            }

            if (bricks.length === 0) {
              stage += 1;
              stageElement.textContent = stage;
              score += 200 + (stage - 2) * 80;
              scoreElement.textContent = score;
              updateHighScore();
              bricks = createBricks();
              resetBall(false);
              statusElement.textContent = `ステージ ${stage}`;
            }
          }

          function draw() {
            context.fillStyle = "rgba(0, 12, 28, 0.96)";
            context.fillRect(0, 0, canvas.width, canvas.height);

            bricks.forEach((brick) => {
              const hue = 185 + Math.floor(brick.y / 10);
              const lightness = Math.max(42, 68 - brick.hits * 7);
              context.fillStyle = brick.isYellow
                ? "#ffe45c"
                : brick.isGreen
                  ? "#5cff9d"
                  : `hsl(${hue}, 85%, ${lightness}%)`;
              context.fillRect(brick.x, brick.y, brick.width, brick.height);
              context.strokeStyle = "rgba(255, 255, 255, 0.35)";
              context.strokeRect(brick.x + 1, brick.y + 1, brick.width - 2, brick.height - 2);
              if (brick.isYellow || brick.isGreen) {
                context.fillStyle = "rgba(0, 18, 40, 0.85)";
                context.font = "bold 13px sans-serif";
                context.textAlign = "center";
                context.textBaseline = "middle";
                context.fillText(brick.isYellow ? "x2" : "W", brick.x + brick.width / 2, brick.y + brick.height / 2);
                return;
              }
              if (brick.maxHits > 1) {
                context.fillStyle = "rgba(255, 255, 255, 0.86)";
                context.font = "bold 13px sans-serif";
                context.textAlign = "center";
                context.textBaseline = "middle";
                context.fillText(brick.hits, brick.x + brick.width / 2, brick.y + brick.height / 2);
              }
            });

            context.fillStyle = "#9feaff";
            context.fillRect(paddle.x, paddle.y, paddle.width, paddle.height);
            context.fillStyle = "#ffe45c";
            balls.forEach((ball) => {
              context.beginPath();
              context.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
              context.fill();
            });
          }

          function update() {
            if (hasStarted && !isPaused && !isGameOver) {
              updatePaddle();
              updateBall();
            }

            draw();
            requestAnimationFrame(update);
          }

          function startGame() {
            paddle = {
              x: canvas.width / 2 - paddleWidth / 2,
              y: canvas.height - 48,
              width: paddleWidth,
              height: paddleHeight,
              speed: 7,
            };
            stage = 1;
            score = 0;
            bricks = createBricks();
            hasStarted = true;
            isPaused = false;
            isGameOver = false;
            keys = {};
            paddleExtendUntil = 0;
            scoreElement.textContent = score;
            stageElement.textContent = stage;
            statusElement.textContent = "Spaceで発射";
            restartButton.textContent = "リスタート";
            resetBall(false);
            hideGameOverDialog();
          }

          document.addEventListener("keydown", (event) => {
            if (event.target.closest("#breakout-game-over")) {
              return;
            }

            if (!hasStarted) {
              if (event.key === "Enter") {
                startGame();
              }
              return;
            }

            if (isGameOver) {
              return;
            }

            if (event.key === "p" || event.key === "P") {
              isPaused = !isPaused;
              statusElement.textContent = isPaused ? "一時停止中" : "プレイ中";
              return;
            }

            if (event.code === "Space") {
              launchBall();
              event.preventDefault();
            }

            if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
              keys[event.key] = true;
              event.preventDefault();
            }
          });

          document.addEventListener("keyup", (event) => {
            if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
              keys[event.key] = false;
            }
          });

          restartButton.addEventListener("click", startGame);
          playAgainButton.addEventListener("click", startGame);
          playerNameInput.addEventListener("input", () => {
            playerNameInput.value = playerNameInput.value.slice(0, 3).toUpperCase();
          });
          scoreForm.addEventListener("submit", (event) => {
            event.preventDefault();
            const playerName = playerNameInput.value.trim().toUpperCase();
            if (!playerName) {
              scoreSaveMessage.textContent = "名前を入力してください";
              return;
            }

            saveScoreEntry(playerName);
            scoreSaveMessage.textContent = "スコアを登録しました";
            scoreForm.querySelector('button[type="submit"]').hidden = true;
          });

          paddle = {
            x: canvas.width / 2 - paddleWidth / 2,
            y: canvas.height - 48,
            width: paddleWidth,
            height: paddleHeight,
            speed: 7,
          };
          stage = 1;
          score = 0;
          bricks = createBricks();
          highScore = Number(localStorage.getItem(highScoreKey) || 0);
          highScoreName = localStorage.getItem(highScoreNameKey) || findHighScoreName(highScore);
          hasStarted = false;
          isPaused = false;
          isGameOver = false;
          keys = {};
          paddleExtendUntil = 0;
          scoreElement.textContent = score;
          stageElement.textContent = stage;
          highScoreElement.textContent = highScore;
          highScoreNameElement.textContent = highScoreName || (highScore > 0 ? "登録待ち" : "---");
          resetBall(false);
          draw();
          update();
        </script>""",
)
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
            nextButton.hidden = currentPlayerIndex === 0 || isGameOver;
            render();
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
            isGameOver = false;

            dealCards(shuffle(createDeck()));
            removeAllPairs();
            normalizeCurrentPlayer();

            setupElement.hidden = true;
            tableElement.hidden = false;
            nextButton.hidden = true;
            statusElement.textContent = "あなたの番です。右隣の相手からカードを1枚選んでください";
            render();
            checkGameOver();
          }

          function resetGame() {
            players = [];
            currentPlayerIndex = 0;
            finishedOrder = [];
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
MEMORY_HTML = render_page(
    title="神経衰弱 | Ocean Game Hub",
    heading="神経衰弱",
    active_page="trump",
    message="このページは後日作成します",
)
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
        </div>
        <script>
          const rankingSources = [
            { elementId: "ranking-tetris", storageKey: "gameHubTetrisRanking" },
            { elementId: "ranking-shooting", storageKey: "gameHubShootingRanking" },
            { elementId: "ranking-puyopuyo", storageKey: "gameHubPuyopuyoRanking" },
            { elementId: "ranking-breakout", storageKey: "gameHubBreakoutRanking" },
          ];

          function loadRanking(storageKey) {
            try {
              const ranking = JSON.parse(localStorage.getItem(storageKey) || "[]");
              return Array.isArray(ranking) ? ranking : [];
            } catch {
              return [];
            }
          }

          function renderRanking({ elementId, storageKey }) {
            const listElement = document.getElementById(elementId);
            const topScores = loadRanking(storageKey)
              .filter((entry) => entry && entry.name && Number.isFinite(Number(entry.score)))
              .sort((left, right) => Number(right.score) - Number(left.score))
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
              .sort((left, right) => Number(right.score) - Number(left.score));
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
              .sort((left, right) => Number(right.score) - Number(left.score));

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
