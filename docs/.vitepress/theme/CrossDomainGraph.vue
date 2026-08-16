<template>
  <div class="cdg-root">
    <div class="cdg-header">
      <h3 class="cdg-title">跨域知识关联</h3>
      <div class="cdg-legend">
        <span v-for="domain in domains" :key="domain.name" class="cdg-domain-chip" :style="{ '--c': domain.color }">
          {{ domain.name }}
        </span>
      </div>
    </div>
    <div class="cdg-canvas-wrap" ref="wrapRef">
      <canvas ref="canvas" class="cdg-canvas" />
      <div v-if="hoveredEdge" class="cdg-edge-tip" :style="edgeTipStyle">
        <span class="cdg-edge-label">{{ hoveredEdge.label }}</span>
      </div>
      <div v-if="hoveredNode" class="cdg-node-tip" :style="nodeTipStyle">
        <strong>{{ hoveredNode.label }}</strong>
        <em>{{ hoveredNode.domainName }}</em>
        <a v-if="hoveredNode.link" :href="hoveredNode.link">前往 →</a>
      </div>
    </div>
    <div class="cdg-footer">
      <span>悬停节点查看详情，悬停连线查看知识关联，点击跳转章节</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch, nextTick } from 'vue'

const props = defineProps({
  data: { type: Object, required: true },
  height: { type: String, default: '420px' }
})

const canvas = ref(null)
const wrapRef = ref(null)
const hoveredNode = ref(null)
const hoveredEdge = ref(null)

let ctx = null, dpr = 1, raf = 0
let nodes = [], edges = [], particles = []
let domains = []
let W = 0, H = 0
let dark = false
let hoveredEdgeT = -1

const domainColors = {
  '算法': '#38bdf8',
  'Java': '#f472b6',
  '分布式': '#f59e0b',
  'AI Agent': '#a78bfa',
  '项目': '#34d399'
}

function init(forceW, forceH) {
  if (!canvas.value) return
  const r = canvas.value.getBoundingClientRect()
  W = forceW || r.width || 600
  H = forceH || r.height || 420
  dpr = window.devicePixelRatio || 1
  canvas.value.width = W * dpr
  canvas.value.height = H * dpr
  ctx = canvas.value.getContext('2d')
  ctx.scale(dpr, dpr)

  const domainDefs = props.data.domains || []
  domains = domainDefs.map(d => ({
    name: d.name,
    color: d.color || domainColors[d.name] || '#64748b'
  }))

  nodes = []
  edges = []

  const cols = Math.min(domains.length, 3)
  const colW = W / cols
  domains.forEach((domain, di) => {
    const col = di % cols
    const x = colW * col + colW / 2
    const domainNodes = (props.data.nodes || []).filter(n => n.domain === domain.name)
    const cnt = domainNodes.length
    const availH = H - 70
    const gap = cnt > 1 ? availH / (cnt - 1) : 0
    domainNodes.forEach((node, ni) => {
      nodes.push({
        id: node.id,
        label: node.label,
        link: node.link || '#',
        domain: domain.name,
        color: domain.color,
        x,
        y: cnt === 1 ? H / 2 : 35 + ni * gap,
        r: 16,
        phase: Math.random() * Math.PI * 2
      })
    })
  })

  const rawEdges = props.data.edges || []
  for (const e of rawEdges) {
    const fn = nodes.find(n => n.id === e.from)
    const tn = nodes.find(n => n.id === e.to)
    if (!fn || !tn) continue
    edges.push({
      from: fn, to: tn,
      label: e.label || '',
      t: 0,
      speed: 0.002 + Math.random() * 0.002,
      particles: []
    })
  }

  for (const e of edges) {
    const cnt = 3 + Math.floor(Math.random() * 3)
    for (let i = 0; i < cnt; i++) {
      e.particles.push({ t: Math.random(), sp: e.speed, sz: 1 + Math.random(), a: 0.4 + Math.random() * 0.3 })
    }
  }
}

