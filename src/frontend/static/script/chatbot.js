"use strict";

const API_BASE = "/api";

document.addEventListener("DOMContentLoaded", () => {
  setupChatbot();
});

function setupChatbot() {
  const chatWindow = document.getElementById("chat-window");
  const chatForm = document.getElementById("chat-form");
  const userInput = document.getElementById("user-input");
  const typingIndicator = document.querySelector(".message.bot.typing");

  if (!chatWindow || !chatForm || !userInput) return;

  if (typingIndicator) typingIndicator.style.display = "none";

  chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage(message, "user");
    userInput.value = "";

    if (typingIndicator) {
        typingIndicator.style.display = "flex";
        scrollToBottom();
    }

   try {
      const res = await fetch(`${API_BASE}/chatbot/message`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
      });

      const data = await res.json().catch(() => ({}));

      if (typingIndicator) typingIndicator.style.display = "none";

      if (res.ok && data.success) {
        appendMessage(data.reply, "bot");
      } else {
        appendMessage("Sorry, I am having trouble connecting right now.", "bot");
      }
    } catch (err) {
      console.error("Chatbot error:", err);
      if (typingIndicator) typingIndicator.style.display = "none";
      appendMessage("Error: Could not reach the server.", "bot");
    }

  function appendMessage(text, sender) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message", sender);
    msgDiv.textContent = text;

    if (typingIndicator && typingIndicator.parentNode === chatWindow) {
        chatWindow.insertBefore(msgDiv, typingIndicator);
    } else {
        chatWindow.appendChild(msgDiv);
    }
    scrollToBottom();
  }
  
  function scrollToBottom() {
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }
}
