<script setup lang="ts">
/**
 * Личный знак «К + курсор» (вариант А, итерация 2) — векторная геометрия
 * viewBox 128×104. По умолчанию жёлтый/золото (cyber-система).
 */
withDefaults(
  defineProps<{
    sign?: string
    cursor?: string
    clazz?: string
  }>(),
  {
    sign: '#FCD116',
    cursor: '#8E751D',
    clazz: 'h-9 w-auto',
  },
)
</script>

<template>
  <svg :class="clazz" viewBox="0 0 128 104" fill="none" aria-hidden="true">
    <rect x="6" y="10" width="18" height="88" :fill="sign" />
    <polygon points="19.61,44.10 28.39,59.86 96.39,21.86 87.61,6.10" :fill="sign" />
    <polygon points="19.61,59.86 28.39,44.10 96.39,96.10 87.61,81.90" :fill="sign" />
    <polygon points="107,78 119,90 107,102 95,90" :fill="cursor" />
  </svg>
</template>
