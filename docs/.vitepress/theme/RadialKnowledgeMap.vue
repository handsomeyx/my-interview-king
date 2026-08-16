<template>
  <div class="rkm-root" ref="rootRef">
    <div v-if="showHeader" class="rkm-header">
      <h3 class="rkm-title">{{ title }}</h3>
      <div class="rkm-legend">
        <span v-for="s in stages" :key="s.name" class="rkm-stage-chip" :style="{ '--c': s.color }">
          {{ s.name.split('：')[0] }}
        </span>
      </div>
    </div>
    <div class="rkm-canvas-wrap" ref="wrapRef">
      <canvas ref="canvas" class="rkm-canvas" />
      <div v-if="hoveredNode" class="rkm-tip" :style="tipStyle">
        <strong>{{ hoveredNode.label }}</strong>
        <em v-if="hoveredNode.description">{{ hoveredNode.description }}</em>
        <a v-if="hoveredNode.link" :href="hoveredNode.link">前往 →</a>
        <span v-if="hoveredNode.hasChildren" class="rkm-tip-hint">{{ hoveredNode.expanded ? '点击收起' : '点击展开' }}</span>
      </div>
      <div class="rkm-center-hint" v-if="showCenterHint">
        点击节点逐步展开 · 探索知识体系
      </div>
    </div>
    <div v-if="showFooter" class="rkm-footer">
      <span>点击节点展开 / 收起 · 点击叶子节点跳转章节</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch, nextTick } from 'vue'

const props = defineProps({
  data: { type: Object, required: true },
  title: { type: String, default: '' },
  showHeader: { type: Boolean, default: true },
  showFooter: { type: Boolean, default: true },
  height: { type: String, default: '520px' }
})

const canvas = ref(null)
const wrapRef = ref(null)
const rootRef = ref(null)
const hoveredNode = ref(null)

let ctx = null, dpr = 1, raf = 0
let dark = false
let W = 0, H = 0
let cx = 0, cy = 0
let nodes = []
let edges = []
let particles = []
let stages = []
let rootNode = null
let expandedIds = new Set()
let animatingNodes = new Map()
let hoveredNodeRef = null

const showCenterHint = computed(() => {
  return nodes.length > 0 && expandedIds.size === 0
})

const MIN_DIST = 90
const MAX_DEPTH = 3

function hexToRgba(hex, a) {
  return `rgba(${parseInt(hex.slice(1,3),16)},${parseInt(hex.slice(3,5),16)},${parseInt(hex.slice(5,7),16)},${a})`
}

function initData() {
  expandedIds.clear()
  animatingNodes.clear()
  particles = []
  nodes = []
  edges = []

  stages = props.data.stages || []

  const root = props.data.root || { label: '知识库', color: '#38bdf8' }
  rootNode = {
    id: 'root',
    label: root.label,
    color: root.color,
    link: root.link || '',
    description: root.description || '',
    depth: 0,
    parentId: null,
    children: [],
    expanded: true,
    x: cx,
    y: cy,
    targetX: cx,
    targetY: cy,
    renderX: cx,
    renderY: cy,
    appear: 1,
    visible: true,
    hasChildren: true
  }

  nodes.push(rootNode)

  const rawChildren = props.data.children || []
  for (const child of rawChildren) {
    const node = createNode(child, 'root', 1)
    rootNode.children.push(node)
    nodes.push(node)
  }

  computeTargets()

  const level1Nodes = nodes.filter(n => n.depth === 1)
  for (const n of level1Nodes) {
    expandedIds.add(n.id)
    n.expanded = true
  }
  computeVisible()
  rebuildEdges()

  for (const node of nodes) {
    if (node.depth === 0) {
      node.renderX = cx
      node.renderY = cy
      node.appear = 1
    } else if (node.visible) {
      const parent = nodes.find(n => n.id === node.parentId)
      node.renderX = parent ? parent.targetX : cx
      node.renderY = parent ? parent.targetY : cy
      node.appear = 0
      startAnimation(node, true)
    }
  }
}

