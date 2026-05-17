import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  site: "https://ttevents.ru",
  integrations: [sitemap({ site: "https://ttevents.ru" })],
  build: {
    assets: "static",
  },
  vite: {
    plugins: [tailwindcss()],
    optimizeDeps: {
      exclude: ["astro/client"],
    },
  },
});
