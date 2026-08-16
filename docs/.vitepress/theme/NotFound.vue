<script setup>
import { useData } from 'vitepress'
const { theme } = useData()
</script>

<template>
  <div class="not-found">
    <div class="nf-code">404</div>
    <h1 class="nf-title">这里什么也没有</h1>
    <p class="nf-desc">页面可能被移动或删除了。试试搜索，或回首页继续学习。</p>
    <div class="nf-actions">
      <a class="nf-btn primary" href="/">回首页</a>
      <a class="nf-btn" href="/algorithm/">看算法</a>
      <a class="nf-btn" href="/ai/">看 AI</a>
      <a class="nf-btn" href="/distributed/scenarios/">看场景题</a>
    </div>
  </div>
</template>

<style scoped>
.not-found {
  max-width: 560px;
  margin: 0 auto;
  padding: 80px 24px;
  text-align: center;
}
.nf-code {
  font-size: 6rem;
  font-weight: 800;
  line-height: 1;
  background: linear-gradient(120deg, #38bdf8, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.nf-title { font-size: 1.5rem; margin: 12px 0 8px; }
.nf-desc { color: var(--vp-c-text-2); margin: 0 0 24px; }
.nf-actions {
  display: flex;
  gap: 10px;
  justify-content: center;
  flex-wrap: wrap;
}
.nf-btn {
  padding: 8px 16px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  text-decoration: none;
  color: var(--vp-c-text-1);
  font-size: 0.9rem;
  transition: border-color 0.2s;
}
.nf-btn:hover { border-color: var(--vp-c-brand); }
.nf-btn.primary {
  background: var(--vp-c-brand);
  color: #fff;
  border-color: var(--vp-c-brand);
}
.nf-btn.primary:hover { opacity: 0.9; }
</style>
