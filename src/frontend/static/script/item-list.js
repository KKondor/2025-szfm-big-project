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

function renderFoods(reset = false) {
  const container = document.querySelector(".item-list");
  if (!container) return;

  if (reset) {
    container.innerHTML = "";
    renderedCount = 0;
  }

  const filtered = allFoods.filter(food => {
    if (currentFilter === "all") return true;
    return (food.category || "").toLowerCase() === currentFilter.toLowerCase();
  });

  const toRender = filtered.slice(renderedCount, renderedCount + PAGE_SIZE);

  toRender.forEach(food => {
    const card = createFoodCard(food);
    container.appendChild(card);
  });

  renderedCount += toRender.length;

  let loadMoreBtn = document.getElementById("load-more-foods");
  if (filtered.length > renderedCount) {
    if (!loadMoreBtn) {
      loadMoreBtn = document.createElement("button");
      loadMoreBtn.id = "load-more-foods";
      loadMoreBtn.textContent = "Load more";
      loadMoreBtn.classList.add("load-more-btn");
      loadMoreBtn.addEventListener("click", () => renderFoods(false));
      container.parentElement.appendChild(loadMoreBtn);
    }
  } else if (loadMoreBtn) {
    loadMoreBtn.remove();
  }
}

function createFoodCard(food) {
  const card = document.createElement("div");
  card.classList.add("item-card");

  const img = document.createElement("img");
  img.src = `/static/images/${food.image || "food.jpg"}`;
  img.alt = food.name;

  const info = document.createElement("div");
  info.classList.add("info");

  const title = document.createElement("h2");
  title.textContent = food.name;

  info.appendChild(title);

  if (food.description) {
    const desc = document.createElement("p");
    desc.textContent = food.description;
    info.appendChild(desc);
  }

  const price = document.createElement("p");
  price.classList.add("price");
  price.textContent = `${Number(food.price).toFixed(2)} Ft`;

  info.appendChild(price);

  const btn = document.createElement("button");
  btn.classList.add("add-btn");
  btn.textContent = "🧺";
  btn.title = "Add to basket";
  btn.addEventListener("click", () => {
    addToBasket({
      id: food.id,
      name: food.name,
      price: Number(food.price)
    });
  });

  card.appendChild(img);
  card.appendChild(info);
  card.appendChild(btn);

  return card;
}
