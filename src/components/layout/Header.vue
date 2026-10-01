<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { Menu, Moon, Sun, X } from 'lucide-vue-next'

import Navigation from '@/components/layout/Navigation.vue'

const isDark = ref(true)
const isMenuOpen = ref(false)
const isScrolled = ref(false)
const scrollProgress = ref(0)

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
        ? 'border-b border-slate-200/60 bg-white/80 shadow-sm backdrop-blur-xl dark:border-white/10 dark:bg-ink-950/80'
        : 'bg-transparent'
    "
  >
    <!-- Прогресс-бар чтения страницы -->
    <div
      class="absolute inset-x-0 top-0 h-0.5 origin-left bg-gradient-to-r from-primary to-accent"
      :style="{ transform: `scaleX(${scrollProgress})` }"
      role="progressbar"
      :aria-valuenow="Math.round(scrollProgress * 100)"
      aria-valuemin="0"
      aria-valuemax="100"
      aria-label="Прогресс прокрутки страницы"
    />

    <div class="section-container flex h-16 items-center justify-between sm:h-20">
      <!-- Логотип -->
      <a
        href="#hero"
        class="group flex items-center gap-2 text-lg font-bold tracking-tight"
        aria-label="Михаил Карпов — на главную"
        @click.prevent="closeMenu"
      >
        <span
          class="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-primary to-accent text-sm font-bold text-white shadow-lg shadow-primary/25 transition-transform duration-300 group-hover:rotate-6 group-hover:scale-110"
          aria-hidden="true"
        >
          МК
        </span>
        <span class="hidden sm:inline">Михаил <span class="text-gradient">Карпов</span></span>
      </a>

      <!-- Десктопная навигация -->
      <div class="hidden lg:block">
        <Navigation />
      </div>

      <div class="flex items-center gap-2">
        <!-- Переключатель темы -->
        <button
          type="button"
          class="rounded-xl p-2.5 text-slate-600 transition-all duration-300 hover:rotate-12 hover:bg-slate-900/5 dark:text-slate-300 dark:hover:bg-white/10"
          :aria-label="isDark ? 'Включить светлую тему' : 'Включить тёмную тему'"
          :aria-pressed="isDark"
          @click="toggleTheme"
        >
          <Sun v-if="isDark" class="h-5 w-5" aria-hidden="true" />
          <Moon v-else class="h-5 w-5" aria-hidden="true" />
        </button>

        <!-- Бургер-кнопка (мобильная) -->
        <button
          type="button"
          class="rounded-xl p-2.5 text-slate-600 transition-colors hover:bg-slate-900/5 dark:text-slate-300 dark:hover:bg-white/10 lg:hidden"
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
        class="border-t border-slate-200/60 bg-white/95 backdrop-blur-xl dark:border-white/10 dark:bg-ink-950/95 lg:hidden"
        @click="closeMenu"
      >
        <div class="section-container py-4">
          <Navigation />
        </div>
      </div>
    </Transition>
  </header>
</template>
