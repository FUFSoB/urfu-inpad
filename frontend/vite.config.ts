import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": "/src",
    },
  },
  css: {
    devSourcemap: true,
    preprocessorOptions: {
      scss: {
        api: "modern-compiler",
      },
    },
  },
  server: {
    port: 7123,
    open: false,
    host: "localhost",
  },
  build: {
    outDir: "build",
    assetsDir: "assets",
    cssCodeSplit: false,
  },
});
