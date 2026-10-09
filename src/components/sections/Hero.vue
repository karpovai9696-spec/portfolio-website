<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { Download, Mail, MessageCircle, Phone, Send } from 'lucide-vue-next'

import Button from '@/components/common/Button.vue'
import ParticleField from '@/components/common/ParticleField.vue'
import { scrollToTarget } from '@/composables/useLenis'
import { usePortfolioStore } from '@/stores/portfolio'

const store = usePortfolioStore()
const { person } = store

/* ---------- Кинетическая типографика: имя по буквам ----------
   Баг-фикс: буквы сгруппированы по СЛОВАМ, каждое слово —
   whitespace-nowrap обёртка, перенос строки возможен только
   между словами (а здесь слова вообще идут отдельными строками). */
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

/* ---------- Видео-фон Hero ----------
   - save-data → только poster (без autoplay);
   - светлая тема → видео скрыто и поставлено на паузу (остаётся aurora);
   - фон спокойный (без вспышек), поэтому играет и при prefers-reduced-motion —
     это осознанное решение владельца сайта-портфолио. */
const videoEl = ref<HTMLVideoElement | null>(null)
const isDarkTheme = ref(true)
const baseUrl = import.meta.env.BASE_URL
const saveData =
  typeof navigator !== 'undefined' &&
  Boolean((navigator as Navigator & { connection?: { saveData?: boolean } }).connection?.saveData)
const videoEnabled = !saveData

let themeObserver: MutationObserver | null = null

/* ---------- Эффект печатающегося текста ---------- */
const phrases = ['Лендинги', 'Веб-приложения', 'Интернет-магазины', 'SPA на Vue/React']
const typed = ref('')

let timer: ReturnType<typeof setTimeout> | null = null
let cancelled = false

function schedule(fn: () => void, delay: number) {
  timer = setTimeout(() => {
    if (!cancelled) fn()
  }, delay)
}

function typeLoop(phraseIndex: number, charIndex: number, deleting: boolean) {
  const phrase = phrases[phraseIndex]
  if (!deleting) {
    typed.value = phrase.slice(0, charIndex + 1)
    if (charIndex + 1 === phrase.length) {
      schedule(() => typeLoop(phraseIndex, phrase.length, true), 1900)
    } else {
      schedule(() => typeLoop(phraseIndex, charIndex + 1, false), 65 + Math.random() * 55)
    }
  } else {
    typed.value = phrase.slice(0, charIndex - 1)
    if (charIndex - 1 <= 0) {
      schedule(() => typeLoop((phraseIndex + 1) % phrases.length, 0, false), 400)
    } else {
      schedule(() => typeLoop(phraseIndex, charIndex - 1, true), 32)
    }
  }
}

onMounted(() => {
  const reduced = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false

  // Каскадный reveal имени по буквам
  if (reduced) lettersIn.value = true
  else schedule(() => (lettersIn.value = true), 120)

  // Видео-фон: пауза/возобновление при переключении темы
  isDarkTheme.value = document.documentElement.classList.contains('dark')
  themeObserver = new MutationObserver(() => {
    isDarkTheme.value = document.documentElement.classList.contains('dark')
    if (!videoEl.value || !videoEnabled) return
    if (isDarkTheme.value) {
      void videoEl.value.play().catch(() => {
        /* autoplay заблокирован — остаётся poster */
      })
    } else {
      videoEl.value.pause()
    }
  })
  themeObserver.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['class'],
  })

  if (reduced) {
    typed.value = phrases[1]
    return
  }
  schedule(() => typeLoop(0, 0, false), 900)
})

onBeforeUnmount(() => {
  cancelled = true
  if (timer) clearTimeout(timer)
  themeObserver?.disconnect()
  themeObserver = null
})

function scrollToContact() {
  scrollToTarget('#contact')
}
</script>

