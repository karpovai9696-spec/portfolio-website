<script setup lang="ts">
/**
 * Секция «Смена сцен при скролле» — тёмный editorial-разрыв между Hero и услугами.
 *
 * Механика 1-в-1 по прототипу scroll-scenes:
 * - секция 480vh (на ≤860px — 320vh), .stage липнет через position:sticky на 100vh;
 * - смена сцен — ScrollTrigger onUpdate по прогрессу (сегмент 1/N, переход
 *   только при смене индекса);
 * - переход кадров: шторка .wipe scaleX 1→0 за 0.7s power3.inOut, контент
 *   кадра scale 1.12→1 за 1.1s power2.out, старый кадр yPercent ∓6 + scale 0.96
 *   за 0.8s power2.inOut;
 * - текст — стопки абсолютных блоков с .active (opacity/translate/blur),
 *   кикер, счётчик 0N/04, огромное outline-число, прогресс-бар scaleX=progress.
 *
 * GSAP подключается динамическим импортом (отдельный чанк, как lenis/three).
 * Синхронизация с Lenis: lenis.on('scroll', ScrollTrigger.update).
 * prefers-reduced-motion намеренно игнорируется (решение владельца сайта).
 */
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import type Lenis from 'lenis'

import { createLenis } from '@/composables/useLenis'

const KICKERS = [
  'scene 01 — разработчик',
  'scene 02 — код',
  'scene 03 — автоматизация',
  'scene 04 — результат',
] as const

/** Индекс активной сцены — управляет текстовой колонкой (классы .active). */
const current = ref(0)

const kickerText = computed(() => KICKERS[current.value])
const counterText = computed(() => String(current.value + 1).padStart(2, '0'))

const rootRef = ref<HTMLElement | null>(null)
const pbarRef = ref<HTMLElement | null>(null)

/** Индекс кадра, реально показанного в стопке (нужен для направления перехода). */
let animCurrent = 0
let ctx: { revert: () => void } | null = null
let lenis: Lenis | null = null
let onLenisScroll: (() => void) | null = null
let destroyed = false

onMounted(async () => {
  const [{ gsap }, { ScrollTrigger }] = await Promise.all([
    import('gsap'),
    import('gsap/ScrollTrigger'),
  ])
  if (destroyed || !rootRef.value) return
  gsap.registerPlugin(ScrollTrigger)

  // Lenis прокручивает window — ScrollTrigger получает нативные scroll-события,
  // а явный update держит прогресс в точной синхронизации с инерцией Lenis.
  lenis = await createLenis()
  if (destroyed) return
  onLenisScroll = () => ScrollTrigger.update()
  lenis?.on('scroll', onLenisScroll)

  const root = rootRef.value
  const frames = gsap.utils.toArray<HTMLElement>(root.querySelectorAll('.frame'))

  ctx = gsap.context(() => {
    // Изначально все кадры «за шторкой» (первый — открыт)
    gsap.set(frames, { visibility: 'visible' })
    frames.forEach((f, i) =>
      gsap.set(f.querySelector('.wipe'), { scaleX: i === 0 ? 0 : 1 }),
    )
    gsap.set(frames.slice(1), { visibility: 'hidden' })

    function goTo(i: number) {
      if (i === animCurrent) return
      const dir = i > animCurrent ? 1 : -1
      const prev = frames[animCurrent]
      const next = frames[i]
      const nextZoom = next.querySelector('.zoom')
      const prevZoom = prev.querySelector('.zoom')

      gsap.set(next, { visibility: 'visible', zIndex: 2 })
      gsap.set(prev, { zIndex: 1 })

      const tl = gsap.timeline({
        onComplete: () => gsap.set(prev, { visibility: 'hidden' }),
      })
      // Новый кадр: шторка уходит в сторону + контент чуть зумится
      tl.fromTo(
        next.querySelector('.wipe'),
        { scaleX: 1, transformOrigin: dir > 0 ? 'right' : 'left' },
        { scaleX: 0, duration: 0.7, ease: 'power3.inOut' },
        0,
      )
        .fromTo(nextZoom, { scale: 1.12 }, { scale: 1, duration: 1.1, ease: 'power2.out' }, 0)
        // Старый уходит с лёгким параллаксом
        .to(prevZoom, { yPercent: dir * -6, scale: 0.96, duration: 0.8, ease: 'power2.inOut' }, 0)

      animCurrent = i
      current.value = i
    }

    ScrollTrigger.create({
      trigger: root,
      start: 'top top',
      end: 'bottom bottom',
      onUpdate(self) {
        const seg = 1 / frames.length
        const i = Math.min(frames.length - 1, Math.floor(self.progress / seg))
        if (i !== animCurrent) goTo(i)
        if (pbarRef.value) gsap.set(pbarRef.value, { scaleX: self.progress })
      },
    })
  }, root)
})

