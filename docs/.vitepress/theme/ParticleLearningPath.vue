<template>
  <div class="plp-root">
    <div v-if="showHeader" class="plp-header">
      <div class="plp-title-row">
        <h3 class="plp-title">{{ title }}</h3>
        <span class="plp-pill">
          <span class="plp-pill-dot" />
          {{ overallPct }}% 已掌握
        </span>
      </div>
      <div class="plp-legend">
        <span v-for="stage in stages" :key="stage.name" class="plp-stage-tag" :style="{ '--c': stage.color }">
          {{ stage.name.split('：')[0] }}
        </span>
      </div>
    </div>

    <div class="plp-canvas-wrap" ref="wrapRef">
      <canvas ref="canvas" class="plp-canvas" />
      <div v-if="hoveredNode" class="plp-tip" :style="tipStyle">
        <strong>{{ stripEmoji(hoveredNode.label) }}</strong>
        <em>{{ hoveredNode.stageName }}</em>
        <a :href="hoveredNode.link">前往 →</a>
      </div>
    </div>

    <div v-if="showFooter" class="plp-footer">
      <span>悬停查看，点击跳转</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch, nextTick } from 'vue'
import { getMastery } from './study-storage'

const props = defineProps({
  data: { type: Object, required: true },
  title: { type: String, default: '' },
  showHeader: { type: Boolean, default: true },
  showFooter: { type: Boolean, default: true },
  height: { type: String, default: '480px' }
})

const canvas = ref(null)
const wrapRef = ref(null)
const hoveredNode = ref(null)

let ctx = null, dpr = 1, raf = 0
let nodes = [], edges = [], particles = []
let regions = []
let W = 0, H = 0
let dark = false

const stages = computed(() => props.data.stages || [])

const allIds = computed(() => {
  const ids = []
  stages.value.forEach(s => s.nodes.forEach(n => ids.push(n.path)))
  return ids
})

const overallPct = computed(() => {
  const m = getMastery()
  const total = allIds.value.length
  const done = allIds.value.filter(id => m[id] === 'mastered').length
  return total > 0 ? Math.round((done / total) * 100) : 0
})

const tipStyle = computed(() => {
  if (!hoveredNode.value) return {}
  const n = hoveredNode.value
  let x = n.x, y = n.y - 12
  if (x < 90) x = n.x + 100
  if (x > W - 90) x = n.x - 100
  return { left: x + 'px', top: y + 'px' }
})

function stripEmoji(label) {
  return label.replace(/[\u{1F300}-\u{1FAFF}]|[\u{2600}-\u{27BF}]|^\s+/u, '').trim()
}

function init() {
  if (!canvas.value) return
  const r = canvas.value.getBoundingClientRect()
  W = r.width
  H = r.height
  dpr = window.devicePixelRatio || 1
  canvas.value.width = W * dpr
  canvas.value.height = H * dpr
  ctx = canvas.value.getContext('2d')
  ctx.scale(dpr, dpr)

  regions = []
  nodes = []
  const n = stages.value.length
  const gap = 8
  const totalW = W - gap * (n - 1)
  const w = totalW / n

  for (let i = 0; i < n; i++) {
    const x0 = i * (w + gap)
    const stage = stages.value[i]
    const cnt = stage.nodes.length
    const pt = 44, pb = 36
    const h = H - pt - pb
    const sp = cnt > 1 ? h / (cnt - 1) : 0

    regions.push({
      x: x0, y: pt - 16, w, h: h + 32,
      color: stage.color, name: stage.name
    })

    for (let j = 0; j < cnt; j++) {
      nodes.push({
        id: stage.nodes[j].id || `${i}-${j}`,
        label: stage.nodes[j].label || stage.nodes[j].title || '',
        link: stage.nodes[j].link || '#',
        x: x0 + w / 2,
        y: cnt === 1 ? H / 2 : pt + j * sp,
        color: stage.color,
        r: 20,
        phase: Math.random() * Math.PI * 2
      })
    }
  }

  edges = (props.data.edges || [])
    .map(e => ({
      fromId: e.from, toId: e.to,
      fn: nodes.find(x => x.id === e.from),
      tn: nodes.find(x => x.id === e.to)
    }))
    .filter(e => e.fn && e.tn)

  particles = []
  for (const e of edges) {
    const cnt = 5 + Math.floor(Math.random() * 3)
    for (let i = 0; i < cnt; i++) {
      particles.push({
        e, t: i / cnt,
        sp: 0.0025 + Math.random() * 0.003,
        sz: 1.5 + Math.random(),
        a: 0.5 + Math.random() * 0.4
      })
    }
  }
}

function bp(f, t, p) {
  const c1x = f.x + (t.x - f.x) * 0.5
  const c1y = f.y
  const c2x = t.x - (t.x - f.x) * 0.5
  const c2y = t.y
  const m = 1 - p
  return {
    x: m*m*m*f.x + 3*m*m*p*c1x + 3*m*p*p*c2x + p*p*p*t.x,
    y: m*m*m*f.y + 3*m*m*p*c1y + 3*m*p*p*c2y + p*p*p*t.y
  }
}

