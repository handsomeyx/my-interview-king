# 面试算法练习

欢迎来到面试算法练习专区！这里汇集了算法与数据结构的核心知识，帮助你系统地准备算法面试。

> 🗺️ **可视化学习路径**：查看完整的 [学习路径图](./learning-path.md)，包含全景知识体系、三阶段学习路线和跨域关联图。

## 学习路线概览

### 第一阶段：打基础
- **算法方法论**：掌握费曼技巧、时空复杂度分析、工程化编码习惯
- **数据结构基础**：熟悉线性结构、树形结构、图论、堆与前缀树

### 第二阶段：练套路
- **算法模式**：掌握搜索、动态规划、优化、数学逻辑等算法模式
- **系统算法**：理解缓存、负载均衡、限流、分布式ID等系统算法

### 第三阶段：刷真题
- **高频真题**：通过数组类、逻辑谜题等高频题目实战练习
- **模拟面试**：按照真实面试场景进行模拟训练

## 📊 学习进度追踪

<style>
/* 进度追踪样式 */
.progress-container {
  margin: 24px 0;
  padding: 20px;
  background: var(--vp-c-bg-soft);
  border-radius: 8px;
  border: 1px solid var(--vp-c-border);
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.progress-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
}

.progress-stats {
  display: flex;
  gap: 20px;
  font-size: 0.9rem;
  color: var(--vp-c-text-2);
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: var(--vp-c-bg-alt);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 20px;
}