onBeforeUnmount(() => {
  destroyed = true
  if (lenis && onLenisScroll) lenis.off('scroll', onLenisScroll)
  ctx?.revert()
  ctx = null
})
</script>

<template>
  <section ref="rootRef" class="stories" aria-label="Кто я — четыре сцены">
    <div class="stage">
      <div class="copy">
        <div class="kicker mono">{{ kickerText }}</div>
        <div class="headline">
          <div class="h" :class="{ active: current === 0 }">
            Михаил Карпов —<br /><span class="accent">разработчик</span>
          </div>
          <div class="h" :class="{ active: current === 1 }">
            Пишу код,<br />который <span class="accent-gold">работает</span>
          </div>
          <div class="h" :class="{ active: current === 2 }">
            Автоматизирую<br /><span class="accent-mint">рутину</span> бизнеса
          </div>
          <div class="h" :class="{ active: current === 3 }">
            Довожу до<br /><span class="accent">результата</span>
          </div>
        </div>
        <div class="sub">
          <div class="s" :class="{ active: current === 0 }">
            Full-stack разработчик. Сайты, веб-приложения, интеграции — от идеи до продакшена.
          </div>
          <div class="s" :class="{ active: current === 1 }">
            Vue 3, TypeScript, Node.js. Чистый код, тесты, ревью — инженерная дисциплина без
            компромиссов.
          </div>
          <div class="s" :class="{ active: current === 2 }">
            Битрикс24, n8n, 1С, Telegram-боты: связываю системы компании в один конвейер без
            ручного труда.
          </div>
          <div class="s" :class="{ active: current === 3 }">
            Запускаю, измеряю, улучшаю. Каждый проект заканчивается работающим продуктом, а не
            презентацией.
          </div>
        </div>
        <div class="progress mono">
          <span class="pnum"
            ><b>{{ counterText }}</b> / 04</span
          >
          <span class="pbar"><i ref="pbarRef"></i></span>
        </div>
      </div>

      <div class="frames">
        <!-- Сцена 1: фото -->
        <div class="frame" data-i="0">
          <div class="zoom"><img src="/images/photo.jpg" alt="Михаил Карпов" /></div>
          <div class="wipe"></div>
        </div>
        <!-- Сцена 2: код -->
        <div class="frame" data-i="1">
          <div class="zoom">
            <div class="mock code-card mono">
              <div class="tabbar"><i></i><i></i><i></i></div>
              <pre><span class="c-com">// конвейер: заявка → договор → оплата</span>
<span class="c-key">const</span> <span class="c-fn">pipeline</span> = <span class="c-key">await</span> b24.<span class="c-fn">createDeal</span>({
  title: <span class="c-str">'Сайт «Динамит»'</span>,
  contact: client.id,
});
<span class="c-key">await</span> n8n.<span class="c-fn">run</span>(<span class="c-str">'generate-contract'</span>, {
  deal: pipeline.id, template: <span class="c-str">'dev-v3'</span>,
});
<span class="c-key">await</span> sbis.<span class="c-fn">send</span>(doc).<span class="c-fn">sign</span>(ukep);
tg.<span class="c-fn">notify</span>(<span class="c-str">`✔ договор подписан, ${money(total)}`</span>);
<span class="c-com">// ручного труда: 0 минут</span></pre>
            </div>
          </div>
          <div class="wipe"></div>
        </div>
        <!-- Сцена 3: автоматизация -->
        <div class="frame" data-i="2">
          <div class="zoom">
            <div class="mock flow-card">
              <div class="flow-title mono">живой конвейер · status: online</div>
              <div class="node">
                <span class="dot" style="background: #b4491a"></span><b>Битрикс24</b
                ><span>заявка и сделка</span>
              </div>
              <div class="wire"></div>
              <div class="node">
                <span class="dot" style="background: #c99a2c"></span><b>n8n</b
                ><span>оркестрация процессов</span>
              </div>
              <div class="wire"></div>
              <div class="node">
                <span class="dot" style="background: #3ba28c"></span><b>1С · СБИС · МДЛП</b
                ><span>документы и учёт</span>
              </div>
              <div class="wire"></div>
              <div class="node">
                <span class="dot" style="background: #fffcf5"></span><b>Telegram</b
                ><span>уведомления команде</span>
              </div>
            </div>
          </div>
          <div class="wipe"></div>
        </div>
        <!-- Сцена 4: результат -->
        <div class="frame" data-i="3">
          <div class="zoom">
            <div class="mock stats-card">
              <div class="stat">
                <span class="val"><em>40+</em></span
                ><span class="lbl">проектов запущено в продакшен</span>
              </div>
              <div class="stat">
                <span class="val"><em class="g">−70%</em></span
                ><span class="lbl">ручных операций у клиентов после автоматизации</span>
              </div>
              <div class="stat">
                <span class="val"><em class="m">24/7</em></span
                ><span class="lbl">мониторинг и поддержка без выходных</span>
              </div>
            </div>
          </div>
          <div class="wipe"></div>
        </div>
      </div>

      <div class="bignum" aria-hidden="true">{{ counterText }}</div>
    </div>
  </section>
