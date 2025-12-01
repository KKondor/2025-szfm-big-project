"use strict";

const API_BASE = "/api";
const BASKET_KEY = "basketItems";
const PAGE_SIZE = 6;

let allFoods = [];
let currentFilter = "all";
let renderedCount = 0;
let searchTerm = "";

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
  const searchInput = document.getElementById("food-search");
  if (searchInput) {
    searchInput.addEventListener("input", () => {
      searchTerm = searchInput.value.trim().toLowerCase();
      renderFoods(true);
    });
  }

  loadFoods().catch(err => console.error("Food load error:", err));
  renderBasketSidebar();
}

async function loadFoods() {
  const container = document.querySelector(".item-list");
  if (container) {
    container.innerHTML = `
      <div class="loading">
        <div class="spinner"></div>
        Loading items...
      </div>`;
  }
  try {
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
  catch (err) {
    console.error("Food load error:", err);
    if (container) {
      container.innerHTML = `<div class="error">Error loading items</div>`;
    }
  }
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
    const matchesCategory =
      currentFilter === "all" ||
      (food.category || "").toLowerCase() === currentFilter.toLowerCase();

    const matchesSearch =
      !searchTerm ||
      food.name.toLowerCase().includes(searchTerm) ||
      (food.description && food.description.toLowerCase().includes(searchTerm));

    return matchesCategory && matchesSearch;
  });



  if (filtered.length === 0 && reset) {
    container.innerHTML = `<div class="empty">No items found</div>`;
    return;
  }

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
  }

  else if (loadMoreBtn) {
    loadMoreBtn.remove();
  }

  loadMoreBtn = document.getElementById("load-more-foods");

  if (window.innerWidth <= 768) {
      if (loadMoreBtn) {
        container.style.marginBottom = "0"; 
        loadMoreBtn.style.marginBottom = "35vh";
      } else {
        container.style.marginBottom = "35vh";
      }
    } else {
      container.style.marginBottom = "1.5rem";
      if (loadMoreBtn) loadMoreBtn.style.marginBottom = "1.5rem";
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
      price: Number(food.price),
      image: food.image
    });
  });

  card.appendChild(img);
  card.appendChild(info);
  card.appendChild(btn);

  if (document.getElementById("is-admin")) {
    const editBtn = document.createElement("button");
    editBtn.classList.add("edit-btn");
    editBtn.textContent = "✏️";
    editBtn.title = "Edit item";
    editBtn.addEventListener("click", () => {
      window.location.href = `/foods/${food.id}`;
    });
    card.appendChild(editBtn);
  }

  return card;
}

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

function addToBasket(food) {
  const items = getBasket();
  const existing = items.find(i => i.id === food.id);
  if (existing) {
    existing.qty += 1;
  } else {
    items.push({ id: food.id, name: food.name, price: food.price, image: food.image, qty: 1 });
  }
  saveBasket(items);
  renderBasketSidebar();
}

function removeFromBasket(foodId) {
  let items = getBasket();
  const idx = items.findIndex(i => i.id === foodId);
  if (idx !== -1) {
    if (items[idx].qty > 1) {
      items[idx].qty -= 1;
    } else {
      items.splice(idx, 1);
    }
    saveBasket(items);
    renderBasketSidebar();
  }
}

function renderBasketSidebar() {
  const sidebar = document.getElementById("basket-sidebar");
  if (!sidebar) return;

  const itemsContainer = sidebar.querySelector(".basket-items");
  const totalSpan = sidebar.querySelector(".basket-total span:last-child");
  const checkoutBtn = sidebar.querySelector(".checkout-btn");

  if (!itemsContainer || !totalSpan || !checkoutBtn) return;

  const items = getBasket();
  itemsContainer.innerHTML = "";

  let total = 0;

  items.forEach(item => {
    total += item.price * item.qty;

    const row = document.createElement("div");
    row.classList.add("basket-item");

    const img = document.createElement("img");
    img.src = `/static/images/${item.image || "food.jpg"}`;
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
    price.textContent = `${(item.price * item.qty).toFixed(2)} Ft`;

    details.appendChild(amount);
    details.appendChild(price);
    info.appendChild(title);
    info.appendChild(details);

    const removeBtn = document.createElement("button");
    removeBtn.classList.add("remove-btn");
    removeBtn.innerHTML = "&times;";
    removeBtn.setAttribute("aria-label", "Remove item");
    removeBtn.addEventListener("click", () => removeFromBasket(item.id));

    row.appendChild(img);
    row.appendChild(info);
    row.appendChild(removeBtn);

    itemsContainer.appendChild(row);
  });

  totalSpan.textContent = `${total.toFixed(2)} Ft`;

  checkoutBtn.onclick = () => {
    window.location.href = "/basket";
  };
  if (items.length === 0) {
    sidebar.classList.remove("active");
  } else {
    sidebar.classList.add("active");
  }
}