function rgba(hex, a) {
  return `rgba(${parseInt(hex.slice(1,3),16)},${parseInt(hex.slice(3,5),16)},${parseInt(hex.slice(5,7),16)},${a})`
}

function rr(x, y, w, h, r) {
  ctx.beginPath()
  ctx.moveTo(x+r, y)
  ctx.lineTo(x+w-r, y)
  ctx.quadraticCurveTo(x+w, y, x+w, y+r)
  ctx.lineTo(x+w, y+h-r)
  ctx.quadraticCurveTo(x+w, y+h, x+w-r, y+h)
  ctx.lineTo(x+r, y+h)
  ctx.quadraticCurveTo(x, y+h, x, y+h-r)
  ctx.lineTo(x, y+r)
  ctx.quadraticCurveTo(x, y, x+r, y)
  ctx.closePath()
}

function frame(t) {
  if (!ctx) return
  dark = document.documentElement.classList.contains('dark')
  ctx.clearRect(0, 0, W, H)

  for (const rg of regions) {
    const g = ctx.createLinearGradient(rg.x, 0, rg.x + rg.w, 0)
    g.addColorStop(0, rgba(rg.color, dark ? 0.06 : 0.035))
    g.addColorStop(0.5, rgba(rg.color, dark ? 0.02 : 0.012))
    g.addColorStop(1, rgba(rg.color, dark ? 0.06 : 0.035))
    ctx.fillStyle = g
    rr(rg.x + 1, rg.y, rg.w - 2, rg.h, 14)
    ctx.fill()
  }

  for (const rg of regions) {
    ctx.fillStyle = rgba(rg.color, 0.85)
    ctx.font = '600 11px -apple-system, BlinkMacSystemFont, sans-serif'
    ctx.textAlign = 'center'
    ctx.textBaseline = 'top'
    const label = rg.name.split('：')[0]
    ctx.fillText(label, rg.x + rg.w / 2, rg.y + 6)
  }

  for (const e of edges) {
    ctx.strokeStyle = rgba(e.fn.color, dark ? 0.3 : 0.18)
    ctx.lineWidth = 1.5
    ctx.lineCap = 'round'
    ctx.beginPath()
    for (let p = 0; p <= 1.01; p += 0.04) {
      const pt = bp(e.fn, e.tn, p)
      p === 0 ? ctx.moveTo(pt.x, pt.y) : ctx.lineTo(pt.x, pt.y)
    }
    ctx.stroke()
  }

  for (const p of particles) {
    p.t += p.sp
    if (p.t >= 1) p.t -= 1
    const pos = bp(p.e.fn, p.e.tn, p.t)
    const col = p.e.fn.color

    ctx.save()
    ctx.shadowColor = rgba(col, 0.8)
    ctx.shadowBlur = 10
    ctx.fillStyle = rgba(col, p.a)
    ctx.beginPath()
    ctx.arc(pos.x, pos.y, p.sz, 0, Math.PI * 2)
    ctx.fill()
    ctx.restore()

    if (p.t > 0.02) {
      const tp = bp(p.e.fn, p.e.tn, Math.max(0, p.t - 0.06))
      ctx.fillStyle = rgba(col, p.a * 0.3)
      ctx.beginPath()
      ctx.arc(tp.x, tp.y, p.sz * 0.6, 0, Math.PI * 2)
      ctx.fill()
    }
  }

  const hoverId = hoveredNode.value?.id
  for (const n of nodes) {
    const phase = t * 0.002 + n.phase
    const pulse = (Math.sin(phase) + 1) * 0.5
    const hovered = n.id === hoverId
    const r = n.r + (hovered ? 3 : 0)

    ctx.save()
    ctx.shadowColor = rgba(n.color, hovered ? 0.4 : 0.18)
    ctx.shadowBlur = hovered ? 20 : 10 + pulse * 6
    const g = ctx.createRadialGradient(n.x, n.y, r * 0.3, n.x, n.y, r * 1.8)
    g.addColorStop(0, rgba(n.color, hovered ? 0.35 : 0.18 + pulse * 0.08))
    g.addColorStop(1, rgba(n.color, 0))
    ctx.fillStyle = g
    ctx.beginPath()
    ctx.arc(n.x, n.y, r * 1.8, 0, Math.PI * 2)
    ctx.fill()
    ctx.restore()

    ctx.save()
    const core = ctx.createRadialGradient(
      n.x - r * 0.3, n.y - r * 0.35, r * 0.05,
      n.x, n.y, r
    )
    core.addColorStop(0, dark ? 'rgba(30,41,59,0.95)' : 'rgba(255,255,255,0.98)')
    core.addColorStop(0.4, rgba(n.color, 0.92))
    core.addColorStop(1, rgba(n.color, 0.72))
    ctx.fillStyle = core
    ctx.beginPath()
    ctx.arc(n.x, n.y, r, 0, Math.PI * 2)
    ctx.fill()
    ctx.restore()

    ctx.save()
    ctx.strokeStyle = rgba(n.color, hovered ? 0.95 : 0.55)
    ctx.lineWidth = hovered ? 2 : 1.2
    ctx.beginPath()
    ctx.arc(n.x, n.y, r, 0, Math.PI * 2)
    ctx.stroke()
    ctx.restore()

    const emojiMatch = n.label.match(/[\u{1F300}-\u{1FAFF}]|[\u{2600}-\u{27BF}]/u)
    const emoji = emojiMatch ? emojiMatch[0] : ''
    const text = stripEmoji(n.label)

    ctx.save()
    ctx.textAlign = 'center'
    ctx.textBaseline = 'middle'
    ctx.font = `${Math.round(r * 0.65)}px -apple-system, "Segoe UI Emoji", sans-serif`
    ctx.fillText(emoji, n.x, n.y)
    ctx.restore()

    ctx.save()
    ctx.font = `500 12px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`
    ctx.textAlign = 'center'
    ctx.textBaseline = 'top'
    ctx.fillStyle = dark ? '#cbd5e1' : '#475569'
    ctx.fillText(text, n.x, n.y + r + 8)
    ctx.restore()
  }

  raf = requestAnimationFrame(frame)
}

