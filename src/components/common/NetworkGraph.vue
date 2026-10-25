<script setup lang="ts">
/**
 * Декоративный сетевой граф Hero: светящиеся узлы и линии (inline SVG).
 * Мерцание — чистый CSS (opacity keyframes), без JS и зависимостей.
 */

interface Node {
  x: number
  y: number
  r: number
  d: number // задержка мерцания, с
  dur: number // длительность цикла, с
}

const nodes: Node[] = [
  { x: 60, y: 70, r: 4, d: 0, dur: 3.2 },
  { x: 150, y: 40, r: 3, d: 0.7, dur: 2.6 },
  { x: 240, y: 90, r: 5, d: 1.3, dur: 3.8 },
  { x: 340, y: 50, r: 3, d: 0.4, dur: 2.9 },
  { x: 420, y: 120, r: 4, d: 1.8, dur: 3.4 },
  { x: 100, y: 180, r: 3, d: 2.2, dur: 2.7 },
  { x: 200, y: 230, r: 4, d: 0.9, dur: 3.1 },
  { x: 320, y: 200, r: 3, d: 1.5, dur: 2.5 },
  { x: 410, y: 280, r: 5, d: 0.2, dur: 3.6 },
  { x: 70, y: 300, r: 3, d: 2.6, dur: 3.0 },
  { x: 250, y: 320, r: 3, d: 1.1, dur: 2.8 },
]

/** Рёбра по индексам узлов */
const edges: Array<[number, number, number]> = [
  [0, 1, 0],
  [1, 2, 0.5],
  [2, 3, 1.0],
  [3, 4, 0.3],
  [0, 5, 0.8],
  [5, 6, 1.4],
  [2, 6, 0.6],
  [6, 7, 1.9],
  [4, 7, 0.2],
  [7, 8, 1.1],
  [5, 9, 2.0],
  [6, 10, 0.9],
  [8, 10, 1.6],
  [2, 7, 2.3],
]
</script>

<template>
  <svg
    class="net-graph"
    viewBox="0 0 480 360"
    fill="none"
    aria-hidden="true"
    preserveAspectRatio="xMidYMid meet"
  >
    <line
      v-for="([a, b, delay], i) in edges"
      :key="`e-${i}`"
      :x1="nodes[a].x"
      :y1="nodes[a].y"
      :x2="nodes[b].x"
      :y2="nodes[b].y"
      class="net-edge"
      :style="{ animationDelay: `${delay}s` }"
    />
    <circle
      v-for="(node, i) in nodes"
      :key="`n-${i}`"
      :cx="node.x"
      :cy="node.y"
      :r="node.r"
      class="net-node"
      :style="{ animationDelay: `${node.d}s`, animationDuration: `${node.dur}s` }"
    />
  </svg>
</template>

<style scoped>
.net-graph {
  width: 100%;
  height: 100%;
}

.net-edge {
  stroke: rgb(142 117 29 / 0.55);
  stroke-width: 1;
  animation: net-flicker 3.4s ease-in-out infinite;
}

.net-node {
  fill: #8e751d;
  animation: net-flicker 3s ease-in-out infinite;
}

:global(.dark) .net-edge {
  stroke: rgb(252 209 22 / 0.35);
}

:global(.dark) .net-node {
  fill: #fcd116;
  filter: drop-shadow(0 0 6px rgb(252 209 22 / 0.55));
}

@keyframes net-flicker {
  0%,
  100% {
    opacity: 0.25;
  }
  50% {
    opacity: 1;
  }
}
</style>
