<script setup lang="ts">
import { computed, ref } from 'vue'

import { usePointerFine } from '@/composables/usePointerFine'

const props = withDefaults(
  defineProps<{
    hover?: boolean
    padding?: boolean
    /** 3D-наклон карточки за курсором (только fine pointer) */
    tilt?: boolean
    /** Световое пятно, следующее за курсором внутри карточки */
    spotlight?: boolean
  }>(),
  {
    hover: true,
    padding: true,
    tilt: false,
    spotlight: false,
  },
)

const pointerFine = usePointerFine()
const el = ref<HTMLElement | null>(null)

const interactive = computed(() => (props.tilt || props.spotlight) && pointerFine.value)

function onPointerMove(event: PointerEvent) {
  if (!interactive.value || !el.value) return
  const rect = el.value.getBoundingClientRect()
  const px = (event.clientX - rect.left) / rect.width
  const py = (event.clientY - rect.top) / rect.height

  // CSS-переменные для spotlight
  el.value.style.setProperty('--mx', `${(px * 100).toFixed(1)}%`)
  el.value.style.setProperty('--my', `${(py * 100).toFixed(1)}%`)

  // 3D-tilt: только transform
  if (props.tilt) {
    const max = 7
    const rx = ((0.5 - py) * max).toFixed(2)
    const ry = ((px - 0.5) * max).toFixed(2)
    el.value.style.transform = `perspective(900px) rotateX(${rx}deg) rotateY(${ry}deg) translateY(-4px)`
  }
}

function onPointerLeave() {
  if (!el.value) return
  el.value.style.transform = ''
}
</script>

<template>
  <div
    ref="el"
    class="glass relative rounded-2xl transition-shadow duration-300"
    :class="[
      padding ? 'p-6' : '',
      hover ? 'hover:-translate-y-1 hover:shadow-xl hover:shadow-primary/10' : '',
      tilt ? 'tilt-card will-change-transform' : '',
      spotlight ? 'overflow-hidden' : '',
    ]"
    :style="{ transitionProperty: 'box-shadow, transform', transitionTimingFunction: 'cubic-bezier(0.22, 1, 0.36, 1)' }"
    @pointermove="onPointerMove"
    @pointerleave="onPointerLeave"
  >
    <div v-if="spotlight" class="spotlight-overlay" aria-hidden="true" />
    <slot />
  </div>
</template>