function onMove(e) {
  if (!canvas.value) return
  const rect = canvas.value.getBoundingClientRect()
  const x = e.clientX - rect.left
  const y = e.clientY - rect.top
  let found = null
  for (const n of nodes) {
    const dx = x - n.x, dy = y - n.y
    if (Math.sqrt(dx*dx + dy*dy) < n.r + 6) { found = n; break }
  }
  if (found !== hoveredNode.value) {
    hoveredNode.value = found
    canvas.value.style.cursor = found ? 'pointer' : 'default'
  }
}

function onClick(e) {
  if (!canvas.value) return
  const rect = canvas.value.getBoundingClientRect()
  const x = e.clientX - rect.left
  const y = e.clientY - rect.top
  for (const n of nodes) {
    const dx = x - n.x, dy = y - n.y
    if (Math.sqrt(dx*dx + dy*dy) < n.r + 6) {
      if (n.link && n.link !== '#') {
        window.location.href = n.link
      }
      break
    }
  }
}

let bound = false

onMounted(() => {
  if (!canvas.value) return
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (reduce) return
  init()
  raf = requestAnimationFrame(frame)
  canvas.value.addEventListener('mousemove', onMove)
  canvas.value.addEventListener('click', onClick)
  window.addEventListener('resize', init)
  bound = true
})

onUnmounted(() => {
  if (raf) cancelAnimationFrame(raf)
  raf = 0
  if (bound && canvas.value) {
    canvas.value.removeEventListener('mousemove', onMove)
    canvas.value.removeEventListener('click', onClick)
    window.removeEventListener('resize', init)
    bound = false
  }
})

watch(() => props.data, () => { init() }, { deep: true })
</script>

<style scoped>
.plp-root {
  margin: 24px 0;
  border-radius: 14px;
  overflow: hidden;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
}

.plp-header {
  padding: 14px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
  border-bottom: 1px solid var(--vp-c-divider);
}

.plp-title-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.plp-title {
  font-size: 0.98rem;
  font-weight: 600;
  margin: 0;
  color: var(--vp-c-text-1);
}

.plp-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 3px 10px;
  border-radius: 10px;
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--vp-c-text-2);
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
}

.plp-pill-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #10b981;
}

.plp-legend {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.plp-stage-tag {
  font-size: 0.72rem;
  padding: 2px 10px;
  border-radius: 10px;
  color: var(--c);
  background: color-mix(in srgb, var(--c) 10%, transparent);
  border: 1px solid color-mix(in srgb, var(--c) 20%, transparent);
  font-weight: 500;
}

.plp-canvas-wrap {
  position: relative;
  width: 100%;
  height: v-bind('height');
}

.plp-canvas {
  display: block;
  width: 100%;
  height: 100%;
}

.plp-tip {
  position: absolute;
  z-index: 10;
  transform: translate(-50%, -100%);
  pointer-events: auto;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 8px 12px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 120px;
}

.plp-tip strong {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
}

.plp-tip em {
  font-size: 0.68rem;
  font-style: normal;
  color: var(--vp-c-text-3);
}

.plp-tip a {
  font-size: 0.74rem;
  font-weight: 500;
  color: var(--vp-c-brand);
  text-decoration: none;
  margin-top: 2px;
}
.plp-tip a:hover { text-decoration: underline; }

.plp-footer {
  padding: 8px 20px;
  border-top: 1px solid var(--vp-c-divider);
  font-size: 0.74rem;
  color: var(--vp-c-text-3);
}
</style>
