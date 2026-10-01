import { onBeforeUnmount, onMounted, ref, type CSSProperties, type Ref } from 'vue'

/**
 * Composable для анимации появления элементов при скролле.
 *
 * Использование:
 *   const { target, isVisible } = useScrollAnimation()
 *   <div ref="target" class="reveal">...</div>
 *
 * Элемент получает класс `is-visible`, когда попадает в область видимости,
 * после чего CSS-переходы проигрывают анимацию. Поддерживаются варианты
 * направления: .reveal (снизу), .reveal-left, .reveal-right, .reveal-scale.
 */
export function useScrollAnimation<T extends HTMLElement = HTMLElement>(options?: {
  threshold?: number
  rootMargin?: string
  once?: boolean
}): { target: Ref<T | null>; isVisible: Ref<boolean> } {
  const target = ref(null) as Ref<T | null>
  const isVisible = ref(false)
  const { threshold = 0.15, rootMargin = '0px 0px -40px 0px', once = true } = options ?? {}

  let observer: IntersectionObserver | null = null

  onMounted(() => {
    if (!target.value || typeof IntersectionObserver === 'undefined') {
      target.value?.classList.add('is-visible')
      isVisible.value = true
      return
    }

    observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible')
            isVisible.value = true
            if (once) observer?.unobserve(entry.target)
          } else if (!once) {
            entry.target.classList.remove('is-visible')
            isVisible.value = false
          }
        }
      },
      { threshold, rootMargin },
    )

    observer.observe(target.value)
  })

  onBeforeUnmount(() => {
    observer?.disconnect()
    observer = null
  })

  return { target, isVisible }
}

/**
 * Inline-стиль с задержкой для staggered-появления элементов списка.
 * Применяется к элементам с классами reveal-* :style="staggerStyle(index)"
 */
export function staggerStyle(index: number, step = 90, base = 0): CSSProperties {
  return { '--reveal-delay': `${base + index * step}ms` } as CSSProperties
}
