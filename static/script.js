const chatLog = document.getElementById("chat-log");
const form = document.getElementById("chat-form");
const input = document.getElementById("chat-input");
const quickButtons = document.querySelectorAll(".pill");

function addMessage(text, sender) {
  const bubble = document.createElement("div");
  bubble.className = `bubble ${sender}`;
  bubble.textContent = text;
  chatLog.appendChild(bubble);
  bubble.scrollIntoView({ behavior: "smooth", block: "end" });
  return bubble;
}

async function sendMessage(text) {
  const trimmed = text.trim();
  if (!trimmed) return;

  addMessage(trimmed, "user");
  input.value = "";

  const loadingBubble = addMessage("Typing...", "bot");
  loadingBubble.classList.add("loading");

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: trimmed }),
    });
    const data = await res.json();

    loadingBubble.remove();

    if (data.error) {
      addMessage(`⚠️ ${data.error}`, "bot");
    } else {
      addMessage(data.reply, "bot");
    }
  } catch (err) {
    loadingBubble.remove();
    addMessage("⚠️ Could not reach the server. Is it running?", "bot");
  }
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  sendMessage(input.value);
});

quickButtons.forEach((btn) => {
  btn.addEventListener("click", () => sendMessage(btn.dataset.prompt));
});
