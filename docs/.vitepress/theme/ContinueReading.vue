<script setup>
import { ref, onMounted } from 'vue'
import { getRecent, getProgress, getMastery, getReviewReminders } from './study-storage'

const items = ref([])

onMounted(() => {
  const recent = getRecent()
  const progress = getProgress()
  const mastery = getMastery()
  const reviewReminders = getReviewReminders()
  const duePaths = new Set(
    Object.values(reviewReminders).filter(r => r.remindAt <= Date.now() && r.stage < 3).map(r => r.path)
  )
  items.value = recent.slice(0, 5).map((r) => ({
    ...r,
    ratio: Math.round((progress[r.path]?.scrollRatio ?? 0) * 100),
    state: mastery[r.path] || 'todo',
    due: duePaths.has(r.path)
  }))
})
</script>

<template>
  <div v-if="items.length" class="continue-reading">
    <h2 class="cr-title">继续学习</h2>
    <div class="cr-list">
      <a v-for="it in items" :key="it.path" :href="it.path" class="cr-item">
        <div class="cr-info">
          <div class="cr-name">{{ it.title }}</div>
          <div class="cr-meta">
            <span class="cr-bar"><span class="cr-bar-inner" :style="{ width: it.ratio + '%' }" /></span>
            <span class="cr-pct">{{ it.ratio }}%</span>
          </div>
        </div>
        <span v-if="it.state === 'mastered'" class="cr-badge mastered">已掌握</span>
        <span v-else-if="it.state === 'learning'" class="cr-badge learning">学习中</span>
        <span v-if="it.due" class="cr-badge review">⏰ 该复习了</span>
      </a>
    </div>
  </div>
</template>

<style scoped>
.continue-reading { margin: 24px 0; }
.cr-title { font-size: 1.25rem; margin: 0 0 12px; }
.cr-list { display: flex; flex-direction: column; gap: 8px; }
.cr-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 14px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  text-decoration: none;
  color: inherit;
  transition: border-color 0.2s, transform 0.2s;
}
.cr-item:hover { border-color: var(--vp-c-brand); transform: translateX(2px); }
.cr-info { flex: 1; min-width: 0; }
.cr-name {
  font-weight: 500;
  margin-bottom: 6px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.cr-meta { display: flex; align-items: center; gap: 8px; }
.cr-bar {
  flex: 1;
  height: 4px;
  background: var(--vp-c-divider);
  border-radius: 2px;
  overflow: hidden;
}
.cr-bar-inner {
  display: block;
  height: 100%;
  background: linear-gradient(90deg, #38bdf8, #8b5cf6);
}
.cr-pct {
  font-size: 0.75rem;
  color: var(--vp-c-text-3);
  min-width: 32px;
  text-align: right;
}
.cr-badge {
  font-size: 0.7rem;
  padding: 2px 8px;
  border-radius: 10px;
  margin-left: 12px;
}
.cr-badge.mastered { background: rgba(16, 185, 129, 0.15); color: #10b981; }
.cr-badge.learning { background: rgba(245, 158, 11, 0.15); color: #f59e0b; }
.cr-badge.review { background: rgba(239, 68, 68, 0.15); color: #ef4444; }
</style>
