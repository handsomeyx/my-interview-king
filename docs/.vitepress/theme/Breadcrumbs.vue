<script setup>
import { computed } from 'vue'
import { useData } from 'vitepress'

const { page } = useData()

const SEG_LABELS = {
  java: 'Java 后端',
  'java/basics': 'Java 基础', 'java/spring': 'Spring', 'java/redis': 'Redis',
  'java/mysql': 'MySQL', 'java/kafka': 'Kafka', 'java/os': '操作系统',
  distributed: '分布式 & 场景', 'distributed/scenarios': '场景题',
  algorithm: '算法',
  'algorithm/00-algorithm-frameworks': '算法框架', 'algorithm/01-methodology': '方法论',
  'algorithm/02-data-structures': '数据结构', 'algorithm/03-algorithm-patterns': '算法模式',
  'algorithm/04-system-algorithms': '系统算法', 'algorithm/05-top-interview-100': '面试 Top 100',
  ai: 'AI 实战',
  'ai/00-basics': '基础入门', 'ai/01-llm': 'LLM 底座', 'ai/02-agent': 'Agent 核心',
  'ai/03-mcp': 'MCP 协议', 'ai/04-skills': 'Skill 技能', 'ai/05-engineering': '工程落地',
  'ai/06-RAG': 'RAG',
  projects: '项目实战'
}

const crumbs = computed(() => {
  const rel = page.value.relativePath
  if (!rel || rel === 'index.md') return []
  const parts = rel.replace(/\.md$/, '').split('/')
  if (parts[parts.length - 1] === 'index') parts.pop()
  if (parts.length === 0) return []
  const result = []
  const top = parts[0]
  if (SEG_LABELS[top]) result.push({ label: SEG_LABELS[top], link: '/' + top + '/' })
  if (parts.length >= 2) {
    const second = top + '/' + parts[1]
    if (SEG_LABELS[second]) result.push({ label: SEG_LABELS[second], link: '/' + second + '/' })
  }
  return result
})
</script>

<template>
  <nav v-if="crumbs.length" class="breadcrumbs" aria-label="Breadcrumb">
    <a href="/" class="bc-link">首页</a>
    <template v-for="(c, i) in crumbs" :key="i">
      <span class="bc-sep">›</span>
      <span v-if="i === crumbs.length - 1" class="bc-current">{{ c.label }}</span>
      <a v-else :href="c.link" class="bc-link">{{ c.label }}</a>
    </template>
  </nav>
</template>

<style scoped>
.breadcrumbs {
  font-size: 0.82rem;
  color: var(--vp-c-text-2);
  padding: 0 0 12px;
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}
.bc-link { color: var(--vp-c-text-2); text-decoration: none; }
.bc-link:hover { color: var(--vp-c-brand); }
.bc-sep { color: var(--vp-c-text-3); }
.bc-current { color: var(--vp-c-text-1); font-weight: 500; }
</style>
