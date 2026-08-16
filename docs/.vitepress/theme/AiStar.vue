<template>
  <RadialKnowledgeMap :data="data" :title="title" />
</template>

<script setup>
import RadialKnowledgeMap from './RadialKnowledgeMap.vue'
import data from './radial-paths/ai.json'
defineProps({ title: { type: String, default: 'AI Agent 学习路径' } })
</script>
