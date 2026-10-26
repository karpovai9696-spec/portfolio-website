<script setup lang="ts">
import { useScrollAnimation } from '@/composables/useScrollAnimation'
import { usePortfolioStore } from '@/stores/portfolio'

const store = usePortfolioStore()
const { projects } = store

const { target } = useScrollAnimation<HTMLDivElement>()

/* ---------- Данные CSS/SVG-моков ---------- */

/** Высоты мини-карточек канбана по колонкам */
const kanbanCols = [
  [18, 12, 22],
  [26, 16],
  [14, 20, 12],
]

/** Высоты столбцов мини-графика админки МДЛП (%) */
const adminBars = [42, 68, 35, 80, 56, 92, 48, 74, 60, 88]

/** Схема «токены → сотрудники»: 4 токена слева, хаб, 5 точек справа */
const tokenChips = [28, 66, 104, 142] // y-координаты токенов
const userDots = [20, 54, 88, 122, 156] // y-координаты сотрудников

/** Сетевой граф VPN: узлы вокруг центрального сервера */
const vpnNodes = [
  { x: 160, y: 88, r: 9, d: 0, dur: 3.2 }, // сервер
  { x: 60, y: 40, r: 4, d: 0.5, dur: 2.8 },
  { x: 262, y: 36, r: 4, d: 1.1, dur: 3.5 },
  { x: 46, y: 136, r: 4, d: 1.7, dur: 2.6 },
  { x: 272, y: 132, r: 4, d: 0.3, dur: 3.0 },
  { x: 160, y: 24, r: 3.5, d: 2.1, dur: 3.7 },
  { x: 108, y: 152, r: 3.5, d: 0.9, dur: 2.9 },
  { x: 222, y: 156, r: 3.5, d: 1.4, dur: 3.3 },
]

