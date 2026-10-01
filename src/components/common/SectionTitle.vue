<script setup lang="ts">
import { computed } from 'vue'

import { useScrollAnimation } from '@/composables/useScrollAnimation'

const props = defineProps<{
  title: string
  subtitle?: string
  /** Номер секции для mono-плашки, например "01" */
  index?: string
  /** Метка секции для mono-плашки, например "услуги" */
  tag?: string
}>()

/** Разбиваем заголовок на слова для reveal с маской */
const words = computed(() => props.title.split(' '))

const { target } = useScrollAnimation<HTMLDivElement>()
</script>

<template>
  <div ref="target" class="reveal mb-12 text-center sm:mb-16">
    <span v-if="index && tag" class="section-badge" aria-hidden="true">
      <span class="text-accent">//</span> {{ index }} — {{ tag }}
    </span>
    <h2 class="mt-4 text-3xl font-bold tracking-tight sm:text-4xl lg:text-5xl">
      <span
        v-for="(word, i) in words"
        :key="`${word}-${i}`"
        class="word-mask"
      ><span class="word-inner text-gradient" :style="{ '--word-index': i }">{{ word }}</span><span v-if="i < words.length - 1" aria-hidden="true">&nbsp;</span></span>
    </h2>
    <p
      v-if="subtitle"
      class="mx-auto mt-4 max-w-2xl text-base text-slate-500 dark:text-slate-400 sm:text-lg"
    >
      {{ subtitle }}
    </p>
    <div
      class="section-underline mx-auto mt-6 h-1 w-24 rounded-full bg-gradient-to-r from-primary to-accent"
      aria-hidden="true"
    />
  </div>
</template>
