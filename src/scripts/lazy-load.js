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
        if (img.dataset.srcset) {
          img.srcset = img.dataset.srcset;
          img.removeAttribute('data-srcset');
        }
        observer.unobserve(img);
      }
    });
  }, { 
    rootMargin: '200px 0px',
    threshold: 0.01 
  });

  document.querySelectorAll('img.lazy-load').forEach(img => {
    observer.observe(img);
  });
}

/**
 * Добавляет класс loaded ко всем видимым изображениям при загрузке
 */
export function initImageLoadEffects() {
  document.querySelectorAll('img:not(.lazy-load)').forEach(img => {
    if (img.complete) {
      img.classList.add('loaded');
    } else {
      img.addEventListener('load', () => {
        img.classList.add('loaded');
      });
    }
  });
}
