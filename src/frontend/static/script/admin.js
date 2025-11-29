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

function setupAddItemForm() {
  const section = document.getElementById("add-item");
  if (!section) return;

  const form = section.querySelector(".admin-form");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const nameInput = form.querySelector("#name");
    const priceInput = form.querySelector("#price");
    const descInput = form.querySelector("#description");
    const typeSelect = form.querySelector("#type");
    const imageInput = form.querySelector("#image");

    const name = nameInput.value.trim();
    const price = parseFloat(priceInput.value);
    const description = descInput.value.trim();
    const category = typeSelect.value;
    const file = imageInput.files[0] || null;

    if (!name || isNaN(price)) {
      alert("Name and price are required.");
      return;
    }

    // Build FormData instead of JSON
    const formData = new FormData();
    formData.append("name", name);
    formData.append("price", price);
    formData.append("description", description);
    formData.append("category", category);
    if (file) {
      formData.append("image", file); // actual file object
    }

    try {
      const res = await fetch(`${API_BASE}/foods/files`, {
        method: "POST",
        body: formData, // no headers, browser sets multipart/form-data automatically
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok || !data.success) {
        throw new Error(data.message || "Failed to create food");
      }

      alert("Food created successfully.");
      form.reset();
    } catch (err) {
      console.error("Error creating food:", err);
      alert("Error creating food: " + err.message);
    }
  });

}

function setupUsers() {
  const section = document.getElementById("manage-users");
  if (!section) return;

  const table = section.querySelector("table.admin-table");
  const tbody = section.querySelector("tbody");
  if (!table || !tbody) return;

  loadUsers(tbody).catch((err) => {
    console.warn("Nem sikerült betölteni a usereket, marad a statikus minta:", err);
  });

  table.addEventListener("change", async (e) => {
    const select = e.target;
    if (!select.classList.contains("role-select")) return;

    const row = select.closest("tr");
    const idCell = row?.querySelector("td:first-child");
    if (!idCell) return;

    const idText = idCell.textContent.trim(); 
    const userId = parseInt(idText.replace("#", ""), 10);
    const uiRole = select.value;            
    const apiRole = uiRole.toLowerCase();   

    try {
      await updateUserRole(userId, apiRole);
      showStatus(row, "Role updated ✓", false);
    } catch (err) {
      console.error(err);
      showStatus(row, "Error updating role", true);
    }
  });
}

async function loadUsers(tbody) {
  const res = await fetch(`${API_BASE}/users`);
  if (!res.ok) throw new Error("GET /api/users failed " + res.status);

  const data = await res.json();
  if (!data.success || !Array.isArray(data.users) || !data.users.length) return;

  tbody.innerHTML = "";

  data.users.forEach((user) => {
    const tr = document.createElement("tr");

    const idTd = document.createElement("td");
    idTd.textContent = `#${user.id}`;

    const nameTd = document.createElement("td");
    nameTd.textContent = user.name;

    const roleTd = document.createElement("td");
    const select = document.createElement("select");
    select.classList.add("role-select");

    ["admin", "user"].forEach((role) => {
      const opt = document.createElement("option");
      opt.value = capitalize(role);
      opt.textContent = capitalize(role);
      if (user.role && user.role.toLowerCase() === role) {
        opt.selected = true;
      }
      select.appendChild(opt);
    });

    roleTd.appendChild(select);
    tr.appendChild(idTd);
    tr.appendChild(nameTd);
    tr.appendChild(roleTd);
    tbody.appendChild(tr);
  });
}

async function updateUserRole(userId, role) {
  const res = await fetch(`${API_BASE}/users/${userId}/role`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ role })
  });

  if (!res.ok) throw new Error("PUT /api/users/id/role failed " + res.status);

  const data = await res.json();
  if (!data.success) {
    throw new Error("Role update error: " + (data.message || ""));
  }
}

function setupOrders() {
  const section = document.getElementById("view-orders");
  if (!section) return;

  const list = section.querySelector(".orders-list");
  if (!list) return;

  loadOrders(list).catch((err) => {
    console.warn("Nem sikerült betölteni az ordereket, marad a statikus minta:", err);
  });

  list.addEventListener("change", async (e) => {
    const select = e.target;
    if (!select.classList.contains("progress-select")) return;

    const card = select.closest(".order-card");
    const idSpan = card?.querySelector(".order-id");
    if (!idSpan) return;

    const orderId = parseInt(idSpan.textContent.replace("#", ""), 10);
    const uiStatus = select.value;  
    const apiStatus = uiStatus.toLowerCase(); 

    try {
      await updateOrderStatus(orderId, apiStatus);
      showStatus(card, "Status updated ✓", false);
    } catch (err) {
      console.error(err);
      showStatus(card, "Error updating status", true);
    }
  });
}

async function loadOrders(list) {
  const res = await fetch(`${API_BASE}/orders`);
  if (!res.ok) throw new Error("GET /api/orders failed " + res.status);

  const data = await res.json();
  if (!data.success || !Array.isArray(data.orders) || !data.orders.length) return;

  list.innerHTML = "";

  data.orders.forEach((order) => {
    const card = document.createElement("div");
    card.classList.add("order-card");

    const info = document.createElement("div");
    info.classList.add("order-info");

    const idSpan = document.createElement("span");
    idSpan.classList.add("order-id");
    idSpan.textContent = `#${order.order_id}`;

    const userSpan = document.createElement("span");
    userSpan.classList.add("user-id");
    userSpan.textContent = `User #${order.user_id} (${order.user_name || ""})`;

    const dateSpan = document.createElement("span");
    dateSpan.classList.add("order-date");
    dateSpan.textContent = order.order_date || "";

    info.appendChild(idSpan);
    info.appendChild(userSpan);
    info.appendChild(dateSpan);

    const progress = document.createElement("div");
    progress.classList.add("order-progress");

    const label = document.createElement("label");
    label.textContent = "Progress";

    const select = document.createElement("select");
    select.classList.add("progress-select");

    ["pending", "completed", "cancelled"].forEach((st) => {
      const opt = document.createElement("option");
      opt.value = capitalize(st);
      opt.textContent = capitalize(st);
      if (order.status && order.status.toLowerCase() === st) {
        opt.selected = true;
      }
      select.appendChild(opt);
    });

    progress.appendChild(label);
    progress.appendChild(select);

    card.appendChild(info);
    card.appendChild(progress);
    list.appendChild(card);
  });
}

async function updateOrderStatus(orderId, status) {
  const res = await fetch(`${API_BASE}/orders/${orderId}/status`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status })
  });

  if (!res.ok) throw new Error("PUT /api/orders/id/status failed " + res.status);

  const data = await res.json();
  if (!data.success) throw new Error("Order status error: " + (data.message || ""));
}

function showStatus(container, msg, isError) {
  /*let el = container.querySelector(".response");
  if (!el) {
    el = document.createElement("div");
    el.classList.add("js-inline-status");
    el.style.fontSize = "0.8rem";
    el.style.marginTop = "0.25rem";
    container.appendChild(el);
  }
  el.textContent = msg;
  el.style.color = isError ? "red" : "green";
  setTimeout(() => { el.textContent = ""; }, 2000);*/
  alert((isError ? "Error: " : "Success: ") + msg);
}

function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}
