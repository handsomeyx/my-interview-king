<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vitepress'
import { isBookmarked, toggleBookmark, getMasteryOf, setMastery } from './study-storage'

const route = useRoute()
const bookmarked = ref(false)
const mastery = ref('todo')

const isArticle = computed(() => !!route.path && route.path !== '/')

const refresh = () => {
  if (!isArticle.value) return
  bookmarked.value = isBookmarked(route.path)
  mastery.value = getMasteryOf(route.path)
}

onMounted(refresh)
watch(() => route.path, refresh)

const onBookmark = () => {
  bookmarked.value = toggleBookmark(route.path)
}

const cycleMastery = () => {
  const order = ['todo', 'learning', 'mastered']
  const next = order[(order.indexOf(mastery.value) + 1) % order.length]
  mastery.value = next
  setMastery(route.path, next)
}

const masteryLabel = () =>
  mastery.value === 'mastered' ? '已掌握' : mastery.value === 'learning' ? '学习中' : '待学'
</script>

<template>
  <div v-if="isArticle" class="article-actions">
    <button
      class="aa-btn"
      :class="{ active: bookmarked }"
      :title="bookmarked ? '取消收藏' : '收藏'"
      @click="onBookmark"
    >
      <svg v-if="bookmarked" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M6 2a2 2 0 0 0-2 2v18l8-5 8 5V4a2 2 0 0 0-2-2H6z" /></svg>
      <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z" /></svg>
    </button>
    <button
      class="aa-btn"
      :class="mastery"
      :title="`掌握状态（点击切换）：${masteryLabel()}`"
      @click="cycleMastery"
    >
      <span class="aa-dot" />
      <span class="aa-label">{{ masteryLabel() }}</span>
    </button>
  </div>
</template>

<style scoped>
.article-actions {
  position: fixed;
  left: 50%;
  bottom: 80px;
  transform: translateX(-50%);
  display: flex;
  gap: 4px;
  padding: 5px;
  z-index: 50;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 999px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.1);
}
.aa-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border: none;
  background: transparent;
  border-radius: 999px;
  cursor: pointer;
  color: var(--vp-c-text-2);
  font-size: 0.8rem;
  transition: background 0.2s, color 0.2s;
}
.aa-btn:hover { background: var(--vp-c-bg-soft); }
.aa-btn.active { color: #38bdf8; }
.aa-btn.mastered { color: #10b981; }
.aa-btn.learning { color: #f59e0b; }
.aa-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
  display: inline-block;
}
@media (max-width: 768px) {
  .article-actions { bottom: 72px; }
}
</style>