function createNode(data, parentId, depth) {
  const stage = stages.find(s => s.children?.some(c => c.id === data.id))
  const color = data.color || (stage ? stage.color : '#64748b')
  const node = {
    id: data.id,
    label: data.label,
    color: color,
    link: data.link || '',
    description: data.description || '',
    depth: depth,
    parentId: parentId,
    children: [],
    expanded: false,
    x: cx,
    y: cy,
    targetX: cx,
    targetY: cy,
    renderX: cx,
    renderY: cy,
    appear: 0,
    visible: false,
    hasChildren: !!(data.children && data.children.length > 0)
  }
  if (data.children) {
    for (const child of data.children) {
      const childNode = createNode(child, data.id, depth + 1)
      node.children.push(childNode)
      nodes.push(childNode)
    }
  }
  return node
}

function computeTargets() {
  const rings = []
  for (let d = 1; d <= MAX_DEPTH; d++) {
    rings.push({
      baseRadius: 110 + (d - 1) * 120,
      nodeRadius: 26 - (d - 1) * 4
    })
  }

  for (const node of nodes) {
    if (node.depth === 0) {
      node.targetX = cx
      node.targetY = cy
      continue
    }

    const parent = nodes.find(n => n.id === node.parentId)
    if (!parent) continue

    if (node.depth === 1) {
      const siblings = nodes.filter(n => n.parentId === 'root')
      const idx = siblings.indexOf(node)
      const total = siblings.length
      const ring = rings[0]
      const angle = (idx / total) * Math.PI * 2 - Math.PI / 2
      node.targetX = cx + Math.cos(angle) * ring.baseRadius
      node.targetY = cy + Math.sin(angle) * ring.baseRadius
    } else {
      const parentAngle = Math.atan2(parent.targetY - cy, parent.targetX - cx)
      const ring = rings[node.depth - 1]
      const siblings = nodes.filter(n => n.parentId === node.parentId)
      const idx = siblings.indexOf(node)
      const total = siblings.length

      const spread = Math.min(Math.PI * 0.8, 0.35 + total * 0.18)
      let startAngle, endAngle
      if (total === 1) {
        startAngle = parentAngle - 0.15
        endAngle = parentAngle + 0.15
      } else {
        startAngle = parentAngle - spread / 2
        endAngle = parentAngle + spread / 2
      }
      const t = idx / Math.max(total - 1, 1)
      const angle = startAngle + t * (endAngle - startAngle)
      node.targetX = cx + Math.cos(angle) * ring.baseRadius
      node.targetY = cy + Math.sin(angle) * ring.baseRadius
    }

    node.nodeRadius = rings[node.depth - 1]?.nodeRadius || 20
  }
}

function computeVisible() {
  for (const node of nodes) {
    if (node.depth === 0) {
      node.visible = true
      continue
    }
    const parent = nodes.find(n => n.id === node.parentId)
    node.visible = !!(parent && parent.visible && parent.expanded)
  }
  rebuildEdges()
}

function rebuildEdges() {
  edges = []
  for (const node of nodes) {
    if (node.depth === 0) continue
    if (!node.visible) continue
    const parent = nodes.find(n => n.id === node.parentId)
    if (parent && parent.visible) {
      edges.push({ from: parent, to: node })
    }
  }
}

function startAnimation(node, appear) {
  animatingNodes.set(node.id, {
    node: node,
    fromX: node.renderX,
    fromY: node.renderY,
    toX: node.targetX,
    toY: node.targetY,
    fromAppear: node.appear,
    toAppear: appear ? 1 : 0,
    t: 0,
    duration: 500,
    done: false
  })
}

function startChildrenAnimation(parent, expanded) {
  const children = nodes.filter(n => n.parentId === parent.id)
  for (const child of children) {
    if (expanded) {
      child.visible = true
      child.renderX = parent.x
      child.renderY = parent.y
      child.appear = 0
      startAnimation(child, true)
      child.x = child.renderX
      child.y = child.renderY
    } else {
      if (child.visible) {
        child.visible = false
        startAnimation(child, false)
      }
    }
  }
  rebuildEdges()
}

function onClick(e) {
  if (!canvas.value) return
  const rect = canvas.value.getBoundingClientRect()
  const x = e.clientX - rect.left
  const y = e.clientY - rect.top

  let hit = null
  for (const node of nodes) {
    if (!node.visible) continue
    const r = (node.nodeRadius || 24) + 4
    const dx = x - node.renderX
    const dy = y - node.renderY
    if (dx*dx + dy*dy < r*r) {
      hit = node
      break
    }
  }

  if (hit) {
    if (hit.hasChildren) {
      hit.expanded = !hit.expanded
      if (hit.expanded) {
        expandedIds.add(hit.id)
      } else {
        expandedIds.delete(hit.id)
      }
      startChildrenAnimation(hit, hit.expanded)
    } else if (hit.link) {
      window.location.href = hit.link
    }
  }
}

