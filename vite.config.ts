import { fileURLToPath, URL } from 'url'
import { resolve } from 'path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  build: {
    target: "es2020",
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'src/main.ts'),
      },
      output: {
        entryFileNames: '[name].js',
        chunkFileNames: '[name].js',
        assetFileNames: '[name].[ext]',
        // manualChunks: {
        //   'player': [
        //     'shaka-player',
        //   ],
        //   'vue': [
        //     'vue',
        //     'vue-router',
        //     'vue-i18n',
        //     'vuex',
        //   ],
        // },
      },
    },
    outDir: resolve(__dirname, 'build'),
    chunkSizeWarningLimit: 1000,
    assetsInlineLimit: 8092,
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    host: '0.0.0.0',
    port: 3000,
    strictPort: true,
    watch: {
      ignored: [
        '**/data/**',
      ],
    },
    proxy: {
      '^((?!src\/|static\/|node_modules\/|@).)*$': {
        target: 'http://local.obr-next:8080',
        // origin: 'http://127.0.0.1:8080/',
        configure: (proxy, options) => {
          proxy.on('proxyReq', function (proxyReq, req, res, options) {
            proxyReq.setHeader('X-VITE-PROXIED', 'on');
          });
        },
      },
    },
  },

})