<template>
  <section
    id="hero"
    class="relative flex min-h-screen flex-col overflow-hidden"
    aria-label="Приветствие"
  >
    <!-- Видео-фон: зацикленные световые ленты (самый нижний слой сцены, только тёмная тема) -->
    <video
      v-if="videoEnabled"
      v-show="isDarkTheme"
      ref="videoEl"
      class="absolute inset-0 h-full w-full object-cover"
      autoplay
      muted
      loop
      playsinline
      preload="metadata"
      :poster="`${baseUrl}videos/hero-poster.jpg`"
      aria-hidden="true"
    >
      <source :src="`${baseUrl}videos/hero-bg.mp4`" type="video/mp4" />
    </video>
    <img
      v-else-if="isDarkTheme"
      :src="`${baseUrl}videos/hero-poster.jpg`"
      alt=""
      class="absolute inset-0 h-full w-full object-cover"
      aria-hidden="true"
    />

    <!-- Анимированный aurora / gradient-mesh фон (в тёмной теме приглушён — видео уже даёт свечение) -->
    <div class="pointer-events-none absolute inset-0" aria-hidden="true">
      <div class="bg-grid absolute inset-0" />
      <div
        class="absolute -left-32 top-1/4 h-[26rem] w-[26rem] animate-aurora rounded-full bg-primary/25 blur-3xl dark:bg-primary/10"
      />
      <div
        class="absolute -right-32 top-1/2 h-[30rem] w-[30rem] animate-aurora-reverse rounded-full bg-accent/25 blur-3xl dark:bg-accent/10"
      />
      <div
        class="absolute bottom-0 left-1/3 h-80 w-80 animate-aurora rounded-full bg-sky-400/20 blur-3xl [animation-delay:-6s] dark:bg-sky-500/[0.07]"
      />
      <div
        class="absolute right-1/4 top-10 h-64 w-64 animate-aurora-reverse rounded-full bg-fuchsia-400/15 blur-3xl [animation-delay:-11s] dark:bg-fuchsia-500/[0.06]"
      />
    </div>

    <!-- Затемняющий оверлей поверх видео (только тёмная тема): общее затемнение + градиент книзу -->
    <div
      v-show="isDarkTheme"
      class="pointer-events-none absolute inset-0"
      aria-hidden="true"
    >
      <div class="absolute inset-0 bg-ink-950/45" />
      <div class="absolute inset-0 bg-gradient-to-b from-ink-950/30 via-ink-950/40 to-ink-950" />
    </div>

    <!-- WebGL-поле частиц (только тёмная тема; поверх aurora, под контентом) -->
    <ParticleField />

    <!-- Editorial-контент во всю ширину -->
    <div class="relative z-10 flex min-h-screen flex-col px-[5vw] pb-6 pt-24 sm:pt-28">
      <!-- Верхняя строка: приветствие слева, meta-блок справа -->
      <div class="flex items-start justify-between gap-6">
        <p
          class="animate-fade-in-up font-mono text-xs tracking-[0.25em] text-slate-500 [animation-delay:80ms] dark:text-slate-400 sm:text-sm"
        >
          Привет, меня зовут
        </p>

        <div
          class="animate-fade-in-up text-right font-mono text-[11px] leading-relaxed tracking-wider text-slate-500 [animation-delay:200ms] dark:text-slate-400 sm:text-xs"
        >
          <p class="font-semibold text-slate-700 dark:text-slate-200">FULL STACK DEVELOPER</p>
          <p class="mt-1">Казань, Россия</p>
          <p class="mt-1 inline-flex items-center justify-end gap-2">
            <span class="relative flex h-1.5 w-1.5" aria-hidden="true">
              <span
                class="absolute inline-flex h-full w-full animate-ping rounded-full bg-green-400 opacity-75"
              />
              <span class="relative inline-flex h-1.5 w-1.5 rounded-full bg-green-500" />
            </span>
            открыт для новых проектов
          </p>
        </div>
      </div>

      <!-- Имя стэком: два слова — две строки, левый край -->
      <h1
        class="mt-8 text-[clamp(3.5rem,16.5vw,15rem)] font-extrabold leading-[0.9] tracking-[-0.02em] sm:mt-12"
        :class="{ 'letters-in': lettersIn }"
        :aria-label="person.name"
      >
        <span class="block whitespace-nowrap" aria-hidden="true">
          <span
            v-for="(letter, i) in nameWords[0]"
            :key="`w0-${i}`"
            class="kinetic-mask"
          ><span
              class="kinetic-letter text-gradient"
              :style="{ '--letter-index': letterIndex(0, i) }"
            >{{ letter }}</span></span>
        </span>
        <span class="block whitespace-nowrap" aria-hidden="true">
          <span
            v-for="(letter, i) in nameWords[1]"
            :key="`w1-${i}`"
            class="kinetic-mask"
          ><span
              class="kinetic-letter hero-outline"
              :style="{ '--letter-index': letterIndex(1, i) }"
            >{{ letter }}</span></span>
        </span>
      </h1>

      <!-- Печатающийся текст рядом со второй строкой -->
      <p
        class="mt-5 flex h-8 animate-fade-in-up items-center font-mono text-base [animation-delay:650ms] sm:text-lg"
        aria-label="Что я делаю: лендинги, веб-приложения, интернет-магазины, SPA на Vue и React"
      >
        <span class="mr-2 text-slate-400 dark:text-slate-500" aria-hidden="true">&gt;</span>
        <span class="text-gradient font-semibold" aria-hidden="true">{{ typed }}</span>
        <span
          class="ml-0.5 inline-block h-5 w-[2px] animate-blink bg-gradient-to-b from-primary to-accent"
          aria-hidden="true"
        />
      </p>

      <!-- Нижняя часть: описание + кнопки слева, scroll-индикатор справа -->
      <div
        class="mt-auto flex flex-col gap-8 pt-12 lg:flex-row lg:items-end lg:justify-between"
      >
        <div class="max-w-[420px]">
          <p
            class="animate-fade-in-up text-sm leading-relaxed text-slate-500 [animation-delay:750ms] dark:text-slate-400 sm:text-base"
          >
            {{ person.tagline }}
          </p>

          <div
            class="mt-6 flex animate-fade-in-up flex-col gap-3 [animation-delay:850ms] sm:flex-row sm:flex-wrap"
          >
            <Button
              size="md"
              magnetic
              class="w-full sm:w-auto"
              aria-label="Перейти к форме связи"
              @click="scrollToContact"
            >
              <MessageCircle class="h-5 w-5" aria-hidden="true" />
              Связаться
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

          <!-- Соцссылки -->
          <div
            class="mt-6 flex animate-fade-in-up items-center gap-3 [animation-delay:950ms]"
          >
            <a
              :href="person.telegram"
              target="_blank"
              rel="noopener noreferrer"
              class="glass rounded-xl p-2.5 text-slate-500 transition-all duration-300 hover:-translate-y-1 hover:shadow-lg hover:shadow-primary/20 hover:text-primary dark:text-slate-400"
              aria-label="Написать в Telegram"
            >
              <Send class="h-5 w-5" aria-hidden="true" />
            </a>
            <a
              :href="`mailto:${person.email}`"
              class="glass rounded-xl p-2.5 text-slate-500 transition-all duration-300 hover:-translate-y-1 hover:shadow-lg hover:shadow-primary/20 hover:text-primary dark:text-slate-400"
              aria-label="Написать на email"
            >
              <Mail class="h-5 w-5" aria-hidden="true" />
            </a>
            <a
              :href="person.phoneHref"
              class="glass rounded-xl p-2.5 text-slate-500 transition-all duration-300 hover:-translate-y-1 hover:shadow-lg hover:shadow-primary/20 hover:text-primary dark:text-slate-400"
              aria-label="Позвонить"
            >
              <Phone class="h-5 w-5" aria-hidden="true" />
            </a>
          </div>
        </div>

        <!-- Scroll-индикатор справа -->
        <div
          class="hidden animate-fade-in-up items-center gap-3 font-mono text-[11px] tracking-[0.25em] text-slate-400 [animation-delay:1050ms] dark:text-slate-500 lg:flex"
          aria-hidden="true"
        >
          <span class="[writing-mode:vertical-rl]">SCROLL</span>
          <span
            class="flex h-10 w-6 items-start justify-center rounded-full border-2 border-slate-400/50 p-1.5 dark:border-slate-500/50"
          >
            <span
              class="h-2 w-1 animate-scroll-dot rounded-full bg-gradient-to-b from-primary to-accent"
            />
          </span>
        </div>
      </div>

      <!-- Нижняя кромка: тонкая линия + mono-мелочь -->
      <div
        class="mt-6 flex animate-fade-in-up items-center justify-between border-t border-slate-200/70 pt-4 font-mono text-[11px] tracking-wider text-slate-400 [animation-delay:1100ms] dark:border-white/10 dark:text-slate-500"
      >
        <span>©2026 — v2.0</span>
        <span class="hidden sm:inline">55.7887° N, 49.1221° E — KAZAN</span>
      </div>
    </div>
  </section>
</template>