function bp(f, t, p) {
  const dx = t.x - f.x
  const dy = t.y - f.y
  const c1x = f.x + dx * 0.35
  const c1y = f.y + dy * 0.1
  const c2x = f.x + dx * 0.65
  const c2y = t.y - dy * 0.1
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

function drawFrame(t) {
  if (!ctx) return
  if (W === 0 || H === 0) return
  dark = document.documentElement.classList.contains('dark')
  ctx.clearRect(0, 0, W, H)

  const cols = Math.min(domains.length || 1, 3)
  const colW = W / cols

  for (let i = 0; i < domains.length; i++) {
    const col = i % cols
    const x0 = col * colW
    const x1 = (col + 1) * colW
    const g = ctx.createLinearGradient(x0, 0, x1, 0)
    g.addColorStop(0, rgba(domains[i].color, dark ? 0.05 : 0.03))
    g.addColorStop(0.5, rgba(domains[i].color, dark ? 0.015 : 0.01))
    g.addColorStop(1, rgba(domains[i].color, dark ? 0.05 : 0.03))
    ctx.fillStyle = g
    rr(x0 + 2, 18, colW - 4, H - 36, 12)
    ctx.fill()

    ctx.fillStyle = rgba(domains[i].color, 0.8)
    ctx.font = '600 11px -apple-system, BlinkMacSystemFont, sans-serif'
    ctx.textAlign = 'center'
    ctx.textBaseline = 'top'
    ctx.fillText(domains[i].name, x0 + colW / 2, 22)
  }

  for (const e of edges) {
    const baseA = dark ? 0.25 : 0.15
    ctx.strokeStyle = rgba(e.from.color, baseA)
    ctx.lineWidth = 1.2
    ctx.lineCap = 'round'
    ctx.beginPath()
    for (let p = 0; p <= 1.02; p += 0.04) {
      const pt = bp(e.from, e.to, p)
      p === 0 ? ctx.moveTo(pt.x, pt.y) : ctx.lineTo(pt.x, pt.y)
    }
    ctx.stroke()
  }

  const hE = hoveredEdge.value
  const hoverKey = hE ? `${hE.fromId || hE.from.id}-${hE.toId || hE.to.id}` : null

  for (const e of edges) {
    for (const p of e.particles) {
      p.t += p.sp
      if (p.t >= 1) p.t -= 1
      const pos = bp(e.from, e.to, p.t)
      const col = e.from.color
      ctx.save()
      ctx.shadowColor = rgba(col, 0.7)
      ctx.shadowBlur = 8
      ctx.fillStyle = rgba(col, p.a)
      ctx.beginPath()
      ctx.arc(pos.x, pos.y, p.sz, 0, Math.PI * 2)
      ctx.fill()
      ctx.restore()
    }

    if (e === hE) {
      const mid = bp(e.from, e.to, 0.5)
      const label = e.label
      ctx.save()
      ctx.font = '500 10px -apple-system, sans-serif'
      const tw = ctx.measureText(label).width + 10
      ctx.fillStyle = dark ? 'rgba(30,41,59,0.92)' : 'rgba(255,255,255,0.95)'
      rr(mid.x - tw / 2, mid.y - 9, tw, 18, 9)
      ctx.fill()
      ctx.fillStyle = e.from.color
      ctx.textAlign = 'center'
      ctx.textBaseline = 'middle'
      ctx.fillText(label, mid.x, mid.y)
      ctx.restore()
    }
  }

  const hN = hoveredNode.value?.id
  for (const n of nodes) {
    const phase = t * 0.002 + n.phase
    const pulse = (Math.sin(phase) + 1) * 0.5
    const hv = n.id === hN
    const r = n.r + (hv ? 3 : 0)

    ctx.save()
    ctx.shadowColor = rgba(n.color, hv ? 0.4 : 0.15)
    ctx.shadowBlur = hv ? 18 : 8 + pulse * 4
    const g = ctx.createRadialGradient(n.x, n.y, r * 0.3, n.x, n.y, r * 2)
    g.addColorStop(0, rgba(n.color, hv ? 0.3 : 0.15 + pulse * 0.05))
    g.addColorStop(1, rgba(n.color, 0))
    ctx.fillStyle = g
    ctx.beginPath()
    ctx.arc(n.x, n.y, r * 2, 0, Math.PI * 2)
    ctx.fill()
    ctx.restore()

    ctx.save()
    const core = ctx.createRadialGradient(
      n.x - r * 0.3, n.y - r * 0.35, r * 0.05,
      n.x, n.y, r
    )
    core.addColorStop(0, dark ? 'rgba(30,41,59,0.95)' : 'rgba(255,255,255,0.98)')
    core.addColorStop(0.4, rgba(n.color, 0.9))
    core.addColorStop(1, rgba(n.color, 0.7))
    ctx.fillStyle = core
    ctx.beginPath()
    ctx.arc(n.x, n.y, r, 0, Math.PI * 2)
    ctx.fill()
    ctx.restore()

    ctx.save()
    ctx.strokeStyle = rgba(n.color, hv ? 0.9 : 0.5)
    ctx.lineWidth = hv ? 1.8 : 1
    ctx.beginPath()
    ctx.arc(n.x, n.y, r, 0, Math.PI * 2)
    ctx.stroke()
    ctx.restore()

    ctx.save()
    ctx.font = `500 ${hv ? 11 : 10}px -apple-system, BlinkMacSystemFont, sans-serif`
    ctx.textAlign = 'center'
    ctx.textBaseline = 'top'
    ctx.fillStyle = dark ? '#cbd5e1' : '#475569'
    ctx.fillText(n.label, n.x, n.y + r + 6)
    ctx.restore()
  }

  raf = requestAnimationFrame(drawFrame)
}

function onMove(e) {
  if (!canvas.value) return
  const rect = canvas.value.getBoundingClientRect()
  const x = e.clientX - rect.left
  const y = e.clientY - rect.top

  let foundNode = null
  for (const n of nodes) {
    const dx = x - n.x, dy = y - n.y
    if (Math.sqrt(dx*dx + dy*dy) < n.r + 6) { foundNode = n; break }
  }

  if (foundNode) {
    hoveredNode.value = foundNode
    hoveredEdge.value = null
    canvas.value.style.cursor = foundNode.link !== '#' ? 'pointer' : 'default'
    return
  }

  let foundEdge = null
  for (const e of edges) {
    let minDist = Infinity
    for (let p = 0; p <= 1.02; p += 0.03) {
      const pt = bp(e.from, e.to, p)
      const dx = x - pt.x, dy = y - pt.y
      const d = Math.sqrt(dx*dx + dy*dy)
      if (d < minDist) minDist = d
    }
    if (minDist < 6) { foundEdge = e; break }
  }
  hoveredEdge.value = foundEdge
  hoveredNode.value = null
  canvas.value.style.cursor = foundEdge ? 'pointer' : 'default'
}

function onClick(e) {
  if (!canvas.value) return
  const rect = canvas.value.getBoundingClientRect()
  const x = e.clientX - rect.left
  const y = e.clientY - rect.top
  for (const n of nodes) {
    const dx = x - n.x, dy = y - n.y
    if (Math.sqrt(dx*dx + dy*dy) < n.r + 6 && n.link && n.link !== '#') {
      window.location.href = n.link
      return
    }
  }
}

const nodeTipStyle = computed(() => {
  if (!hoveredNode.value) return {}
  const n = hoveredNode.value
  let l = n.x, t = n.y - 14
  if (l < 80) l = n.x + 80
  if (l > W - 80) l = n.x - 80
  return { left: l + 'px', top: t + 'px' }
})

const edgeTipStyle = computed(() => {
  if (!hoveredEdge.value) return {}
  const e = hoveredEdge.value
  const mid = bp(e.from, e.to, 0.5)
  return { left: mid.x + 'px', top: mid.y + 'px' }
})

let bound = false

onMounted(() => {
  nextTick(() => {
    if (!canvas.value) return
    const r = canvas.value.getBoundingClientRect()
    if (r.width < 10 || r.height < 10) {
      requestAnimationFrame(() => {
        const r2 = canvas.value.getBoundingClientRect()
        W = r2.width || 600
        H = r2.height || 420
        doInit()
      })
      return
    }
    W = r.width
    H = r.height
    doInit()
  })
})

function doInit() {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (reduce) return
  init(W, H)
  raf = requestAnimationFrame(drawFrame)
  canvas.value.addEventListener('mousemove', onMove)
  canvas.value.addEventListener('click', onClick)
  window.addEventListener('resize', () => init())
  bound = true
}

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
.cdg-root {
  margin: 20px 0;
  border-radius: 14px;
  overflow: hidden;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
}

.cdg-header {
  padding: 12px 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
  border-bottom: 1px solid var(--vp-c-divider);
}

.cdg-title {
  font-size: 0.92rem;
  font-weight: 600;
  margin: 0;
  color: var(--vp-c-text-1);
}

.cdg-legend {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
}

.cdg-domain-chip {
  font-size: 0.68rem;
  padding: 2px 9px;
  border-radius: 8px;
  color: var(--c);
  background: color-mix(in srgb, var(--c) 10%, transparent);
  border: 1px solid color-mix(in srgb, var(--c) 20%, transparent);
  font-weight: 500;
}

.cdg-canvas-wrap {
  position: relative;
  width: 100%;
  height: v-bind('height');
}

.cdg-canvas {
  display: block;
  width: 100%;
  height: 100%;
}

.cdg-node-tip {
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
  min-width: 110px;
  opacity: 0;
  transition: opacity 0.12s ease;
}
.cdg-node-tip[style*="left"] { opacity: 1; }

.cdg-node-tip strong {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
}

.cdg-node-tip em {
  font-size: 0.66rem;
  font-style: normal;
  color: var(--vp-c-text-3);
}

.cdg-node-tip a {
  font-size: 0.72rem;
  font-weight: 500;
  color: var(--vp-c-brand);
  text-decoration: none;
  margin-top: 2px;
}
.cdg-node-tip a:hover { text-decoration: underline; }

.cdg-edge-tip {
  position: absolute;
  z-index: 10;
  transform: translate(-50%, -100%);
  pointer-events: none;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  padding: 4px 10px;
  font-size: 0.72rem;
  font-weight: 500;
  color: var(--vp-c-text-2);
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.12s ease;
}
.cdg-edge-tip[style*="left"] { opacity: 1; }

.cdg-footer {
  padding: 8px 18px;
  border-top: 1px solid var(--vp-c-divider);
  font-size: 0.72rem;
  color: var(--vp-c-text-3);
}
</style>
