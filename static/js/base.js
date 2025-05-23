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
