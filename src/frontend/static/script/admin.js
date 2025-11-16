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