.progress-fill {
  height: 100%;
  background: var(--vp-c-brand);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-item {
  display: flex;
  align-items: center;
  padding: 12px;
  margin-bottom: 8px;
  background: var(--vp-c-bg);
  border-radius: 6px;
  border: 1px solid var(--vp-c-border);
  transition: all 0.2s ease;
}

.progress-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.progress-checkbox {
  margin-right: 12px;
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.progress-text {
  flex: 1;
  font-size: 0.95rem;
  color: var(--vp-c-text-1);
}

.progress-date {
  font-size: 0.8rem;
  color: var(--vp-c-text-3);
}

/* 响应式适配 */
@media (max-width: 768px) {
  .progress-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .progress-stats {
    flex-direction: column;
    gap: 5px;
  }
  
  .progress-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .progress-checkbox {
    align-self: flex-start;
  }
}
</style>

<script>
// 学习进度追踪功能
const progressItems = [
  { id: 'methodology-1', name: '用费曼技巧记录逻辑漏洞的模板', completed: false, date: '' },
  { id: 'methodology-2', name: '时空复杂度分析深度指南', completed: false, date: '' },
  { id: 'methodology-3', name: '工程化编码习惯（如变量命名、边界检查）', completed: false, date: '' },
  { id: 'data-structures-1', name: '线性结构：链表、栈、队列、数组', completed: false, date: '' },
  { id: 'data-structures-2', name: '树形结构：二叉树、红黑树、B+树（结合数据库）', completed: false, date: '' },
  { id: 'data-structures-3', name: '图论：并查集、最短路径、拓扑排序', completed: false, date: '' },
  { id: 'data-structures-4', name: '堆与前缀树', completed: false, date: '' },
  { id: 'algorithm-patterns-1', name: '二分搜索、DFS/BFS、回溯', completed: false, date: '' },
  { id: 'algorithm-patterns-2', name: '动态规划专题（背包、区间、状态机）', completed: false, date: '' },
  { id: 'algorithm-patterns-3', name: '贪心、双指针、滑动窗口、单调栈', completed: false, date: '' },
  { id: 'algorithm-patterns-4', name: '位运算、大数运算、概率算法', completed: false, date: '' },
  { id: 'system-algorithms-1', name: '手写 LRU、LFU 逻辑', completed: false, date: '' },
  { id: 'system-algorithms-2', name: '一致性哈希算法逻辑', completed: false, date: '' },
  { id: 'system-algorithms-3', name: '令牌桶、漏桶算法设计', completed: false, date: '' },
  { id: 'system-algorithms-4', name: '分布式 ID（如 Snowflake）逻辑拆解', completed: false, date: '' },
  { id: 'top-interview-1', name: '数组类 Top 题', completed: false, date: '' },
  { id: 'top-interview-2', name: '智力题与逻辑推演', completed: false, date: '' }
];

// 从本地存储加载进度
function loadProgress() {
  if (typeof localStorage === 'undefined') return;
  const savedProgress = localStorage.getItem('codingProgress');
  if (savedProgress) {
    const parsedProgress = JSON.parse(savedProgress);
    progressItems.forEach(item => {
      const savedItem = parsedProgress.find(p => p.id === item.id);
      if (savedItem) {
        item.completed = savedItem.completed;
        item.date = savedItem.date;
      }
    });
  }
}

// 保存进度到本地存储
function saveProgress() {
  if (typeof localStorage === 'undefined') return;
  localStorage.setItem('codingProgress', JSON.stringify(progressItems));
  updateProgress();
}

// 更新进度显示
function updateProgress() {
  if (typeof document === 'undefined') return;
  const progressContainer = document.querySelector('.progress-container');
  if (!progressContainer) return;
  
  const completedItems = progressItems.filter(item => item.completed).length;
  const totalItems = progressItems.length;
  const progressPercentage = Math.round((completedItems / totalItems) * 100);
  
  const progressItemsHtml = progressItems.map(item => `
    <div class="progress-item">
      <input type="checkbox" class="progress-checkbox" data-id="${item.id}" ${item.completed ? 'checked' : ''}>
      <span class="progress-text">${item.name}</span>
      <span class="progress-date">${item.date || ''}</span>
    </div>
  `).join('');
  
  progressContainer.innerHTML = `
    <div class="progress-header">
      <h3 class="progress-title">学习进度</h3>
      <div class="progress-stats">
        <span>已完成: ${completedItems}/${totalItems}</span>
        <span>进度: ${progressPercentage}%</span>
      </div>
    </div>
    <div class="progress-bar">
      <div class="progress-fill" style="width: ${progressPercentage}%"></div>
    </div>
    <div class="progress-list">
      ${progressItemsHtml}
    </div>
  `;
  
  // 添加事件监听器
  document.querySelectorAll('.progress-checkbox').forEach(checkbox => {
    checkbox.addEventListener('change', (e) => {
      const id = e.target.dataset.id;
      const item = progressItems.find(item => item.id === id);
      if (item) {
        item.completed = e.target.checked;
        if (e.target.checked) {
          const today = new Date().toISOString().split('T')[0];
          item.date = today;
        } else {
          item.date = '';
        }
        saveProgress();
      }
    });
  });
}

// 初始化
if (typeof window !== 'undefined') {
  window.addEventListener('DOMContentLoaded', () => {
    loadProgress();
    updateProgress();
  });
}
</script>

<div class="progress-container"></div>

## 目录结构

```
docs/algorithm/
 ├── 01-methodology/           # 【方法论】算法方法论 
 │   ├── feynman-template.md   # 用费曼技巧记录逻辑漏洞的模板 
 │   ├── complexity-guide.md   # 时空复杂度分析深度指南 
 │   └── coding-habits.md      # 工程化编码习惯（如变量命名、边界检查） 
 │ 
 ├── 02-data-structures/       # 【数据结构】数据结构基础 
 │   ├── linear/               # 线性结构：链表、栈、队列、数组 
 │   ├── tree/                 # 树形结构：二叉树、红黑树、B+树（结合数据库） 
 │   ├── graph/                # 图论：并查集、最短路径、拓扑排序 
 │   └── heap-and-trie/        # 堆与前缀树 
 │ 
 ├── 03-algorithm-patterns/    # 【算法套路】算法模式 
 │   ├── search/               # 二分搜索、DFS/BFS、回溯 
 │   ├── dynamic-programming/  # 动态规划专题（背包、区间、状态机） 
 │   ├── optimization/         # 贪心、双指针、滑动窗口、单调栈 
 │   └── math-logic/           # 位运算、大数运算、概率算法 
 │ 
 ├── 04-system-algorithms/     # 【系统算法】后端核心 
 │   ├── caching/              # 手写 LRU、LFU 逻辑 
 │   ├── load-balancing/       # 一致性哈希算法逻辑 
 │   ├── rate-limiting/        # 令牌桶、漏桶算法设计 
 │   └── unique-id/            # 分布式 ID（如 Snowflake）逻辑拆解 
 │ 
 ├── 05-top-interview-100/     # 【真题训练】高频真题练习 
 │   ├── arrays/               # 数组类 Top 题 
 │   └── logic-puzzles/        # 智力题与逻辑推演 
 │ 
 └── index.md                  # 刷题主页（包含进度表和学习路线图） 
```

## 学习建议

1. **循序渐进**：按照学习路线图的顺序，从基础方法论开始，逐步深入到算法套路和系统算法
2. **理解原理**：不仅要记住代码实现，更要理解算法的核心原理和设计思想
3. **多做练习**：通过高频真题的练习，巩固所学知识，提高解题能力
4. **模拟面试**：按照真实面试场景进行模拟训练，提高临场发挥能力
5. **总结归纳**：定期总结所学知识，形成自己的知识体系

## 资源推荐

- **LeetCode**：[https://leetcode.com/](https://leetcode.com/)
- **CodeTop**：[https://codetop.cc/](https://codetop.cc/)
- **剑指 Offer**：《剑指 Offer：名企面试官精讲典型编程题》
- **算法导论**：《算法导论》（Introduction to Algorithms）

## 联系我们

如果你在学习过程中遇到问题，或者有任何建议，欢迎联系我们。祝你在面试中取得好成绩！