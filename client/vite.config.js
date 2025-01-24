import { resolve } from 'path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'


// https://vite.dev/config/
export default defineConfig({
  base: "./",
  build: {
    emptyOutDir: false,
    rollupOptions: {
      input: {
        main: resolve(__dirname, "index.html")
      },
      output: {
        assetFileNames: (assetInfo) => {
          let extType = assetInfo.name.split('.')[1];
          if (/png|jpe?g|svg|gif|tiff|bmp|ico/i.test(extType)) {
            extType = 'img';
          }
          if (/woff|woff2|ttf/i.test(extType)) {
            extType = 'fonts';
          }
          return `bundles/${extType}/[name][extname]`;
        },
        chunkFileNames: 'bundles/js/[name].js',
        entryFileNames: 'bundles/js/[name].js',
      },
    }
  },
  plugins: [vue()],
  css: {

  }
})
