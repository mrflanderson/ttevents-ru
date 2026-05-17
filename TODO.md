# Рефакторинг дизайна и архитектуры (Tailwind CSS + Astro 5)

## ✅ Выполнено
- [x] **Tailwind / дизайн**:
  - [x] Footer: новые градиенты, glassmorphism, современные элементы.
  - [x] Header: backdrop-blur, чистая навигация, hover-переходы.
  - [x] Hero: улучшенная система оверлеев для читаемости.
  - [x] Layout: глобальный фон (`bg-gray-50`), flex-структура для футера.
  - [x] Tailwind: добавлены кастомные анимации (scroll, shimmer, fadeIn).
  - [x] Удалены legacy CSS файлы (footer.css, header.css, hero.css и др., 10 файлов).
- [x] **FAQ**: переписан как реактивный компонент, без accordion.js.
- [x] **MobileMenu / Header (a11y)**:
  - [x] Добавлены ARIA-атрибуты, keyboard-навигация, Escape, базовый focus-trap.
- [x] **Архитектура / маршрутизация**:
  - [x] Внедрены Astro Content Collections: blog, cases.
  - [x] Созданы динамические страницы /blog/[slug], /case/[slug].
  - [x] Перенесены списки на getCollection вместо жёсткого кода.
  - [x] Добавлены шаблоны TEMPLATE_EXAMPLE.md для авторов контента.
  - [x] Добавлены 301-редиректы из старых URL (blog-post-*, case-*).
- [x] **Конфигурация / качество**:
  - [x] Обновлены зависимости: astro, sitemap, tailwind, lightbox.
  - [x] Добавлены скрипты: check, typecheck, lint.
  - [x] Обновлён tsconfig (strict, NodeNext, verbatimModuleSyntax).

## 📋 К выполнению (near-term)

### SEO и мета (High)
- [ ] Ввести единый SEO-шаблон:
  - [ ] Компонент `SeoMeta.astro` или `seo.ts` с типизацией, без автофоллов.
  - [ ] Каждая страница передаёт явные title/description/canonical/og.
- [ ] Настроить canonical URL:
  - [ ] Использовать `site + pathname` вместо `Astro.url.pathname`.
- [ ] Прописать page-level JSON-LD:
  - [ ] Article schema для постов блога (/blog/[slug]).
  - [ ] Event/Case schema для кейсов (/case/[slug]).
- [ ] Поправить Organization JSON-LD:
  - [ ] Поставить реальный logo (не favicon).
  - [ ] Добавить contactPoint с телефоном и e-mail.
- [ ] Добавить поддержку noindex для черновиков / служебных страниц.

### HTML-семантика и доступность (High/Med)
- [ ] Добавить aria-label к ключевым секциям (cases, faq, partners, contacts).
- [ ] Пройти по ссылкам с неясным текстом (стрелки, “→”) и добавить aria-label где нужно.
- [ ] Проверить alt у изображений:
  - [ ] Для декора (фон, лого в футере) использовать alt="" + aria-hidden.
  - [ ] Для информативных изображений — описательные alt.

### Производительность (High/Med)
- [ ] Оптимизировать hero-видео на главной:
  - [ ] Загружать только на десктопе.
  - [ ] На мобилке использовать poster + лёгкий fallback.
- [ ] Заменить прямые <img> на Astro <Image /> для ключевых страниц (hero, кейсы, блог, услуги).
- [ ] Добавить width/height/sizes к основным изображениям для снижения CLS.
- [ ] Проверить подключение yet-another-react-lightbox:
  - [ ] Убедиться, что грузится только на страницах с галереями (client:visible/client:idle).
- [ ] Прогнать проект через Lighthouse (core metrics LCP/CLS/INP) и исправить критичные пункты.

### Архитектура и контент (High)
- [ ] Создать базовые layout-компоненты:
  - [ ] `PageLayout.astro` (hero + main + seo).
  - [ ] `CaseLayout.astro` / `BlogLayout.astro` для единообразия.
- [ ] Вынести повторяющиеся секции в компоненты:
  - [ ] `Section.astro` (обертка с aria-label и padding).
  - [ ] Привести FAQ.astro к единой схеме (props: title, items) по всем страницам.

### Конфигурация, безопасность, CI (Med)
- [ ] Уточнить CSP в astro.config.mjs под реальный трафик (на основе логов / devtools).
- [ ] Перенести site URL, телефон, e-mail в .env и экспортировать через astro.config.mjs.
- [ ] Настроить GitHub Actions:
  - [ ] install + astro check + build на push/PULL_REQUEST.
  - [ ] Добавить stage для typecheck.