const statusMeta: Record<string, { label: string; cls: string }> = {
  production: {
    label: 'В продакшене',
    cls: 'bg-[#FCD116] text-[#09090A]',
  },
  ready: {
    label: 'Готов к внедрению',
    cls: 'border border-[#8E751D] text-[#C9B45C]',
  },
  designed: {
    label: 'Спроектировано',
    cls: 'border border-[#8E751D] text-[#C9B45C]',
  },
}
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
          Шесть ключевых кейсов: порталы, интеграции, криптография, инфраструктура
        </p>

        <div class="mt-10 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          <article
            v-for="project in projects"
            :key="project.id"
            class="group flex flex-col overflow-hidden rounded-2xl border border-gold/20 bg-paper-raised transition-all duration-300 hover:-translate-y-1 hover:border-gold/50 hover:shadow-[0_0_20px_rgba(142,117,29,0.18)] dark:border-primary/10 dark:bg-ink-900/70 dark:backdrop-blur-md dark:hover:border-primary/40 dark:hover:shadow-[0_0_20px_rgba(252,209,22,0.15)]"
          >
            <!-- Превью: CSS/SVG-мок -->
            <div class="relative h-44 overflow-hidden" aria-hidden="true">
              <div
                class="absolute inset-0 transition-transform duration-500 ease-out group-hover:scale-[1.02]"
              >
                <!-- 1. Канбан корпоративного портала -->
                <div
                  v-if="project.mock === 'kanban'"
                  class="flex h-full flex-col bg-[#0D0D10] p-3"
                >
                  <div class="mb-2 flex items-center gap-2">
                    <span class="h-2 w-2 rounded-full bg-[#FCD116]" />
                    <span class="h-1.5 w-16 rounded bg-white/15" />
                    <span class="ml-auto h-1.5 w-8 rounded bg-[#8E751D]/60" />
                  </div>
                  <div class="grid flex-1 grid-cols-3 gap-2">
                    <div
                      v-for="(col, ci) in kanbanCols"
                      :key="ci"
                      class="flex flex-col gap-1.5 rounded-md border border-white/5 bg-white/[0.03] p-1.5"
                    >
                      <span
                        class="mb-0.5 h-1 w-3/4 rounded-full"
                        :class="ci === 1 ? 'bg-[#FCD116]/70' : 'bg-white/15'"
                      />
                      <span
                        v-for="(h, i) in col"
                        :key="i"
                        class="rounded-sm bg-white/[0.08]"
                        :style="{ height: `${h}px` }"
                      />
                    </div>
                  </div>
                </div>

                <!-- 2. Админка агрегатора МДЛП -->
                <div
                  v-else-if="project.mock === 'admin'"
                  class="flex h-full bg-[#0D0D10]"
                >
                  <div class="flex w-10 flex-col gap-1.5 border-r border-white/5 p-2">
                    <span class="h-1.5 w-full rounded-sm bg-[#FCD116]/70" />
                    <span class="h-1.5 w-full rounded-sm bg-white/10" />
                    <span class="h-1.5 w-full rounded-sm bg-white/10" />
                    <span class="mt-auto h-1.5 w-full rounded-sm bg-[#8E751D]/60" />
                  </div>
                  <div class="flex flex-1 flex-col p-3">
                    <div class="flex gap-1.5">
                      <span
                        class="rounded-t bg-[#FCD116] px-2 py-0.5 font-mono text-[9px] font-semibold text-[#09090A]"
                      >Остатки</span>
                      <span
                        class="rounded-t bg-white/5 px-2 py-0.5 font-mono text-[9px] text-[#FFF5B8]/60"
                      >Документы</span>
                    </div>
                    <div
                      class="mt-2 flex flex-1 items-end gap-1 rounded-b rounded-tr border border-white/5 bg-white/[0.03] p-2"
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

                <!-- 3. Схема сетевого доступа к токенам ЭЦП -->
                <svg
                  v-else-if="project.mock === 'tokens'"
                  class="h-full w-full bg-[#0D0D10]"
                  viewBox="0 0 320 176"
                  fill="none"
                  preserveAspectRatio="xMidYMid meet"
                >
                  <!-- линии: токены → хаб -->
                  <line
                    v-for="y in tokenChips"
                    :key="`tl-${y}`"
                    x1="52"
                    :y1="y + 8"
                    x2="150"
                    y2="88"
                    class="mock-wire"
                  />
                  <!-- линии: хаб → сотрудники -->
                  <line
                    v-for="y in userDots"
                    :key="`ul-${y}`"
                    x1="170"
                    y1="88"
                    x2="286"
                    :y2="y"
                    class="mock-wire"
                  />
                  <!-- хаб -->
                  <circle cx="160" cy="88" r="11" class="mock-hub" />
                  <circle cx="160" cy="88" r="18" class="mock-hub-ring" />
                  <!-- токены -->
                  <rect
                    v-for="y in tokenChips"
                    :key="`t-${y}`"
                    x="16"
                    :y="y"
                    width="36"
                    height="16"
                    rx="4"
                    class="mock-node"
                  />
                  <!-- сотрудники -->
                  <circle
                    v-for="y in userDots"
                    :key="`u-${y}`"
                    cx="292"
                    :cy="y"
                    r="5"
                    class="mock-leaf"
                  />
                </svg>

                <!-- 4. Мини-лендинг «Динамит» -->
                <div
                  v-else-if="project.mock === 'landing'"
                  class="flex h-full flex-col bg-[#0D0D10] p-3"
                >
                  <div
                    class="flex flex-1 flex-col overflow-hidden rounded-md border border-white/10 bg-[#141417]"
                  >
                    <div class="flex items-center gap-1.5 border-b border-white/5 px-2 py-1.5">
                      <span class="h-1.5 w-1.5 rounded-full bg-white/20" />
                      <span class="h-1.5 w-1.5 rounded-full bg-white/20" />
                      <span class="ml-1 h-1.5 flex-1 rounded-full bg-white/[0.07]" />
                    </div>
                    <div
                      class="flex flex-1 flex-col items-center justify-center gap-1.5 bg-gradient-to-b from-[#FCD116]/10 to-transparent p-2"
                    >
                      <span class="h-2 w-20 rounded bg-[#FCD116]" />
                      <span class="h-1.5 w-24 rounded bg-white/20" />
                      <span
                        class="mt-1 rounded-full bg-[#FCD116] px-2 py-0.5 font-mono text-[8px] font-bold text-[#09090A]"
                      >ЗАПИСАТЬСЯ</span>
                    </div>
                    <div class="grid grid-cols-3 gap-1.5 p-2">
                      <span
                        v-for="i in 3"
                        :key="i"
                        class="flex h-8 flex-col justify-center gap-1 rounded-sm bg-white/[0.05] px-1.5"
                      >
                        <span class="h-1 w-2/3 rounded-full bg-[#8E751D]/70" />
                        <span class="h-1 w-full rounded-full bg-white/10" />
                      </span>
                    </div>
                  </div>
                </div>

                <!-- 5. Экран Telegram Mini App «Штаб» -->
                <div
                  v-else-if="project.mock === 'miniapp'"
                  class="flex h-full items-center justify-center bg-[#0D0D10]"
                >
                  <div
                    class="flex h-[92%] w-24 flex-col overflow-hidden rounded-xl border border-white/10 bg-[#141417]"
                  >
                    <div class="flex items-center justify-between bg-[#1C1C21] px-2 py-1.5">
                      <span class="h-1.5 w-8 rounded bg-[#FCD116]/80" />
                      <span class="h-1.5 w-3 rounded bg-white/20" />
                    </div>
                    <div class="flex flex-1 flex-col gap-1.5 p-2">
                      <span class="h-1.5 w-14 rounded bg-white/25" />
                      <div class="h-1.5 overflow-hidden rounded-full bg-white/10">
                        <span class="block h-full w-[70%] rounded-full bg-[#FCD116]" />
                      </div>
                      <div class="flex gap-1">
                        <span
                          v-for="i in 5"
                          :key="i"
                          class="h-2 w-2 rounded-full"
                          :class="i <= 3 ? 'bg-[#FCD116]' : 'bg-white/10'"
                        />
                      </div>
                      <span
                        class="mt-auto rounded-md bg-[#FCD116] py-1 text-center font-mono text-[8px] font-bold text-[#09090A]"
                      >ТРЕНИРОВКА</span>
                      <span
                        class="rounded-md border border-[#8E751D]/60 py-1 text-center font-mono text-[8px] text-[#C9B45C]"
                      >ДНЕВНИК</span>
                    </div>
                  </div>
                </div>

                <!-- 6. Сетевой граф VPN-инфраструктуры -->
                <svg
                  v-else
                  class="h-full w-full bg-[#0D0D10]"
                  viewBox="0 0 320 176"
                  fill="none"
                  preserveAspectRatio="xMidYMid meet"
                >
                  <circle
                    cx="160"
                    cy="88"
                    r="58"
                    stroke="#8E751D"
                    stroke-opacity="0.35"
                    stroke-dasharray="4 6"
                  />
                  <line
                    v-for="(n, i) in vpnNodes.slice(1)"
                    :key="`vl-${i}`"
                    x1="160"
                    y1="88"
                    :x2="n.x"
                    :y2="n.y"
                    class="mock-wire mock-flicker"
                    :style="{ animationDelay: `${n.d}s` }"
                  />
                  <circle
                    v-for="(n, i) in vpnNodes"
                    :key="`vn-${i}`"
                    :cx="n.x"
                    :cy="n.y"
                    :r="n.r"
                    :class="i === 0 ? 'mock-hub mock-flicker' : 'mock-node-round mock-flicker'"
                    :style="{ animationDelay: `${n.d}s`, animationDuration: `${n.dur}s` }"
                  />
                </svg>
              </div>

              <!-- Бейдж статуса -->
              <span
                class="absolute left-3 top-3 z-10 rounded-full px-2.5 py-1 font-mono text-[10px] font-semibold"
                :class="statusMeta[project.status].cls"
              >
                {{ statusMeta[project.status].label }}
              </span>
            </div>

            <!-- Тело карточки -->
            <div class="flex flex-1 flex-col p-5">
              <h3
                class="font-display text-base font-bold leading-snug text-ink-800 transition-colors group-hover:text-gold dark:text-white dark:group-hover:text-primary"
              >
                {{ project.title }}
              </h3>
              <p class="mt-2 flex-1 text-[13px] leading-relaxed text-ink-100 dark:text-ink-300">
                {{ project.description }}
              </p>

              <!-- Теги стека -->
              <ul class="mt-4 flex flex-wrap gap-1.5" aria-label="Стек технологий">
                <li
                  v-for="tech in project.stack"
                  :key="tech"
                  class="rounded-md border border-gold/30 bg-gold/5 px-2 py-0.5 font-mono text-[11px] font-medium text-gold dark:border-primary/25 dark:bg-primary/10 dark:text-primary"
                >
                  {{ tech }}
                </li>
              </ul>

              <p class="mt-4 font-mono text-[11px] tracking-wider text-ink-50 dark:text-ink-300">
                // кейс по запросу
              </p>
            </div>
          </article>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* Общие элементы SVG-моков (тёмный экран #0D0D10 в обеих темах) */
.mock-wire {
  stroke: rgb(252 209 22 / 0.3);
  stroke-width: 1;
}

.mock-hub {
  fill: #fcd116;
  filter: drop-shadow(0 0 6px rgb(252 209 22 / 0.6));
}

.mock-hub-ring {
  stroke: rgb(252 209 22 / 0.35);
  stroke-width: 1;
  fill: none;
}

.mock-node {
  fill: rgb(252 209 22 / 0.85);
}

.mock-node-round {
  fill: #fcd116;
  filter: drop-shadow(0 0 5px rgb(252 209 22 / 0.5));
}

.mock-leaf {
  fill: rgb(255 245 184 / 0.7);
}

.mock-flicker {
  animation: mock-flicker 3.2s ease-in-out infinite;
}

@keyframes mock-flicker {
  0%,
  100% {
    opacity: 0.35;
  }
  50% {
    opacity: 1;
  }
}
</style>
