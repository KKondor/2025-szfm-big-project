"use strict";

const API_BASE = "/api";

document.addEventListener("DOMContentLoaded", () => {
  setupEditForm();
});

function setupEditForm() {
  const form = document.getElementById("edit-food-form");
  const deleteBtn = document.getElementById("delete-food-btn");
  
  if (!form) return;

  // Az ID-t a HTML data attribútumból olvassuk ki
  const foodId = form.dataset.foodId; 
  
  console.log("Editing food ID:", foodId);
}
