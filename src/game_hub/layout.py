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
      height: 100vh;
      padding: 42px 28px;
      overflow-y: auto;
      scrollbar-color: rgba(150, 235, 255, 0.72) rgba(4, 18, 36, 0.88);
      scrollbar-width: thin;
      background: rgba(4, 18, 36, 0.88);
      border-right: 2px solid rgba(120, 225, 255, 0.45);
      box-shadow: 12px 0 36px rgba(0, 0, 0, 0.32);
    }

    .sidebar::-webkit-scrollbar {
      width: 10px;
    }

    .sidebar::-webkit-scrollbar-track {
      background: rgba(4, 18, 36, 0.88);
    }

    .sidebar::-webkit-scrollbar-thumb {
      background: rgba(150, 235, 255, 0.72);
      border: 2px solid rgba(4, 18, 36, 0.88);
      border-radius: 999px;
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
      font-size: 20px;
      font-weight: 700;
      white-space: nowrap;
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

    .page-tetris main {
      padding: 16px 28px;
    }

    .page-tetris .hero {
      padding: 18px 28px;
    }

    .page-tetris .hero h2 {
      margin-bottom: 8px;
      font-size: 36px;
    }

    .page-tetris .hero > p {
      font-size: 16px;
    }

    .page-tetris .game-panel {
      gap: 18px;
      margin-top: 12px;
    }

    .page-tetris .game-board {
      width: 240px;
      height: 480px;
    }

    .page-tetris .game-info {
      gap: 8px;
    }

    .page-tetris .info-card {
      padding: 10px 12px;
    }

    .page-tetris .info-card h3 {
      margin-bottom: 6px;
      font-size: 15px;
    }

    .page-tetris .info-card p,
    .page-tetris .info-card ul {
      font-size: 13px;
      line-height: 1.45;
    }

    .page-tetris .primary-button {
      padding: 10px 12px;
      font-size: 15px;
    }

    .page-shooting main,
    .page-puyopuyo main {
      padding: 16px 28px;
    }

    .page-shooting .hero,
    .page-puyopuyo .hero {
      padding: 18px 28px;
    }

    .page-shooting .hero h2,
    .page-puyopuyo .hero h2 {
      margin-bottom: 8px;
      font-size: 36px;
    }

    .page-shooting .hero > p,
    .page-puyopuyo .hero > p {
      font-size: 16px;
    }

    .page-shooting .game-panel,
    .page-puyopuyo .game-panel {
      gap: 18px;
      margin-top: 12px;
    }

    .page-shooting .shooting-board {
      width: 400px;
      height: 477px;
    }

    .page-puyopuyo .puyo-board {
      width: 200px;
      height: 400px;
    }

    .page-shooting .game-info,
    .page-puyopuyo .game-info {
      gap: 8px;
    }

    .page-shooting .info-card,
    .page-puyopuyo .info-card {
      padding: 10px 12px;
    }

    .page-shooting .info-card h3,
    .page-puyopuyo .info-card h3 {
      margin-bottom: 6px;
      font-size: 15px;
    }

    .page-shooting .info-card p,
    .page-shooting .info-card ul,
    .page-puyopuyo .info-card p,
    .page-puyopuyo .info-card ul {
      font-size: 13px;
      line-height: 1.45;
    }

    .page-shooting .primary-button,
    .page-puyopuyo .primary-button {
      padding: 10px 12px;
      font-size: 15px;
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

    .score-name-form select {
      width: 100%;
      padding: 14px 16px;
      color: #ffffff;
      font-size: 16px;
      font-weight: 700;
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

    .memory-setup {
      display: grid;
      gap: 18px;
      max-width: 420px;
      margin: 30px auto 0;
      text-align: left;
    }

    .memory-setup label {
      display: grid;
      gap: 8px;
      color: #d8f7ff;
      font-size: 16px;
      font-weight: 700;
    }

    .memory-setup select {
      width: 100%;
      padding: 14px 16px;
      color: #ffffff;
      font-size: 18px;
      background: rgba(0, 18, 40, 0.72);
      border: 1px solid rgba(150, 235, 255, 0.78);
      border-radius: 12px;
      outline: none;
    }

    .memory-table {
      display: grid;
      gap: 18px;
      width: 760px;
      max-width: calc(100vw - 420px);
      margin-top: 30px;
      text-align: left;
    }

    .memory-table[hidden] {
      display: none;
    }

    .memory-actions {
      display: grid;
      grid-template-columns: repeat(2, minmax(180px, 1fr));
      gap: 14px;
    }

    .memory-board {
      display: grid;
      grid-template-columns: repeat(5, minmax(80px, 1fr));
      gap: 12px;
      padding: 16px;
      background: rgba(0, 18, 40, 0.68);
      border: 1px solid rgba(150, 235, 255, 0.5);
      border-radius: 18px;
    }

    .memory-card {
      display: grid;
      place-items: center;
      height: 86px;
      color: #ffffff;
      font-size: 26px;
      font-weight: 700;
      cursor: pointer;
      background: rgba(28, 150, 205, 0.88);
      border: 1px solid rgba(190, 245, 255, 0.82);
      border-radius: 14px;
    }

    .memory-card:hover {
      transform: translateY(-3px);
      background: rgba(45, 170, 220, 0.95);
    }

    .memory-card.is-open,
    .memory-card.is-matched {
      cursor: default;
      background: rgba(4, 32, 64, 0.95);
    }

    .memory-card.is-matched {
      color: #9feaff;
      opacity: 0.66;
    }

    .memory-players {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
    }

    .memory-player {
      min-width: 0;
      padding: 14px;
      background: rgba(0, 18, 40, 0.68);
      border: 1px solid rgba(150, 235, 255, 0.5);
      border-radius: 16px;
    }

    .memory-player.is-active {
      border-color: #ffffff;
      box-shadow: 0 0 0 3px rgba(120, 225, 255, 0.22);
    }

    .memory-player h3 {
      margin: 0 0 8px;
      color: #9feaff;
      font-size: 18px;
    }

    .memory-player p {
      margin: 0;
      color: #ffffff;
      font-size: 15px;
      line-height: 1.7;
    }

    .fifteen-puzzle-table {
      display: grid;
      gap: 18px;
      width: 520px;
      max-width: 100%;
      margin: 30px auto 0;
      text-align: left;
    }

    .fifteen-puzzle-board {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      padding: 16px;
      background: rgba(0, 18, 40, 0.68);
      border: 1px solid rgba(150, 235, 255, 0.5);
      border-radius: 18px;
    }

    .fifteen-tile {
      display: grid;
      place-items: center;
      aspect-ratio: 1;
      color: #ffffff;
      font-size: 30px;
      font-weight: 800;
      cursor: pointer;
      background: rgba(28, 150, 205, 0.9);
      border: 1px solid rgba(190, 245, 255, 0.9);
      border-radius: 14px;
      transition: transform 0.16s ease, background 0.16s ease;
    }

    .fifteen-tile:hover {
      transform: translateY(-3px);
      background: rgba(45, 170, 220, 0.95);
    }

    .fifteen-tile.is-empty {
      cursor: default;
      background: rgba(0, 8, 20, 0.42);
      border-style: dashed;
      opacity: 0.72;
    }

    .fifteen-tile.is-empty:hover {
      transform: none;
    }

    .fifteen-puzzle-actions {
      display: grid;
      grid-template-columns: repeat(2, minmax(160px, 1fr));
      gap: 14px;
    }

    .minesweeper-table {
      display: grid;
      gap: 18px;
      width: min(760px, 100%);
      margin: 30px auto 0;
      text-align: left;
    }

    .minesweeper-status-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(120px, 1fr));
      gap: 14px;
    }

    .minesweeper-board {
      display: grid;
      gap: 6px;
      padding: 14px;
      background: rgba(0, 18, 40, 0.68);
      border: 1px solid rgba(150, 235, 255, 0.5);
      border-radius: 18px;
    }

    .minesweeper-cell {
      display: grid;
      place-items: center;
      aspect-ratio: 1;
      color: #ffffff;
      font-size: 18px;
      font-weight: 800;
      cursor: pointer;
      background: rgba(28, 150, 205, 0.9);
      border: 1px solid rgba(190, 245, 255, 0.86);
      border-radius: 10px;
      transition: transform 0.12s ease, background 0.12s ease;
    }

    .minesweeper-cell:hover {
      transform: translateY(-2px);
      background: rgba(45, 170, 220, 0.95);
    }

    .minesweeper-cell.is-open {
      cursor: default;
      background: rgba(0, 18, 40, 0.78);
      border-color: rgba(150, 235, 255, 0.38);
      transform: none;
    }

    .minesweeper-cell.is-flagged {
      background: rgba(255, 170, 70, 0.86);
    }

    .minesweeper-cell.is-mine {
      background: rgba(210, 60, 80, 0.92);
    }

    .minesweeper-actions {
      display: grid;
      grid-template-columns: repeat(3, minmax(160px, 1fr));
      gap: 14px;
      align-items: end;
    }

    .uno-setup {
      display: grid;
      gap: 18px;
      max-width: 420px;
      margin: 30px auto 0;
      text-align: left;
    }

    .uno-setup label {
      display: grid;
      gap: 8px;
      color: #d8f7ff;
      font-size: 16px;
      font-weight: 700;
    }

    .uno-setup select,
    .uno-color-select {
      width: 100%;
      padding: 14px 16px;
      color: #ffffff;
      font-size: 18px;
      font-weight: 700;
      background: rgba(0, 18, 40, 0.72);
      border: 1px solid rgba(150, 235, 255, 0.78);
      border-radius: 12px;
      outline: none;
    }

    .uno-table {
      display: grid;
      gap: 18px;
      width: 960px;
      max-width: calc(100vw - 420px);
      margin-top: 30px;
      text-align: left;
    }

    .uno-table[hidden] {
      display: none;
    }

    .uno-actions {
      display: grid;
      grid-template-columns: repeat(4, minmax(140px, 1fr));
      gap: 14px;
      align-items: end;
    }

    .uno-actions label {
      display: grid;
      gap: 8px;
      color: #d8f7ff;
      font-size: 16px;
      font-weight: 700;
    }

    .uno-board {
      display: grid;
      grid-template-areas:
        ". top ."
        "left center right"
        ". bottom .";
      grid-template-columns: minmax(170px, 1fr) minmax(300px, 1.4fr) minmax(170px, 1fr);
      grid-template-rows: auto minmax(260px, auto) auto;
      gap: 16px;
      align-items: center;
      padding: 18px;
      background: rgba(0, 10, 24, 0.42);
      border: 1px solid rgba(150, 235, 255, 0.28);
      border-radius: 22px;
    }

    .uno-seat {
      min-height: 116px;
    }

    .uno-seat-top {
      grid-area: top;
    }

    .uno-seat-left {
      grid-area: left;
    }

    .uno-seat-right {
      grid-area: right;
    }

    .uno-seat-bottom {
      grid-area: bottom;
      display: grid;
      gap: 12px;
    }

    .uno-center {
      grid-area: center;
      display: grid;
      grid-template-columns: repeat(2, minmax(120px, 1fr));
      gap: 16px;
      align-items: center;
      justify-items: center;
      min-height: 250px;
      padding: 20px;
      background: radial-gradient(circle, rgba(28, 150, 205, 0.24), rgba(0, 18, 40, 0.72));
      border: 1px solid rgba(150, 235, 255, 0.5);
      border-radius: 24px;
    }

    .uno-deck-area,
    .uno-discard {
      display: grid;
      place-items: center;
      min-height: 190px;
      padding: 18px;
      background: rgba(0, 18, 40, 0.68);
      border: 1px solid rgba(150, 235, 255, 0.5);
      border-radius: 18px;
      text-align: center;
    }

    .uno-deck-area h3,
    .uno-discard h3 {
      margin: 0 0 10px;
      color: #9feaff;
      font-size: 20px;
    }

    .uno-deck-area p,
    .uno-discard p {
      margin: 10px 0 0;
      color: #ffffff;
      font-weight: 700;
    }

    .uno-card,
    .uno-card-back {
      display: grid;
      place-items: center;
      width: 76px;
      height: 106px;
      padding: 8px;
      color: #ffffff;
      font-size: 18px;
      font-weight: 900;
      text-align: center;
      border: 2px solid rgba(255, 255, 255, 0.8);
      border-radius: 14px;
      box-shadow: 0 8px 18px rgba(0, 0, 0, 0.28);
    }

    .uno-card {
      cursor: pointer;
      transition: transform 0.14s ease, box-shadow 0.14s ease;
    }

    .uno-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 12px 22px rgba(0, 0, 0, 0.36);
    }

    .uno-card.is-disabled {
      cursor: not-allowed;
      opacity: 0.46;
      transform: none;
    }

    .uno-card-back {
      background: rgba(4, 32, 64, 0.92);
    }

    .uno-card.is-red {
      background: #d94343;
    }

    .uno-card.is-blue {
      background: #2878d8;
    }

    .uno-card.is-green {
      background: #2f9d55;
    }

    .uno-card.is-yellow {
      color: #1d2430;
      background: #f2d24b;
    }

    .uno-card.is-wild {
      background: linear-gradient(135deg, #d94343 0 25%, #2878d8 25% 50%, #2f9d55 50% 75%, #f2d24b 75%);
    }

    .uno-hand {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 10px;
      min-height: 132px;
      padding: 14px;
      background: rgba(0, 18, 40, 0.68);
      border: 1px solid rgba(150, 235, 255, 0.5);
      border-radius: 18px;
    }

    .uno-player {
      padding: 16px;
      text-align: center;
      background: rgba(0, 18, 40, 0.68);
      border: 1px solid rgba(150, 235, 255, 0.5);
      border-radius: 16px;
    }

    .uno-player.is-active {
      border-color: #ffffff;
      box-shadow: 0 0 0 3px rgba(120, 225, 255, 0.22);
    }

    .uno-player h3,
    .uno-player p {
      margin: 0 0 10px;
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
    puzzle_class = "active" if active_page == "puzzle" else ""
    minesweeper_class = "active" if active_page == "minesweeper" else ""
    uno_class = "active" if active_page == "uno" else ""
    chat_room_class = "active" if active_page == "chat-room" else ""
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
<body class="page-{active_page or 'home'}">
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
        <a class="{puzzle_class}" href="/puzzle">15パズル</a>
        <a class="{minesweeper_class}" href="/minesweeper">マインスイーパー</a>
        <a class="{uno_class}" href="/uno">UNO</a>
        <a class="{chat_room_class}" href="/chat-room">チャットルーム</a>
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
