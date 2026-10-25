<script setup lang="ts">
import { Github } from 'lucide-vue-next'

import { useScrollAnimation } from '@/composables/useScrollAnimation'
import { usePortfolioStore } from '@/stores/portfolio'

const store = usePortfolioStore()
const { projects } = store

const { target } = useScrollAnimation<HTMLDivElement>()

/* ---------- Данные CSS-моков ---------- */

/** Высоты столбцов мини-графика админки (%) */
const adminBars = [42, 68, 35, 80, 56, 92, 48, 74, 60, 88]

/** Строки логов терминала маркировки */
const terminalLogs = [
  { cls: 'ok', text: '[OK] документ 552 · вывод из оборота' },
  { cls: 'plain', text: 'sgtin: 04607003123456ABCDE' },
  { cls: 'ok', text: '[OK] подпись УКЭП · verify_successful' },
  { cls: 'dim', text: 'queue: 12 → processed · retry 0' },
  { cls: 'accent', text: 'status: ok · latency 38 ms' },
]
</script>

<template>
  <section
    id="portfolio"
    class="relative scroll-mt-20 overflow-hidden py-20 sm:py-28"
    aria-label="Портфолио"
  >
    <div class="section-container relative">
      <div ref="target" class="reveal">
        <h2
          class="border-l-4 border-gold pl-4 font-display text-3xl font-extrabold uppercase tracking-tight text-ink-800 dark:border-primary dark:text-white"
        >
          Мои проекты
        </h2>
        <p class="mt-3 max-w-2xl text-base text-ink-100 dark:text-ink-300">
          Боевые системы: мониторинг, интеграции, криптография
        </p>

        <div class="mt-10 grid gap-6 md:grid-cols-2">
          <article
            v-for="project in projects"
            :key="project.id"
            class="group overflow-hidden rounded-2xl border border-gold/20 bg-paper-raised transition-all duration-300 hover:-translate-y-1 hover:border-gold/50 hover:shadow-[0_0_20px_rgba(142,117,29,0.18)] dark:border-primary/10 dark:bg-ink-900/70 dark:backdrop-blur-md dark:hover:border-primary/40 dark:hover:shadow-[0_0_20px_rgba(252,209,22,0.15)]"
          >
            <!-- Превью: CSS-мок -->
            <div class="relative h-52 overflow-hidden sm:h-60" aria-hidden="true">
              <div
                class="absolute inset-0 transition-transform duration-500 ease-out group-hover:scale-[1.02]"
              >
                <!-- Мок тёмной админки АМДЛП -->
                <div v-if="project.mock === 'admin'" class="flex h-full bg-[#0D0D10]">
                  <!-- Сайдбар -->
                  <div class="flex w-14 flex-col gap-2 border-r border-white/5 p-3 sm:w-16">
                    <span class="h-2 w-full rounded-sm bg-[#FCD116]/70" />
                    <span class="h-2 w-full rounded-sm bg-white/10" />
                    <span class="h-2 w-full rounded-sm bg-white/10" />
                    <span class="h-2 w-full rounded-sm bg-white/10" />
                    <span class="mt-auto h-2 w-full rounded-sm bg-[#8E751D]/60" />
                  </div>
                  <!-- Основная область -->
                  <div class="flex flex-1 flex-col p-4">
                    <!-- Жёлтые вкладки -->
                    <div class="flex gap-2">
                      <span
                        class="rounded-t-md bg-[#FCD116] px-3 py-1 font-mono text-[10px] font-semibold text-[#09090A]"
                      >Остатки</span>
                      <span
                        class="rounded-t-md bg-white/5 px-3 py-1 font-mono text-[10px] text-[#FFF5B8]/60"
                      >Документы</span>
                      <span
                        class="rounded-t-md bg-white/5 px-3 py-1 font-mono text-[10px] text-[#FFF5B8]/60"
                      >Отчёты</span>
                    </div>
                    <!-- Мини-график -->
                    <div
                      class="mt-3 flex flex-1 items-end gap-1.5 rounded-b-md rounded-tr-md border border-white/5 bg-white/[0.03] p-3"
                    >
                      <span
                        v-for="(h, i) in adminBars"
                        :key="i"
                        class="flex-1 rounded-sm"
                        :class="i % 3 === 0 ? 'bg-[#FCD116]/80' : 'bg-[#8E751D]/60'"
                        :style="{ height: `${h}%` }"
                      />
                    </div>
                  </div>
                </div>

                <!-- Мок терминала с логами маркировки -->
                <div
                  v-else
                  class="flex h-full flex-col bg-[#0D0D10] p-4 font-mono text-[11px] leading-relaxed sm:text-xs"
                >
                  <div class="mb-3 flex gap-1.5">
                    <span class="h-2.5 w-2.5 rounded-full bg-[#FF5F57]" />
                    <span class="h-2.5 w-2.5 rounded-full bg-[#FEBC2E]" />
                    <span class="h-2.5 w-2.5 rounded-full bg-[#28C840]" />
                  </div>
                  <p
                    v-for="(log, i) in terminalLogs"
                    :key="i"
                    :class="{
                      'text-[#7EE787]': log.cls === 'ok',
                      'text-[#FFF5B8]/85': log.cls === 'plain',
                      'text-[#FFF5B8]/45': log.cls === 'dim',
                      'font-semibold text-[#FCD116]': log.cls === 'accent',
                    }"
                  >
                    {{ log.text }}
                  </p>
                </div>
              </div>

              <!-- Кнопка GitHub в углу превью -->
              <a
                :href="project.codeUrl"
                target="_blank"
                rel="noopener noreferrer"
                class="absolute right-3 top-3 rounded-lg border border-white/10 bg-black/50 p-2 text-[#FFF5B8]/80 backdrop-blur-sm transition-all hover:border-[#FCD116]/50 hover:text-[#FCD116]"
                :aria-label="`Исходный код проекта «${project.title}» на GitHub`"
              >
                <Github class="h-4 w-4" aria-hidden="true" />
              </a>
            </div>

            <!-- Тело карточки -->
            <div class="p-6">
              <h3
                class="font-display text-lg font-bold text-ink-800 transition-colors group-hover:text-gold dark:text-white dark:group-hover:text-primary"
              >
                {{ project.title }}
              </h3>
              <p class="mt-2 text-sm leading-relaxed text-ink-100 dark:text-ink-300">
                {{ project.description }}
              </p>

              <!-- Бейджи -->
              <ul class="mt-4 flex flex-wrap gap-2" aria-label="Тип проекта">
                <li
                  v-for="tech in project.stack"
                  :key="tech"
                  class="rounded-md border border-gold/30 bg-gold/5 px-2.5 py-1 font-mono text-xs font-medium text-gold dark:border-primary/25 dark:bg-primary/10 dark:text-primary"
                >
                  {{ tech }}
                </li>
              </ul>
            </div>
          </article>
        </div>
      </div>
    </div>
  </section>
</template>
