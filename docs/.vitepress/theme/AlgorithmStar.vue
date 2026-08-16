<template>
  <RadialKnowledgeMap :data="data" :title="title" />
</template>

<script setup>
import RadialKnowledgeMap from './RadialKnowledgeMap.vue'
import data from './radial-paths/algorithm.json'
defineProps({ title: { type: String, default: '算法学习路径' } })
</script>
