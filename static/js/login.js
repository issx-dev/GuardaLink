const signUpButton = document.getElementById("signUp");
const signInButton = document.getElementById("signIn");
const container = document.getElementById("container");

// Función para alternar contraseña
document.addEventListener("click", function (e) {
    if (e.target.closest(".toggle-password")) {
        const iconContainer = e.target.closest(".toggle-password");
        const input = iconContainer.previousElementSibling;
        const isPassword = input.type === "password";

        // Alternar tipo de input
        input.type = isPassword ? "text" : "password";

        // Alternar ícono
        iconContainer.setAttribute(
            "data-lucide",
            isPassword ? "eye-off" : "eye"
        );

        // Destruir y recrear ícono
        const icon = iconContainer.querySelector("svg");
        if (icon) icon.remove();
        lucide.createIcons();
    }
});

// Inicializar
document.addEventListener("DOMContentLoaded", () => {
    lucide.createIcons();
});

signUpButton.addEventListener("click", () => {
    container.classList.add("right-panel-active");
});

signInButton.addEventListener("click", () => {
    container.classList.remove("right-panel-active");
});
