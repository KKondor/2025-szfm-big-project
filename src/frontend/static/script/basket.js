"use strict";

const API_BASE = "/api";
const BASKET_KEY = "basketItems";

document.addEventListener("DOMContentLoaded", () => {
  renderBasketPage();
});

function getBasket() {
  try {
    const raw = localStorage.getItem(BASKET_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function saveBasket(items) {
  localStorage.setItem(BASKET_KEY, JSON.stringify(items));
}
