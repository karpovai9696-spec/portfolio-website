<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'

import { usePointerFine } from '@/composables/usePointerFine'

/**
 * Мягкое световое пятно, следующее за курсором.
 * Рендерится только на устройствах с точным указателем
 * и отключено при prefers-reduced-motion (см. usePointerFine + CSS).
 */
const pointerFine = usePointerFine()
const glow = ref<HTMLElement | null>(null)

let raf = 0
let targetX = -1000
let targetY = -1000
let currentX = -1000
let currentY = -1000

function onPointerMove(event: PointerEvent) {
  targetX = event.clientX
  targetY = event.clientY
}

/** Плавное следование с линейной интерполяцией (только transform) */
function tick() {
  currentX += (targetX - currentX) * 0.12
  currentY += (targetY - currentY) * 0.12
  if (glow.value) {
    glow.value.style.transform = `translate3d(${currentX - 260}px, ${currentY - 260}px, 0)`
  }
  raf = requestAnimationFrame(tick)
}

watch(pointerFine, (enabled) => {
  if (enabled) {
    window.addEventListener('pointermove', onPointerMove, { passive: true })
    raf = requestAnimationFrame(tick)
  } else {
    window.removeEventListener('pointermove', onPointerMove)
    cancelAnimationFrame(raf)
  }
})

onMounted(() => {
  if (pointerFine.value) {
    window.addEventListener('pointermove', onPointerMove, { passive: true })
    raf = requestAnimationFrame(tick)
  }
})

onBeforeUnmount(() => {
  window.removeEventListener('pointermove', onPointerMove)
  cancelAnimationFrame(raf)
})
</script>

<template>
  <div v-if="pointerFine" ref="glow" class="cursor-glow" aria-hidden="true" />
</template>
