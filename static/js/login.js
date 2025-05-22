const signUpButton = document.getElementById("signUp");
const signInButton = document.getElementById("signIn");
const container = document.getElementById("container");

// Esta función se encarga de alternar el tipo de input entre password y text
// Añade un evento click a los elementos con la clase "toggle-password"
document.addEventListener("click", function (e) {
    // Verifica si el elemento clicado tiene la clase "toggle-password"
    if (e.target.closest(".toggle-password")) {
        // Si es así, busca el contenedor padre más cercano con la clase "toggle-password"
        const iconContainer = e.target.closest(".toggle-password");

        // Verifica si el contenedor tiene un elemento hermano anterior
        const input = iconContainer.previousElementSibling;
        // Valida si el input es de tipo password
        const isPassword = input.type === "password";

        // Alternar tipo de input, cambiando entre password y text
        input.type = isPassword ? "text" : "password"; // Si isPassword es true, cambia a text, de lo contrario a password

        // Alternar ícono, cambiar el atributo data-lucide
        iconContainer.setAttribute(
            "data-lucide",
            isPassword ? "eye-off" : "eye" // Cambia el ícono a "eye-off" si es password, de lo contrario a "eye"
        );

        // Eliminar el ícono existente y volver a crear los íconos de lucide
        const icon = iconContainer.querySelector("svg");
        if (icon) icon.remove();
        lucide.createIcons();
    }
});

// Inicializar, crear los íconos de lucide
// Se ejecuta cuando el DOM está completamente cargado
document.addEventListener("DOMContentLoaded", () => {
    lucide.createIcons();
});

// Añadir evento click a los botones de inicio de sesión y registro
// Cambia la clase del contenedor para mostrar el formulario correspondiente
signUpButton.addEventListener("click", () => {
    container.classList.add("right-panel-active");
});

signInButton.addEventListener("click", () => {
    container.classList.remove("right-panel-active");
});

// Auto-eliminación con barra de progreso
// Selecciona todos los mensajes de flash y les aplica un efecto de desvanecimiento
document.querySelectorAll(".mensajes-flash > div").forEach((message) => {
    // Crear un tiempo de animación para la barra de progreso
    setTimeout(() => {
        message.style.opacity = "0";
        setTimeout(() => message.remove(), 300);
    }, 3000); // 3 segundos = duración de la animación
});
