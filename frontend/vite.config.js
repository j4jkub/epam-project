import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

// In dev, requests to /api/* are forwarded to your FastAPI server with the
// "/api" prefix removed (so /api/projects -> http://localhost:8000/projects).
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  return {
    plugins: [react()],
    server: {
      port: 5173,
      proxy: {
        '/api': {
          target: env.API_PROXY_TARGET || 'http://localhost:8000',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ''),
        },
      },
    },
  };
});
