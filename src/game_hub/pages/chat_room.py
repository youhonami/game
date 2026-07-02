from ..layout import render_page


CHAT_ROOM_HTML = render_page(
    title="チャットルーム | Ocean Game Hub",
    heading="チャットルーム",
    active_page="chat-room",
    body_html="""<p>ユーザー同士でメッセージを投稿できます。投稿されたメッセージは誰でも閲覧できます。</p>
        <section class="info-card">
          <h3>メッセージ</h3>
          <div id="chat-room-messages" style="display: grid; gap: 10px; max-height: 360px; overflow-y: auto; margin-bottom: 18px;"></div>
          <form id="chat-room-form" class="contact-form">
            <label>
              お名前
              <input id="chat-room-name" type="text" maxlength="12" autocomplete="name" required>
            </label>
            <label>
              メッセージ
              <textarea id="chat-room-message" required></textarea>
            </label>
            <button type="submit">送信する</button>
          </form>
        </section>
        <script>
          const chatRoomMessagesElement = document.getElementById("chat-room-messages");
          const chatRoomForm = document.getElementById("chat-room-form");
          const chatRoomNameInput = document.getElementById("chat-room-name");
          const chatRoomMessageInput = document.getElementById("chat-room-message");

          function escapeChatRoomHtml(value) {
            return String(value)
              .replaceAll("&", "&amp;")
              .replaceAll("<", "&lt;")
              .replaceAll(">", "&gt;")
              .replaceAll('"', "&quot;")
              .replaceAll("'", "&#039;");
          }

          function renderChatRoomMessages(messages) {
            if (messages.length === 0) {
              chatRoomMessagesElement.innerHTML = '<p class="ranking-empty">まだメッセージがありません</p>';
              return;
            }

            chatRoomMessagesElement.innerHTML = messages
              .map((message) => `
                <div class="info-card">
                  <strong>${escapeChatRoomHtml(String(message.name).slice(0, 12))}</strong>
                  <p>${escapeChatRoomHtml(message.text)}</p>
                  <small>${escapeChatRoomHtml(message.sent_at)}</small>
                </div>
              `)
              .join("");
            chatRoomMessagesElement.scrollTop = chatRoomMessagesElement.scrollHeight;
          }

          async function loadChatRoomMessages() {
            const response = await fetch("/chat-room/messages");
            if (!response.ok) {
              chatRoomMessagesElement.innerHTML = '<p class="ranking-empty">メッセージを読み込めませんでした</p>';
              return;
            }

            const data = await response.json();
            renderChatRoomMessages(Array.isArray(data.messages) ? data.messages : []);
          }

          chatRoomForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            const name = chatRoomNameInput.value.trim();
            const text = chatRoomMessageInput.value.trim();
            if (!name || !text) {
              return;
            }

            const response = await fetch("/chat-room/messages", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ name, text }),
            });
            if (!response.ok) {
              return;
            }

            chatRoomMessageInput.value = "";
            const data = await response.json();
            renderChatRoomMessages(Array.isArray(data.messages) ? data.messages : []);
          });

          loadChatRoomMessages();
          setInterval(loadChatRoomMessages, 5000);
        </script>""",
)
