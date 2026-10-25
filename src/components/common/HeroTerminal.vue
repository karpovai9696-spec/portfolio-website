<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'

/**
 * Интерактивный терминал Hero: построчный typing-эффект псевдокода
 * (логи МДЛП / криптография). Чистый Vue + setTimeout, без зависимостей.
 * После полного прохода — пауза и перезапуск цикла.
 */

interface TermLine {
  text: string
  cls: string
  /** true — строка «команды» (печатается посимвольно), false — вывод (появляется сразу) */
  typed: boolean
}

const script: TermLine[] = [
  { text: 'mdlp-gateway --status', cls: 'cmd', typed: true },
  { text: '[OK] соединение с ФГИС МДЛП ... established', cls: 'ok', typed: false },
  { text: '[OK] документ 552 подписан (УКЭП)', cls: 'ok', typed: false },
  { text: 'crypto_signature: verify_successful', cls: 'fn', typed: false },
  { text: '[INFO] остатки синхронизированы: 12 483 ед.', cls: 'info', typed: false },
  { text: 'status: ok', cls: 'accent', typed: false },
  { text: './sync --watch', cls: 'cmd', typed: true },
  { text: '[INFO] канал активен · latency 42 ms', cls: 'info', typed: false },
]

/** Уже напечатанные строки + текущая печатаемая */
const doneLines = ref<TermLine[]>([])
const currentText = ref('')
const currentCls = ref('cmd')
const typingNow = ref(false)

let timer: ReturnType<typeof setTimeout> | null = null
let cancelled = false

function schedule(fn: () => void, delay: number) {
  timer = setTimeout(() => {
    if (!cancelled) fn()
  }, delay)
}

function runLine(index: number, charIndex: number) {
  if (index >= script.length) {
    // Полный проход: пауза, очистка, перезапуск
    typingNow.value = false
    schedule(() => {
      doneLines.value = []
      currentText.value = ''
      runLine(0, 0)
    }, 5200)
    return
  }

  const line = script[index]
  currentCls.value = line.cls

  if (!line.typed) {
    // Строка вывода появляется целиком с небольшой задержкой
    typingNow.value = false
    schedule(() => {
      doneLines.value = [...doneLines.value, line]
      currentText.value = ''
      runLine(index + 1, 0)
    }, 380 + Math.random() * 320)
    return
  }

  typingNow.value = true
  currentText.value = line.text.slice(0, charIndex + 1)
  if (charIndex + 1 >= line.text.length) {
    schedule(() => {
      doneLines.value = [...doneLines.value, line]
      currentText.value = ''
      runLine(index + 1, 0)
    }, 520)
  } else {
    schedule(() => runLine(index, charIndex + 1), 42 + Math.random() * 60)
  }
}

onMounted(() => {
  schedule(() => runLine(0, 0), 1100)
})

onBeforeUnmount(() => {
  cancelled = true
  if (timer) clearTimeout(timer)
})
</script>

<template>
  <div
    class="overflow-hidden rounded-xl border border-gold/25 bg-white/80 shadow-xl backdrop-blur-md dark:border-primary/10 dark:bg-ink-900/80 dark:shadow-[0_0_30px_rgba(252,209,22,0.08)]"
    role="img"
    aria-label="Терминал с логами интеграции ФГИС МДЛП: подписание документов УКЭП, статус ok"
  >
    <!-- Заголовок окна -->
    <div
      class="flex items-center gap-2 border-b border-hairline px-4 py-3 dark:border-white/5"
      aria-hidden="true"
    >
      <span class="h-3 w-3 rounded-full bg-[#FF5F57]" />
      <span class="h-3 w-3 rounded-full bg-[#FEBC2E]" />
      <span class="h-3 w-3 rounded-full bg-[#28C840]" />
      <span class="ml-3 font-mono text-[11px] tracking-wider text-ink-100 dark:text-ink-300">
        mk@spec: ~/mdlp-gateway
      </span>
      <span
        class="ml-auto inline-flex items-center gap-1.5 font-mono text-[10px] uppercase tracking-wider text-[#1f8a4c] dark:text-[#7EE787]"
      >
        <span class="relative flex h-1.5 w-1.5">
          <span
            class="absolute inline-flex h-full w-full animate-ping rounded-full bg-[#1f8a4c] opacity-75 dark:bg-[#7EE787]"
          />
          <span
            class="relative inline-flex h-1.5 w-1.5 rounded-full bg-[#1f8a4c] dark:bg-[#7EE787]"
          />
        </span>
        live
      </span>
    </div>

    <!-- Тело терминала -->
    <div
      class="term-body min-h-[15rem] px-4 py-4 font-mono text-[12px] leading-relaxed sm:text-[13px]"
    >
      <p v-for="(line, i) in doneLines" :key="i" class="term-line" :class="`term-${line.cls}`">
        <span v-if="line.typed" class="term-prompt" aria-hidden="true">$&nbsp;</span>{{ line.text }}
      </p>
      <p v-if="typingNow" class="term-line" :class="`term-${currentCls}`">
        <span class="term-prompt" aria-hidden="true">$&nbsp;</span>{{ currentText
        }}<span class="term-caret" aria-hidden="true" />
      </p>
      <p v-else class="term-line">
        <span class="term-prompt" aria-hidden="true">$&nbsp;</span
        ><span class="term-caret" aria-hidden="true" />
      </p>
    </div>
  </div>
</template>

<style scoped>
.term-line {
  white-space: pre-wrap;
  word-break: break-word;
}

.term-prompt {
  color: #8e751d;
  font-weight: 600;
}

.term-caret {
  display: inline-block;
  width: 7px;
  height: 14px;
  margin-left: 2px;
  vertical-align: -2px;
  background: #8e751d;
  animation: term-blink 1.1s step-end infinite;
}

/* Светлая тема */
.term-cmd {
  color: #2e2c1e;
}
.term-ok {
  color: #1f8a4c;
}
.term-fn {
  color: #6b5a17;
}
.term-info {
  color: #6b6552;
}
.term-accent {
  color: #8e751d;
  font-weight: 600;
}

/* Тёмная тема (глобальный селектор: scoped + :global не компилируется) */
:global(.dark) .term-prompt {
  color: #fcd116;
}
:global(.dark) .term-caret {
  background: #fcd116;
}
:global(.dark) .term-cmd {
  color: #fff5b8;
}
:global(.dark) .term-ok {
  color: #7ee787;
}
:global(.dark) .term-fn {
  color: #7ee787;
}
:global(.dark) .term-info {
  color: rgb(255 245 184 / 0.6);
}
:global(.dark) .term-accent {
  color: #fcd116;
}

@keyframes term-blink {
  0%,
  45% {
    opacity: 1;
  }
  50%,
  95% {
    opacity: 0;
  }
}
</style>
