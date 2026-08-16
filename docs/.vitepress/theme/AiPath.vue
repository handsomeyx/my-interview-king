<script setup>
import ParticleLearningPath from './ParticleLearningPath.vue'
import data from './particle-paths/ai.json'
</script>

<template>
  <ParticleLearningPath :data="data" title="AI Agent 学习路径" height="520px" />
</template>
