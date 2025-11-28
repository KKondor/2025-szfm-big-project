"use strict";

const API_BASE = "/api";

document.addEventListener("DOMContentLoaded", () => {
  setupForgotPassword();
});

function setupForgotPassword() {
  const form = document.getElementById("forgotForm");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const emailInput = document.getElementById("email");
    const newPasswordInput = document.getElementById("new-password");
    const confirmPasswordInput = document.getElementById("confirm-password");
    const errorMessageDiv = document.getElementById("error-message");

    const email = emailInput.value.trim();
    const newPassword = newPasswordInput.value.trim();
    const confirmPassword = confirmPasswordInput.value.trim();

    // Reset messages
    errorMessageDiv.innerHTML = "";
    errorMessageDiv.classList.remove("success");

    if (!email || !newPassword || !confirmPassword) {
      errorMessageDiv.textContent = "Please fill in all fields.";
      return;
    }

    if (newPassword !== confirmPassword) {
      errorMessageDiv.textContent = "New password and confirmation do not match.";
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/auth/change-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: email,
          new_password: newPassword
        })
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok || !data.success) {
        throw new Error(data.message || "Password reset failed");
      }

      // Show inline success message
      errorMessageDiv.textContent = "Password reset successfully. Redirecting to login...";
      errorMessageDiv.classList.add("success");

      form.reset();

      // Redirect after 2 seconds
      setTimeout(() => {
        window.location.href = "/login";
      }, 2000);

    } catch (err) {
      console.error("Password reset error:", err);
      errorMessageDiv.textContent = "Error resetting password: " + err.message;
    }
  });
}