</template>

<style scoped>
/* Намеренно тёмный «разрыв» в обеих темах сайта — не подгонять под light/dark. */
.stories {
  --ss-ink-950: #0e0b08;
  --ss-ink-500: #4a443b;
  --ss-ink-300: #8f8677;
  --ss-ink-100: #e2dccb;
  --ss-terra: #b4491a;
  --ss-gold: #c99a2c;
  --ss-mint: #3ba28c;
  --ss-paper: #fffcf5;

  height: 480vh;
  position: relative;
  background: var(--ss-ink-950);
}

.mono {
  font-family: 'JetBrains Mono', 'Fira Code', Consolas, Menlo, monospace;
}

.stage {
  position: sticky;
  top: 0;
  height: 100vh;
  overflow: hidden;
  background:
    radial-gradient(1200px 700px at 78% 30%, rgba(180, 73, 26, 0.1), transparent 60%),
    radial-gradient(900px 600px at 15% 80%, rgba(59, 162, 140, 0.07), transparent 60%),
    var(--ss-ink-950);
  color: var(--ss-paper);
  display: grid;
  grid-template-columns: minmax(320px, 42%) 1fr;
  gap: 5vw;
  padding: 0 6vw;
  align-items: center;
}

/* левая колонка — текст */
.copy {
  position: relative;
  z-index: 3;
}
.kicker {
  font-size: 12px;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  color: var(--ss-mint);
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 22px;
}
.kicker::before {
  content: '';
  width: 28px;
  height: 1px;
  background: var(--ss-mint);
}
.headline {
  position: relative;
  height: 3.4em;
  font-size: clamp(30px, 4vw, 52px);
  font-weight: 800;
  letter-spacing: -0.02em;
  line-height: 1.06;
}
.headline .h {
  position: absolute;
  inset: 0;
  opacity: 0;
  transform: translateY(40px);
  filter: blur(6px);
  transition:
    opacity 0.55s cubic-bezier(0.22, 0.8, 0.24, 1),
    transform 0.55s cubic-bezier(0.22, 0.8, 0.24, 1),
    filter 0.55s;
}
.headline .h.active {
  opacity: 1;
  transform: translateY(0);
  filter: blur(0);
}
.headline .accent {
  color: var(--ss-terra);
}
.headline .accent-gold {
  color: var(--ss-gold);
}
.headline .accent-mint {
  color: var(--ss-mint);
}
.sub {
  position: relative;
  height: 5.2em;
  margin-top: 18px;
  max-width: 46ch;
  color: var(--ss-ink-300);
  font-size: 16px;
  line-height: 1.65;
}
.sub .s {
  position: absolute;
  inset: 0;
  opacity: 0;
  transform: translateY(24px);
  transition:
    opacity 0.55s 0.08s,
    transform 0.55s 0.08s;
}
.sub .s.active {
  opacity: 1;
  transform: translateY(0);
}

/* прогресс сцен */
.progress {
  margin-top: 36px;
  display: flex;
  align-items: center;
  gap: 16px;
}
.pnum {
  font-size: 13px;
  color: var(--ss-ink-300);
}
.pnum b {
  color: var(--ss-paper);
  font-weight: 700;
}
.pbar {
  position: relative;
  width: 180px;
  height: 2px;
  background: rgba(226, 220, 203, 0.18);
  border-radius: 2px;
  overflow: hidden;
}
.pbar i {
  position: absolute;
  inset: 0;
  transform-origin: left;
  transform: scaleX(0);
  background: linear-gradient(90deg, var(--ss-terra), var(--ss-gold));
}

