# TODO — TT Events Astro (Tailwind CSS)

## ✅ Сделано

### Инфраструктура
- [x] Tailwind CSS v4 + `@tailwindcss/vite` в `astro.config.mjs`
- [x] `tailwind/tailwind.css` — кастомные компоненты, утилиты, анимации
- [x] `tailwind/tailwind.config.js` — цвета, шрифты, тени

### Компоненты (все на Tailwind, без inline `<style>`)
- [x] `Layout.astro` — Header + Footer + SEO + JSON-LD Schema.org
- [x] `Header.astro` — навигация + мобильное меню на `client:visible` (0 строк JS)
- [x] `Footer.astro` — футер с услугами и контактами
- [x] `Hero.astro` — hero с фоном/видео + CTA
- [x] `FAQ.astro` — аккордеон (требуется `accordion.js`)
- [x] `Partners.astro` — слайдер с бесконечной прокруткой
- [x] `ServiceCard.astro` — карточка услуги
- [x] `CaseCard.astro` — карточка кейса
- [x] `SEO.astro`

### Страницы
- [x] `index.astro` — полностью на Tailwind
- [x] `korporativy-moskva.astro` — Корпоративные мероприятия ✅
- [x] `timbilding-moskva.astro` — Тимбилдинги ✅
- [x] `novogodniy-korporativ.astro` — Новогодний корпоратив ✅
- [x] `case.astro` — Список кейсов ✅
- [ ] `home.astro` — дублирует index, удалить или переписать

---

## 📋 Осталось переписать на Tailwind

### Главная страница (2 страницы)
- [ ] `home.astro` — дублирует index, удалить или переписать

### Страницы услуг (34 страницы)
- [x] `aktivnye-timbildingi.astro` — Активные тимбилдинги ✅
- [x] `korporativy-moskva.astro` — Корпоративные мероприятия ✅
- [x] `timbilding-moskva.astro` — Тимбилдинги ✅
- [ ] `konferencii-i-forumy.astro` — Конференции и форумы
- [x] `novogodniy-korporativ.astro` — Новогодние корпоративы ✅
- [x] `prezentacii-novyh-produktov-launch-events.astro` — Launch Events ✅
- [x] `festivaly-i-gorodskie-meropriyatiya.astro` — Фестивали ✅
- [x] `gosudarstvennye-prazdniki.astro` — Государственные праздники ✅
- [x] `intellektualnye-igry.astro` — Интеллектуальные игры ✅
- [x] `kvesty-i-igry.astro` — Квесты и игры ✅
- [x] `master-klassy.astro` — Мастер-классы ✅
- [ ] `sportivnye-meropriyatiya.astro` — Спортивные мероприятия
- [x] `mice-delovoj-turizm.astro` — MICE и деловой туризм ✅
- [x] `party.astro` — Party ✅
- [x] `classic.astro` — Classic ✅
- [x] `mediaproekty.astro` — Медиапроекты ✅
- [x] `festivali.astro` — Фестивули ✅
- [ ] `zimnij-korporativ.astro` — Зимний корпоратив
- [x] `letnij-korporativ.astro` — Летний корпоратив ✅
- [x] `korporativ-na-prirode.astro` — Корпоратив на природе ✅
- [x] `korporativ-na-9-maya.astro` — Корпоратив на 9 Мая ✅
- [ ] `timilding-na-prirode.astro` — Тимбилдинг на природе
- [x] `immersivnyj-korporativ.astro` — Иммерсивный корпоратив ✅
- [x] `kreativnye-timbildingi.astro` — Креативные тимбилдинги ✅
- [x] `delovye-meropriyatiya.astro` — Деловые мероприятия ✅
- [x] `seminary-i-treningi.astro` — Семинары и тренинги ✅
- [ ] `strategicheskie-sessii-i-vorkshopy.astro` — Стратегические сессии
- [x] `onlajn-meropriyatiya.astro` — Онлайн мероприятия ✅
- [ ] `tendery.astro` — Тендеры
- [ ] `turisticheskie-i-ekskursionnye-meropriyatiya.astro` — Туристические мероприятия
- [ ] `yubilej-kompanii.astro` — Юбилей компании
- [x] `event-agentstvo-moskva.astro` — Event агентство ✅
- [x] `organizaciya-meropriyatij-v-moskve.astro` — Организация мероприятий ✅
- [ ] `aktivnye-timbildingi.astro` — Активные тимбилдинги
- [ ] `art-korporativ.astro` — Арт корпоратив

