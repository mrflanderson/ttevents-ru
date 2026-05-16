import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://ttevents.ru',
  build: {
    assets: 'static',
  },
  vite: {
    optimizeDeps: {
      exclude: ['astro/client'],
    },
  },
});
