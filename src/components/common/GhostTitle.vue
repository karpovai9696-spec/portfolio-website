<script setup lang="ts">
import { useParallax } from '@/composables/useParallax'

/**
 * Огромный полупрозрачный outlined-текст на фоне секции
 * с лёгким параллаксом при скролле (только transform).
 */
defineProps<{
  text: string
}>()

const { target } = useParallax<HTMLDivElement>(0.07)
</script>

<template>
  <div
    ref="target"
    class="ghost-title"
    aria-hidden="true"
  >
    {{ text }}
  </div>
</template>
