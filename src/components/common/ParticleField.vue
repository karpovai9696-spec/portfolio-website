<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import type {
  BufferGeometry,
  PerspectiveCamera,
  Points,
  PointsMaterial,
  Scene,
  WebGLRenderer,
} from 'three'

/**
 * WebGL-фон Hero: интерактивное поле частиц с волновой деформацией.
 *
 * - Three.js подгружается динамически (отдельный чанк) после первого рендера.
 * - Частицы в сине-фиолетовом спектре (#3B82F6 → #8B5CF6), прозрачный canvas.
 * - Реакция на курсор: repel-деформация волны + parallax камеры.
 * - Пауза rAF: вкладка скрыта / Hero вне viewport / светлая тема.
 * - devicePixelRatio ≤ 2, на мобильных — уменьшенная сетка.
 * - prefers-reduced-motion: WebGL не инициализируется вообще.
 */
const canvas = ref<HTMLCanvasElement | null>(null)
const isActive = ref(false) // canvas виден (тёмная тема); управляет opacity

let dispose: (() => void) | null = null

onMounted(async () => {
  const canvasEl = canvas.value
  if (!canvasEl) return
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return

  /* ---------- Динамический импорт three (отдельный чанк) ---------- */
  const THREE = await import('three')

  const parent = canvasEl.parentElement as HTMLElement
  const isMobile = window.innerWidth < 768 || window.matchMedia('(pointer: coarse)').matches

  const renderer: WebGLRenderer = new THREE.WebGLRenderer({
    canvas: canvasEl,
    alpha: true,
    antialias: false,
    powerPreference: 'high-performance',
  })
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  renderer.setSize(parent.clientWidth, parent.clientHeight, false)

  const scene: Scene = new THREE.Scene()
  const camera: PerspectiveCamera = new THREE.PerspectiveCamera(
    55,
    parent.clientWidth / parent.clientHeight,
    0.1,
    100,
  )
  camera.position.set(0, 1.1, 7.5)
  camera.lookAt(0, -0.4, 0)

  /* ---------- Сетка частиц ---------- */
  const COLS = isMobile ? 64 : 128
  const ROWS = isMobile ? 32 : 60
  const PLANE_W = 22
  const PLANE_H = 12
  const COUNT = COLS * ROWS

  const positions = new Float32Array(COUNT * 3)
  const base = new Float32Array(COUNT * 2) // исходные x/y
  const colors = new Float32Array(COUNT * 3)

  const blue = new THREE.Color('#3B82F6')
  const violet = new THREE.Color('#8B5CF6')
  const tmpColor = new THREE.Color()

  let i = 0
  for (let row = 0; row < ROWS; row++) {
    for (let col = 0; col < COLS; col++) {
      const x = (col / (COLS - 1) - 0.5) * PLANE_W
      const y = (row / (ROWS - 1) - 0.5) * PLANE_H
      positions[i * 3] = x
      positions[i * 3 + 1] = y
      positions[i * 3 + 2] = 0
      base[i * 2] = x
      base[i * 2 + 1] = y

      // Градиент синий → фиолетовый по X с лёгкой вариацией по Y
      const mix = Math.min(1, Math.max(0, col / (COLS - 1) + (row / ROWS - 0.5) * 0.25))
      tmpColor.copy(blue).lerp(violet, mix)
      colors[i * 3] = tmpColor.r
      colors[i * 3 + 1] = tmpColor.g
      colors[i * 3 + 2] = tmpColor.b
      i++
    }
  }

  const geometry: BufferGeometry = new THREE.BufferGeometry()
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3))

  const material: PointsMaterial = new THREE.PointsMaterial({
    size: isMobile ? 0.06 : 0.085,
    vertexColors: true,
    transparent: true,
    opacity: 0.95,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
    sizeAttenuation: true,
  })

  const points: Points = new THREE.Points(geometry, material)
  points.rotation.x = -0.35 // лёгкий наклон плоскости для глубины
  scene.add(points)

  /* ---------- Курсор: repel + parallax камеры ---------- */
  let targetNX = 0
  let targetNY = 0
  let nx = 0
  let ny = 0

  const onPointerMove = (event: PointerEvent) => {
    targetNX = (event.clientX / window.innerWidth) * 2 - 1
    targetNY = -(event.clientY / window.innerHeight) * 2 + 1
  }
  window.addEventListener('pointermove', onPointerMove, { passive: true })

  /* ---------- Управление циклом: viewport / вкладка / тема ---------- */
  let rafId = 0
  let inView = true
  const isDark = () => document.documentElement.classList.contains('dark')

  const loop = (time: number) => {
    rafId = requestAnimationFrame(loop)
    const t = time * 0.001

    // Плавное следование курсора
    nx += (targetNX - nx) * 0.06
    ny += (targetNY - ny) * 0.06

    // Parallax камеры
    camera.position.x = nx * 0.7
    camera.position.y = 1.1 + ny * 0.35
    camera.lookAt(0, -0.4, 0)

    // Волна + repel-деформация
    const mx = nx * (PLANE_W / 2)
    const my = ny * (PLANE_H / 2)
    const pos = geometry.attributes.position.array as Float32Array
    for (let p = 0; p < COUNT; p++) {
      const x = base[p * 2]
      const y = base[p * 2 + 1]
      let z =
        Math.sin(x * 0.75 + t * 1.1) * 0.32 +
        Math.cos(y * 0.85 + t * 0.85) * 0.28 +
        Math.sin((x + y) * 0.4 + t * 0.5) * 0.15
      const dx = x - mx
      const dy = y - my
      const distSq = dx * dx + dy * dy
      z += Math.exp(-distSq / 3.2) * 1.1 // отталкивание от курсора
      pos[p * 3 + 2] = z
    }
    geometry.attributes.position.needsUpdate = true

    renderer.render(scene, camera)
  }

  const start = () => {
    if (!rafId) rafId = requestAnimationFrame(loop)
  }
  const stop = () => {
    cancelAnimationFrame(rafId)
    rafId = 0
  }
  const refresh = () => {
    const dark = isDark()
    isActive.value = dark
    if (inView && !document.hidden && dark) start()
    else stop()
  }

  const io = new IntersectionObserver(
    (entries) => {
      inView = entries[0]?.isIntersecting ?? true
      refresh()
    },
    { threshold: 0.05 },
  )
  io.observe(parent)

  const onVisibility = () => refresh()
  document.addEventListener('visibilitychange', onVisibility)

  const themeObserver = new MutationObserver(refresh)
  themeObserver.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['class'],
  })

  const onResize = () => {
    camera.aspect = parent.clientWidth / parent.clientHeight
    camera.updateProjectionMatrix()
    renderer.setSize(parent.clientWidth, parent.clientHeight, false)
  }
  window.addEventListener('resize', onResize, { passive: true })

  refresh()

  /* ---------- Аккуратное уничтожение ---------- */
  dispose = () => {
    stop()
    io.disconnect()
    themeObserver.disconnect()
    document.removeEventListener('visibilitychange', onVisibility)
    window.removeEventListener('pointermove', onPointerMove)
    window.removeEventListener('resize', onResize)
    geometry.dispose()
    material.dispose()
    renderer.dispose()
    renderer.forceContextLoss()
  }
})

onBeforeUnmount(() => {
  dispose?.()
  dispose = null
})
</script>

<template>
  <canvas
    ref="canvas"
    class="pointer-events-none absolute inset-0 h-full w-full transition-opacity duration-700"
    :class="isActive ? 'opacity-100' : 'opacity-0'"
    aria-hidden="true"
  />
</template>
