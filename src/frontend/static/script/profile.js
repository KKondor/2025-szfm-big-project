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
