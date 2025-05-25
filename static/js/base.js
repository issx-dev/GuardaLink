function toggleAvatarMenu() {
  const menu = document.getElementById("avatarMenu");
  menu.style.display = menu.style.display === "block" ? "none" : "block";
}

document.addEventListener("click", function (event) {
  const avatar = document.querySelector(".user-avatar");
  const menu = document.getElementById("avatarMenu");
  if (!avatar.contains(event.target) && !menu.contains(event.target)) {
    menu.style.display = "none";
  }
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