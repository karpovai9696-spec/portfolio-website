import { onBeforeUnmount, onMounted, ref, type Ref } from 'vue'

/**
 * Лёгкий scroll-параллакс: элемент смещается по Y пропорционально
 * удалению от центра viewport. Только transform, без layout thrashing.
 *
 * @param speed — коэффициент смещения (0.04–0.1 — аккуратный параллакс)
 */
export function useParallax<T extends HTMLElement = HTMLElement>(speed = 0.06): {
  target: Ref<T | null>
} {
  const target = ref(null) as Ref<T | null>

  let raf = 0

  const update = () => {
    raf = 0
    const el = target.value
    if (!el) return
    const rect = el.getBoundingClientRect()
    const delta = rect.top + rect.height / 2 - window.innerHeight / 2
    el.style.transform = `translate3d(0, ${(-delta * speed).toFixed(1)}px, 0)`
  }

  const onScroll = () => {
    if (!raf) raf = requestAnimationFrame(update)
  }

  onMounted(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    window.addEventListener('scroll', onScroll, { passive: true })
    update()
  })

  onBeforeUnmount(() => {
    window.removeEventListener('scroll', onScroll)
    cancelAnimationFrame(raf)
  })

  return { target }
}
