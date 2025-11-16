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

    const imageName = file ? file.name : null;

    const payload = {
      name: name,
      description: description || null,
      image: imageName,
      price: price,
      category: category || null,
    };

    try {
      const res = await fetch(`${API_BASE}/foods`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
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

    const idText = idCell.textContent.trim(); // pl. "#001"
    const userId = parseInt(idText.replace("#", ""), 10);
    const uiRole = select.value;            // "Admin" vagy "User"
    const apiRole = uiRole.toLowerCase();   // "admin" / "user"

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
