import react from "@vitejs/plugin-react";
import { type UserConfig, defineConfig } from "vite";

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
  },
  server: {
    port: 7123,
    open: true,
    host: "localhost",
  },
  build: {
    outDir: "build",
    assetsDir: "assets",
    cssCodeSplit: false,
  },
});
