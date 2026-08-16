<template>
  <Teleport v-if="target" :to="target">
    <div class="search-ranges" role="tablist" aria-label="搜索范围">
      <button
        v-for="r in ranges"
        :key="r.prefix"
        class="sp-range"
        :class="{ active: activeRange === r.prefix }"
        :title="r.prefix ? `仅在「${r.label}」内搜索` : '全站搜索'"
        @click="setRange(r.prefix)"
      >{{ r.label }}</button>
    </div>
    <div v-show="visible" class="search-history-panel">
      <div v-if="history.length" class="sp-section">
        <div class="sp-head">
          <span class="sp-title">最近搜索</span>
          <button class="sp-clear" @click="clearAll">清空</button>
        </div>
        <ul class="sp-list">
          <li v-for="(item, i) in history" :key="'h' + i" class="sp-item">
            <button class="sp-text" @click="choose(item)">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10" /><polyline points="12 6 12 12 16 14" /></svg>
              <span>{{ item }}</span>
            </button>
            <button class="sp-remove" aria-label="删除" @click="removeAt(i)">×</button>
          </li>
        </ul>
      </div>
      <div class="sp-section">
        <div class="sp-head"><span class="sp-title">猜你想搜</span></div>
        <ul class="sp-list">
          <li v-for="(item, i) in suggestions" :key="'s' + i" class="sp-item">
            <button class="sp-text sp-suggest" @click="choose(item)">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" /></svg>
              <span>{{ item }}</span>
            </button>
          </li>
        </ul>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const STORAGE_KEY = 'searchHistory'
const suggestions = ['Java 基础', '算法框架', 'Redis 缓存', 'MySQL 索引', '分布式系统', 'AI Agent', '动态规划', '数据结构']

const ranges = [
  { label: '全部', prefix: '' },
  { label: 'Java', prefix: 'java' },
  { label: '算法', prefix: 'algorithm' },
  { label: 'AI', prefix: 'ai' },
  { label: '分布式', prefix: 'distributed' },
  { label: '项目', prefix: 'projects' }
]

const target = ref(null)
const visible = ref(false)
const history = ref([])
const activeRange = ref('')

let observer = null
let resultsObserver = null
let modalEl = null
let inputEl = null

const loadHistory = () => {
  try { history.value = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]') } catch { history.value = [] }
}
const persist = () => localStorage.setItem(STORAGE_KEY, JSON.stringify(history.value))
const pushHistory = (q) => {
  const items = history.value.filter(x => x !== q)
  items.unshift(q)
  history.value = items.slice(0, 10)
  persist()
}
const removeAt = (i) => { history.value.splice(i, 1); persist() }
const clearAll = () => { history.value = []; persist() }

const choose = (text) => {
  if (!inputEl) return
  inputEl.value = text
  inputEl.dispatchEvent(new InputEvent('input', { bubbles: true }))
  inputEl.focus()
}

const syncVisible = () => { visible.value = inputEl ? !inputEl.value : false }
const onInput = () => { loadHistory(); syncVisible() }
const onKeydown = (e) => {
  if (e.key === 'Enter') {
    const q = inputEl.value.trim()
    if (q) pushHistory(q)
  }
}
const onModalClick = (e) => {
  if (inputEl && e.target.closest('.result')) {
    const q = inputEl.value.trim()
    if (q) pushHistory(q)
  }
}

