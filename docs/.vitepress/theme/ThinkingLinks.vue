<template>
  <div v-if="links && links.related && links.related.length > 0" class="thinking-links">
    <div class="thinking-links-header">
      <span class="thinking-links-title">🔗 跨域关联</span>
      <span class="thinking-links-subtitle">学完这篇，不妨看看这些</span>
    </div>
    
    <div class="thinking-links-grid">
      <a
        v-for="link in links.related"
        :key="link.url"
        :href="link.url"
        class="thinking-link-card"
        target="_blank"
        rel="noopener"
      >
        <div class="thinking-link-icon">→</div>
        <div class="thinking-link-content">
          <div class="thinking-link-title">{{ link.title }}</div>
          <div class="thinking-link-reason">{{ link.reason }}</div>
        </div>
      </a>
    </div>

    <div v-if="links.think && links.think.length > 0" class="thinking-questions">
      <div class="thinking-questions-header">
        <span class="thinking-questions-icon">🤔</span>
        <span class="thinking-questions-title">读者思考</span>
      </div>
      <ul class="thinking-questions-list">
        <li v-for="(question, idx) in links.think" :key="idx" class="thinking-question-item">
          {{ question }}
        </li>
      </ul>
      <div class="thinking-questions-hint">
        <span>💡 提示：先独立思考，再回到文中找答案</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import linksData from './thinking-links.json'

const props = defineProps<{
  pageKey: string
}>()

const links = computed(() => {
  return (linksData as Record<string, { related: Array<{title: string, url: string, reason: string}>, think: string[] }>)[props.pageKey]
})
</script>

<style scoped>
.thinking-links {
  margin: 2rem 0;
  padding: 1.5rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(56, 189, 248, 0.03) 0%, rgba(139, 92, 246, 0.03) 100%);
}

.thinking-links-header {
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.thinking-links-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--vp-c-brand);
}

.thinking-links-subtitle {
  font-size: 0.85rem;
  color: var(--vp-c-text-2);
}

.thinking-links-grid {
  display: grid;
  gap: 0.75rem;
}

.thinking-link-card {
  display: flex;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  border-radius: 8px;
  background: var(--vp-c-bg-alt);
  border: 1px solid var(--vp-c-divider);
  text-decoration: none;
  color: inherit;
  transition: all 0.2s ease;
}

.thinking-link-card:hover {
  border-color: var(--vp-c-brand);
  background: rgba(56, 189, 248, 0.05);
  transform: translateX(4px);
}

.thinking-link-icon {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  background: var(--vp-c-brand);
  color: white;
  font-size: 0.875rem;
}

.thinking-link-content {
  flex: 1;
  min-width: 0;
}

.thinking-link-title {
  font-weight: 500;
  color: var(--vp-c-text-1);
  margin-bottom: 0.25rem;
}

.thinking-link-reason {
  font-size: 0.8rem;
  color: var(--vp-c-text-2);
  line-height: 1.5;
}

.thinking-questions {
  margin-top: 1.25rem;
  padding-top: 1rem;
  border-top: 1px dashed var(--vp-c-divider);
}

.thinking-questions-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.thinking-questions-icon {
  font-size: 1.2rem;
}

.thinking-questions-title {
  font-weight: 600;
  color: var(--vp-c-text-1);
}

.thinking-questions-list {
  list-style: none;
  padding: 0;
  margin: 0 0 0.75rem 0;
}

.thinking-question-item {
  position: relative;
  padding-left: 1.25rem;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: var(--vp-c-text-2);
  line-height: 1.6;
}

.thinking-question-item::before {
  content: '▸';
  position: absolute;
  left: 0;
  color: var(--vp-c-brand);
}

.thinking-questions-hint {
  font-size: 0.8rem;
  color: var(--vp-c-text-3);
  font-style: italic;
}

@media (max-width: 640px) {
  .thinking-links {
    padding: 1rem;
  }
  
  .thinking-link-card {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>
