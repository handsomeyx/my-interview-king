<script setup>
import ParticleLearningPath from './ParticleLearningPath.vue'
import data from './particle-paths/projects.json'
</script>

<template>
  <ParticleLearningPath :data="data" title="项目实战学习路径" height="520px" />
</template>
