import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 8080,
    proxy: {
      '/api': {
        // 使用 127.0.0.1 强制走 IPv4，避免 localhost 解析为 ::1 导致 ECONNREFUSED
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        rewrite: (path) => path
      }
    }
  }
})

