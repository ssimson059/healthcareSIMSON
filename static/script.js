const form = document.getElementById("chat-form");
const input = document.getElementById("user-input");
const messages = document.getElementById("messages");
const suggestions = document.getElementById("suggestions");

function addMessage(text, sender) {
  const div = document.createElement("div");
  div.className = "message " + sender;
  div.textContent = text;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

async function sendMessage(text) {
  addMessage(text, "user");
  input.value = "";

  const thinking = document.createElement("div");
  thinking.className = "message bot";
  thinking.textContent = "Thinking...";
  messages.appendChild(thinking);
  messages.scrollTop = messages.scrollHeight;

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });
    const data = await res.json();
    thinking.textContent = data.reply || "Sorry, something went wrong.";
  } catch (err) {
    thinking.textContent = "Error reaching the server. Is the backend running?";
  }
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  sendMessage(text);
});

suggestions.addEventListener("click", (e) => {
  if (e.target.tagName === "BUTTON") {
    sendMessage(e.target.textContent);
  }
});
