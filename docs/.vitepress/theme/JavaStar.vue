<template>
  <RadialKnowledgeMap :data="data" :title="title" />
</template>

<script setup>
import RadialKnowledgeMap from './RadialKnowledgeMap.vue'
import data from './radial-paths/java.json'
defineProps({ title: { type: String, default: 'Java 学习路径' } })
</script>
