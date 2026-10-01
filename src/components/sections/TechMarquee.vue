<script setup lang="ts">
import { computed } from 'vue'

import { usePortfolioStore } from '@/stores/portfolio'

const store = usePortfolioStore()

/** Плоский список всех технологий из стора */
const technologies = computed(() => store.skillCategories.flatMap((c) => c.items))

/** Дублируем список для бесшовного зацикливания (translateX -50%) */
const marqueeItems = computed(() => [...technologies.value, ...technologies.value])
</script>

<template>
  <div
    class="marquee border-y border-slate-200/60 bg-white/40 py-5 backdrop-blur-sm dark:border-white/5 dark:bg-white/[0.02]"
    aria-hidden="true"
  >
    <div class="marquee-track items-center gap-8 pr-8">
      <span
        v-for="(tech, i) in marqueeItems"
        :key="`${tech}-${i}`"
        class="flex items-center gap-8 whitespace-nowrap font-mono text-sm font-medium tracking-wide text-slate-400 transition-colors hover:text-primary dark:text-slate-500 dark:hover:text-primary"
      >
        {{ tech }}
        <span class="h-1.5 w-1.5 rounded-full bg-gradient-to-r from-primary to-accent" />
      </span>
    </div>
  </div>
</template>
