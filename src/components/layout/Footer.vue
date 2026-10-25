<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { ArrowUp, Github, Mail, Send } from 'lucide-vue-next'

import { scrollToTarget } from '@/composables/useLenis'
import { usePortfolioStore } from '@/stores/portfolio'
import LogoSign from '@/components/common/LogoSign.vue'

const store = usePortfolioStore()
const { person } = store

const GITHUB_URL = 'https://github.com/karpovai9696-spec'

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
  <footer class="border-t border-hairline py-10 dark:border-ink-900">
    <div class="section-container">
      <div class="flex flex-col items-center gap-6 sm:flex-row sm:justify-between">
        <div class="flex items-center gap-2.5">
          <LogoSign sign="#8E751D" cursor="#3F3820" clazz="h-7 w-auto dark:hidden" />
          <LogoSign sign="#FCD116" cursor="#8E751D" clazz="hidden h-7 w-auto dark:block" />
          <p class="text-sm leading-tight text-ink-100 dark:text-ink-300">
            © 2026 {{ person.name }}
            <span class="block font-mono text-[10px] tracking-wider text-gold">mk.spec</span>
          </p>
        </div>

        <!-- Соцссылки -->
        <div class="flex items-center gap-3">
          <a
            :href="person.telegram"
            target="_blank"
            rel="noopener noreferrer"
            class="rounded-xl p-2.5 text-ink-100 transition-all hover:-translate-y-0.5 hover:bg-gold/10 hover:text-gold dark:text-ink-300 dark:hover:bg-primary/10 dark:hover:text-primary"
            aria-label="Telegram — @Phoenix9696"
          >
            <Send class="h-5 w-5" aria-hidden="true" />
          </a>
          <a
            :href="`mailto:${person.email}`"
            class="rounded-xl p-2.5 text-ink-100 transition-all hover:-translate-y-0.5 hover:bg-gold/10 hover:text-gold dark:text-ink-300 dark:hover:bg-primary/10 dark:hover:text-primary"
            aria-label="Email"
          >
            <Mail class="h-5 w-5" aria-hidden="true" />
          </a>
          <a
            :href="GITHUB_URL"
            target="_blank"
            rel="noopener noreferrer"
            class="rounded-xl p-2.5 text-ink-100 transition-all hover:-translate-y-0.5 hover:bg-gold/10 hover:text-gold dark:text-ink-300 dark:hover:bg-primary/10 dark:hover:text-primary"
            aria-label="GitHub — karpovai9696-spec"
          >
            <Github class="h-5 w-5" aria-hidden="true" />
          </a>
        </div>
      </div>

      <p class="mt-6 text-center font-mono text-[11px] tracking-wider text-gold sm:text-left">
        Разработал: Карпов Михаил
      </p>
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
        class="fixed bottom-6 right-6 z-40 inline-flex items-center gap-2 rounded-2xl bg-primary px-4 py-3 text-sm font-semibold text-[#09090A] shadow-[0_0_18px_rgba(252,209,22,0.4)] transition-transform duration-300 hover:-translate-y-1 hover:shadow-[0_0_26px_rgba(252,209,22,0.55)]"
        aria-label="Вернуться наверх страницы"
        @click="scrollToTop"
      >
        <ArrowUp class="h-4 w-4" aria-hidden="true" />
        <span class="hidden sm:inline">Наверх</span>
      </button>
    </Transition>
  </footer>
</template>
