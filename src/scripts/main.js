import { initAccordion } from "./accordion.js";
import { initLazyLoad, initImageLoadEffects } from "./lazy-load.js";
import { initParticles } from "./particles.js";
import { initAnalytics } from "./analytics.js";

document.addEventListener("DOMContentLoaded", () => {
  console.log("TT Events site initialized");

  // Инициализация компонентов
  // Мобильное меню работает на чистом CSS (peer-checked), не требует JS
  // initMobileMenu();
  initAccordion();
  initLazyLoad();
  initImageLoadEffects();
  initParticles();

  // Аналитика с согласием
  if (localStorage.getItem("analytics-consent") === "true") {
    initAnalytics();
  }
});
