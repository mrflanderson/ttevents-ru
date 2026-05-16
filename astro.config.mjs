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
