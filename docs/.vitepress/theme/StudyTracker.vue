<script setup>
import { onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useRoute } from 'vitepress'
import { setProgress, pushRecent } from './study-storage'

const route = useRoute()
let ticking = false

const getTitle = () =>
  (document.title.replace(/\s*[-|].*$/, '').trim()) || route.path

const record = () => {
  const path = route.path
  if (!path || path === '/') {
    ticking = false
    return
  }
  const scrollable = document.documentElement.scrollHeight - window.innerHeight
  const ratio = scrollable > 0 ? window.scrollY / scrollable : 0
  setProgress(path, getTitle(), Math.min(1, Math.max(0, ratio)))
  ticking = false
}

const onScroll = () => {
  if (!ticking) {
    requestAnimationFrame(record)
    ticking = true
  }
}

const visit = (path) => {
  if (!path || path === '/') return
  pushRecent(path, getTitle())
}

onMounted(() => {
  visit(route.path)
  record()
  window.addEventListener('scroll', onScroll, { passive: true })
  window.addEventListener('resize', onScroll, { passive: true })
})

watch(
  () => route.path,
  (p) => {
    visit(p)
    nextTick(() => setTimeout(record, 300))
  }
)

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
  window.removeEventListener('resize', onScroll)
})
</script>

<template>
  <span style="display: none" />
</template>
