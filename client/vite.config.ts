import react from '@vitejs/plugin-react';
import path from 'node:path';
import { defineConfig, loadEnv } from 'vite';

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), 'VITE_');

  return {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },
    plugins: [react()],

    server: {
      proxy: {
        [env.VITE_API_URL || '/api']:
          `http://${env.VITE_BACKEND_HOST || 'localhost'}:${env.VITE_BACKEND_PORT || '8000'}`,
      },
      host: '0.0.0.0',
      port: 5173,
    },
  };
});
