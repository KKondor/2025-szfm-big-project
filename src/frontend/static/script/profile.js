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

function initProfile() {
  const email = getEmailFromProfileInfo();
  if (!email) {
    console.warn("Nem találtam emailt a .profile-info blokkban.");
    setupPasswordChange(null);
    return;
  }

  loadUserDataAndOrders(email);
  setupPasswordChange(email);
}

function getEmailFromProfileInfo() {
  const infoDiv = document.querySelector(".profile-info");
  if (!infoDiv) return null;

  const paragraphs = infoDiv.querySelectorAll("p");
  for (const p of paragraphs) {
    const text = p.textContent.toLowerCase();
    if (text.includes("email")) {
      const parts = p.textContent.split(":");
      if (parts.length >= 2) {
        return parts[1].trim();
      }
    }
  }
  return null;
}

async function loadUserDataAndOrders(email) {
  try {
    const res = await fetch(`${API_BASE}/users/${encodeURIComponent(email)}`);
    if (!res.ok) {
      console.warn("GET /api/users/<email> hiba:", res.status);
      return;
    }

    const data = await res.json();
    if (!data.success || !data.user) {
      console.warn("User adat válasz hibás:", data);
      return;
    }

    const user = data.user;
    renderUserInfo(user);

    if (user.id) {
      await loadUserOrders(user.id);
    }
  } catch (err) {
    console.error("Hiba a user adatok betöltésekor:", err);
  }
}

function renderUserInfo(user) {
  const infoDiv = document.querySelector(".profile-info");
  if (!infoDiv) return;

  infoDiv.innerHTML = "";

  const nameP = document.createElement("p");
  nameP.innerHTML = `<strong>Name: </strong>${user.name || ""}`;

  const emailP = document.createElement("p");
  emailP.innerHTML = `<strong>Email: </strong>${user.email || ""}`;

  const phoneP = document.createElement("p");
  phoneP.innerHTML = `<strong>Phone: </strong>${user.phone || ""}`;

  const addressP = document.createElement("p");
  addressP.innerHTML = `<strong>Address: </strong>${user.address || ""}`;

  const roleP = document.createElement("p");
  const roleLabel = user.role === "admin" ? "Admin" : "Customer";
  roleP.innerHTML = `<strong>Role: </strong>${roleLabel}`;

  infoDiv.appendChild(nameP);
  infoDiv.appendChild(emailP);
  infoDiv.appendChild(phoneP);
  infoDiv.appendChild(addressP);
  infoDiv.appendChild(roleP);
}

async function loadUserOrders(userId) {
  const ordersList = document.querySelector(
    '.profile-section#view-orders .orders-list'
  );
  if (!ordersList) {
    console.warn("Nem találom a .orders-list elemet a view-orders szekcióban.");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/orders/user/${userId}`);
    if (!res.ok) {
      console.warn("GET /api/orders/user/<user_id> hiba:", res.status);
      return;
    }

    const data = await res.json();
    if (!data.success || !Array.isArray(data.orders)) {
      console.warn("Orders válasz hibás:", data);
      return;
    }

    ordersList.innerHTML = "";

    if (!data.orders.length) {
      const emptyMsg = document.createElement("p");
      emptyMsg.textContent = "You have no orders yet.";
      ordersList.appendChild(emptyMsg);
      return;
    }

    data.orders.forEach((order) => {
      const card = createOrderCard(order);
      ordersList.appendChild(card);
    });
  } catch (err) {
    console.error("Hiba az orders betöltésekor:", err);
  }
}

function createOrderCard(order) {
  const card = document.createElement("div");
  card.classList.add("order-card");

  const info = document.createElement("div");
  info.classList.add("order-info");

  const idSpan = document.createElement("span");
  idSpan.classList.add("order-id");
  idSpan.textContent = `#${order.order_id}`;

  const dateSpan = document.createElement("span");
  dateSpan.classList.add("order-date");
  const dateStr = order.order_date
    ? order.order_date.split("T")[0]
    : "";
  dateSpan.textContent = dateStr;

  info.appendChild(idSpan);
  info.appendChild(dateSpan);

  const progress = document.createElement("div");
  progress.classList.add("order-progress");

  const label = document.createElement("label");
  label.textContent = "Status";

  const bar = document.createElement("div");
  bar.classList.add("progress-bar");

  const fill = document.createElement("div");
  fill.classList.add("progress-fill");

  const status = (order.status || "").toLowerCase();
  fill.dataset.status = status;
  fill.textContent = capitalize(status);

  let width = "30%";
  if (status === "completed") width = "100%";
  if (status === "cancelled") width = "100%";
  fill.style.width = width;

  bar.appendChild(fill);
  progress.appendChild(label);
  progress.appendChild(bar);

  const summary = document.createElement("div");
  summary.classList.add("order-summary");

  if (Array.isArray(order.items) && order.items.length) {
    const ul = document.createElement("ul");
    ul.classList.add("order-items");

    order.items.forEach((item) => {
      const li = document.createElement("li");

      const nameSpan = document.createElement("span");
      nameSpan.classList.add("item-name");
      nameSpan.textContent = item.food_name;

      const qtySpan = document.createElement("span");
      qtySpan.classList.add("item-qty");
      qtySpan.textContent = `x${item.quantity}`;

      const priceSpan = document.createElement("span");
      priceSpan.classList.add("item-price");
      priceSpan.textContent = `${item.item_price} Ft`;

      li.appendChild(nameSpan);
      li.appendChild(qtySpan);
      li.appendChild(priceSpan);
      ul.appendChild(li);
    });

    summary.appendChild(ul);
  }

  const totalSpan = document.createElement("span");
  totalSpan.classList.add("order-total");
  totalSpan.innerHTML = `<strong>Total:</strong> ${order.total_price} Ft`;
  summary.appendChild(totalSpan);

  card.appendChild(info);
  card.appendChild(progress);
  card.appendChild(summary);

  return card;
}

function setupPasswordChange(initialEmail) {
  const form = document.querySelector("#change-password .profile-form");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const inputs = form.querySelectorAll("input[type='password']");
    if (inputs.length < 3) return;

    const currentPassword = inputs[0].value.trim();
    const newPassword = inputs[1].value.trim();
    const confirmPassword = inputs[2].value.trim();

    if (!currentPassword || !newPassword || !confirmPassword) {
      alert("Please fill in all password fields.");
      return;
    }

    if (newPassword !== confirmPassword) {
      alert("New password and confirmation do not match.");
      return;
    }

    const email = initialEmail || getEmailFromProfileInfo();
    if (!email) {
      alert("Cannot determine user email, password change failed.");
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/auth/change-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: email,
          new_password: newPassword
        })
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok || !data.success) {
        throw new Error(data.message || "Password change failed");
      }

      alert("Password changed successfully.");
      form.reset();
    } catch (err) {
      console.error("Password change error:", err);
      alert("Error changing password: " + err.message);
    }
  });
}
