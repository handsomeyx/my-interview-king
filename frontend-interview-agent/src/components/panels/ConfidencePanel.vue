<template>
  <div class="confidence-panel">
    <h3 class="panel-title">💯 信心指数</h3>
    <div class="gauge">
      <div class="gauge-circle" :style="{ background: `conic-gradient(${color} ${score * 3.6}deg, var(--border-color) 0)` }">
        <div class="gauge-inner">
          <span class="score">{{ score }}</span>
        </div>
      </div>
    </div>
    <div class="level-label" :style="{ color }">{{ level }}</div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  score: number
}>()

const level = computed(() => {
  if (props.score >= 80) return '非常自信'
  if (props.score >= 60) return '较为自信'
  if (props.score >= 40) return '一般'
  return '需要加强'
})

const color = computed(() => {
  if (props.score >= 80) return '#10b981'
  if (props.score >= 60) return '#3b82f6'
  if (props.score >= 40) return '#f59e0b'
  return '#ef4444'
})
</script>

<style scoped>
.confidence-panel {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 16px;
}

.panel-title {
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 12px;
}

.gauge {
  display: flex;
  justify-content: center;
  margin-bottom: 8px;
}

.gauge-circle {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.gauge-inner {
  width: 76px;
  height: 76px;
  border-radius: 50%;
  background: var(--bg-surface);
  display: flex;
  align-items: center;
  justify-content: center;
}

.score {
  font-size: 1.5rem;
  font-weight: 700;
}

.level-label {
  text-align: center;
  font-weight: 500;
  font-size: 0.85rem;
}
</style>
