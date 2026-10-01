<script setup lang="ts">
import type { FunctionalComponent } from 'vue'
import {
  Blocks,
  Globe,
  MonitorSmartphone,
  Search,
  ShoppingCart,
  Smartphone,
  Wrench,
} from 'lucide-vue-next'

import Card from '@/components/common/Card.vue'
import GhostTitle from '@/components/common/GhostTitle.vue'
import SectionTitle from '@/components/common/SectionTitle.vue'
import { staggerStyle, useScrollAnimation } from '@/composables/useScrollAnimation'
import { usePortfolioStore } from '@/stores/portfolio'

const store = usePortfolioStore()
const { services } = store

const iconMap: Record<string, FunctionalComponent> = {
  Globe,
  MonitorSmartphone,
  ShoppingCart,
  Wrench,
  Smartphone,
  Blocks,
  Search,
}

const { target } = useScrollAnimation<HTMLDivElement>()

/** Разная визуальная ритмика: первая и шестая карточки шире остальных */
function cardSpan(index: number): string {
  if (index === 0) return 'sm:col-span-2 lg:col-span-2'
  if (index === 5) return 'sm:col-span-2 lg:col-span-2'
  return ''
}
</script>

<template>
  <section
    id="services"
    class="relative scroll-mt-20 overflow-hidden bg-slate-100/60 py-20 dark:bg-white/[0.02] sm:py-28"
    aria-label="Услуги"
  >
    <GhostTitle text="УСЛУГИ" />
    <div class="section-container relative">
      <SectionTitle
        title="Услуги"
        subtitle="Что я могу сделать для вашего бизнеса"
        index="02"
        tag="услуги"
      />

      <div ref="target" class="reveal grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <Card
          v-for="(service, i) in services"
          :key="service.id"
          tilt
          spotlight
          :hover="false"
          class="reveal-child group"
          :class="cardSpan(i)"
          :style="staggerStyle(i, 80)"
        >
          <div class="relative">
            <div class="flex items-start justify-between">
              <div
                class="inline-flex rounded-2xl bg-gradient-to-br from-primary to-accent p-3 text-white shadow-lg shadow-primary/25 transition-transform duration-300 group-hover:scale-110 group-hover:rotate-3"
              >
                <component :is="iconMap[service.icon]" class="h-6 w-6" aria-hidden="true" />
              </div>
              <span
                class="font-mono text-4xl font-bold text-slate-200 transition-colors duration-300 group-hover:text-primary/30 dark:text-white/5 dark:group-hover:text-primary/20"
                aria-hidden="true"
              >
                {{ String(service.id).padStart(2, '0') }}
              </span>
            </div>
            <h3 class="mt-4 text-lg font-semibold transition-colors duration-300 group-hover:text-primary">
              {{ service.title }}
            </h3>
            <p class="mt-2 text-sm leading-relaxed text-slate-500 dark:text-slate-400">
              {{ service.description }}
            </p>
          </div>
        </Card>

        <!-- Карточка-призыв -->
        <a
          href="#contact"
          class="reveal-child group flex flex-col items-center justify-center rounded-2xl border-2 border-dashed border-primary/40 p-6 text-center transition-all duration-300 hover:-translate-y-1 hover:border-primary hover:bg-primary/5"
          :style="staggerStyle(services.length, 80)"
        >
          <span class="text-gradient text-lg font-semibold">Нужно что-то другое?</span>
          <span class="mt-2 text-sm text-slate-500 dark:text-slate-400">
            Напишите мне — обсудим вашу задачу и подберём решение
          </span>
        </a>
      </div>
    </div>
  </section>
</template>
