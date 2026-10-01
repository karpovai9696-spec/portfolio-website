<script setup lang="ts">
import { onBeforeUnmount, ref, watch } from 'vue'

import Card from '@/components/common/Card.vue'
import GhostTitle from '@/components/common/GhostTitle.vue'
import SectionTitle from '@/components/common/SectionTitle.vue'
import { staggerStyle, useScrollAnimation } from '@/composables/useScrollAnimation'
import { usePortfolioStore } from '@/stores/portfolio'

const store = usePortfolioStore()
const { skillCategories, skillLevels } = store

const { target: categoriesBlock } = useScrollAnimation<HTMLDivElement>()
const { target: barsBlock, isVisible: barsVisible } = useScrollAnimation<HTMLDivElement>({
  threshold: 0.2,
})

/* ---------- Анимированные счётчики процентов ---------- */
const displayedPercents = ref<number[]>(skillLevels.map(() => 0))
let raf = 0

watch(barsVisible, (visible) => {
  if (!visible) return

  const reduced = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false
  if (reduced) {
    displayedPercents.value = skillLevels.map((s) => s.level)
    return
  }

  const duration = 1300
  const start = performance.now()
  const tick = (now: number) => {
    const progress = Math.min(1, (now - start) / duration)
    const eased = 1 - Math.pow(1 - progress, 3)
    displayedPercents.value = skillLevels.map((s) => Math.round(s.level * eased))
    if (progress < 1) raf = requestAnimationFrame(tick)
  }
  raf = requestAnimationFrame(tick)
})

onBeforeUnmount(() => cancelAnimationFrame(raf))

const labelColors: Record<string, string> = {
  Expert: 'text-green-500 dark:text-green-400',
  Advanced: 'text-primary',
  Intermediate: 'text-amber-500 dark:text-amber-400',
  Basic: 'text-slate-500 dark:text-slate-400',
}
</script>

<template>
  <section
    id="skills"
    class="relative scroll-mt-20 overflow-hidden py-20 sm:py-28"
    aria-label="Навыки"
  >
    <GhostTitle text="НАВЫКИ" />
    <div class="section-container relative">
      <SectionTitle
        title="Навыки"
        subtitle="Технологии, с которыми я работаю каждый день"
        index="03"
        tag="навыки"
      />

      <!-- Категории технологий -->
      <div ref="categoriesBlock" class="reveal grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <Card
          v-for="(category, i) in skillCategories"
          :key="category.title"
          spotlight
          class="reveal-child"
          :style="staggerStyle(i, 90)"
        >
          <h3 class="text-gradient relative mb-4 text-lg font-semibold">{{ category.title }}</h3>
          <ul class="relative flex flex-wrap gap-2">
            <li
              v-for="item in category.items"
              :key="item"
              class="rounded-lg border border-slate-200/80 bg-white/60 px-3 py-1.5 text-sm font-medium text-slate-600 transition-all duration-300 hover:-translate-y-0.5 hover:border-primary/50 hover:text-primary hover:shadow-md hover:shadow-primary/10 dark:border-white/10 dark:bg-white/5 dark:text-slate-300 dark:hover:border-primary/50 dark:hover:text-primary"
            >
              {{ item }}
            </li>
          </ul>
        </Card>
      </div>

      <!-- Уровни владения -->
      <div ref="barsBlock" class="reveal mt-14">
        <h3 class="mb-8 text-center text-xl font-bold">Уровень владения</h3>
        <div class="grid gap-x-10 gap-y-6 sm:grid-cols-2">
          <div
            v-for="(skill, i) in skillLevels"
            :key="skill.name"
            class="reveal-child"
            :style="staggerStyle(i, 60)"
          >
            <div class="mb-2 flex items-baseline justify-between">
              <span class="font-medium">{{ skill.name }}</span>
              <span class="text-sm">
                <span class="font-semibold" :class="labelColors[skill.label]">
                  {{ skill.label }}
                </span>
                <span class="ml-2 tabular-nums text-slate-400 dark:text-slate-500">
                  {{ displayedPercents[i] }}%
                </span>
              </span>
            </div>
            <div
              class="h-2.5 overflow-hidden rounded-full bg-slate-200 dark:bg-slate-800"
              role="progressbar"
              :aria-valuenow="skill.level"
              aria-valuemin="0"
              aria-valuemax="100"
              :aria-label="`Уровень владения ${skill.name}: ${skill.level}%`"
            >
              <div
                class="skill-bar-fill relative h-full rounded-full bg-gradient-to-r from-primary to-accent"
                :style="{ '--skill-level': `${skill.level}%` }"
              >
                <span
                  class="absolute inset-y-0 right-0 w-8 bg-gradient-to-r from-transparent to-white/30"
                  aria-hidden="true"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
