<template>
  <canvas ref="canvas" class="particle-canvas"></canvas>
</template>

<script setup>
import { onMounted, ref, onUnmounted } from 'vue'

const canvas = ref(null)
let ctx, particles = [], animationFrame = 0
const mouse = { x: null, y: null, radius: 100 }

class Particle {
  constructor(w, h) {
    this.x = Math.random() * w
    this.y = Math.random() * h
    this.size = Math.random() * 2 + 1
    this.vx = (Math.random() - 0.5) * 1.5
    this.vy = (Math.random() - 0.5) * 1.5
  }
  update() {
    this.x += this.vx
    this.y += this.vy

    if (this.x < 0 || this.x > canvas.value.width) this.vx *= -1
    if (this.y < 0 || this.y > canvas.value.height) this.vy *= -1

    if (mouse.x !== null && mouse.y !== null) {
      const dx = mouse.x - this.x
      const dy = mouse.y - this.y
      const distance = Math.sqrt(dx * dx + dy * dy)
      if (distance > 0 && distance < mouse.radius) {
        const force = (mouse.radius - distance) / mouse.radius
        this.x -= (dx / distance) * force * 5
        this.y -= (dy / distance) * force * 5
      }
    }

    if (Math.random() < 0.01) {
      this.vx += (Math.random() - 0.5) * 0.5
      this.vy += (Math.random() - 0.5) * 0.5
      const speed = Math.sqrt(this.vx * this.vx + this.vy * this.vy)
      if (speed > 1.5) {
        this.vx *= 0.8
        this.vy *= 0.8
      }
    }
  }
  draw() {
    const isDarkMode = document.documentElement.classList.contains('dark')
    ctx.fillStyle = isDarkMode ? 'rgba(56, 189, 248, 0.4)' : 'rgba(59, 130, 246, 0.4)'
    ctx.beginPath()
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2)
    ctx.fill()
  }
}

const PARTICLE_CAP = 150
const computeCount = (w, h) => Math.min(PARTICLE_CAP, Math.round((w * h) / 13000))

const init = () => {
  canvas.value.width = window.innerWidth
  canvas.value.height = window.innerHeight
  particles = []
  const count = computeCount(canvas.value.width, canvas.value.height)
  for (let i = 0; i < count; i++) {
    particles.push(new Particle(canvas.value.width, canvas.value.height))
  }
}

const animate = () => {
  ctx.clearRect(0, 0, canvas.value.width, canvas.value.height)
  particles.forEach(p => { p.update(); p.draw() })
  animationFrame = requestAnimationFrame(animate)
}

const onMouseMove = (e) => { mouse.x = e.x; mouse.y = e.y }
const onResize = () => init()
const onVisibilityChange = () => {
  if (document.hidden) {
    if (animationFrame) {
      cancelAnimationFrame(animationFrame)
      animationFrame = 0
    }
  } else if (!animationFrame && ctx) {
    animate()
  }
}

let listenersBound = false

onMounted(() => {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  const isMobile = window.matchMedia('(max-width: 768px)').matches
  // 移动端/无障碍模式下不启动动画，canvas 仅保留 CSS 渐变底色
  if (reduceMotion || isMobile) return

  ctx = canvas.value.getContext('2d')
  init()
  animate()
  window.addEventListener('mousemove', onMouseMove, { passive: true })
  window.addEventListener('resize', onResize)
  document.addEventListener('visibilitychange', onVisibilityChange)
  listenersBound = true
})

onUnmounted(() => {
  if (animationFrame) cancelAnimationFrame(animationFrame)
  animationFrame = 0
  if (listenersBound) {
    window.removeEventListener('mousemove', onMouseMove)
    window.removeEventListener('resize', onResize)
    document.removeEventListener('visibilitychange', onVisibilityChange)
    listenersBound = false
  }
})
</script>

<style scoped>
.particle-canvas {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: -1; /* 确保在内容最底层 */
  pointer-events: none; /* 让鼠标事件穿透，不影响点击按钮 */
  background: radial-gradient(circle at center, #ffffff 0%, #f1f4f8 100%); /* 渐变底色 */
}

/* 深色模式背景 */
:root.dark .particle-canvas {
  background: radial-gradient(circle at center, #0a192f 0%, #1e293b 100%);
}
</style>