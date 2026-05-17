import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  site: "https://ttevents.ru",
  integrations: [sitemap()],
  content: {
    collections: {
      blog: {
        type: "content",
        schema: {
          title: { type: "string" },
          description: { type: "string" },
          date: { type: "string", transform: "date" },
          published: { type: "boolean", default: true },
          coverImage: { type: "string" },
          tags: { type: "array", items: { type: "string" } },
        },
      },
      cases: {
        type: "content",
        schema: {
          title: { type: "string" },
          description: { type: "string" },
          date: { type: "string", transform: "date", optional: true },
          published: { type: "boolean", default: true },
          coverImage: { type: "string" },
          tags: { type: "array", items: { type: "string" }, default: [] },
          client: { type: "string", optional: true },
          budget: { type: "string", optional: true },
        },
      },
      services: {
        type: "content",
        schema: {
          title: { type: "string" },
          description: { type: "string" },
          icon: {
            type: "enum",
            values: [
              "briefcase",
              "team",
              "tree",
              "building",
              "rocket",
              "camera",
            ],
          },
          relatedLinks: {
            type: "array",
            items: { type: "string" },
            optional: true,
          },
        },
      },
    },
  },
  build: {
    assets: "static",
    clientLocals: "lazy",
  },
  vite: {
    plugins: [tailwindcss()],
    optimizeDeps: {
      exclude: ["astro/client"],
    },
  },
  security: {
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'", "fonts.googleapis.com"],
        styleSrc: ["'self'", "'unsafe-inline'", "fonts.googleapis.com"],
        imgSrc: [
          "'self'",
          "data:",
          "https://*.rutube.ru",
          "https://img.youtube.com",
        ],
        mediaSrc: ["'self'", "https://*.rutube.ru"],
        fontSrc: ["'self'", "fonts.gstatic.com"],
        connectSrc: ["'self'", "api.telegram.org"],
      },
      reportOnly: true,
    },
  },
  redirects: {
    // General legacy
    "/old": { status: 301, destination: "/" },

    // Blog legacy paths → /blog/[slug] or /blog
    "/blog-3-trenda": {
      status: 301,
      destination: "/blog/3-trendy-organizacii-korporativov-2026",
    },
    "/blog-korporativ-na-9-maya-2026-v-moskve": {
      status: 301,
      destination: "/blog",
    },
    "/blog-organizatsiya-korporativov-moskva-2026": {
      status: 301,
      destination: "/blog/3-trendy-organizacii-korporativov-2026",
    },
    "/blog-post-it-corporativ-idei": {
      status: 301,
      destination: "/blog",
    },
    "/blog-post-it-corporativ": {
      status: 301,
      destination: "/blog",
    },
    "/blog-post-kak-provesti-launch-event-10-formatov-prezentacii-novogo-produkta":
      {
        status: 301,
        destination: "/blog",
      },
    "/blog-post-kak-vybrat-event-agentstvo-v-moskve": {
      status: 301,
      destination: "/blog",
    },
    "/blog-post-korporativ-na-9-maya-dlya-kompanii-12-idej-meropriyatij-ko-dnyu-pobedy-scenarii-i-formaty-2026":
      {
        status: 301,
        destination: "/blog",
      },
    "/blog-post-pochemu-russkie-narodnye-motivy-populyarny": {
      status: 301,
      destination: "/blog",
    },

    // Case legacy paths → /case/[slug] or /case
    "/case-9may": {
      status: 301,
      destination: "/case/9may-corporate",
    },
    "/case-art-novy-god-otel-svezhy-veter-2026": {
      status: 301,
      destination: "/case/otel-svezhy-veter-2026",
    },
    "/case-artpop": {
      status: 301,
      destination: "/case/artpop",
    },
    "/case-eho-pobedy-ope-air-2025": {
      status: 301,
      destination: "/case",
    },
    "/case-ek-park": {
      status: 301,
      destination: "/case",
    },
    "/case-imersivny-thatr": {
      status: 301,
      destination: "/case",
    },
    "/case-korolevsky-novy-god-24": {
      status: 301,
      destination: "/case/korolevsky-ny-24",
    },
    "/case-lauch-event-umg": {
      status: 301,
      destination: "/case/lauch-event-umg",
    },
    "/case-maslenitsa-izmaylovo25case": {
      status: 301,
      destination: "/case",
    },
    "/case-nad-moskvoy-zarya": {
      status: 301,
      destination: "/case/zarya-festival",
    },
    "/case-open-air-slava-skripka-bober-2025": {
      status: 301,
      destination: "/case",
    },
    "/case-post-den_nko_2024": {
      status: 301,
      destination: "/case",
    },
    "/case-post-mediaproekt-i-fotovystavka-supersila": {
      status: 301,
      destination: "/case",
    },
    "/case-vremena-goda": {
      status: 301,
      destination: "/case",
    },
    "/case-vremnadezhdfest2025": {
      status: 301,
      destination: "/case",
    },
  },
  devToolbar: {
    enabled: true,
  },
});
