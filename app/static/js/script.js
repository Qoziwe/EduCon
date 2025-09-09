document.addEventListener("DOMContentLoaded", () => {
  const closeBtns = document.querySelectorAll(".flash-close-btn");

  closeBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const overlay = btn.closest(".flash-modal-overlay");
      overlay.style.animation = "fadeOut 0.3s ease forwards";
      setTimeout(() => overlay.remove(), 300);
    });
  });
});

// Дополнительная анимация закрытия
const style = document.createElement("style");
style.textContent = `
@keyframes fadeOut {
  from { opacity: 1; }
  to { opacity: 0; }
}`;
document.head.appendChild(style);

document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById("avatar-upload");
  const avatarImg = document.querySelector(".avatar-img-large");

  fileInput.addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (file && file.type.startsWith("image/")) {
      const reader = new FileReader();
      reader.onload = (e) => {
        avatarImg.src = e.target.result; // обновляем аватарку на странице
      };
      reader.readAsDataURL(file);
    }
  });
});
