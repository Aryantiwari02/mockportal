import react from '@vitejs/plugin-react'
import { defineConfig, loadEnv } from 'vite'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')

  // Backend URL for the dev proxy — can be overridden via VITE_BACKEND_URL in .env
  const backendUrl = env.VITE_BACKEND_URL || 'http://127.0.0.1:8000'

  return {
    plugins: [react()],

    server: {
      proxy: {
        // Forward /api requests to the Django backend during development
        '/api': {
          target: backendUrl,
          changeOrigin: true,
          secure: false,
        },
        // Also proxy /media so uploaded document downloads work in dev
        '/media': {
          target: backendUrl,
          changeOrigin: true,
          secure: false,
        },
      },
    },
  }
})