// 范围筛选：按结果 href 前缀过滤
const applyRange = () => {
  if (!modalEl) return
  const items = modalEl.querySelectorAll('.results .result')
  items.forEach((el) => {
    const a = el.tagName === 'A' ? el : el.querySelector('a')
    if (!a) return
    const href = (a.getAttribute('href') || '').replace(/^\//, '')
    const match = !activeRange.value || href.startsWith(activeRange.value + '/')
    el.style.display = match ? '' : 'none'
  })
}
const setRange = (prefix) => {
  activeRange.value = activeRange.value === prefix ? '' : prefix
  applyRange()
  if (inputEl) inputEl.focus()
}

const attach = (el) => {
  const shell = el.querySelector('.shell')
  const inp = el.querySelector('.search-input')
  if (!shell || !inp) return false
  modalEl = el
  inputEl = inp
  let mount = shell.querySelector('.search-history-mount')
  if (!mount) {
    mount = document.createElement('div')
    mount.className = 'search-history-mount'
    shell.querySelector('.search-bar').after(mount)
  }
  target.value = mount
  loadHistory()
  syncVisible()
  inputEl.addEventListener('input', onInput)
  inputEl.addEventListener('keydown', onKeydown)
  el.addEventListener('click', onModalClick)
  resultsObserver = new MutationObserver(applyRange)
  resultsObserver.observe(el, { childList: true, subtree: true })
  applyRange()
  return true
}

const tryAttach = (el, attempts = 0) => {
  if (attach(el) || attempts > 20) return
  setTimeout(() => tryAttach(el, attempts + 1), 20)
}

const detach = () => {
  if (inputEl) {
    inputEl.removeEventListener('input', onInput)
    inputEl.removeEventListener('keydown', onKeydown)
    inputEl = null
  }
  if (modalEl) {
    modalEl.removeEventListener('click', onModalClick)
    modalEl = null
  }
  if (resultsObserver) {
    resultsObserver.disconnect()
    resultsObserver = null
  }
  target.value = null
  visible.value = false
  activeRange.value = ''
}

const onMutation = (mutations) => {
  for (const m of mutations) {
    m.addedNodes.forEach((node) => {
      if (node.nodeType === 1 && node.classList?.contains('VPLocalSearchBox')) {
        tryAttach(node)
      }
    })
    m.removedNodes.forEach((node) => {
      if (node.nodeType === 1 && node.classList?.contains('VPLocalSearchBox')) {
        detach()
      }
    })
  }
}

onMounted(() => {
  loadHistory()
  observer = new MutationObserver(onMutation)
  observer.observe(document.body, { childList: true })
})

onUnmounted(() => {
  observer?.disconnect()
  detach()
})
</script>

<style scoped>
.search-ranges {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  padding: 0 0 8px;
  border-bottom: 1px solid var(--vp-c-divider);
  margin-bottom: 8px;
}
.sp-range {
  padding: 3px 10px;
  font-size: 0.75rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  background: transparent;
  color: var(--vp-c-text-2);
  cursor: pointer;
  transition: all 0.15s;
}
.sp-range:hover { border-color: var(--vp-c-brand); color: var(--vp-c-brand); }
.sp-range.active { background: var(--vp-c-brand); color: #fff; border-color: var(--vp-c-brand); }
.search-history-panel {
  border: 1px solid var(--vp-c-divider);
  border-radius: 4px;
  padding: 8px 0;
  background: var(--vp-c-bg);
}
.sp-section + .sp-section { margin-top: 6px; }
.sp-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 12px;
}
.sp-title { font-size: 0.72rem; color: var(--vp-c-text-3); font-weight: 600; letter-spacing: 0.04em; }
.sp-clear { font-size: 0.72rem; color: var(--vp-c-brand-1); background: none; border: none; cursor: pointer; padding: 0; }
.sp-list { list-style: none; margin: 0; padding: 0; }
.sp-item { display: flex; align-items: center; justify-content: space-between; padding: 0 4px 0 8px; }
.sp-text {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  min-width: 0;
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px 8px;
  font-size: 0.88rem;
  color: var(--vp-c-text-1);
  text-align: left;
  border-radius: 4px;
}
.sp-text:hover { background: var(--vp-c-bg-soft); color: var(--vp-c-brand-1); }
.sp-text span { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.sp-text svg { opacity: 0.5; flex-shrink: 0; }
.sp-suggest { color: var(--vp-c-text-2); }
.sp-remove {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--vp-c-text-3);
  font-size: 16px;
  line-height: 1;
  padding: 4px 8px;
  border-radius: 4px;
}
.sp-remove:hover { color: var(--vp-c-text-1); background: var(--vp-c-bg-soft); }
</style>
