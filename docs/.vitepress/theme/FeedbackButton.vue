<script setup>
import { computed } from 'vue'
import { useRoute } from 'vitepress'

const route = useRoute()
const isArticle = computed(() => !!route.path && route.path !== '/')
const REPO = 'handsomeyx/my-interview-king'

const issueUrl = computed(() => {
  const title = encodeURIComponent(`[纠错] ${route.path}`)
  const body = encodeURIComponent(`页面路径：${route.path}\n\n问题描述：\n`)
  return `https://github.com/${REPO}/issues/new?title=${title}&body=${body}`
})
</script>

<template>
  <a
    v-if="isArticle"
    class="feedback-btn"
    :href="issueUrl"
    target="_blank"
    rel="noopener"
    title="反馈纠错"
  >
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z" /></svg>
    <span>反馈</span>
  </a>
</template>

<style scoped>
.feedback-btn {
  position: fixed;
  right: 24px;
  bottom: 136px;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 999px;
  color: var(--vp-c-text-2);
  text-decoration: none;
  font-size: 0.8rem;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
  z-index: 50;
  transition: border-color 0.2s, color 0.2s;
}
.feedback-btn:hover {
  border-color: var(--vp-c-brand);
  color: var(--vp-c-brand);
}
@media (max-width: 768px) {
  .feedback-btn { right: 16px; bottom: 128px; }
}
</style>
