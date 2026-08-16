<script setup>
import { ref, computed, onMounted } from 'vue'
import { getMastery, getBookmarks, getRecent, getDueReviews, advanceReview, cancelReview } from './study-storage'

const mastery = ref({})
const bookmarks = ref([])
const recent = ref([])
const dueReviews = ref([])

const refresh = () => {
  mastery.value = getMastery()
  bookmarks.value = getBookmarks()
  recent.value = getRecent()
  dueReviews.value = getDueReviews()
}

onMounted(refresh)

const titleMap = computed(() => {
  const m = {}
  recent.value.forEach((r) => { m[r.path] = r.title })
  return m
})

const titleOf = (path) =>
  titleMap.value[path] || path.replace(/^\//, '').replace(/\/$/, '').replace(/-/g, ' ')

const mastered = computed(() =>
  Object.entries(mastery.value).filter(([, v]) => v === 'mastered').map(([p]) => p)
)
const learning = computed(() =>
  Object.entries(mastery.value).filter(([, v]) => v === 'learning').map(([p]) => p)
)

const markReviewed = (path) => { advanceReview(path); refresh() }
const skipReview = (path) => { cancelReview(path); refresh() }
</script>

<template>
  <div class="my-progress">
    <div class="mp-overview">
      <div class="mp-stat"><b>{{ mastered.length }}</b>已掌握</div>
      <div class="mp-stat"><b>{{ learning.length }}</b>学习中</div>
      <div class="mp-stat"><b>{{ bookmarks.length }}</b>收藏</div>
      <div class="mp-stat"><b>{{ recent.length }}</b>最近阅读</div>
    </div>

    <div v-if="recent.length" class="mp-section">
      <h3>最近阅读</h3>
      <a v-for="r in recent.slice(0, 10)" :key="r.path" :href="r.path" class="mp-item">{{ r.title }}</a>
    </div>

    <div v-if="bookmarks.length" class="mp-section">
      <h3>收藏</h3>
      <a v-for="p in bookmarks" :key="p" :href="p" class="mp-item">{{ titleOf(p) }}</a>
    </div>

    <div v-if="learning.length" class="mp-section">
      <h3>学习中</h3>
      <a v-for="p in learning" :key="p" :href="p" class="mp-item">{{ titleOf(p) }}</a>
    </div>

    <div v-if="mastered.length" class="mp-section">
      <h3>已掌握</h3>
      <a v-for="p in mastered" :key="p" :href="p" class="mp-item">{{ titleOf(p) }}</a>
    </div>

    <div v-if="dueReviews.length" class="mp-section">
      <h3>复习提醒 ⏰</h3>
      <div v-for="r in dueReviews" :key="r.path" class="mp-item review-item">
        <a :href="r.path" class="review-link">{{ r.title }}</a>
        <div class="review-actions">
          <button class="review-done" @click="markReviewed(r.path)">已复习</button>
          <button class="review-skip" @click="skipReview(r.path)">跳过</button>
        </div>
      </div>
    </div>

    <div
      v-if="!bookmarks.length && !recent.length && !mastered.length"
      class="mp-empty"
    >
      还没有学习记录。阅读文章、收藏或标记掌握状态后，数据会在这里汇总。
    </div>
  </div>
</template>

<style scoped>
.mp-overview {
  display: flex;
  gap: 28px;
  flex-wrap: wrap;
  padding: 16px 0;
  border-bottom: 1px solid var(--vp-c-divider);
  margin-bottom: 24px;
}
.mp-stat {
  font-size: 0.9rem;
  color: var(--vp-c-text-2);
}
.mp-stat b {
  font-size: 1.6rem;
  color: var(--vp-c-brand);
  margin-right: 6px;
}
.mp-section {
  margin-bottom: 28px;
}
.mp-section h3 {
  font-size: 1.05rem;
  margin: 0 0 12px;
}
.mp-item {
  display: block;
  padding: 9px 14px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  margin-bottom: 6px;
  text-decoration: none;
  color: var(--vp-c-text-1);
  transition: border-color 0.2s, color 0.2s;
}
.mp-item:hover {
  border-color: var(--vp-c-brand);
  color: var(--vp-c-brand);
}
.mp-empty {
  color: var(--vp-c-text-3);
  padding: 32px 0;
  text-align: center;
}
.review-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.review-link {
  flex: 1;
  text-decoration: none;
  color: var(--vp-c-text-1);
}
.review-actions {
  display: flex;
  gap: 6px;
}
.review-done, .review-skip {
  font-size: 0.75rem;
  padding: 4px 10px;
  border-radius: 4px;
  border: 1px solid var(--vp-c-divider);
  cursor: pointer;
  background: transparent;
  transition: all 0.2s;
}
.review-done {
  color: #10b981;
  border-color: #10b981;
}
.review-done:hover {
  background: rgba(16, 185, 129, 0.1);
}
.review-skip {
  color: var(--vp-c-text-3);
}
.review-skip:hover {
  color: var(--vp-c-text-1);
  border-color: var(--vp-c-text-2);
}
</style>
