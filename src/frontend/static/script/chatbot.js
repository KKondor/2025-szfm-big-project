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
}
