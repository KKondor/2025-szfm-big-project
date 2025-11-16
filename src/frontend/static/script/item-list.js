"use strict";

const API_BASE = "/api";
const BASKET_KEY = "basketItems";
const PAGE_SIZE = 6;

let allFoods = [];
let currentFilter = "all";
let renderedCount = 0;

document.addEventListener("DOMContentLoaded", () => {
  initItemListPage();
});

function initItemListPage() {
  const filterSelect = document.getElementById("food-type");
  if (filterSelect) {
    filterSelect.addEventListener("change", () => {
      currentFilter = filterSelect.value;
      renderFoods(true);
    });
  }

  loadFoods().catch(err => console.error("Food load error:", err));
  renderBasketSidebar();
}

async function loadFoods() {
  const res = await fetch(`${API_BASE}/foods`);
  if (!res.ok) throw new Error("GET /api/foods failed " + res.status);

  const data = await res.json();
  if (!data.success || !Array.isArray(data.foods)) {
    throw new Error("Invalid foods response");
  }

  allFoods = data.foods;

  buildTypeOptionsFromFoods(allFoods);
  renderedCount = 0;
  renderFoods(true);
}

function buildTypeOptionsFromFoods(foods) {
  const select = document.getElementById("food-type");
  if (!select) return;

  const typesSet = new Set();
  foods.forEach(food => {
    if (food.category) {
      typesSet.add(food.category.toLowerCase());
    }
  });

  select.innerHTML = "";

  const allOpt = document.createElement("option");
  allOpt.value = "all";
  allOpt.textContent = "All";
  select.appendChild(allOpt);

  Array.from(typesSet)
    .sort()
    .forEach(type => {
      const opt = document.createElement("option");
      opt.value = type;
      opt.textContent = type.charAt(0).toUpperCase() + type.slice(1);
      select.appendChild(opt);
    });

  currentFilter = "all";
}
