"use strict";

const API_BASE = "/api";

document.addEventListener("DOMContentLoaded", () => {
  setupTabs();
  initProfile();
});

function setupTabs() {
  const buttons = document.querySelectorAll(".tab-btn");
  const sections = document.querySelectorAll(".profile-section");

  if (!buttons.length || !sections.length) return;

  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      buttons.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      sections.forEach((sec) => sec.classList.remove("active"));
      const target = document.getElementById(btn.dataset.target);
      if (target) target.classList.add("active");
    });
  });
}
