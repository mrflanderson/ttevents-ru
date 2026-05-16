# TT Events Website Scraper (Astro-Ready)

## 📋 Описание

Этот проект содержит оптимизированный скрепер для сайта ttevents.ru, подготовленный для миграции на Astro. Скрипт собирает страницы, ресурсы и метаданные в формате, совместимом с Astro.

## 🚀 Быстрый старт

### 1. Запуск скрепера

```bash
cd C:\ai\ttevents-ru\ttevents
python scrape.py
```

### 2. Что создается после скрейпа:

```
ttevents/
├── scrape.py          # Основной скрепер
├── sitemap.xml        # Sitemap для SEO
├── seo-metadata.json  # Метаданные страниц для Astro
├── index.html         # Главная страница
├── ...                # Остальные страницы
└── (ресурсы: CSS, JS, изображения)
```

---

## 🔄 Миграция на Astro

### Шаг 1: Установка Astro

```bash
cd C:\ai\ttevents-ru
npx astro init --template minimal
```

### Шаг 2. Структура проекта Astro

```plaintext
ttevents-ru/
├── public/
│   └── (копируем собранные ресурсы здесь)
├── src/
│   ├── layouts/
│   │   └── Layout.astro       # Общий layout
│   ├── pages/
│   │   ├── index.astro        # Главная
│   │   └── [slug].astro       # Динамические страницы
│   └── components/
│       └── Shared.astro       # Общие компоненты
├── astro.config.mjs
├── src/env.d.ts
└── tsconfig.json
```

### Шаг 3. Импорт страниц из скрейпа

Создайте скрипт для импорта HTML из скрейпа в Astro:

```javascript
// import-html.mjs
import fs from 'fs/promises';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const scrapedDir = join(__dirname, 'ttevents');

// Читаем все HTML файлы
const htmlFiles = await fs.readdir(scrapedDir);
const pages = htmlFiles.filter(f => f.endsWith('.html'));

// Генерируем Astro страницы
for (const page of pages) {
  const content = await fs.readFile(join(scrapedDir, page), 'utf-8');
  const slug = page.replace('.html', '');
  
  const astroContent = `
---
// ${slug}.astro
---
<html lang="ru">
  <head>
    <title>${page}</title>
  </head>
  <body>
    ${content}
  </body>
</html>
---

<a href="/">Home</a>
<slot />
  </body>
</html>
`;

  await fs.writeFile(
    join(__dirname, 'src/pages', `${slug}.astro`),
    astroContent
  );
}

console.log(`Imported ${pages.length} pages to Astro`);
```

### Шаг 4. Настройка astro.config.mjs

```javascript
import { defineConfig } from 'astro/config';

export default defineConfig({
  build: {
    assets: 'static',
  },
  vite: {
    optimizeDeps: {
      exclude: ['astro/client'],
    },
  },
});
```

### Шаг 5. Создание Layout

```astro
---
// src/layouts/Layout.astro
---
<!DOCTYPE html>
<html lang="ru">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title><%= title %></title>
    <link rel="stylesheet" href="/styles/global.css">
  </head>
  <body>
    <header>
      <nav>
        <a href="/">Главная</a>
      </nav>
    </header>
    <main>
      <slot />
    </main>
  </body>
</html>
---

<a href="/">Home</a>
<slot />
  </body>
</html>
```

---

## 📊 Использование Metadata

### SEO Metadata (seo-metadata.json)

Файл содержит метаданные всех scraped страниц:

```json
{
  "https://ttevents.ru/": {
    "path": "index.html",
    "title": "TT Events",
    "description": "Event platform",
    "keywords": "events, tickets",
    "og_tags": {},
    "h1": [],
    "h2": [],
    "h3": [],
    "links": 15,
    "images": 5
  }
}
```

Можно использовать для генерации SEO в Astro:

```astro
---
// src/pages/index.astro
import seoData from '../../seo-metadata.json';
const homepage = seoData['https://ttevents.ru/'];
---

<html lang="ru">
  <head>
    <title>{homepage.title}</title>
    <meta name="description" content={homepage.description}>
    <meta name="keywords" content={homepage.keywords}>
    
    {homepage.og_tags.title && (
      <meta property="og:title" content={homepage.og_tags.title}>
    )}
    {homepage.og_tags.description && (
      <meta property="og:description" content={homepage.og_tags.description}>
    )}
    {homepage.og_tags.image && (
      <meta property="og:image" content={homepage.og_tags.image}>
    )}
  </head>
  <body>
    <!-- Page content -->
  </body>
</html>
---

<a href="/">Home</a>
<slot />
  </body>
</html>
```

---

## ⚙️ Настройки скрейпера

Все параметры находятся в начале `scrape.py`:

| Параметр | Значение | Описание |
|----------|----------|----------|
| `BASE_URL` | "https://ttevents.ru" | Целевой сайт |
| `MAX_DEPTH` | 3 | Максимальная глубина |
| `DELAY` | 1 | Задержка между запросами |
| `MAX_WORKERS` | 5 | Потоки для загрузки |
| `MAX_RETRIES` | 3 | Повторные попытки |
| `RETRY_DELAY` | 2 | Задержка повторных попыток |
| `REQUEST_TIMEOUT` | 30 | Таймаут запроса |

---

## 🧪 Тестирование

```bash
# Запуск скрейпера
python ttevents/scrape.py

# Проверка синтаксиса
python -m py_compile ttevents/scrape.py

# Установка Astro
cd ttevents-ru
npx astro check
```

---

## 📝 Changelog

### Версия 2.0 (Astro-Ready)
- ✅ Добавлен сбор SEO metadata
- ✅ Генерация sitemap.xml
- ✅ Поддержка meta tags (og:, description, keywords)
- ✅ Извлечение заголовков (h1-h3)
- ✅ Подготовка структуры для Astro
- ✅ Параллельная загрузка ресурсов
- ✅ Повторные попытки при ошибках
- ✅ Rate limiting
- ✅ Поддержка gzip/deflate
- ✅ Безопасное SSL-соединение

---

## 📚 Дополнительные ресурсы

- [Astro Documentation](https://docs.astro.build/)
- [Astro Image Component](https://docs.astro.build/en/guides/images/)
- [Astro Content Collections](https://docs.astro.build/en/guides/content-collections/)

---

## 📄 License

MIT License