function onMove(e) {
  if (!canvas.value) return
  const rect = canvas.value.getBoundingClientRect()
  const x = e.clientX - rect.left
  const y = e.clientY - rect.top

  let hit = null
  for (const node of nodes) {
    if (!node.visible) continue
    const r = (node.nodeRadius || 24) + 4
    const dx = x - node.renderX
    const dy = y - node.renderY
    if (dx*dx + dy*dy < r*r) {
      hit = node
      break
    }
  }

  hoveredNode.value = hit
  hoveredNodeRef = hit
  if (canvas.value) {
    canvas.value.style.cursor = (hit && (hit.hasChildren || hit.link)) ? 'pointer' : 'default'
  }
}

const tipStyle = computed(() => {
  if (!hoveredNode.value) return {}
  const n = hoveredNode.value
  let l = n.renderX, t = n.renderY
  const pad = 100
  if (l > W - pad) l = n.renderX - 90
  else l = n.renderX + 15
  if (t < pad) t = n.renderY + 30
  else t = n.renderY - 60
  return { left: l + 'px', top: t + 'px' }
})

function bp(fx, fy, tx, ty, p) {
  const dx = tx - fx
  const dy = ty - fy
  const cx1 = fx + dx * 0.2
  const cy1 = fy + dy * 0.05
  const cx2 = fx + dx * 0.8
  const cy2 = fy + dy * 0.95
  const m = 1 - p
  return {
    x: m*m*m*fx + 3*m*m*p*cx1 + 3*m*p*p*cx2 + p*p*p*tx,
    y: m*m*m*fy + 3*m*m*p*cy1 + 3*m*p*p*cy2 + p*p*p*ty
  }
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

function drawFrame(time) {
  if (!ctx) return
  dark = document.documentElement.classList.contains('dark')
  ctx.clearRect(0, 0, W, H)

  updateAnimations(time)

  const bgAlpha = dark ? 0.06 : 0.035
  for (const node of nodes) {
    if (!node.visible || node.appear < 0.1) continue
    const r = (node.nodeRadius || 24) * 2.5
    const g = ctx.createRadialGradient(node.renderX, node.renderY, 0, node.renderX, node.renderY, r)
    g.addColorStop(0, hexToRgba(node.color, bgAlpha * node.appear))
    g.addColorStop(1, hexToRgba(node.color, 0))
    ctx.fillStyle = g
    ctx.beginPath()
    ctx.arc(node.renderX, node.renderY, r, 0, Math.PI * 2)
    ctx.fill()
  }

  for (const edge of edges) {
    const f = edge.from, t = edge.to
    const a = Math.min(f.appear, t.appear)
    if (a < 0.05) continue

    ctx.save()
    ctx.strokeStyle = hexToRgba(t.color, 0.2 * a)
    ctx.lineWidth = 1
    ctx.lineCap = 'round'
    ctx.beginPath()
    for (let p = 0; p <= 1.02; p += 0.03) {
      const pt = bp(f.renderX, f.renderY, t.renderX, t.renderY, p)
      p === 0 ? ctx.moveTo(pt.x, pt.y) : ctx.lineTo(pt.x, pt.y)
    }
    ctx.stroke()
    ctx.restore()
  }

  for (const edge of edges) {
    const f = edge.from, t = edge.to
    const a = Math.min(f.appear, t.appear)
    if (a < 0.05) continue

    for (let i = 0; i < 3; i++) {
      if (!edge.particles) edge.particles = []
      if (edge.particles[i] === undefined) {
        edge.particles[i] = { t: Math.random(), sp: 0.004 + Math.random() * 0.003 }
      }
      const p = edge.particles[i]
      p.t += p.sp
      if (p.t > 1) p.t -= 1
      const pos = bp(f.renderX, f.renderY, t.renderX, t.renderY, p.t)
      ctx.save()
      ctx.shadowColor = hexToRgba(t.color, 0.8)
      ctx.shadowBlur = 6
      ctx.fillStyle = hexToRgba(t.color, 0.7 * a)
      ctx.beginPath()
      ctx.arc(pos.x, pos.y, 1.5, 0, Math.PI * 2)
      ctx.fill()
      ctx.restore()
    }
  }

  for (const node of nodes) {
    if (!node.visible || node.appear < 0.05) continue
    drawNode(node)
  }

  raf = requestAnimationFrame(drawFrame)
}

function drawNode(node) {
  const r = node.nodeRadius || 24
  const scale = node.appear
  const hv = hoveredNodeRef === node
  const depth = node.depth

  ctx.save()
  ctx.translate(node.renderX, node.renderY)
  ctx.scale(scale, scale)

  const pulse = Math.sin(performance.now() * 0.002 + (node.id.charCodeAt(0) || 0)) * 0.15 + 0.85

  ctx.shadowColor = hexToRgba(node.color, hv ? 0.5 : 0.2)
  ctx.shadowBlur = hv ? 20 : 10 + pulse * 5

  const g = ctx.createRadialGradient(-r*0.3, -r*0.3, r*0.05, 0, 0, r)
  const bgColor = dark ? '#1e293b' : '#ffffff'
  g.addColorStop(0, bgColor)
  g.addColorStop(0.35, hexToRgba(node.color, 0.85))
  g.addColorStop(1, hexToRgba(node.color, 0.6))
  ctx.fillStyle = g
  ctx.beginPath()
  ctx.arc(0, 0, r, 0, Math.PI * 2)
  ctx.fill()

  ctx.strokeStyle = hexToRgba(node.color, hv ? 0.95 : 0.55)
  ctx.lineWidth = hv ? 2 : 1
  ctx.beginPath()
  ctx.arc(0, 0, r, 0, Math.PI * 2)
  ctx.stroke()

  if (node.hasChildren && node.expanded) {
    ctx.strokeStyle = hexToRgba(node.color, 0.3)
    ctx.lineWidth = 1
    ctx.setLineDash([3, 3])
    ctx.beginPath()
    ctx.arc(0, 0, r + 6, 0, Math.PI * 2)
    ctx.stroke()
    ctx.setLineDash([])
  }

  if (node.depth === 0) {
    ctx.fillStyle = dark ? '#e2e8f0' : '#334155'
    ctx.font = `700 ${r * 0.55}px -apple-system, BlinkMacSystemFont, sans-serif`
    ctx.textAlign = 'center'
    ctx.textBaseline = 'middle'
    ctx.fillText(node.label, 0, 0)
  } else {
    const fontSize = Math.min(r * 0.6, 12)
    ctx.fillStyle = dark ? '#e2e8f0' : '#334155'
    ctx.font = `600 ${fontSize}px -apple-system, BlinkMacSystemFont, sans-serif`
    ctx.textAlign = 'center'
    ctx.textBaseline = 'middle'

    const maxW = r * 1.6
    const display = node.label.length > 6 ? node.label.slice(0, 5) + '…' : node.label
    ctx.fillText(display, 0, 0)
  }

  ctx.restore()

  if (node.depth > 0) {
    ctx.save()
    ctx.globalAlpha = node.appear
    ctx.fillStyle = dark ? '#cbd5e1' : '#475569'
    ctx.font = `500 ${Math.min(11, r * 0.45)}px -apple-system, sans-serif`
    ctx.textAlign = 'center'
    ctx.textBaseline = 'top'
    const label = node.label
    const maxLabelW = r * 2.2
    let displayLabel = label
    let truncated = false
    ctx.font = `500 ${Math.min(11, r * 0.45)}px -apple-system, sans-serif`
    if (ctx.measureText(label).width > maxLabelW) {
      truncated = true
      for (let i = label.length; i > 0; i--) {
        const s = label.slice(0, i) + '…'
        if (ctx.measureText(s).width <= maxLabelW) {
          displayLabel = s
          break
        }
      }
    }
    ctx.fillText(displayLabel, node.renderX, node.renderY + r + 6)
    ctx.restore()
  }
}

function updateAnimations(time) {
  const toDelete = []
  for (const [id, anim] of animatingNodes) {
    anim.t += 16
    const p = Math.min(anim.t / anim.duration, 1)
    const eased = 1 - Math.pow(1 - p, 3)

    anim.node.renderX = anim.fromX + (anim.toX - anim.fromX) * eased
    anim.node.renderY = anim.fromY + (anim.toY - anim.fromY) * eased
    anim.node.appear = anim.fromAppear + (anim.toAppear - anim.fromAppear) * eased

    if (p >= 1) {
      anim.node.renderX = anim.toX
      anim.node.renderY = anim.toY
      anim.node.appear = anim.toAppear
      anim.node.x = anim.toX
      anim.node.y = anim.toY
      if (anim.toAppear === 0) {
        anim.node.visible = false
        anim.node.renderX = anim.toX
        anim.node.renderY = anim.toY
      }
      toDelete.push(id)
    }
  }
  for (const id of toDelete) animatingNodes.delete(id)
}

function resize() {
  if (!canvas.value) return
  const r = wrapRef.value.getBoundingClientRect()
  W = r.width || 700
  H = r.height || 520
  dpr = window.devicePixelRatio || 1
  canvas.value.width = W * dpr
  canvas.value.height = H * dpr
  canvas.value.style.width = W + 'px'
  canvas.value.style.height = H + 'px'
  ctx = canvas.value.getContext('2d')
  ctx.scale(dpr, dpr)
  cx = W / 2
  cy = H / 2
}

let bound = false

onMounted(() => {
  nextTick(() => {
    resize()
    initData()
    canvas.value.addEventListener('mousemove', onMove)
    canvas.value.addEventListener('click', onClick)
    window.addEventListener('resize', () => { resize(); computeTargets() })
    bound = true
    raf = requestAnimationFrame(drawFrame)
  })
})

onUnmounted(() => {
  if (raf) cancelAnimationFrame(raf)
  raf = 0
  if (bound && canvas.value) {
    canvas.value.removeEventListener('mousemove', onMove)
    canvas.value.removeEventListener('click', onClick)
    window.removeEventListener('resize', resize)
    bound = false
  }
})

watch(() => props.data, () => {
  nextTick(() => {
    resize()
    initData()
  })
}, { deep: true })
</script>

<style scoped>
.rkm-root {
  margin: 16px 0;
  border-radius: 14px;
  overflow: hidden;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
}

.rkm-header {
  padding: 12px 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
  border-bottom: 1px solid var(--vp-c-divider);
}

.rkm-title {
  font-size: 0.92rem;
  font-weight: 600;
  margin: 0;
  color: var(--vp-c-text-1);
}

.rkm-legend {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
}

.rkm-stage-chip {
  font-size: 0.68rem;
  padding: 2px 9px;
  border-radius: 8px;
  color: var(--c);
  background: color-mix(in srgb, var(--c) 10%, transparent);
  border: 1px solid color-mix(in srgb, var(--c) 20%, transparent);
  font-weight: 500;
}

.rkm-canvas-wrap {
  position: relative;
  width: 100%;
  height: v-bind('height');
  overflow: hidden;
}

.rkm-canvas {
  display: block;
  width: 100%;
  height: 100%;
}

.rkm-center-hint {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 0.75rem;
  color: var(--vp-c-text-3);
  pointer-events: none;
  animation: pulseHint 2s ease-in-out infinite;
}

@keyframes pulseHint {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 0.9; }
}

.rkm-tip {
  position: absolute;
  z-index: 10;
  transform: translate(-50%, -100%);
  pointer-events: auto;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 8px 12px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 140px;
  opacity: 0;
  transition: opacity 0.15s ease;
  white-space: nowrap;
}
.rkm-tip[style*="left"] { opacity: 1; }

.rkm-tip strong {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
}

.rkm-tip em {
  font-size: 0.68rem;
  font-style: normal;
  color: var(--vp-c-text-3);
}

.rkm-tip a {
  font-size: 0.74rem;
  font-weight: 500;
  color: var(--vp-c-brand);
  text-decoration: none;
  margin-top: 2px;
}
.rkm-tip a:hover { text-decoration: underline; }

.rkm-tip-hint {
  font-size: 0.62rem;
  color: var(--vp-c-text-3);
  font-style: italic;
}

.rkm-footer {
  padding: 8px 18px;
  border-top: 1px solid var(--vp-c-divider);
  font-size: 0.72rem;
  color: var(--vp-c-text-3);
}
</style>
