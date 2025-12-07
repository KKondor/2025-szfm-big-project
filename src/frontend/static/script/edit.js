"use strict";

const API_BASE = "/api";

document.addEventListener("DOMContentLoaded", () => {
  setupEditForm();
});

function setupEditForm() {
  const form = document.getElementById("edit-food-form");
  const deleteBtn = document.getElementById("delete-food-btn");
  
  if (!form) return;

  const foodId = form.dataset.foodId;

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
      window.location.href = `/item-list`; 
    } catch (err) {
      console.error("Error updating food:", err);
      alert("Error: " + err.message);
    }
  });

  if (deleteBtn) {
    deleteBtn.addEventListener("click", async () => {
        if (!confirm("Are you sure you want to delete this food?")) return;

        try {
            const res = await fetch(`${API_BASE}/foods/${foodId}`, {
                method: "DELETE"
            });
            const data = await res.json().catch(() => ({}));

            if (!res.ok || !data.success) {
                throw new Error(data.message || "Failed to delete food");
            }

            alert("Food deleted successfully.");
            window.location.href = "/item-list"; 
        } catch (err) {
            console.error("Error deleting food:", err);
            alert("Error: " + err.message);
        }
    });
  }
}
