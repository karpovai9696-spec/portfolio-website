<script setup lang="ts">
import { onBeforeUnmount, ref, watch } from 'vue'

import { staggerStyle, useScrollAnimation } from '@/composables/useScrollAnimation'

/** Честные цифры, согласованные с контентом стора */
const stats = [
  { value: 2, suffix: '+', label: 'года коммерческой разработки' },
  { value: 4, suffix: '', label: 'года обучения и практики' },
  { value: 28, suffix: '', label: 'технологий в стеке' },
  { value: 7, suffix: '', label: 'направлений услуг' },
]

const displayed = ref<number[]>(stats.map(() => 0))

const { target, isVisible } = useScrollAnimation<HTMLDivElement>({ threshold: 0.3 })

let raf = 0

watch(isVisible, (visible) => {
  if (!visible) return

  const reduced = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false
  if (reduced) {
    displayed.value = stats.map((s) => s.value)
    return
  }

  const duration = 1400
  const start = performance.now()
  const tick = (now: number) => {
    const progress = Math.min(1, (now - start) / duration)
    const eased = 1 - Math.pow(1 - progress, 3)
    displayed.value = stats.map((s) => Math.round(s.value * eased))
    if (progress < 1) raf = requestAnimationFrame(tick)
  }
  raf = requestAnimationFrame(tick)
})

onBeforeUnmount(() => cancelAnimationFrame(raf))
</script>

<template>
  <section class="py-14 sm:py-16" aria-label="Ключевые цифры">
    <div class="section-container">
      <div
        ref="target"
        class="grid grid-cols-2 gap-4 sm:gap-6 lg:grid-cols-4"
        :class="{ 'is-visible': isVisible }"
      >
        <div
          v-for="(stat, i) in stats"
          :key="stat.label"
          class="reveal-child glass rounded-2xl p-6 text-center transition-shadow duration-300 hover:shadow-xl hover:shadow-primary/10"
          :style="staggerStyle(i, 110)"
        >
          <p class="text-4xl font-extrabold tracking-tight sm:text-5xl">
            <span class="text-gradient tabular-nums">{{ displayed[i] }}{{ stat.suffix }}</span>
          </p>
          <p class="mt-2 text-sm text-slate-500 dark:text-slate-400">{{ stat.label }}</p>
        </div>
      </div>
    </div>
  </section>
</template>
