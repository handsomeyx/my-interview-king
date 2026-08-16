<template>
  <CrossDomainGraph :data="data" />
</template>

<script setup>
import CrossDomainGraph from './CrossDomainGraph.vue'
import data from './cross-domain/java.json'
</script>
