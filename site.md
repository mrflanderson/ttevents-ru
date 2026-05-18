# TT Events — Site Architecture & Migration

Version: 3.0
Based on: live ttevents.ru, sitemap, and Astro implementation.
Purpose: single source of truth for URLs, structure, and migration.

---

## 1. Goals

- Preserve all current SEO URLs and weight.
- Introduce hub architecture for services, cases, and media.
- Turn the site into a premium event ecosystem, not just SEO pages.
- Provide a clear, incremental migration path.

Principles:
- No mass URL renaming at once.
- No mass title/H1/content changes at once.
- Each URL: one primary intent; clear hub → child relationships.
- Hubs and trust pages must be explicit.

---

## 2. Core rules

- Phase 1:
  - Keep all existing URLs exactly as they are (1:1 Astro pages).
- Phase 2:
  - Create hubs and internal links.
- Phase 3:
  - Apply controlled 301 redirects in batches, only after hubs are stable.
- Phase 4:
  - Improve content, performance, accessibility, and visual design.

Never change structure + titles + redirects simultaneously.

---

## 3. Current live URLs (to preserve)

These URLs are live and indexed. Keep them exactly (Phase 1).

Root / trust:
- /
- /o-nas
- /kontakty
- /tendery

Corporate:
- /korporativy-moskva
- /novogodniy-korporativ
- /letnij-korporativ
- /korporativ-na-prirode
- /art-korporativ
- /immersivnyj-korporativ
- /yubilej-kompanii

Business / MICE:
- /event-agentstvo-moskva
- /organizaciya-meropriyatij-v-moskve
- /delovye-meropriyatiya
- /konferencii-i-forumy
- /strategicheskie-sessii-i-vorkshopy
- /seminary-i-treningi
- /mice-delovoj-turizm
- /prezentacii-novyh-produktov-launch-events
- /master-klassy

Team building:
- /timbilding-moskva
- /timbilding-na-prirode
- /aktivnye-timbildingi
- /kreativnye-timbildingi
- /kvesty-i-igry
- /intellektualnye-igry

Festivals & city:
- /festivali
- /festivaly-i-gorodskie-meropriyatiya
- /gosudarstvennye-prazdniki
- /sportivnye-meropriyatiya
- /turisticheskie-i-ekskursionnye-meropriyatiya

Media / blog / cases:
- /videoproduction
- /video-portfolio
- /mediaproekty
- /onlajn-meropriyatiya
- /blog, /blog/*
- /case, /case/*

Astro requirement:
- Each of these must have a corresponding page in src/pages.
- Preserve URL, title, H1, main SEO paragraphs initially.

---

## 4. New hub architecture

Hubs are NEW pages; they do NOT immediately delete existing URLs.

Core hubs:
- /services
- /services/corporate-events
- /services/mice-business
- /services/team-building
- /services/festivals

Examples of child pages:
- /services/corporate-events/novogodnie
- /services/corporate-events/na-prirode
- /services/corporate-events/art
- /services/corporate-events/immersivnye
- /services/corporate-events/yubilei

- /services/mice-business/konferencii
- /services/mice-business/foruma
- /services/mice-business/launch-events
- /services/mice-business/seminars
- /services/mice-business/strategy-sessions

- /services/team-building/aktivnye
- /services/team-building/kreativnye
- /services/team-building/kvesty-i-igry

- /services/festivals/city-events
- /services/festivals/sports
- /services/festivals/public-holidays

Cases / media / B2B:
- /cases (portfolio hub; keep /case as main, align links)
- /media
- /media/video-production
- /media/online-events
- /media/portfolio
- /for-business
- /process
- /faq
- /tenders

These are ADDED in parallel; they gradually become primary.

---

## 5. Page roles (short)

- /:
  - Premium landing + brand statement. Not an SEO soup page.
  - Show scale, quality, cases, clients, Event + Media.
- /services:
  - Central hub for all service directions.
- /services/corporate-events:
  - Pillar for corporate events.
- /services/mice-business:
  - Pillar for MICE, conferences, launch events.
- /services/team-building:
  - Pillar for team building.
- /services/festivals:
  - Pillar for festivals, city events, public holidays, sports.
- /cases:
  - Core portfolio hub (case-first approach).
- /media, /media/*:
  - Position TT Events as Event + Media, not just logistics.
- /for-business:
  - B2B landing for HR, marketing, PR, procurement.
- /process:
  - Trust page: how we work.
- /faq:
  - Central FAQ hub + SEO snippets.
- /blog:
  - SEO knowledge base (articles), not company news.
- /tenders:
  - Tenders & government procurement.
- /contacts (or /kontakty initially):
  - Main contact page.

---

## 6. Migration phases

Phase 1: 1:1 SEO skeleton
- Replicate all live URLs as Astro pages.
- Same URL, same title/H1, same core SEO paragraphs.
- Use BaseLayout + Layout for clean meta, canonical, OG, JSON-LD.
- No redirects yet.

Phase 2: Hubs + internal linking
- Create all hubs and child pages.
- Add internal links from old pages → hubs.
- Add internal links from hubs → cases, for-business, media.

Phase 3: Controlled redirects
- Only after hubs are live and stable.
- Apply 301s in batches (see Redirect map).
- Monitor Search Console; adjust gradually.

Phase 4: Content + performance + UX
- Upgrade homepage, hubs, cases to premium design.
- Optimize Core Web Vitals, images, video, accessibility.

---

## 7. Redirect map (planned, incremental)

Examples (to be applied step-by-step, not all at once):

Corporate:
- /korporativy-moskva → /services/corporate-events
- /novogodniy-korporativ → /services/corporate-events/novogodnie
- /art-korporativ → /services/corporate-events/art
- /immersivnyj-korporativ → /services/corporate-events/immersivnye
- /yubilej-kompanii → /services/corporate-events/yubilei
- /korporativ-na-prirode → /services/corporate-events/na-prirode

Business / MICE:
- /event-agentstvo-moskva → /for-business
- /organizaciya-meropriyatij-v-moskve → /services/corporate-events
- /delovye-meropriyatiya → /services/mice-business
- /mice-delovoj-turizm → /services/mice-business

Team building:
- /timbilding-moskva → /services/team-building
- /timbilding-na-prirode → /services/team-building
- /aktivnye-timbildingi → /services/team-building/aktivnye
- /kreativnye-timbildingi → /services/team-building/kreativnye
- /kvesty-i-igry → /services/team-building/kvesty-i-igry
- /intellektualnye-igry → /services/team-building/kvesty-i-igry

Festivals & city:
- /festivali → /services/festivals
- /festivaly-i-gorodskie-meropriyatiya → /services/festivals
- /gosudarstvennye-prazdniki → /services/festivals/public-holidays
- /sportivnye-meropriyatiya → /services/festivals/sports
- /turisticheskie-i-ekskursionnye-meropriyatiya → /services/festivals/city-events

Media / blog:
- /videoproduction → /media/video-production
- /video-portfolio → /media/portfolio
- /mediaproekty → /media
- /onlajn-meropriyatiya → /media/online-events

Other:
- /tendery → /tenders

Only apply incrementally; never all at once.

---

## 8. Technical notes

- Astro:
  - Uses static output; site: "https://ttevents.ru".
- SEO:
  - Sitemap via @astrojs/sitemap.
  - Canonical: set per page (canonicalURL).
  - JSON-LD: Organization, WebSite, BreadcrumbList; FAQPage where applicable.
- Components:
  - BaseLayout.astro: global head, meta, canonical, OG, JSON-LD.
  - Layout.astro: visual shell + Header/Footer.

This document is canonical for the TT Events site architecture and migration.
