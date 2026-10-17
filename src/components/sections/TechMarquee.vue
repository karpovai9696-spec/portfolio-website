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
    class="marquee border-y border-hairline bg-paper-raised/70 py-5 dark:border-white/5 dark:bg-ink-900/40"
    aria-hidden="true"
  >
    <div class="marquee-track items-center gap-8 pr-8">
      <span
        v-for="(tech, i) in marqueeItems"
        :key="`${tech}-${i}`"
        class="flex items-center gap-8 whitespace-nowrap font-mono text-sm font-medium tracking-wide text-ink-50 transition-colors hover:text-primary dark:text-[#A39B8B] dark:hover:text-[#e8703c]"
      >
        {{ tech }}
        <span class="h-1.5 w-1.5 rounded-full bg-primary" />
      </span>
    </div>
  </div>
</template>
