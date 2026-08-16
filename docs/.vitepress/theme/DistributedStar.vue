<template>
  <RadialKnowledgeMap :data="data" :title="title" />
</template>

<script setup>
import RadialKnowledgeMap from './RadialKnowledgeMap.vue'
import data from './radial-paths/distributed.json'
defineProps({ title: { type: String, default: '分布式学习路径' } })
</script>
