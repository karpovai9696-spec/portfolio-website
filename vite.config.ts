import { fileURLToPath, URL } from 'node:url'

import { defineConfig, type Plugin } from 'vite'
import vue from '@vitejs/plugin-vue'

/**
 * Preload критичных шрифтов (woff2 с кириллицей): Montserrat для hero-заголовка
 * (LCP-кандидат) и Inter для основного текста. Шрифты лежат в src/assets/fonts,
 * поэтому имена хешируются при сборке — ссылки подставляются из bundle.
 */
function preloadCriticalFonts(): Plugin {
  let base = '/'
  return {
    name: 'preload-critical-fonts',
    apply: 'build',
    configResolved(config) {
      base = config.base
    },
    transformIndexHtml: {
      order: 'post',
      handler(html, ctx) {
        const bundle = ctx.bundle
        if (!bundle) return html
        const tags = Object.keys(bundle)
          .filter((name) => name.endsWith('.woff2'))
          .map((name) => name.split('/').pop() ?? '')
          .filter((name) => /^(montserrat|inter)-cyrillic-/.test(name))
          .map((name) => ({
            tag: 'link',
            attrs: {
              rel: 'preload',
              as: 'font',
              type: 'font/woff2',
              href: `${base}assets/${name}`,
              crossorigin: '',
            },
            injectTo: 'head-prepend' as const,
          }))
        return { html, tags }
      },
    },
  }
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), preloadCriticalFonts()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    // strictPort намеренно не включён: CLI-аргументы --port/--host
    // (например, `npm run dev -- --port 7100`) должны переопределять конфиг.
    port: 5173,
  },
})
