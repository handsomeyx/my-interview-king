<script setup>
import { ref, computed, onMounted } from 'vue'
import { getMastery, getBookmarks, getRecent } from './study-storage'

const mastery = ref({})
const bookmarkCount = ref(0)
const recentCount = ref(0)

onMounted(() => {
  mastery.value = getMastery()
  bookmarkCount.value = getBookmarks().length
  recentCount.value = getRecent().length
})

const masteredCount = computed(() => Object.values(mastery.value).filter((v) => v === 'mastered').length)
const trackedCount = computed(() => Object.keys(mastery.value).length)
</script>

<template>
  <div class="stats-container">
    <div class="stat-card">
      <div class="stat-number">{{ masteredCount }}<span class="stat-sub"> / {{ trackedCount }}</span></div>
      <div class="stat-label">已掌握 / 追踪</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">{{ bookmarkCount }}</div>
      <div class="stat-label">已收藏</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">{{ recentCount }}</div>
      <div class="stat-label">最近阅读</div>
    </div>
  </div>
</template>

<style scoped>
.stat-sub {
  font-size: 0.6em;
  color: var(--vp-c-text-3);
  font-weight: 400;
}
</style>
