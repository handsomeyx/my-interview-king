<script setup>
import ParticleLearningPath from './ParticleLearningPath.vue'
import data from './particle-paths/java.json'
</script>

<template>
  <ParticleLearningPath :data="data" title="Java 后端学习路径" height="520px" />
</template>
