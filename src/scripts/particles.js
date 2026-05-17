/**
 * Particles.js для анимации фона
 * Запускается только на десктопе
 */
export function initParticles() {
  // Не запускаем на мобильных
  const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
  if (isMobile) return;

  // Проверяем, есть ли контейнер
  const particlesContainer = document.getElementById('particles-js');
  if (!particlesContainer) return;

  // Проверяем, есть ли particles.js
  if (typeof particlesJS === 'undefined') {
    // Загружаем particles.js динамически
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js';
    script.onload = () => {
      createParticles(particlesContainer);
    };
    document.head.appendChild(script);
  } else {
    createParticles(particlesContainer);
  }
}

function createParticles(container) {
  particlesJS(container.id, {
    "particles": {
      "number": { "value": 60 },
      "color": { "value": "#ff2d55" },
      "opacity": { "value": 1 },
      "size": { "value": 5 },
      "line_linked": { "enable": true, "distance": 150, "color": "#ff2d55", "opacity": 1 },
      "move": { "enable": true, "speed": 1.5 }
    },
    "interactivity": {
      "detect_on": "canvas",
      "events": {
        "onhover": { "enable": true, "mode": "grab" },
        "onclick": { "enable": false },
        "resize": true
      }
    }
  });
}
