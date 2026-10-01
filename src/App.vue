<script setup lang="ts">
import { onMounted } from 'vue'

import CursorGlow from '@/components/common/CursorGlow.vue'
import Header from '@/components/layout/Header.vue'
import Footer from '@/components/layout/Footer.vue'
import { createLenis } from '@/composables/useLenis'

onMounted(() => {
  // Инертный скролл (динамический импорт lenis; отключён при prefers-reduced-motion)
  void createLenis()
})
</script>

<template>
  <div
    class="min-h-screen bg-slate-50 text-slate-800 transition-colors duration-300 dark:bg-ink-950 dark:text-slate-200"
  >
    <!-- Film-grain текстура поверх всего сайта -->
    <div class="noise-overlay" aria-hidden="true" />

    <!-- Световое пятно за курсором (только fine pointer, без reduced-motion) -->
    <CursorGlow />

    <Header />
    <main>
      <RouterView />
    </main>
    <Footer />
  </div>
</template>
