import { onBeforeUnmount, onMounted, ref, type Ref } from 'vue'

/**
 * Возвращает true, когда устройство имеет точный указатель (мышь/трекпад).
 *
 * Используется для включения «тяжёлых» pointer-эффектов:
 * cursor-glow, magnetic buttons, 3D-tilt. На тач-устройствах эффекты
 * отключаются (гейт ТОЛЬКО по указателю; настройка prefers-reduced-motion
 * намеренно игнорируется — владелец сайта хочет полную анимацию всегда).
 */
export function usePointerFine(): Ref<boolean> {
  const enabled = ref(false)

  let mqPointer: MediaQueryList | null = null

  const update = () => {
    enabled.value = Boolean(mqPointer?.matches)
  }

  onMounted(() => {
    mqPointer = window.matchMedia('(pointer: fine)')
    update()
    mqPointer.addEventListener('change', update)
  })

  onBeforeUnmount(() => {
    mqPointer?.removeEventListener('change', update)
  })

  return enabled
}
