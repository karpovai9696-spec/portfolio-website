import { onBeforeUnmount, onMounted, ref, type Ref } from 'vue'

/**
 * Возвращает true, когда устройство имеет точный указатель (мышь/трекпад)
 * и пользователь НЕ просил уменьшить анимации (prefers-reduced-motion).
 *
 * Используется для включения «тяжёлых» pointer-эффектов:
 * cursor-glow, magnetic buttons, 3D-tilt. На тач-устройствах и при
 * reduced-motion эффекты отключаются.
 */
export function usePointerFine(): Ref<boolean> {
  const enabled = ref(false)

  let mqPointer: MediaQueryList | null = null
  let mqMotion: MediaQueryList | null = null

  const update = () => {
    enabled.value = Boolean(mqPointer?.matches && mqMotion && !mqMotion.matches)
  }

  onMounted(() => {
    mqPointer = window.matchMedia('(pointer: fine)')
    mqMotion = window.matchMedia('(prefers-reduced-motion: reduce)')
    update()
    mqPointer.addEventListener('change', update)
    mqMotion.addEventListener('change', update)
  })

  onBeforeUnmount(() => {
    mqPointer?.removeEventListener('change', update)
    mqMotion?.removeEventListener('change', update)
  })

  return enabled
}
