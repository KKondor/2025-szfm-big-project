"use strict";

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("registerForm");
    if (!form) return;

    const passwordInput = document.getElementById("password");
    const errorMessage = document.getElementById("error-message");

    function validatePassword(pwd) {
        const hasLength = pwd.length >= 6;
        const hasUpper = /[A-Z]/.test(pwd);
        const hasLower = /[a-z]/.test(pwd);
        const hasNumber = /[0-9]/.test(pwd);
        
        return {
            isValid: hasLength && hasUpper && hasLower && hasNumber,
            errors: { hasLength, hasUpper, hasLower, hasNumber }
        };
    }

    form.addEventListener("submit", (e) => {
        const pwd = passwordInput.value;
        const result = validatePassword(pwd);

        if (!result.isValid) {
            e.preventDefault();
            errorMessage.innerHTML = "Password must meet all requirements:<br>";
            if (!result.errors.hasLength) errorMessage.innerHTML += "- At least 6 characters<br>";
            if (!result.errors.hasUpper) errorMessage.innerHTML += "- At least one uppercase letter<br>";
            if (!result.errors.hasLower) errorMessage.innerHTML += "- At least one lowercase letter<br>";
            if (!result.errors.hasNumber) errorMessage.innerHTML += "- At least one number<br>";
            errorMessage.style.color = "red";
        }
    });
});
