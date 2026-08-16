<template>
  <RadialKnowledgeMap :data="data" :title="title" />
</template>

<script setup>
import RadialKnowledgeMap from './RadialKnowledgeMap.vue'
import data from './radial-paths/projects.json'
defineProps({ title: { type: String, default: '项目实战学习路径' } })
</script>
