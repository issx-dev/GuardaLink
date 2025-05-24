
const popup = document.getElementById("popupContrasena");
const abrirBtn = document.getElementById("abrirPopup");
const cancelarBtn = document.getElementById("btnCancelar");

abrirBtn.addEventListener("click", () => {
    popup.style.display = "flex";
});

cancelarBtn.addEventListener("click", () => {
    popup.style.display = "none";
});

window.addEventListener("click", (e) => {
    if (e.target === popup) {
        popup.style.display = "none";
    }
});

