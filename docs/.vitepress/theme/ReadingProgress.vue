<template>
  <div ref="bar" class="reading-progress" />
  <Transition name="fade-up">
    <button v-show="show" class="back-to-top" aria-label="返回顶部" @click="scrollTop">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7" /></svg>
    </button>
  </Transition>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useRoute } from 'vitepress'

const bar = ref(null)
const show = ref(false)
let ticking = false

const update = () => {
  const scrollable = document.documentElement.scrollHeight - window.innerHeight
  const ratio = scrollable > 0 ? window.scrollY / scrollable : 0
  if (bar.value) bar.value.style.transform = `scaleX(${ratio})`
  show.value = window.scrollY > 400
  ticking = false
}

const onScroll = () => {
  if (!ticking) {
    requestAnimationFrame(update)
    ticking = true
  }
}

const scrollTop = () => window.scrollTo({ top: 0, behavior: 'smooth' })

const route = useRoute()
watch(() => route.path, () => nextTick(update))

onMounted(() => {
  update()
  window.addEventListener('scroll', onScroll, { passive: true })
  window.addEventListener('resize', onScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
  window.removeEventListener('resize', onScroll)
})
</script>

<style scoped>
.reading-progress {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  transform: scaleX(0);
  transform-origin: left center;
  background: linear-gradient(90deg, #38bdf8, #8b5cf6);
  z-index: 100;
  pointer-events: none;
}

.back-to-top {
  position: fixed;
  right: 24px;
  bottom: 24px;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 50%;
  background: var(--vp-c-brand, #38bdf8);
  color: #fff;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.18);
  z-index: 100;
  transition: opacity .2s, transform .2s;
}
.back-to-top:hover { transform: translateY(-2px); }

.fade-up-enter-active, .fade-up-leave-active { transition: opacity .2s, transform .2s; }
.fade-up-enter-from, .fade-up-leave-to { opacity: 0; transform: translateY(10px); }

@media (max-width: 768px) {
  .back-to-top { right: 16px; bottom: 16px; width: 40px; height: 40px; }
}
</style>
