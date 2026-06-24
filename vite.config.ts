import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  // Relative base so the build works under a GitHub Pages sub-path
  // (https://<user>.github.io/<repo>/) as well as at a domain root.
  base: './',
  plugins: [react(), tailwindcss()],
  build: {
    rollupOptions: {
      // The Vite/ComplyScope entry lives at index.vite.html so the repo root
      // index.html can hold the built portfolio (served directly in branch mode).
      input: 'index.vite.html',
    },
  },
  server: {
    host: true,
    port: 5173,
  },
})
