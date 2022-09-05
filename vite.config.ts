import { fileURLToPath, URL } from "url";
import { resolve } from "path";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import vueI18n from "@intlify/vite-plugin-vue-i18n";

// https://vitejs.dev/config/
export default defineConfig({
  define: {
    __VUE_I18N_FULL_INSTALL__: false,
    __VUE_I18N_LEGACY_API__: false,
    __INTLIFY_PROD_DEVTOOLS__: false,
  },
  plugins: [
    vue(),
    vueI18n({
      include: resolve(__dirname, "src/locales/**"),
    }),
  ],
  build: {
    target: "es2020",
    rollupOptions: {
      input: {
        main: resolve(__dirname, "src/main.ts"),
      },
      output: {
        entryFileNames: "[name].js",
        chunkFileNames: "[name].js",
        assetFileNames: "[name].[ext]",
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
    outDir: resolve(__dirname, "build"),
    chunkSizeWarningLimit: 1500,
    assetsInlineLimit: 8092,
  },
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
      // "vue": "vue/dist/vue.esm-bundler.js",
      "vue-i18n": "vue-i18n/dist/vue-i18n.runtime.esm-bundler.js",
    },
  },
  server: {
    host: "0.0.0.0",
    port: 3000,
    strictPort: true,
    watch: {
      ignored: ["**/data/**"],
    },
    proxy: {
      "^((?!src/|static/|node_modules/|@).)*$": {
        target: "http://local.obr-next:8080",
        // origin: 'http://127.0.0.1:8080/',
        configure: (proxy) => {
          proxy.on("proxyReq", function (proxyReq) {
            proxyReq.setHeader("X-VITE-PROXIED", "on");
          });
        },
      },
    },
  },
});
