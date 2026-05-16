# TT Events Scraper Architecture (Astro-Ready)

## Overview

This document describes the complete architecture for scraping ttevents.ru and preparing it for Astro migration.

---

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│                   TT Events Scraper                  │
├─────────────────────────────────────────────────────┤
│  scrape.py (Main Scraper)                           │
│  ├── HTTP Request Handler                           │
│  ├── HTML Parser (LinkParser)                       │
│  ├── URL Normalizer                                  │
│  ├── Rate Limiter                                    │
│  ├── Retry Mechanism                                │
│  └── Metadata Collector                             │
├─────────────────────────────────────────────────────┤
│  convert-to-astro.py (Converter)                    │
│  ├── HTML Analyzer                                  │
│  ├── Astro Template Generator                       │
│  └── SEO Metadata Injector                          │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                   Output Files                       │
├─────────────────────────────────────────────────────┤
│  • *.html (Scraped pages)                           │
│  • sitemap.xml (SEO sitemap)                       │
│  • seo-metadata.json (Page metadata)               │
│  • *.astro (Converted Astro pages)                 │
│  • public/ (Static assets)                         │
└─────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### 1. scrape.py - Main Scraper

**Features:**
- Parallel resource downloading (up to 5 workers)
- Retry logic with exponential backoff (3 attempts)
- Rate limiting (1 second between requests)
- Gzip/deflate support
- SSL certificate validation
- Progress tracking

**Configuration:**
```python
BASE_URL = "https://ttevents.ru"
MAX_DEPTH = 3      # How deep to crawl
DELAY = 1          # Seconds between requests
MAX_WORKERS = 5    # Parallel downloads
MAX_RETRIES = 3    # Retry attempts
REQUEST_TIMEOUT = 30  # Timeout in seconds
```

**Output:**
- HTML pages with relative URLs
- Static assets (CSS, JS, images)
- `sitemap.xml` for SEO
- `seo-metadata.json` with page data

---

### 2. LinkParser - HTML Parser

**Extracts:**
- All links (for crawling)
- Images (for downloading)
- Stylesheets (for styling)
- Scripts (for functionality)
- Meta tags (description, keywords, OG tags)
- Heading tags (h1-h6)
- Title element

---

### 3. convert-to-astro.py - HTML to Astro Converter

**Process:**
1. Reads scraped HTML files
2. Extracts SEO metadata
3. Generates Astro page templates
4. Injects frontmatter with SEO data
5. Wraps content in Astro layout

**Example Output:**
```astro
---
import {definePageMeta} from 'astro:content';

const seo = {
  title: 'TT Events Home',
  description: 'Event platform',
  keywords: 'events, tickets',
  ogTitle: 'TT Events Home',
  ogDescription: 'Event platform',
  ogImage: 'https://ttevents.ru/og-image.png',
};

export const pageMeta = definePageMeta(() => ({
  seo,
}));
---

<html lang="ru">
  <head>
    <title>{seo.title}</title>
    <meta name="description" content={seo.description}>
    ...
  </head>
  <body>
    <div class="astro-wrapper">
      <!-- Original HTML content -->
    </div>
  </body>
</html>
```

---

## Data Flow

```
1. User runs: python scrape.py
   ↓
2. Scraper crawls ttevents.ru
   ↓
3. Pages saved as HTML + assets
   ↓
4. Metadata collected (SEO, OG tags, headings)
   ↓
5. Files created:
   - sitemap.xml
   - seo-metadata.json
   ↓
6. User runs: python tools/convert-to-astro.py
   ↓
7. HTML pages converted to .astro
   ↓
8. Ready for Astro development
```

---

## File Structure After Complete

```
ttevents-ru/
├── README.md                    # Main documentation
├── scrape.py                    # Main scraper
├── tools/
│   └── convert-to-astro.py      # HTML to Astro converter
├── ttevents/
│   ├── scrape.py                # Scraper module
│   ├── sitemap.xml              # Generated sitemap
│   ├── seo-metadata.json        # Page metadata
│   ├── index.html               # Home page
│   ├── page1.html               # Other pages
│   └── assets/
│       ├── css/
│       ├── js/
│       └── images/
└── src/                         # Created by converter
    ├── pages/
│       ├── home.astro           # Converted pages
│       └── page1.astro
    └── layouts/
        └── Layout.astro         # Astro layout
```

---

## Usage Instructions

### Step 1: Scrape the Website

```bash
cd C:\ai\ttevents-ru\ttevents
python scrape.py
```

**Expected output:**
```
================================================================================
TT Events Website Scraper (Optimized for Astro)
================================================================================
Base URL: https://ttevents.ru
Output directory: C:\ai\ttevents-ru\ttevents
Max depth: 3
Max workers: 5
Max retries: 3
Request timeout: 30s
================================================================================
...

✓ Pages processed: 15
✗ Pages failed: 0
✓ Files downloaded: 127
⊘ Files skipped: 2
Total URLs visited: 23
Time elapsed: 45.2 seconds

📝 Sitemap saved: C:\ai\ttevents-ru\ttevents\sitemap.xml
📝 SEO metadata saved: C:\ai\ttevents-ru\ttevents\seo-metadata.json
================================================================================
SCRAPING COMPLETE
================================================================================
```

---

### Step 2: Convert to Astro

```bash
cd C:\ai\ttevents-ru
cd ..
python tools\convert-to-astro.py
```

**Expected output:**
```
================================================================================
HTML to Astro Converter
================================================================================
Input directory: C:\ai\ttevents-ru\ttevents
Output directory: C:\ai\ttevents-ru\src\pages
================================================================================

Found 15 HTML files
✓ Created: C:\ai\ttevents-ru\src\pages\home.astro
✓ Created: C:\ai\ttevents-ru\src\pages\events.astro
...

================================================================================
Conversion complete: 15 pages created
================================================================================

To start the Astro dev server:
  cd C:\ai\ttevents-ru
  npm run dev
```

---

### Step 3: Start Astro Development

```bash
cd C:\ai\ttevents-ru
npm install
cp -r ttevents/public .  # Copy static assets
npm run dev
```

---

## Key Features

### ✅ Reliability
- Automatic retries (3 attempts)
- Exponential backoff
- Error handling with detailed logging

### ✅ Performance
- Parallel resource downloads (5 workers)
- Gzip/deflate support
- Connection keep-alive

### ✅ SEO Ready
- Sitemap generation
- Meta tags extraction
- OG tags collection
- Heading hierarchy tracking

### ✅ Astro Compatible
- Automatic Astro conversion
- Frontmatter injection
- SEO metadata preservation

---

## Troubleshooting

### Issue: SSL Certificate Error
```bash
# Solution: Temporarily disable verification
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
```

### Issue: Too Many Requests
```bash
# Solution: Increase delay
DELAY = 2  # Increase from 1 to 2 seconds
```

### Issue: Memory Limit
```bash
# Solution: Decrease parallel workers
MAX_WORKERS = 2  # Reduce from 5 to 2
```

---

## Future Enhancements

1. **Incremental crawling** - Only update changed pages
2. **Image optimization** - Convert to WebP automatically
3. **Lazy loading** - Add Astro image component support
4. **Dynamic routes** - Use `[slug].astro` pattern
5. **Content collections** - Use Astro content collections API

---

## License

MIT License
