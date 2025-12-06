"use strict";

const API_BASE = "/api";

document.addEventListener("DOMContentLoaded", () => {
  setupEditForm();
});

function setupEditForm() {
  const form = document.getElementById("edit-food-form");
  const deleteBtn = document.getElementById("delete-food-btn");
  
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    
    const formData = new FormData(form);

    try {
      const res = await fetch(`${API_BASE}/foods/files/${foodId}`, {
        method: "PUT",
        body: formData 
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok || !data.success) {
        throw new Error(data.message || "Failed to update food");
      }

      alert("Food updated successfully.");
      window.location.href = "/item-list.html"; 
    } catch (err) {
      console.error("Error updating food:", err);
      alert("Error: " + err.message);
    }
  });
}