/* правая колонка — стопка картинок */
.frames {
  position: relative;
  z-index: 2;
  height: min(66vh, 620px);
  width: 100%;
  border-radius: 18px;
  perspective: 1200px;
}
.frame {
  position: absolute;
  inset: 0;
  border-radius: 18px;
  overflow: hidden;
  box-shadow:
    0 40px 80px -20px rgba(0, 0, 0, 0.55),
    0 0 0 1px rgba(226, 220, 203, 0.08);
  visibility: hidden;
}
.frame .zoom {
  position: absolute;
  inset: -6%;
  will-change: transform;
}
.frame img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.frame .wipe {
  position: absolute;
  inset: 0;
  background: var(--ss-ink-950);
  transform: scaleX(1);
  transform-origin: right;
}

/* карточки-«картинки», свёрстанные в коде */
.mock {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
}
.code-card {
  background: #191410;
  padding: 22px;
  font-size: 13.5px;
  line-height: 1.75;
  overflow: hidden;
}
.code-card pre {
  margin: 0;
  font-family: inherit;
  white-space: pre;
}
.code-card .tabbar {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}
.code-card .tabbar i {
  width: 11px;
  height: 11px;
  border-radius: 50%;
  background: var(--ss-ink-500);
  display: block;
}
.code-card .tabbar i:nth-child(1) {
  background: var(--ss-terra);
}
.code-card .tabbar i:nth-child(2) {
  background: var(--ss-gold);
}
.code-card .tabbar i:nth-child(3) {
  background: var(--ss-mint);
}
.c-key {
  color: var(--ss-terra);
}
.c-str {
  color: var(--ss-gold);
}
.c-fn {
  color: var(--ss-mint);
}
.c-com {
  color: var(--ss-ink-300);
}
.c-pln {
  color: var(--ss-ink-100);
}

.flow-card {
  background: linear-gradient(160deg, #171310, #100d09);
  padding: 34px;
  justify-content: center;
  gap: 14px;
}
.flow-title {
  font-size: 12px;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--ss-ink-300);
  margin-bottom: 14px;
}
.node {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 18px;
  border-radius: 12px;
  background: rgba(226, 220, 203, 0.05);
  border: 1px solid rgba(226, 220, 203, 0.1);
}
.node .dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}
.node b {
  font-size: 15px;
}
.node span {
  margin-left: auto;
  font-size: 12px;
  color: var(--ss-ink-300);
}
.wire {
  width: 2px;
  height: 20px;
  margin-left: 28px;
  background: linear-gradient(var(--ss-terra), var(--ss-gold));
}

.stats-card {
  background: linear-gradient(160deg, #171310, #100d09);
  padding: 34px;
  justify-content: center;
  gap: 12px;
}
.stat {
  display: flex;
  align-items: baseline;
  gap: 14px;
  padding: 16px 0;
  border-bottom: 1px solid rgba(226, 220, 203, 0.08);
}
.stat:last-child {
  border-bottom: 0;
}
.stat .val {
  font-size: clamp(30px, 3vw, 44px);
  font-weight: 800;
  letter-spacing: -0.02em;
}
.stat .val em {
  font-style: normal;
  color: var(--ss-terra);
}
.stat .val em.g {
  color: var(--ss-gold);
}
.stat .val em.m {
  color: var(--ss-mint);
}
.stat .lbl {
  color: var(--ss-ink-300);
  font-size: 14px;
}

/* фоновая номерация */
.bignum {
  position: absolute;
  right: 2vw;
  bottom: -4vh;
  z-index: 1;
  pointer-events: none;
  font-size: 38vh;
  font-weight: 800;
  line-height: 1;
  letter-spacing: -0.05em;
  color: transparent;
  -webkit-text-stroke: 1px rgba(226, 220, 203, 0.07);
}

@media (max-width: 860px) {
  .stories {
    height: 320vh;
  }
  .stage {
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr;
    gap: 20px;
    padding: 88px 6vw 40px;
    align-content: start;
  }
  .headline {
    font-size: clamp(26px, 7.4vw, 34px);
  }
  .sub {
    font-size: 14px;
    height: 6.4em;
  }
  .bignum {
    font-size: 30vh;
  }
}
</style>
