<script setup>
import ParticleLearningPath from './ParticleLearningPath.vue'
import data from './particle-paths/algorithm.json'
</script>

<template>
  <ParticleLearningPath :data="data" title="算法学习三阶段路径" height="520px" />
</template>
