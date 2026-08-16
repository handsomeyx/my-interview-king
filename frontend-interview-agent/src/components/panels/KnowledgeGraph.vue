<template>
  <div class="knowledge-graph">
    <h3 class="panel-title">🕸️ 知识图谱</h3>
    <div ref="chartRef" class="chart-container" :style="{ height: nodes.length > 0 ? '220px' : '60px' }" />
    <div v-if="nodes.length === 0" class="empty-hint">
      AI 回答后将生成知识图谱
    </div>
    <div v-if="nodes.length > 0" class="nodes-list">
      <div
        v-for="(node, i) in nodes"
        :key="i"
        class="graph-node"
        :class="node.strength"
      >
        <span class="node-dot" />
        <span class="node-name">{{ node.name }}</span>
        <span class="node-strength">{{ strengthLabel(node.strength) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import type { KGNode } from '@/types/chat'

const props = defineProps<{
  nodes: KGNode[]
}>()

const chartRef = ref<HTMLDivElement | null>(null)
let chart: echarts.ECharts | null = null

function strengthLabel(s: string) {
  return s === 'strong' ? '精通' : s === 'medium' ? '掌握' : '了解'
}

function initChart() {
  if (!chartRef.value) return
  if (chart) {
    chart.dispose()
  }
  chart = echarts.init(chartRef.value)
  updateChart()
}

function updateChart() {
  if (!chart || !chartRef.value) return

  const nodes = props.nodes.map((n, i) => ({
    id: `node-${i}`,
    name: n.name,
    symbolSize: n.strength === 'strong' ? 40 : n.strength === 'medium' ? 32 : 26,
    itemStyle: {
      color: n.strength === 'strong' ? '#10b981' : n.strength === 'medium' ? '#3b82f6' : '#9ca3af'
    },
    label: {
      show: true,
      position: 'right',
      fontSize: 11,
      color: 'var(--text-1)'
    }
  }))

  const links = []
  for (let i = 1; i < nodes.length; i++) {
    links.push({
      source: nodes[0].id,
      target: nodes[i].id,
      lineStyle: { color: 'var(--border-color)', opacity: 0.4 }
    })
  }

  const option: echarts.EChartsOption = {
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        if (params.dataType === 'node') {
          const idx = params.data.id.replace('node-', '')
          const node = props.nodes[parseInt(idx)]
          return `${node.name}<br/><span style="color:#999">${strengthLabel(node.strength)}</span>`
        }
        return ''
      }
    },
    animationDuration: 600,
    animationEasingUpdate: 'quinticInOut',
    series: [{
      type: 'graph',
      layout: 'force',
      roam: true,
      draggable: true,
      data: nodes,
      links: links,
      lineStyle: {
        curveness: 0.15
      },
      force: {
        repulsion: 200,
        edgeLength: [40, 80]
      },
      emphasis: {
        focus: 'adjacency',
        lineStyle: { width: 3 }
      }
    }]
  }

  chart.setOption(option)
}

watch(() => props.nodes, () => {
  nextTick(updateChart)
}, { deep: true })

function handleResize() {
  chart?.resize()
}

onMounted(() => {
  nextTick(initChart)
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chart?.dispose()
  chart = null
})
</script>

<style scoped>
.knowledge-graph {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 16px;
}

.panel-title {
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 12px;
}

.chart-container {
  width: 100%;
  transition: height 0.3s ease;
}

.empty-hint {
  text-align: center;
  color: var(--text-secondary);
  font-size: 0.8rem;
  padding: 20px 0;
}

.nodes-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--border-color);
}

.graph-node {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 0.85rem;
}

.graph-node.strong .node-dot { background: #10b981; }
.graph-node.medium .node-dot { background: #3b82f6; }
.graph-node.weak .node-dot { background: #9ca3af; }

.node-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.node-name {
  flex: 1;
  font-weight: 500;
}

.node-strength {
  font-size: 0.75rem;
  color: var(--text-secondary);
}
</style>
