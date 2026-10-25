<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { Github, Menu, Moon, Sun, X } from 'lucide-vue-next'

import Navigation from '@/components/layout/Navigation.vue'
import LogoSign from '@/components/common/LogoSign.vue'
import { scrollToTarget } from '@/composables/useLenis'

const isDark = ref(true)
const isMenuOpen = ref(false)
const isScrolled = ref(false)
const scrollProgress = ref(0)

const GITHUB_URL = 'https://github.com/karpovai9696-spec'

function applyTheme(dark: boolean) {
  isDark.value = dark
  document.documentElement.classList.toggle('dark', dark)
  try {
    localStorage.setItem('theme', dark ? 'dark' : 'light')
  } catch {
    /* localStorage недоступен — игнорируем */
  }
}

function toggleTheme() {
  applyTheme(!isDark.value)
}

function closeMenu() {
  isMenuOpen.value = false
}

function onScroll() {
  isScrolled.value = window.scrollY > 10
  const doc = document.documentElement
  const max = doc.scrollHeight - doc.clientHeight
  scrollProgress.value = max > 0 ? Math.min(1, window.scrollY / max) : 0
}

function onKeydown(event: KeyboardEvent) {
  if (event.key === 'Escape') closeMenu()
}

function goContact() {
  closeMenu()
  scrollToTarget('#contact')
}

onMounted(() => {
  isDark.value = document.documentElement.classList.contains('dark')
  window.addEventListener('scroll', onScroll, { passive: true })
  window.addEventListener('keydown', onKeydown)
  onScroll()
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll)
  window.removeEventListener('keydown', onKeydown)
})
</script>

<template>
  <header
    class="fixed inset-x-0 top-0 z-50 transition-all duration-300"
    :class="
      isScrolled || isMenuOpen
        ? 'border-b border-hairline bg-paper/85 backdrop-blur-xl dark:border-ink-900 dark:bg-ink-950/85'
        : 'bg-transparent'
    "
  >
    <!-- Прогресс-бар чтения страницы -->
    <div
      class="absolute inset-x-0 top-0 h-0.5 origin-left bg-primary"
      :style="{ transform: `scaleX(${scrollProgress})` }"
      role="progressbar"
      :aria-valuenow="Math.round(scrollProgress * 100)"
      aria-valuemin="0"
      aria-valuemax="100"
      aria-label="Прогресс прокрутки страницы"
    />

    <div class="section-container flex h-16 items-center justify-between sm:h-20">
      <!-- Логотип: личный знак + MK.SPEC -->
      <a
        href="#hero"
        class="group flex items-center gap-2.5"
        aria-label="MK.SPEC Михаил Карпов — на главную"
        @click.prevent="closeMenu"
      >
        <LogoSign
          class="transition-transform duration-300 group-hover:-rotate-3 group-hover:scale-105"
          :sign="isDark ? '#FCD116' : '#8E751D'"
          :cursor="isDark ? '#8E751D' : '#3F3820'"
          clazz="h-8 w-auto"
        />
        <span
          class="font-display text-lg font-extrabold tracking-tight text-ink-800 dark:text-white"
        >
          MK<span class="text-gold dark:text-primary">.</span>SPEC
        </span>
      </a>

      <!-- Десктопная навигация -->
      <div class="hidden lg:block">
        <Navigation />
      </div>

      <div class="flex items-center gap-2">
        <!-- GitHub -->
        <a
          :href="GITHUB_URL"
          target="_blank"
          rel="noopener noreferrer"
          class="hidden rounded-xl p-2.5 text-ink-700 transition-all duration-300 hover:text-gold sm:inline-flex dark:text-ink-300 dark:hover:text-primary"
          aria-label="GitHub — karpovai9696-spec"
        >
          <Github class="h-5 w-5" aria-hidden="true" />
        </a>

        <!-- Переключатель темы -->
        <button
          type="button"
          class="rounded-xl p-2.5 text-ink-700 transition-all duration-300 hover:rotate-12 hover:bg-ink-950/5 dark:text-ink-300 dark:hover:bg-white/10"
          :aria-label="isDark ? 'Включить светлую тему' : 'Включить тёмную тему'"
          :aria-pressed="isDark"
          @click="toggleTheme"
        >
          <Sun v-if="isDark" class="h-5 w-5" aria-hidden="true" />
          <Moon v-else class="h-5 w-5" aria-hidden="true" />
        </button>

        <!-- CTA: Связаться -->
        <button
          type="button"
          class="hidden rounded-full border border-gold px-5 py-2 text-sm font-semibold text-gold transition-all duration-300 hover:bg-gold hover:text-[#FFFDF0] sm:inline-flex dark:border-primary dark:text-primary dark:hover:bg-primary dark:hover:text-[#09090A] dark:hover:shadow-[0_0_18px_rgba(252,209,22,0.45)]"
          @click="goContact"
        >
          Связаться
        </button>

        <!-- Бургер-кнопка (мобильная) -->
        <button
          type="button"
          class="rounded-xl p-2.5 text-ink-700 transition-colors hover:bg-ink-950/5 dark:text-ink-300 dark:hover:bg-white/10 lg:hidden"
          :aria-expanded="isMenuOpen"
          aria-controls="mobile-menu"
          :aria-label="isMenuOpen ? 'Закрыть меню' : 'Открыть меню'"
          @click="isMenuOpen = !isMenuOpen"
        >
          <X v-if="isMenuOpen" class="h-6 w-6" aria-hidden="true" />
          <Menu v-else class="h-6 w-6" aria-hidden="true" />
        </button>
      </div>
    </div>

    <!-- Мобильное меню -->
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="-translate-y-2 opacity-0"
      enter-to-class="translate-y-0 opacity-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="translate-y-0 opacity-100"
      leave-to-class="-translate-y-2 opacity-0"
    >
      <div
        v-if="isMenuOpen"
        id="mobile-menu"
        class="border-t border-hairline bg-paper/95 backdrop-blur-xl dark:border-ink-900 dark:bg-ink-950/95 lg:hidden"
        @click="closeMenu"
      >
        <div class="section-container py-4">
          <Navigation />
          <a
            :href="GITHUB_URL"
            target="_blank"
            rel="noopener noreferrer"
            class="mt-3 inline-flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium text-ink-700 dark:text-ink-300"
            aria-label="GitHub — karpovai9696-spec"
          >
            <Github class="h-5 w-5" aria-hidden="true" />
            GitHub
          </a>
        </div>
      </div>
    </Transition>
  </header>
</template>
