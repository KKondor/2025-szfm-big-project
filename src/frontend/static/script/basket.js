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
    img.src = `/static/images/food.jpg`;
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

function removeItem(foodId) {
  let items = getBasket();
  const idx = items.findIndex((i) => i.id === foodId);
  if (idx !== -1) {
    if (items[idx].qty > 1) {
      items[idx].qty -= 1;
    } else {
      items.splice(idx, 1);
    }
    saveBasket(items);
    renderBasketPage();
  }
}

async function checkout(items) {
  if (!items.length) {
    alert("Your basket is empty.");
    return;
  }

  const foodIds = [];
  items.forEach((item) => {
    for (let i = 0; i < item.qty; i++) {
      foodIds.push(item.id);
    }
  });

  try {
    const res = await fetch(`${API_BASE}/orders`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ food_ids: foodIds, note: "" })
    });

    const data = await res.json().catch(() => ({}));

    if (!res.ok || !data.success) {
      throw new Error(data.message || "Order creation failed");
    }

    saveBasket([]);
    renderBasketPage();
    alert("Order created successfully!");
    window.location.href = "/profile";
  } catch (err) {
    console.error(err);
    alert("Error creating order: " + err.message);
  }
}
