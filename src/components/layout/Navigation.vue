<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'

import { scrollToTarget } from '@/composables/useLenis'

export interface NavLink {
  href: string
  label: string
}

const links: NavLink[] = [
  { href: '#hero', label: 'Главная' },
  { href: '#about', label: 'Обо мне' },
  { href: '#services', label: 'Услуги' },
  { href: '#skills', label: 'Навыки' },
  { href: '#portfolio', label: 'Портфолио' },
  { href: '#experience', label: 'Опыт' },
  { href: '#contact', label: 'Контакты' },
]

/* ---------- Scrollspy: подсветка активной секции ---------- */
const activeId = ref('hero')
let spy: IntersectionObserver | null = null

onMounted(() => {
  const sections = links
    .map((link) => document.querySelector(link.href))
    .filter((el): el is Element => el !== null)

  if (typeof IntersectionObserver === 'undefined') return

  spy = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) activeId.value = entry.target.id
      }
    },
    { rootMargin: '-35% 0px -55% 0px' },
  )
  sections.forEach((section) => spy!.observe(section))
})

onBeforeUnmount(() => {
  spy?.disconnect()
  spy = null
})

function scrollTo(event: MouseEvent, href: string) {
  event.preventDefault()
  scrollToTarget(href) // Lenis-инертный скролл (или нативный fallback)
  history.replaceState(null, '', href)
}
</script>

<template>
  <nav aria-label="Основная навигация">
    <ul class="flex flex-col gap-1 lg:flex-row lg:items-center lg:gap-1">
      <li v-for="link in links" :key="link.href">
        <a
          :href="link.href"
          class="group relative block rounded-lg px-3 py-2 text-sm font-medium transition-colors duration-300"
          :class="
            activeId === link.href.slice(1)
              ? 'text-primary'
              : 'text-slate-600 hover:bg-slate-900/5 hover:text-primary dark:text-slate-300 dark:hover:bg-white/10 dark:hover:text-primary'
          "
          :aria-current="activeId === link.href.slice(1) ? 'true' : undefined"
          @click="scrollTo($event, link.href)"
        >
          {{ link.label }}
          <span
            class="absolute inset-x-3 -bottom-0.5 hidden h-0.5 rounded-full bg-gradient-to-r from-primary to-accent transition-all duration-300 group-hover:scale-x-100 group-hover:opacity-70 lg:block"
            :class="activeId === link.href.slice(1) ? 'scale-x-100 opacity-100' : 'scale-x-0 opacity-0'"
            aria-hidden="true"
          />
        </a>
      </li>
    </ul>
  </nav>
</template>