### Кейсы (~15 страниц)
- [ ] `case.astro` — список кейсов
- [ ] `case-9may.astro`
- [ ] `case-art-novy-god-otel-svezhy-veter-2026.astro`
- [ ] `case-artpop.astro`
- [ ] `case-eho-pobedy-ope-air-2025.astro`
- [ ] `case-ek-park.astro`
- [ ] `case-imersivny-thatr.astro`
- [ ] `case-korolevsky-novy-god-24.astro`
- [ ] `case-lauch-event-umg.astro`
- [ ] `case-maslenitsa-izmaylovo25case.astro`
- [ ] `case-nad-moskvoy-zarya.astro`
- [ ] `case-open-air-slava-skripka-bober-2025.astro`
- [ ] `case-post-den_nko_2024.astro`
- [ ] `case-post-mediaproekt-i-fotovystavka-supersila.astro`
- [ ] `case-vremena-goda.astro`
- [ ] `case-vremnadezhdfest2025.astro`

### Блог (~10 страниц)
- [ ] `blog.astro` — список статей
- [ ] `blog-3-trenda.astro`
- [ ] `blog-korporativ-na-9-maya-2026-v-moskve.astro`
- [ ] `blog-organizatsiya-korporativov-moskva-2026.astro`
- [ ] `blog-post-it-corporativ-idei.astro`
- [ ] `blog-post-it-corporativ.astro`
- [ ] `blog-post-kak-provesti-launch-event-10-formatov-prezentacii-novogo-produkta.astro`
- [ ] `blog-post-kak-vybrat-event-agentstvo-v-moskve.astro`
- [ ] `blog-post-korporativ-na-9-maya-dlya-kompanii-12-idej-meropriyatij-ko-dnyu-pobedy-scenarii-i-formaty-2026.astro`
- [ ] `blog-post-pochemu-russkie-narodnye-motivy-populyarny.astro`

### Прочее (5 страниц)
- [x] `o-nas.astro` — О нас ✅
- [ ] `video-portfolio.astro` — Видео портфолио
- [ ] `videoproduction.astro` — Видеопродакшн

---

## 🎯 Шаблон переписывания страницы

```astro
---
import Layout from '../components/Layout.astro';

const pageMeta = {
  title: '...'
  description: '...'
  ogTitle: '...'
  ogDescription: '...'
};
---

<Layout {...pageMeta}>
  <section class="py-16 bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Breadcrumbs -->
      <nav class="text-sm text-text-light mb-4">
        <a href="/" class="hover:text-primary">Главная</a> / <span class="font-medium text-text">Раздел</span>
      </nav>
      <h1 class="text-3xl md:text-4xl lg:text-5xl font-bold text-dark font-heading mb-8">Заголовок</h1>
      <p class="text-lg text-text-light max-w-3xl">Текст</p>
    </div>
  </section>
  
  <section class="py-16 md:py-24">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
        <!-- ServiceCard / CaseCard -->
      </div>
    </div>
  </section>
</Layout>
```

### Правила:
1. **Только** `import Layout` — Header/Footer внутри Layout
2. **Никаких** inline `<style>`, `<script>` блоков
3. **Только** Tailwind классы
4. **Уникальные** SEO мета-теги для каждой страницы
5. **Semantic HTML**: `<article>`, `<section>`, `<nav>`, `<main>`
6. **Изображения**: `alt`, `width`, `height`, `loading="lazy"`

---

## 🎨 Палитра Tailwind

| Токен | Значение | CSS |
|-------|----------|-----|
| `primary` | `#f15264` | `bg-primary` |
| `primary-dark` | `#d93f50` | `bg-primary-dark` |
| `dark` | `#1a1a1a` | `text-dark` |
| `text` | `#333333` | `text-text` |
| `text-light` | `#666666` | `text-text-light` |

### Полезные классы:
- **Container**: `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`
- **Section**: `py-16 md:py-24`
- **Section alt**: `py-16 md:py-24 bg-gray-50`
- **Grid**: `grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8`
- **Card**: `bg-white rounded-xl shadow-card hover:shadow-card-hover transition-all`
- **Title**: `text-3xl md:text-4xl lg:text-5xl font-bold text-dark font-heading`
- **Breadcrumbs**: `text-sm text-text-light mb-4`
- **Breadcrumb link**: `hover:text-primary`
ВАЖНО использовать edit file . когда mcp - файл уходит в никуда
и ещё я все картики сложил в public/images а видео в public/video
и cover рядом с видео с расширением png
НЕ ВЫДУМЫВАЕМ!
---

## 🚀 Запуск

```bash
npm run dev     # dev сервер
npm run build   # production build
npm run preview # предпросмотр
```
