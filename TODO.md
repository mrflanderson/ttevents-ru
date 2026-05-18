# TT Events — Project TODO

Version: 2.0
Based on: site.md + current Astro migration status.

## Legend

- [ ] Not done
- [x] Done
- [ ] Blocked (needs decision)

---

## 1. SEO-secure migration: MegaGroup → Astro (DONE) [Phase 1–3] ✅ DONE

Core goal: preserve all current indexed URLs while introducing hub architecture.

- [x] 1:1 SEO skeleton:
  - [x] All existing live URLs preserved as Astro pages.
  - [x] BaseLayout + Layout with:
    - [x] meta title, description, keywords
    - [x] canonical URL
    - [x] OG/Twitter meta
    - [x] JSON-LD (Organization, WebSite, BreadcrumbList)
- [x] Hubs created (Phase 2):
  - [x] /services
  - [x] /services/corporate-events
  - [x] /services/mice-business
  - [x] /services/team-building
  - [x] /services/festivals
  - [x] Child pages under each hub (corporate, MICE, team-building, festivals).
- [x] B2B & trust pages:
  - [x] /cases hub
  - [x] /media, /media/video-production, /media/online-events, /media/portfolio
  - [x] /for-business
  - [x] /process
  - [x] /faq
- [x] Redirects (Phase 3–4, incremental):
  - [x] /korporativy-moskva → /services/corporate-events
  - [x] /novogodniy-korporativ → /services/corporate-events/novogodnie
  - [x] /art-korporativ → /services/corporate-events/art
  - [x] /immersivnyj-korporativ → /services/corporate-events/immersivnye
  - [x] /yubilej-kompanii → /services/corporate-events/yubilei
  - [x] /korporativ-na-prirode → /services/corporate-events/na-prirode
  - [x] /event-agentstvo-moskva → /for-business
  - [x] /organizaciya-meropriyatij-v-moskve → /services/corporate-events
  - [x] /delovye-meropriyatiya → /services/mice-business
  - [x] /mice-delovoj-turizm → /services/mice-business
  - [x] /timbilding-moskva → /services/team-building
  - [x] /timbilding-na-prirode → /services/team-building
  - [x] /aktivnye-timbildingi → /services/team-building/aktivnye
  - [x] /kreativnye-timbildingi → /services/team-building/kreativnye
  - [x] /kvesty-i-igry → /services/team-building/kvesty-i-igry
  - [x] /intellektualnye-igry → /services/team-building/kvesty-i-igry
  - [x] /festivali → /services/festivals
  - [x] /festivaly-i-gorodskie-meropriyatiya → /services/festivals
  - [x] /gosudarstvennye-prazdniki → /services/festivals/public-holidays
  - [x] /sportivnye-meropriyatiya → /services/festivals/sports
  - [x] /turisticheskie-i-ekskursionnye-meropriyatiya → /services/festivals/city-events
  - [x] /videoproduction → /media/video-production
  - [x] /video-portfolio → /media/portfolio
  - [x] /mediaproekty → /media
  - [x] /onlajn-meropriyatiya → /media/online-events
  - [x] /tendery → /tenders
- [x] Internal linking:
  - [x] Legacy pages → new hubs (corporate, MICE, team-building, festivals).
  - [x] Hubs → /cases, /for-business, /media.

---

## 2. Build, structure, hygiene ✅ DONE

- [x] astro build runs successfully (no import errors).
- [x] Blog and case collections use Content Collections and dynamic routes.
- [x] Sitemap + robots configured: 
  - [x] @astrojs/sitemap
  - [x] robots.txt points to sitemap.xml
- [x] BaseLayout unified (canonical, OG, JSON-LD).

---

## 3. Content & UX improvements (HIGH) 🔥 Next

Tasks that improve how site sells and converts, without touching SEO aggressively.

### 3.1 Homepage (index.astro) as premium landing
- [ ] Rewrite hero:
  - [ ] Strong headline (corporate events + production + media).
  - [ ] 2 CTAs: “Обсудить проект”, “Смотреть кейсы”.
- [ ] Add 4 directions block:
  - [ ] Corporate events
  - [ ] MICE & business
  - [ ] Team building
  - [ ] Festivals & city events
- [ ] Add featured cases block (3–4 flagship projects).
- [ ] Add clients/partners block.
- [ ] Add “Why TT Events” metrics block.
- [ ] Add Event + Media block (positioning).
- [ ] Keep SEO paragraph minimal, at the bottom.

### 3.2 Service hubs (/services/*) as conversion pages
- [ ] Improve /services/corporate-events:
  - [ ] Hero + value proposition
  - [ ] Tasks we solve
  - [ ] Child links
  - [ ] Related cases
  - [ ] FAQ snippet + CTA
