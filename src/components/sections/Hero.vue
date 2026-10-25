<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { ArrowRight, Download } from 'lucide-vue-next'

import Button from '@/components/common/Button.vue'
import HeroTerminal from '@/components/common/HeroTerminal.vue'
import NetworkGraph from '@/components/common/NetworkGraph.vue'
import ParticleField from '@/components/common/ParticleField.vue'
import { scrollToTarget } from '@/composables/useLenis'
import { usePortfolioStore } from '@/stores/portfolio'

const store = usePortfolioStore()
const { person } = store

/* ---------- Кинетическая типографика: имя по буквам ----------
   Буквы сгруппированы по словам (whitespace-nowrap), перенос
   возможен только между словами. Первое слово — жёлтое. */
const nameWords = computed(() =>
  person.name.toUpperCase().split(' ').map((word) => word.split('')),
)
const lettersIn = ref(false)

/** Сквозной индекс буквы для каскадной задержки */
function letterIndex(wordIndex: number, charIndex: number): number {
  let offset = 0
  for (let w = 0; w < wordIndex; w++) offset += nameWords.value[w].length
  return offset + charIndex
}

/* ---------- Теги специализации ---------- */
const tags = ['Node.js', 'Go', 'Python', 'API', 'Cryptography', 'React', 'Docker']

let timer: ReturnType<typeof setTimeout> | null = null
let cancelled = false

function schedule(fn: () => void, delay: number) {
  timer = setTimeout(() => {
    if (!cancelled) fn()
  }, delay)
}

onMounted(() => {
  schedule(() => (lettersIn.value = true), 120)
})

onBeforeUnmount(() => {
  cancelled = true
  if (timer) clearTimeout(timer)
})

function scrollToProjects() {
  scrollToTarget('#portfolio')
}
</script>

<template>
  <section
    id="hero"
    class="relative flex min-h-screen flex-col overflow-hidden"
    aria-label="Приветствие"
  >
    <!-- Фон: тонкая сетка + жёлтое свечение (обе темы) -->
    <div class="pointer-events-none absolute inset-0" aria-hidden="true">
      <div class="bg-grid absolute inset-0" />
      <div
        class="absolute -right-40 top-1/4 h-[30rem] w-[30rem] rounded-full bg-primary/[0.07] blur-3xl dark:bg-primary/[0.1]"
      />
      <div
        class="absolute -left-40 bottom-0 h-[26rem] w-[26rem] rounded-full bg-gold/[0.06] blur-3xl dark:bg-gold/[0.1]"
      />
    </div>

    <!-- WebGL-поле частиц (только тёмная тема; под контентом) -->
    <ParticleField />

    <!-- Контент: две колонки -->
    <div
      class="section-container relative z-10 grid flex-1 items-center gap-12 pb-16 pt-28 sm:pt-32 lg:grid-cols-12 lg:gap-8"
    >
      <!-- Левая колонка: идентификация -->
      <div class="lg:col-span-7">
        <p
          class="animate-fade-in-up font-mono text-xs tracking-[0.25em] text-ink-100 [animation-delay:80ms] dark:text-ink-300 sm:text-sm"
        >
          // системный инженер · казань
        </p>

        <h1
          class="mt-5 font-display text-[clamp(2.5rem,7vw,3.5rem)] font-extrabold leading-[1.05] tracking-tight"
          :class="{ 'letters-in': lettersIn }"
          :aria-label="person.name"
        >
          <span class="block whitespace-nowrap" aria-hidden="true">
            <span
              v-for="(letter, i) in nameWords[0]"
              :key="`w0-${i}`"
              class="kinetic-mask"
            ><span
                class="kinetic-letter text-gold dark:text-primary"
                :style="{ '--letter-index': letterIndex(0, i) }"
              >{{ letter }}</span></span>
          </span>
          <span class="block whitespace-nowrap" aria-hidden="true">
            <span
              v-for="(letter, i) in nameWords[1]"
              :key="`w1-${i}`"
              class="kinetic-mask"
            ><span
                class="kinetic-letter text-ink-800 dark:text-white"
                :style="{ '--letter-index': letterIndex(1, i) }"
              >{{ letter }}</span></span>
          </span>
        </h1>

        <p
          class="mt-5 animate-fade-in-up font-mono text-sm font-semibold uppercase tracking-widest text-gold [animation-delay:600ms]"
        >
          Full-Stack разработчик / Системный инженер
        </p>

        <p
          class="mt-5 max-w-[520px] animate-fade-in-up text-base leading-relaxed text-ink-700 [animation-delay:700ms] dark:text-[#FFF5B8]/80"
        >
          Создаю сложные веб-системы, интеграции и высоконагруженные сервисы.
          Специализируюсь на автоматизации, криптографии и работе с государственными
          системами (МДЛП/ГИС).
        </p>

        <div
          class="mt-8 flex animate-fade-in-up flex-col gap-3 [animation-delay:800ms] sm:flex-row sm:flex-wrap"
        >
          <Button
            size="md"
            magnetic
            class="w-full sm:w-auto"
            aria-label="Посмотреть проекты — перейти к портфолио"
            @click="scrollToProjects"
          >
            <ArrowRight class="h-5 w-5" aria-hidden="true" />
            Посмотреть проекты
          </Button>
          <Button
            size="md"
            variant="outline"
            magnetic
            class="w-full sm:w-auto"
            :href="person.resume"
            download
            aria-label="Скачать резюме в формате PDF"
          >
            <Download class="h-5 w-5" aria-hidden="true" />
            Скачать резюме
          </Button>
        </div>

        <!-- Теги стека -->
        <ul
          class="mt-8 flex animate-fade-in-up flex-wrap gap-2 [animation-delay:900ms]"
          aria-label="Ключевые технологии"
        >
          <li
            v-for="tag in tags"
            :key="tag"
            class="rounded-md border border-gold/30 bg-paper-raised px-3 py-1.5 font-mono text-xs font-medium text-ink-700 transition-colors hover:border-gold/60 dark:border-gold/30 dark:bg-ink-900 dark:text-[#FFF5B8]/90 dark:hover:border-primary/50"
          >
            {{ tag }}
          </li>
        </ul>
      </div>

      <!-- Правая колонка: терминал + сетевой граф -->
      <div class="relative animate-fade-in-up [animation-delay:500ms] lg:col-span-5">
        <div
          class="pointer-events-none absolute -inset-10 opacity-70 sm:-inset-14"
          aria-hidden="true"
        >
          <NetworkGraph />
        </div>
        <div class="relative">
          <HeroTerminal />
        </div>
      </div>
    </div>
  </section>
</template>
