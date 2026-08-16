<script setup>
import { computed } from 'vue'
import { useData } from 'vitepress'

const { frontmatter } = useData()
const problems = computed(() => frontmatter.value.problems || [])

const diffColor = { easy: '#10b981', medium: '#f59e0b', hard: '#ef4444' }
const diffLabel = { easy: '简单', medium: '中等', hard: '困难' }
</script>

<template>
  <div v-if="problems.length" class="related-problems">
    <h2 class="rp-title">相关题目</h2>
    <div class="rp-list">
      <a
        v-for="(p, i) in problems"
        :key="i"
        :href="p.url"
        target="_blank"
        rel="noopener"
        class="rp-item"
      >
        <span class="rp-name">{{ p.title }}</span>
        <span
          v-if="p.difficulty"
          class="rp-diff"
          :style="{ color: diffColor[p.difficulty], borderColor: diffColor[p.difficulty] }"
        >{{ diffLabel[p.difficulty] || p.difficulty }}</span>
      </a>
    </div>
  </div>
</template>

<style scoped>
.related-problems {
  margin-top: 32px;
  padding-top: 16px;
  border-top: 1px solid var(--vp-c-divider);
}
.rp-title { font-size: 1.15rem; margin: 0 0 12px; }
.rp-list { display: flex; flex-direction: column; gap: 8px; }
.rp-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 14px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  text-decoration: none;
  color: var(--vp-c-text-1);
  transition: border-color 0.2s, transform 0.2s;
}
.rp-item:hover { border-color: var(--vp-c-brand); transform: translateX(2px); }
.rp-name { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.rp-diff {
  font-size: 0.72rem;
  padding: 2px 8px;
  border: 1px solid;
  border-radius: 10px;
  flex-shrink: 0;
}
</style>
