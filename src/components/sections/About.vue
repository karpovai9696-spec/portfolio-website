<script setup lang="ts">
import { Cake, CheckCircle2, GraduationCap, Languages, MapPin } from 'lucide-vue-next'

import Card from '@/components/common/Card.vue'
import SectionTitle from '@/components/common/SectionTitle.vue'
import { useParallax } from '@/composables/useParallax'
import { staggerStyle, useScrollAnimation } from '@/composables/useScrollAnimation'
import { usePortfolioStore } from '@/stores/portfolio'

const store = usePortfolioStore()
const { person, education } = store

const { target: textBlock } = useScrollAnimation<HTMLDivElement>()
const { target: photoBlock } = useScrollAnimation<HTMLDivElement>()
const { target: eduBlock } = useScrollAnimation<HTMLDivElement>()
const { target: photoParallax } = useParallax<HTMLDivElement>(0.05)
</script>

<template>
  <section id="about" class="scroll-mt-20 py-20 sm:py-28" aria-label="Обо мне">
    <div class="section-container">
      <SectionTitle
        title="Обо мне"
        subtitle="Немного о том, кто я и чем занимаюсь"
        index="01"
        tag="обо мне"
      />

      <div class="grid items-start gap-10 lg:grid-cols-5 lg:gap-14">
        <!-- Фото -->
        <div ref="photoBlock" class="reveal-left mx-auto w-full max-w-sm lg:col-span-2">
          <div ref="photoParallax" class="will-change-transform">
            <div class="gradient-border">
              <div class="overflow-hidden rounded-[1.35rem] bg-slate-200 dark:bg-slate-800">
              <img
                :src="person.photo"
                :alt="`Фотография — ${person.name}`"
                width="640"
                height="640"
                loading="lazy"
                class="aspect-square w-full object-cover grayscale transition-all duration-500 hover:scale-105 hover:grayscale-0"
              />
              </div>
            </div>
          </div>

          <!-- Факты -->
          <Card class="mt-6" :hover="false" spotlight>
            <ul class="relative space-y-3 text-sm">
              <li class="flex items-center gap-3">
                <Cake class="h-4 w-4 shrink-0 text-primary" aria-hidden="true" />
                <span class="text-slate-500 dark:text-slate-400">Возраст:</span>
                <span class="ml-auto font-medium">{{ person.age }} года</span>
              </li>
              <li class="flex items-center gap-3">
                <MapPin class="h-4 w-4 shrink-0 text-primary" aria-hidden="true" />
                <span class="text-slate-500 dark:text-slate-400">Город:</span>
                <span class="ml-auto font-medium">{{ person.city }}</span>
              </li>
              <li class="flex items-center gap-3">
                <Languages class="h-4 w-4 shrink-0 text-primary" aria-hidden="true" />
                <span class="text-slate-500 dark:text-slate-400">Языки:</span>
                <span class="ml-auto font-medium">{{ person.languages }}</span>
              </li>
            </ul>
          </Card>
        </div>

        <!-- Текст -->
        <div ref="textBlock" class="reveal-right lg:col-span-3">
          <h3 class="text-2xl font-bold">
            {{ person.role }} <span class="text-slate-400 dark:text-slate-500">/</span>
            <span class="text-gradient">Фрилансер</span>
          </h3>

          <div class="mt-5 space-y-4 leading-relaxed text-slate-600 dark:text-slate-300">
            <p v-for="(paragraph, i) in person.aboutText" :key="i">{{ paragraph }}</p>
          </div>

          <!-- Личные качества -->
          <h4 class="mt-8 text-lg font-semibold">Личные качества</h4>
          <ul class="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2">
            <li
              v-for="(quality, i) in person.qualities"
              :key="quality"
              class="reveal-child flex items-center gap-2.5 rounded-xl border border-slate-200/70 bg-white/50 px-4 py-3 text-sm font-medium transition-colors hover:border-primary/40 dark:border-white/10 dark:bg-white/5"
              :style="staggerStyle(i, 90, 200)"
            >
              <CheckCircle2 class="h-5 w-5 shrink-0 text-primary" aria-hidden="true" />
              {{ quality }}
            </li>
          </ul>
        </div>
      </div>

      <!-- Образование -->
      <div ref="eduBlock" class="reveal mt-16">
        <h3 class="mb-6 flex items-center gap-3 text-xl font-bold">
          <GraduationCap class="h-6 w-6 text-primary" aria-hidden="true" />
          Образование и курсы
        </h3>
        <div class="grid gap-4 sm:grid-cols-2">
          <Card
            v-for="(item, i) in education"
            :key="item.id"
            spotlight
            class="reveal-child"
            :style="staggerStyle(i, 100)"
          >
            <p class="relative text-xs font-semibold uppercase tracking-wide text-primary">
              {{ item.period }}
            </p>
            <h4 class="relative mt-1.5 font-semibold">{{ item.title }}</h4>
            <p class="relative mt-1 text-sm text-slate-500 dark:text-slate-400">
              {{ item.organization }}
            </p>
          </Card>
        </div>
      </div>
    </div>
  </section>
</template>
