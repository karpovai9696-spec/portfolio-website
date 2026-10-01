<script setup lang="ts">
import { Briefcase, CheckCircle2, MapPin } from 'lucide-vue-next'

import GhostTitle from '@/components/common/GhostTitle.vue'
import SectionTitle from '@/components/common/SectionTitle.vue'
import { staggerStyle, useScrollAnimation } from '@/composables/useScrollAnimation'
import { usePortfolioStore } from '@/stores/portfolio'

const store = usePortfolioStore()
const { experience } = store

const { target } = useScrollAnimation<HTMLDivElement>({ threshold: 0.1 })
</script>

<template>
  <section
    id="experience"
    class="relative scroll-mt-20 overflow-hidden py-20 sm:py-28"
    aria-label="Опыт работы"
  >
    <GhostTitle text="ОПЫТ" />
    <div class="section-container relative">
      <SectionTitle title="Опыт" subtitle="Мой путь в разработке" index="05" tag="опыт" />

      <div ref="target" class="reveal relative mx-auto max-w-3xl">
        <!-- Вертикальная линия таймлайна: прорисовывается при скролле -->
        <div
          class="timeline-line absolute bottom-2 left-5 top-2 w-0.5 rounded-full bg-gradient-to-b from-primary via-accent to-transparent sm:left-1/2 sm:-translate-x-1/2"
          aria-hidden="true"
        />

        <ol class="space-y-12">
          <li
            v-for="(item, index) in experience"
            :key="item.id"
            class="reveal-child relative pl-14 sm:w-1/2 sm:pl-0"
            :class="index % 2 === 0 ? 'sm:pr-12 sm:text-right' : 'sm:ml-auto sm:pl-12'"
            :style="staggerStyle(index, 250, 300)"
          >
            <!-- Точка-узел со свечением -->
            <span
              class="absolute left-5 top-1.5 flex h-10 w-10 -translate-x-1/2 items-center justify-center sm:left-auto"
              :class="index % 2 === 0 ? 'sm:-right-5 sm:translate-x-1/2' : 'sm:-left-5 sm:-translate-x-1/2'"
              aria-hidden="true"
            >
              <span
                class="absolute inline-flex h-full w-full animate-pulse-ring rounded-full bg-primary/40"
              />
              <span
                class="relative flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-primary to-accent text-white shadow-lg shadow-primary/40"
              >
                <Briefcase class="h-5 w-5" />
              </span>
            </span>

            <article
              class="glass rounded-2xl p-6 text-left transition-all duration-300 hover:-translate-y-1 hover:shadow-xl hover:shadow-primary/10"
            >
              <p class="font-mono text-xs font-semibold uppercase tracking-wide text-primary">
                {{ item.period }}
              </p>
              <h3 class="mt-1.5 text-lg font-bold">{{ item.role }}</h3>
              <p class="mt-0.5 font-medium text-slate-600 dark:text-slate-300">{{ item.place }}</p>
              <p class="mt-1 flex items-center gap-1.5 text-sm text-slate-400 dark:text-slate-500">
                <MapPin class="h-3.5 w-3.5" aria-hidden="true" />
                {{ item.location }}
              </p>
              <ul class="mt-4 space-y-2">
                <li
                  v-for="point in item.points"
                  :key="point"
                  class="flex items-start gap-2 text-sm text-slate-600 dark:text-slate-300"
                >
                  <CheckCircle2 class="mt-0.5 h-4 w-4 shrink-0 text-accent" aria-hidden="true" />
                  {{ point }}
                </li>
              </ul>
            </article>
          </li>
        </ol>
      </div>
    </div>
  </section>
</template>
