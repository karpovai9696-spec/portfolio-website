<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { ArrowUp, Mail, Phone, Send } from 'lucide-vue-next'

import { scrollToTarget } from '@/composables/useLenis'
import { usePortfolioStore } from '@/stores/portfolio'

const store = usePortfolioStore()
const { person } = store

const showBackToTop = ref(false)

function onScroll() {
  showBackToTop.value = window.scrollY > 600
}

function scrollToTop() {
  scrollToTarget(0) // Lenis-инертный скролл (или нативный fallback)
}

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
  onScroll()
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll)
})
</script>

<template>
  <footer class="border-t border-slate-200/60 py-10 dark:border-white/10">
    <div class="section-container">
      <div class="flex flex-col items-center gap-6 sm:flex-row sm:justify-between">
        <p class="text-sm text-slate-500 dark:text-slate-400">
          © 2026 {{ person.name }}. Все права защищены.
        </p>

        <!-- Соцссылки -->
        <div class="flex items-center gap-3">
          <a
            :href="person.telegram"
            target="_blank"
            rel="noopener noreferrer"
            class="rounded-xl p-2.5 text-slate-500 transition-all hover:-translate-y-0.5 hover:bg-primary/10 hover:text-primary dark:text-slate-400"
            aria-label="Telegram"
          >
            <Send class="h-5 w-5" aria-hidden="true" />
          </a>
          <a
            :href="`mailto:${person.email}`"
            class="rounded-xl p-2.5 text-slate-500 transition-all hover:-translate-y-0.5 hover:bg-primary/10 hover:text-primary dark:text-slate-400"
            aria-label="Email"
          >
            <Mail class="h-5 w-5" aria-hidden="true" />
          </a>
          <a
            :href="person.phoneHref"
            class="rounded-xl p-2.5 text-slate-500 transition-all hover:-translate-y-0.5 hover:bg-primary/10 hover:text-primary dark:text-slate-400"
            aria-label="Телефон"
          >
            <Phone class="h-5 w-5" aria-hidden="true" />
          </a>
        </div>
      </div>
    </div>

    <!-- Плавающая кнопка «Наверх»: появляется после прокрутки -->
    <Transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="translate-y-4 scale-75 opacity-0"
      enter-to-class="translate-y-0 scale-100 opacity-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="translate-y-0 scale-100 opacity-100"
      leave-to-class="translate-y-4 scale-75 opacity-0"
    >
      <button
        v-if="showBackToTop"
        type="button"
        class="fixed bottom-6 right-6 z-40 inline-flex items-center gap-2 rounded-2xl bg-gradient-to-r from-primary to-accent px-4 py-3 text-sm font-semibold text-white shadow-xl shadow-primary/30 transition-transform duration-300 hover:-translate-y-1 hover:shadow-2xl hover:shadow-primary/40"
        aria-label="Вернуться наверх страницы"
        @click="scrollToTop"
      >
        <ArrowUp class="h-4 w-4" aria-hidden="true" />
        <span class="hidden sm:inline">Наверх</span>
      </button>
    </Transition>
  </footer>
</template>
