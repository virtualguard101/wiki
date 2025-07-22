document.addEventListener("DOMContentLoaded", () => {
  const elems = document.querySelectorAll(".scroll-fade");
  const io = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const img = el.querySelector("img[data-src]");
        if (img && img.dataset.src) {
          img.src = img.dataset.src;
          delete img.dataset.src;
        }
        el.classList.add("in-view");
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.2 });
  elems.forEach(el => io.observe(el));
});
