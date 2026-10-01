<script setup lang="ts">
import { computed, ref } from 'vue'

import { usePointerFine } from '@/composables/usePointerFine'

const props = withDefaults(
  defineProps<{
    variant?: 'primary' | 'outline' | 'ghost'
    size?: 'sm' | 'md' | 'lg'
    href?: string
    type?: 'button' | 'submit'
    download?: boolean
    ariaLabel?: string
    /** Магнитный эффект: кнопка притягивается к курсору (только fine pointer) */
    magnetic?: boolean
  }>(),
  {
    variant: 'primary',
    size: 'md',
    type: 'button',
    href: undefined,
    download: false,
    ariaLabel: undefined,
    magnetic: false,
  },
)

const pointerFine = usePointerFine()
const el = ref<HTMLElement | null>(null)

const classes = computed(() => {
  const base =
    'inline-flex items-center justify-center gap-2 rounded-xl font-semibold transition-all duration-300 focus-visible:ring-2 focus-visible:ring-primary disabled:cursor-not-allowed disabled:opacity-50 will-change-transform'

  const sizes: Record<string, string> = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg',
  }

  const variants: Record<string, string> = {
    primary:
      'bg-gradient-to-r from-primary to-accent text-white shadow-lg shadow-primary/25 hover:shadow-xl hover:shadow-primary/40 hover:-translate-y-0.5',
    outline:
      'border-2 border-primary/60 text-primary hover:bg-primary/10 dark:text-primary dark:hover:bg-primary/15 hover:-translate-y-0.5',
    ghost: 'text-slate-600 hover:bg-slate-900/5 dark:text-slate-300 dark:hover:bg-white/10',
  }

  return `${base} ${sizes[props.size]} ${variants[props.variant]}`
})

/** Магнитное притяжение к курсору (только transform, без layout) */
function onPointerMove(event: PointerEvent) {
  if (!props.magnetic || !pointerFine.value || !el.value) return
  const rect = el.value.getBoundingClientRect()
  const dx = event.clientX - (rect.left + rect.width / 2)
  const dy = event.clientY - (rect.top + rect.height / 2)
  const strength = 0.28
  el.value.style.transform = `translate(${dx * strength}px, ${dy * strength}px)`
}

function onPointerLeave() {
  if (!props.magnetic || !el.value) return
  el.value.style.transform = ''
}
</script>

<template>
  <a
    v-if="href"
    ref="el"
    :href="href"
    :class="classes"
    :download="download || undefined"
    :aria-label="ariaLabel"
    @pointermove="onPointerMove"
    @pointerleave="onPointerLeave"
  >
    <slot />
  </a>
  <button
    v-else
    ref="el"
    :type="type"
    :class="classes"
    :aria-label="ariaLabel"
    @pointermove="onPointerMove"
    @pointerleave="onPointerLeave"
  >
    <slot />
  </button>
</template>