- [ ] Improve /services/mice-business
- [ ] Improve /services/team-building
- [ ] Improve /services/festivals
- [ ] For each hub: 
  - [ ] Consistent structure
  - [ ] Internal links to child pages
  - [ ] Links to /cases and /for-business

### 3.3 Cases (/case, /cases) as primary trust engine
- [ ] Polish /case index:
  - [ ] Categories/filters (corporate, MICE, team-building, festivals, media).
- [ ] Ensure each case:
  - [ ] Has clear structure: Task → Solution → Implementation → Results.
  - [ ] Links back to relevant hub(s).

### 3.4 B2B and trust pages
- [ ] /for-business:
  - [ ] Sections: HR, Marketing, PR, Procurement/Tenders.
  - [ ] Clear CTA “Request proposal”.
- [ ] /process:
  - [ ] Step-by-step: Brief → Concept → Budget → Production → Implementation → Content & reporting.
- [ ] /faq:
  - [ ] Ensure 8–12 focused Q&A.
  - [ ] Use consistent answers across pages.

---

## 4. SEO and technical SEO (HIGH/MEDIUM) 🔥 Next

### 4.1 Technical SEO
- [ ] Implement a clean SeoMeta pattern:
  - [ ] Reusable component or helper to standardize meta tags.
- [ ] Enforce canonical using site URL + pathname consistently.
- [ ] Add page-level JSON-LD where applicable:
  - [ ] FAQPage for /faq and relevant hubs.
  - [ ] Article schema for blog posts.
  - [ ] Case/Event-like schema for /case pages.
- [ ] Configure noindex for drafts/internal pages (if any).

### 4.2 Content SEO
- [ ] Audit H1/H2 structure on key pages (/, hubs, cases, blog).
- [ ] Remove SEO-text walls: convert to structured blocks (features, cases, FAQ).
- [ ] Improve internal linking between:
  - [ ] Hubs ↔ children
  - [ ] Services ↔ cases ↔ blog

---

## 5. Performance / Lighthouse / Core Web Vitals (HIGH) 🔥 Next

Focus on LCP, CLS, TBT, INP. Tie to PageSpeed recommendations.

- [ ] Optimize hero video (index.astro):
  - [ ] Use preload="metadata" or "none"
  - [ ] Show only poster/background on mobile
- [ ] Lazy-load Rutube iframes:
  - [ ] Show poster + Play button
  - [ ] Load iframe on interaction or when visible
- [ ] Improve images:
  - [ ] Use Astro <Image /> or srcset for key images (hero, cases, services).
  - [ ] Add width/height/sizes to reduce CLS.
  - [ ] Use modern formats where possible.
- [ ] Ensure yet-another-react-lightbox:
  - [ ] Loaded only where used (client:visible / client:idle).
- [ ] Run Lighthouse (desktop + mobile) and fix:
  - [ ] Largest LCP delays
  - [ ] Long main-thread tasks
  - [ ] Layout shift culprits

---

## 6. Accessibility / UX quality (MEDIUM) 🔥 Next

- [ ] Normalize headings hierarchy:
  - [ ] One <h1> per page.
  - [ ] Sequential h2/h3/h4 (no decorative headings).
- [ ] Improve interactive elements:
  - [ ] Use <button> for actions, <a> for navigation.
- [ ] Add/fix ARIA labels:
  - [ ] Iframes (Rutube, analytics)
  - [ ] Menus and accordions
- [ ] Check contrast:
  - [ ] Primary buttons, links, secondary text.

---

## 7. Infra, CI, security (MEDIUM/LOW) 🔥 Next

- [ ] Tune CSP in astro.config.mjs:
  - [ ] Based on actual usage.
  - [ ] Move from reportOnly to enforced where safe.
- [ ] Store secrets/variables:
  - [ ] site, phone, emails in .env / Astro integrations.
- [ ] GitHub Actions:
  - [ ] install + astro check + build on PRs.
  - [ ] Typecheck stage.

---

## 8. Migration & release checklist (IMPORTANT) 🔥 Next

Tasks before deploying the new Astro build to production.

- [ ] Final SEO checks:
  - [ ] Ensure all critical URLs are accessible (no 404s).
  - [ ] Validate redirects (spot-check).
- [ ] Search Console:
  - [ ] Submit new sitemap.
  - [ ] Review coverage / errors after launch.
- [ ] Analytics:
  - [ ] Ensure Yandex Metrica / GTM scripts active and correct.
- [ ] Visual QA:
  - [ ] Compare key pages (/, /case, /services/*) with current site.
- [ ] Performance:
  - [ ] Run PageSpeed Insights (desktop + mobile) post-launch.
