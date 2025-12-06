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
  });

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
