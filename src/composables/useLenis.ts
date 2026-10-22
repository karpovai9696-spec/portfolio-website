/**
 * Инертный скролл на Lenis (динамический импорт — отдельный чанк).
 *
 * - Lenis работает всегда (prefers-reduced-motion намеренно игнорируется —
 *   владелец сайта хочет полную анимацию независимо от системной настройки).
 * - Lenis прокручивает window, поэтому scroll-события, scrollspy
 *   и прогресс-бар продолжают работать без изменений.
 */
import type Lenis from 'lenis'

let instance: Lenis | null = null
let rafId = 0

/** Создать singleton Lenis. Вызывается один раз из App.vue. */
export async function createLenis(): Promise<Lenis | null> {
  if (instance) return instance
  if (typeof window === 'undefined') return null

  const { default: Lenis } = await import('lenis')
  instance = new Lenis({
    duration: 1.15,
    easing: (t: number) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    smoothWheel: true,
  })

  const loop = (time: number) => {
    instance?.raf(time)
    rafId = requestAnimationFrame(loop)
  }
  rafId = requestAnimationFrame(loop)

  return instance
}

/**
 * Плавный скролл к якорю ('#about') или позиции (0).
 * Без Lenis (например, до его инициализации) — нативный fallback.
 */
export function scrollToTarget(target: string | number) {
  if (instance) {
    instance.scrollTo(target, {
      offset: typeof target === 'string' ? -80 : 0,
      duration: 1.2,
    })
    return
  }
  if (typeof target === 'number') {
    window.scrollTo({ top: target, behavior: 'smooth' })
  } else {
    document.querySelector(target)?.scrollIntoView({ behavior: 'smooth' })
  }
}

export function destroyLenis() {
  cancelAnimationFrame(rafId)
  rafId = 0
  instance?.destroy()
  instance = null
}
