<script setup>
import { onMounted, watch } from 'vue'
import { useRoute } from 'vitepress'
import problemLinks from './problem-links.json'

const route = useRoute()

// 题名按长度降序（长先匹配，避免短题名吞掉长题名的一部分）
const sortedNames = Object.keys(problemLinks).sort((a, b) => b.length - a.length)
const escapeRegex = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
const regex = new RegExp(`(${sortedNames.map(escapeRegex).join('|')})`, 'g')

const SKIP_TAGS = new Set(['CODE', 'PRE', 'A', 'SCRIPT', 'STYLE', 'KBD'])

function linkifyNode(node) {
  const text = node.nodeValue
  regex.lastIndex = 0
  if (!regex.test(text)) return
  regex.lastIndex = 0

  const frag = document.createDocumentFragment()
  let last = 0
  let m
  while ((m = regex.exec(text))) {
    if (m.index > last) frag.appendChild(document.createTextNode(text.slice(last, m.index)))
    const a = document.createElement('a')
    a.href = problemLinks[m[0]]
    a.target = '_blank'
    a.rel = 'noopener'
    a.className = 'problem-link'
    a.textContent = m[0]
    frag.appendChild(a)
    last = m.index + m[0].length
  }
  if (last < text.length) frag.appendChild(document.createTextNode(text.slice(last)))
  node.parentNode.replaceChild(frag, node)
}

function linkify() {
  const root = document.querySelector('.vp-doc')
  if (!root) return
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
    acceptNode(node) {
      let p = node.parentElement
      while (p && p !== root) {
        if (SKIP_TAGS.has(p.tagName)) return NodeFilter.FILTER_REJECT
        p = p.parentElement
      }
      regex.lastIndex = 0
      return regex.test(node.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT
    }
  })
  const targets = []
  let n
  while ((n = walker.nextNode())) targets.push(n)
  targets.forEach(linkifyNode)
}

onMounted(() => setTimeout(linkify, 300))
watch(() => route.path, () => setTimeout(linkify, 300))
</script>

<template>
  <span style="display: none" />
</template>

<style>
/* 注入到 .vp-doc 的题名链接样式（全局，非 scoped） */
.vp-doc a.problem-link {
  color: var(--vp-c-brand);
  text-decoration: underline;
  text-decoration-style: dotted;
  text-underline-offset: 2px;
  font-weight: 500;
  padding: 0 1px;
  transition: color 0.15s;
}
.vp-doc a.problem-link:hover {
  text-decoration-style: solid;
}
.vp-doc a.problem-link::after {
  content: '↗';
  font-size: 0.75em;
  margin-left: 2px;
  opacity: 0.7;
}
</style>
