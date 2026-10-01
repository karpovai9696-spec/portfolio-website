<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { Code2, ExternalLink } from 'lucide-vue-next'

import Card from '@/components/common/Card.vue'
import GhostTitle from '@/components/common/GhostTitle.vue'
import SectionTitle from '@/components/common/SectionTitle.vue'
import { staggerStyle, useScrollAnimation } from '@/composables/useScrollAnimation'
import { usePortfolioStore } from '@/stores/portfolio'

const store = usePortfolioStore()

const filters = [
  { value: 'all', label: 'Все' },
  { value: 'vue', label: 'Vue' },
  { value: 'react', label: 'React' },
  { value: 'fullstack', label: 'Full Stack' },
] as const

const activeFilter = ref<string>('all')
const projects = computed(() => store.filteredProjects(activeFilter.value))

const { target } = useScrollAnimation<HTMLDivElement>()

/* ---------- Лёгкий scroll-параллакс превью (только transform) ---------- */
let parallaxRaf = 0

function updatePreviewParallax() {
  parallaxRaf = 0
  if (!target.value) return
  const els = target.value.querySelectorAll<HTMLElement>('.preview-parallax')
  els.forEach((el) => {
    const rect = el.getBoundingClientRect()
    const delta = rect.top + rect.height / 2 - window.innerHeight / 2
    el.style.transform = `translate3d(0, ${(-delta * 0.045).toFixed(1)}px, 0)`
  })
}

function onScrollParallax() {
  if (!parallaxRaf) parallaxRaf = requestAnimationFrame(updatePreviewParallax)
}

onMounted(() => {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
  window.addEventListener('scroll', onScrollParallax, { passive: true })
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScrollParallax)
  cancelAnimationFrame(parallaxRaf)
})
</script>

<template>
  <section
    id="portfolio"
    class="relative scroll-mt-20 overflow-hidden bg-slate-100/60 py-20 dark:bg-white/[0.02] sm:py-28"
    aria-label="Портфолио"
  >
    <GhostTitle text="ПОРТФОЛИО" />
    <div class="section-container relative">
      <SectionTitle
        title="Портфолио"
        subtitle="Примеры проектов, над которыми я работал"
        index="04"
        tag="портфолио"
      />

      <!-- Фильтры -->
      <div
        class="mb-10 flex flex-wrap justify-center gap-2"
        role="group"
        aria-label="Фильтр проектов"
      >
        <button
          v-for="filter in filters"
          :key="filter.value"
          type="button"
          class="rounded-xl px-5 py-2.5 text-sm font-semibold transition-all duration-300"
          :class="
            activeFilter === filter.value
              ? 'scale-105 bg-gradient-to-r from-primary to-accent text-white shadow-lg shadow-primary/25'
              : 'border border-slate-200/80 text-slate-600 hover:-translate-y-0.5 hover:border-primary/50 hover:text-primary dark:border-white/10 dark:text-slate-300'
          "
          :aria-pressed="activeFilter === filter.value"
          @click="activeFilter = filter.value"
        >
          {{ filter.label }}
        </button>
      </div>

      <!-- Сетка проектов с плавной анимацией при смене фильтра -->
      <div ref="target" class="reveal relative">
        <TransitionGroup name="portfolio" tag="div" class="relative grid gap-6 sm:grid-cols-2">
          <Card
            v-for="(project, i) in projects"
            :key="project.id"
            :padding="false"
            :hover="false"
            class="group overflow-hidden transition-all duration-300 hover:-translate-y-1.5 hover:shadow-2xl hover:shadow-primary/15"
            :style="staggerStyle(i, 90)"
          >
            <!-- Скриншот-плейсхолдер (CSS-градиент) с параллакс-масштабом при наведении -->
            <div class="relative h-48 overflow-hidden sm:h-56" aria-hidden="true">
              <!-- Параллакс-обёртка (scroll), внутри — hover-масштаб слоёв -->
              <div class="preview-parallax absolute inset-x-0 -inset-y-8 will-change-transform">
                <div
                  class="absolute inset-0 bg-gradient-to-br transition-transform duration-700 ease-out group-hover:scale-110 group-hover:rotate-1"
                  :class="project.gradient"
                />
                <div
                  class="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,rgba(255,255,255,0.25),transparent_50%)] transition-transform duration-700 group-hover:scale-125"
                />
                <div
                  class="absolute inset-0 flex items-center justify-center transition-transform duration-500 group-hover:-translate-y-2"
                >
                  <span class="text-4xl font-extrabold tracking-tight text-white/90 drop-shadow-lg">
                    {{ project.title.charAt(0) }}
                  </span>
                </div>
              </div>
              <div
                class="absolute inset-x-0 bottom-0 h-16 bg-gradient-to-t from-black/25 to-transparent"
              />
            </div>

            <div class="p-6">
              <h3 class="text-lg font-semibold transition-colors group-hover:text-primary">
                {{ project.title }}
              </h3>
              <p class="mt-2 text-sm leading-relaxed text-slate-500 dark:text-slate-400">
                {{ project.description }}
              </p>

              <!-- Стек -->
              <ul class="mt-4 flex flex-wrap gap-2" aria-label="Стек технологий">
                <li
                  v-for="tech in project.stack"
                  :key="tech"
                  class="rounded-md bg-primary/10 px-2.5 py-1 text-xs font-semibold text-primary"
                >
                  {{ tech }}
                </li>
              </ul>

              <!-- Кнопки-заглушки -->
              <div class="mt-5 flex gap-3">
                <a
                  :href="project.demoUrl"
                  class="inline-flex cursor-not-allowed items-center gap-1.5 rounded-lg bg-gradient-to-r from-primary to-accent px-4 py-2 text-sm font-semibold text-white opacity-80"
                  aria-label="Демо проекта (скоро будет доступно)"
                  title="Ссылка появится позже"
                  @click.prevent
                >
                  <ExternalLink class="h-4 w-4" aria-hidden="true" />
                  Демо
                </a>
                <a
                  :href="project.codeUrl"
                  class="inline-flex cursor-not-allowed items-center gap-1.5 rounded-lg border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-500 opacity-80 dark:border-white/15 dark:text-slate-400"
                  aria-label="Исходный код проекта (скоро будет доступен)"
                  title="Ссылка появится позже"
                  @click.prevent
                >
                  <Code2 class="h-4 w-4" aria-hidden="true" />
                  Код
                </a>
              </div>
            </div>
          </Card>
        </TransitionGroup>
      </div>
    </div>
  </section>
</template>
