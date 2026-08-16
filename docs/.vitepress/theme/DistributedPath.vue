<script setup>
import ParticleLearningPath from './ParticleLearningPath.vue'
import data from './particle-paths/distributed.json'
</script>

<template>
  <ParticleLearningPath :data="data" title="分布式学习路径" height="520px" />
</template>
