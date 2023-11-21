import VueI18nPlugin from "@intlify/unplugin-vue-i18n/vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "path";
import { fileURLToPath, URL } from "url";
import { defineConfig, splitVendorChunkPlugin } from "vite";

// https://vitejs.dev/config/
export default defineConfig({
  define: {
    __VUE_I18N_FULL_INSTALL__: false,
    __VUE_I18N_LEGACY_API__: false,
    __INTLIFY_PROD_DEVTOOLS__: false,
  },
  plugins: [
    splitVendorChunkPlugin(),
    vue(),
    VueI18nPlugin({
      runtimeOnly: true,
      compositionOnly: true,
      include: resolve(__dirname, "obr_ui/locales/**"),
    }),
  ],
  build: {
    target: "es2020",
    rollupOptions: {
      input: {
        main: resolve(__dirname, "obr_ui/main.ts"),
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
    sourcemap: true,
    chunkSizeWarningLimit: 1000,
    assetsInlineLimit: 8092,
  },
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./obr_ui", import.meta.url)),
      // "vue": "vue/dist/vue.esm-bundler.js",
      "vue-i18n": "vue-i18n/dist/vue-i18n.cjs.js",
      // "hls.js": "hls.js/dist/hls.light.js",
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
      "^((?!src/|obr_ui/|static/|node_modules/|@).)*$": {
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
