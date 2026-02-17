import { defineConfig } from "electron-vite";
import react from "@vitejs/plugin-react";
import { resolve } from "path";

export default defineConfig({
  main: {
    build: {
      outDir: "dist/main",
    },
  },
  preload: {
    build: {
      outDir: "dist/preload",
    },
  },
  renderer: {
    plugins: [react()],
    resolve: {
      alias: {
        "@shared": resolve(__dirname, "../shared/src"),
      },
    },
    build: {
      outDir: "dist/renderer",
    },
  },
});
