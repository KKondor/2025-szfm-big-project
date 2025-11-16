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

function renderBasketPage() {
  const container = document.querySelector(".basket-items");
  const totalSpan = document.querySelector(".basket-total span:last-child");
  const checkoutBtn = document.querySelector(".checkout-btn");

  if (!container || !totalSpan || !checkoutBtn) return;

  const items = getBasket();
  container.innerHTML = "";

  let total = 0;

  items.forEach((item) => {
    total += item.price * item.qty;

    const row = document.createElement("div");
    row.classList.add("basket-item");

    const img = document.createElement("img");
    img.src = `/static/images/food.jpg`; // vagy saját image mező, ha elmented
    img.alt = item.name;

    const info = document.createElement("div");
    info.classList.add("basket-info");

    const title = document.createElement("h3");
    title.textContent = item.name;

    const details = document.createElement("div");
    details.classList.add("basket-details");

    const amount = document.createElement("span");
    amount.classList.add("basket-amount");
    amount.textContent = `x${item.qty}`;

    const price = document.createElement("span");
    price.classList.add("basket-price");
    price.textContent = `$${(item.price * item.qty).toFixed(2)}`;

    details.appendChild(amount);
    details.appendChild(price);

    info.appendChild(title);
    info.appendChild(details);

    const removeBtn = document.createElement("button");
    removeBtn.classList.add("remove-btn");
    removeBtn.innerHTML = "&times;";
    removeBtn.setAttribute("aria-label", "Remove item");
    removeBtn.addEventListener("click", () => {
      removeItem(item.id);
    });

    row.appendChild(img);
    row.appendChild(info);
    row.appendChild(removeBtn);

    container.appendChild(row);
  });

  totalSpan.textContent = `$${total.toFixed(2)}`;

  checkoutBtn.onclick = () => checkout(items);
}
