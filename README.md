# TT Events — Astro

Astro-based site for TT Events (event production, MICE, teambuilding, festivals, media).
SEO-secure migration from legacy platform → Astro with hub architecture and future-ready structure.

## Tech stack

- Astro 5
- TypeScript
- Tailwind CSS (via Vite)
- Astro Content Collections (blog, cases)

## Quick start

- Install deps:
  - npm install
- Dev:
  - npm run dev
- Build:
  - npm run build
- Preview:
  - npm run preview
- Lint / check:
  - npm run check
  - npm run typecheck

## Structure

High level:

- site.md:
  - Canonical site architecture + migration plan.
- TODO.md:
  - Task tracker: what is done, what to implement next.
- src/
  - components/
    - Layout.astro, Header.astro, Footer.astro
    - sections (Hero, FAQ, CTA, etc.)
  - pages/
    - index.astro
    - All current live URLs (1:1 for SEO)
    - services/
    - cases/
    - blog/
    - media/
    - for-business
    - process
    - faq
    - tenders

## Architecture

- Goal:
  - Preserve existing SEO URLs.
  - Add new hub structure:
    - /services/corporate-events
    - /services/mice-business
    - /services/team-building
    - /services/festivals
  - B2B/trust:
    - /cases
    - /media
    - /for-business
    - /process
    - /faq
    - /tenders

Migration approach:
- Phase 1:
  - 1:1 replication of existing URLs in Astro.
- Phase 2:
  - Create hubs and internal links.
- Phase 3:
  - Controlled 301 redirects from legacy URLs to hubs (batch by batch).
- Phase 4:
  - Performance, Lighthouse, accessibility, content polish.

See site.md for full architecture and redirect map.

## SEO / migration

- Sitemap: @astrojs/sitemap configured.
- Canonical / meta:
  - Managed via Layout with canonicalURL per page.
- Redirects:
  - Configured in astro.config.mjs; incremental, aligned with site.md.

Do not change URLs in bulk. Update only via redirects + Search Console monitoring.

## Notes

- This is the canonical repository for the TT Events website.
- All structural decisions should be aligned with site.md and TODO.md.