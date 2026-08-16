<script setup>
import { ref, computed, onMounted } from 'vue'
import { getMastery, setMastery, scheduleReview, cancelReview } from './study-storage'
import learningPathData from './learning-path.json'

const stages = ref(learningPathData.stages)

const masteryMap = ref({})
const refresh = () => { masteryMap.value = getMastery() }
onMounted(refresh)

const allNodes = computed(() => stages.value.flatMap((s) => s.nodes))
const masteredCount = computed(() => allNodes.value.filter((n) => masteryMap.value[n.path] === 'mastered').length)
const totalCount = computed(() => allNodes.value.length)
const overallPct = computed(() => (totalCount.value ? Math.round((masteredCount.value / totalCount.value) * 100) : 0))

const stateOf = (path) => masteryMap.value[path] || 'todo'

const cycle = (path) => {
  const order = ['todo', 'learning', 'mastered']
  const prev = stateOf(path)
  const next = order[(order.indexOf(prev) + 1) % order.length]
  setMastery(path, next)
  if (next === 'mastered') {
    const node = allNodes.value.find(n => n.path === path)
    if (node) scheduleReview(path, node.title)
  } else if (prev === 'mastered') {
    cancelReview(path)
  }
  refresh()
}
</script>

<template>
  <div class="learning-path">
    <div class="lp-header">
      <h2 class="lp-title">学习路径</h2>
      <div class="lp-progress">
        <span class="lp-bar"><span class="lp-bar-inner" :style="{ width: overallPct + '%' }" /></span>
        <span class="lp-pct">已掌握 {{ masteredCount }}/{{ totalCount }}（{{ overallPct }}%）</span>
      </div>
    </div>

    <div class="lp-stages">
      <div v-for="stage in stages" :key="stage.name" class="lp-stage">
        <div class="lp-stage-name">{{ stage.name }}</div>
        <div class="lp-nodes">
          <div v-for="node in stage.nodes" :key="node.path" class="lp-node" :class="stateOf(node.path)">
            <button
              class="lp-dot"
              :title="`点击切换掌握状态（当前：${stateOf(node.path) === 'mastered' ? '已掌握' : stateOf(node.path) === 'learning' ? '学习中' : '待学'}）`"
              @click.prevent="cycle(node.path)"
            />
            <a :href="node.path" class="lp-link">{{ node.title }}</a>
          </div>
        </div>
      </div>
    </div>
    <p class="lp-hint">点圆点切换掌握状态（待学 → 学习中 → 已掌握），点文字跳转章节。状态本地保存。</p>
    <p class="lp-hint">💡 建议每学完一个节点，回到对应文章末尾做一下「复述自测」——能讲出来才算真正掌握。</p>
  </div>
</template>

<style scoped>
.learning-path { margin: 24px 0; }
.lp-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 16px;
}
.lp-title { font-size: 1.25rem; margin: 0; }
.lp-progress { display: flex; align-items: center; gap: 10px; }
.lp-bar {
  width: 160px;
  height: 6px;
  background: var(--vp-c-divider);
  border-radius: 3px;
  overflow: hidden;
  display: inline-block;
}
.lp-bar-inner {
  display: block;
  height: 100%;
  background: linear-gradient(90deg, #38bdf8, #8b5cf6);
  transition: width 0.3s;
}
.lp-pct { font-size: 0.78rem; color: var(--vp-c-text-2); }
.lp-stages { display: flex; flex-direction: column; gap: 14px; }
.lp-stage {
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 12px 14px;
}
.lp-stage-name {
  font-weight: 600;
  margin-bottom: 10px;
  color: var(--vp-c-brand);
  font-size: 0.95rem;
}
.lp-nodes { display: flex; flex-wrap: wrap; gap: 10px 16px; }
.lp-node { display: flex; align-items: center; gap: 6px; }
.lp-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  border: 2px solid var(--vp-c-divider);
  background: transparent;
  cursor: pointer;
  padding: 0;
  transition: all 0.2s;
}
.lp-node.learning .lp-dot { border-color: #f59e0b; background: #f59e0b; }
.lp-node.mastered .lp-dot { border-color: #10b981; background: #10b981; }
.lp-dot:hover { transform: scale(1.2); }
.lp-link {
  font-size: 0.88rem;
  color: var(--vp-c-text-1);
  text-decoration: none;
}
.lp-link:hover { color: var(--vp-c-brand); }
.lp-node.mastered .lp-link { color: #10b981; }
.lp-node.learning .lp-link { color: #f59e0b; }
.lp-hint { font-size: 0.78rem; color: var(--vp-c-text-3); margin-top: 12px; }
</style>
