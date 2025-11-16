"use strict";

const API_BASE = "/api";

document.addEventListener("DOMContentLoaded", () => {
  setupTabs();
  setupAddItemForm();
  setupUsers();
  setupOrders();
});


function setupTabs() {
  const tabButtons = document.querySelectorAll(".tab-btn");
  const sections = document.querySelectorAll(".admin-section");

  if (!tabButtons.length || !sections.length) return;

  tabButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      tabButtons.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      sections.forEach((sec) => sec.classList.remove("active"));
      const target = document.getElementById(btn.dataset.target);
      if (target) target.classList.add("active");
    });
  });
}
