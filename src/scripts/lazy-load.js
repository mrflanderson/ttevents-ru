export function initLazyLoad() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        if (img.dataset.src) {
          img.src = img.dataset.src;
          img.classList.add('loaded');
          img.removeAttribute('data-src');
        }
        observer.unobserve(img);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('img.lazy-load').forEach(img => {
    observer.observe(img);
  });
}
