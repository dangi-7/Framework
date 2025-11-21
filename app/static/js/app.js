document.querySelectorAll('.ratings input[type="range"]').forEach((slider) => {
  slider.addEventListener("input", () => {
    const badge = slider.nextElementSibling;
    if (badge) {
      badge.textContent = slider.value;
    }
  });
});
