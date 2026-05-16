import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://ttevents.ru',
  integrations: [sitemap()],
  build: {
    assets: 'static',
  },
  vite: {
    optimizeDeps: {
      exclude: ['astro/client'],
    },
  },
});
