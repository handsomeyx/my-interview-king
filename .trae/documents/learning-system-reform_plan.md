# 学习体系改造实施计划

> 基于 `010-学习体系改造设计-20260816.md` 的全面实施计划
> 目标：将「被动阅读」改造为「主动思考→输出→连接→复习」的深度学习体验

---

## 一、项目现状调研结论

### 1.1 项目技术栈
- **文档框架**: VitePress（Vue 3 + Vite）
- **主题定制**: `docs/.vitepress/theme/` 下有 15+ 自定义 Vue 组件
- **样式**: `custom.css` 全局样式，已支持明暗主题
- **数据持久化**: `study-storage.ts` 基于 localStorage，支持阅读进度/收藏/掌握状态

### 1.2 文章结构现状
- 核心文章采用 `标题 → 配套提示 → Q&A 问答 → 易错点速查表 → 相关链接` 的结构
- 每篇文章开头有 `>` 引用块作为"配套"提示
- 文章末尾有交叉引用链接
- 练习题文章有 `框架速记 → 题目清单 → 例题精讲 → 练习建议` 的结构

### 1.3 已有组件
| 组件 | 功能 | 配合改造 |
|------|------|----------|
| `RelatedProblems.vue` | 渲染 frontmatter 中的相关题目 | 下方新增 ThinkingLinks 区域 |
| `LearningPath.vue` | 三阶段学习路径 + 掌握状态 | 底部加复述引导提示 |
| `ContinueReading.vue` | 继续学习卡片 | 掌握状态旁加"该做复述自测了"图标 |
| `ProblemLinker.vue` | 自动将文中题名转为 LeetCode 链接 | 无需改动 |
| `StudyTracker.vue` | 阅读进度追踪 | 无需改动 |

---

## 二、改造任务分解

### 改造 A：「思考锚点」段落（P0）

#### 2.1.1 改造范围

共 **30 篇核心文章**，分四大板块：

**Java 板块（15 篇）：**
| 文件路径 | 主题 |
|----------|------|
| `docs/java/concurrent/volatile-jmm.md` | volatile 与 JMM |
| `docs/java/concurrent/lock.md` | synchronized / AQS |
| `docs/java/concurrent/thread-pool.md` | 线程池 |
| `docs/java/concurrent/threadlocal.md` | ThreadLocal |
| `docs/java/jvm/garbage-collection.md` | JVM GC |
| `docs/java/jvm/class-loading.md` | 类加载 |
| `docs/spring/ioc-aop.md` | Spring IoC/AOP |
| `docs/spring/transaction.md` | Spring 事务 |
| `docs/spring/circular-dependency.md` | 循环依赖 |
| `docs/java/mysql/indexing.md` | MySQL 索引 |
| `docs/java/mysql/transaction-mvcc.md` | MySQL 事务/MVCC |
| `docs/java/mysql/lock.md` | MySQL 锁 |
| `docs/java/redis/persistence-cache-problems.md` | Redis 持久化与缓存问题 |
| `docs/java/redis/data-structures.md` | Redis 数据结构 |
| `docs/java/kafka/index.md` | Kafka |

**分布式板块（4 篇）：**
| 文件路径 | 主题 |
|----------|------|
| `docs/distributed/basics.md` | CAP/BASE/Raft |
| `docs/distributed/scenarios/gateway.md` | 接入与路由层 |
| `docs/distributed/scenarios/service.md` | 业务逻辑与处理层 |
| `docs/distributed/scenarios/storage.md` | 数据持久化与异步层 |

**算法板块框架文（8 篇）：**
| 文件路径 | 主题 |
|----------|------|
| `docs/algorithm/00-algorithm-frameworks/sliding-window/index.md` | 滑动窗口 |
| `docs/algorithm/00-algorithm-frameworks/dynamic-programming/index.md` | 动态规划 |
| `docs/algorithm/00-algorithm-frameworks/binary-search/index.md` | 二分查找 |
| `docs/algorithm/00-algorithm-frameworks/dfs-bfs/index.md` | DFS/BFS |
| `docs/algorithm/00-algorithm-frameworks/greedy/index.md` | 贪心算法 |
| `docs/algorithm/00-algorithm-frameworks/left-right-pointers/index.md` | 左右指针 |
| `docs/algorithm/00-algorithm-frameworks/union-find/index.md` | 并查集 |
| `docs/algorithm/04-system-algorithms/consistent-hashing.md` | 一致性哈希 |

**AI 板块（3 篇）：**
| 文件路径 | 主题 |
|----------|------|
| `docs/ai/02-agent/index.md` | Agent 核心概念 |
| `docs/ai/03-mcp/index.md` | MCP 协议 |
| `docs/ai/06-RAG/index.md` | RAG 基础 |

#### 2.1.2 改造方式

每篇文章在 **标题 + `---` 分隔线之后、正文 Q&A 之前**，插入 `## 思考锚点` 段落：

```markdown
## 思考锚点

[第一步：讲这个技术要解决的物理/工程事实]

[第二步：如果不解决会导致什么具体后果]

[第三步：点出"本文介绍的技术就是为了解决这个问题而存在的"]
```

**写法规则：**
- 3-5 句话，不超过 5 行
- 不直接给结论，引导读者带着好奇心往下读
- 贴合各板块风格：Java 八股文→底层约束视角；算法→解题思路视角；分布式→工程取舍视角；AI→系统设计视角

---

### 改造 B：「复述自测」引导（P0）

#### 2.2.1 改造范围
与改造 A 相同的 30 篇核心文章

#### 2.2.2 改造方式

在文章 **最后一个章节之后、`---` 分隔线之前**，插入 `## 复述自测` 段落：

```markdown
## 复述自测

读完这篇，试试用自己的话回答三个问题：

1. **一句话总结**：[针对文章核心的总结问题]？（提示：[引导方向]）

2. **讲给初学者听**：[用生活类比解释核心概念]？（可以用[具体类比方向]之类的类比）

3. **预判追问**：如果你是面试官，读完这篇你会追问什么？（比如[具体追问方向]）
```

**写法规则：**
- 三个问题，每个 1-2 句话引导
- 不提供答案
- 问题要精准针对本篇核心内容

---

### 改造 C：「读者思考」微提示（P1）

#### 2.3.1 改造范围
改造 A 中的 30 篇核心文章，**每篇挑选 1-2 个关键推导步骤**插入

#### 2.3.2 改造方式

在长段落或复杂推导中间，插入：

```markdown
> 🤔 停下来想想：[具体的引导性问题]
```

**选择位置的原则：**
- 从物理事实推导出设计约束的环节
- 关键权衡决策点（如 Raft 为什么选多数派）
- 容易混淆的概念辨析处
- 算法核心洞察处（如动态规划的状态定义）

---

### 改造 D：跨域关联提示（P2）

#### 2.4.1 新建文件

**`docs/.vitepress/theme/thinking-links.json`** — 跨域关联数据表

```json
{
  "links": [
    {
      "from": "/java/concurrent/volatile-jmm",
      "to": ["/distributed/basics"],
      "text": "volatile 的内存屏障和分布式系统的顺序一致性在解决同一类问题：并发环境下的操作顺序保证。"
    }
  ]
}
```

**`docs/.vitepress/theme/ThinkingLinks.vue`** — 渲染组件

在 `RelatedProblems.vue` 下方渲染跨域关联提示。

#### 2.4.2 修改文件

- `docs/.vitepress/theme/index.ts` — 注册 ThinkingLinks 组件，在 `doc-after` 插槽中 RelatedProblems 之后添加

---

### 改造 E：扩展 feynman-template.md（P1）

#### 2.5.1 修改文件

**`docs/algorithm/01-methodology/feynman-template.md`**

#### 2.5.2 改造方式

在现有算法题模板基础上，新增两个模板：

1. **技术点模板**：一句话总结 → 讲给初学者 → 预判追问 → 自己的盲点
2. **系统设计模板**：需求拆解 → 核心约束 → 架构决策 → 权衡分析

保持现有篇幅级别，每个模板精炼。

---

### 改造 F：练习题复盘引导（P2）

#### 2.6.1 改造范围

10 篇练习题文章：
- `docs/algorithm/06-practice/sliding-window-practice.md`
- `docs/algorithm/06-practice/binary-search-practice.md`
- `docs/algorithm/06-practice/binary-tree-practice-i.md`
- `docs/algorithm/06-practice/binary-tree-practice-ii.md`
- `docs/algorithm/06-practice/dfs-bfs-practice-i.md`
- `docs/algorithm/06-practice/dfs-bfs-practice-ii.md`
- `docs/algorithm/06-practice/dynamic-programming-practice-i.md`
- `docs/algorithm/06-practice/dynamic-programming-practice-ii.md`
- `docs/algorithm/06-practice/backtrack-practice-i.md`

#### 2.6.2 改造方式

在每篇练习题末尾添加「复盘三步」：

```markdown
## 做完之后试试

1. **盖住答案重新做一遍**：不看本文的解法提示，你能在 20 分钟内独立写出来吗？
2. **用一句话讲清楚**：如果让你给面试官讲这道题的思路，你会怎么说？（不能直接念代码）
3. **举一反三**：这道题的思路可以用来解决哪些其他题？（可以回头看看框架章节的对应部分）
```

---

### 改造 G：前端组件微改造（P2）

#### 2.7.1 修改文件

**`docs/.vitepress/theme/LearningPath.vue`**
- 在三阶段的 `stage` 标题旁添加小图标（💡）
- 在学习路径底部添加提醒文字

**`docs/.vitepress/theme/ContinueReading.vue`**
- 在掌握状态旁添加小图标提示

**`docs/.vitepress/theme/custom.css`**
- 为「思考锚点」「复述自测」「🤔 停下来想想」添加样式
- 为 ThinkingLinks 组件添加样式

---

## 三、执行顺序与依赖关系

```
Phase 1 (P0): 思考锚点 + 复述自测
├── Task 1.1: Java 板块 15 篇文章
├── Task 1.2: 分布式板块 4 篇文章
├── Task 1.3: 算法板块 8 篇框架文章
└── Task 1.4: AI 板块 3 篇文章

Phase 2 (P1): 读者思考微提示 + 模板扩展
├── Task 2.1: 为 30 篇核心文章添加「🤔 停下来想想」
└── Task 2.2: 扩展 feynman-template.md

Phase 3 (P2): 跨域关联 + 练习题 + 前端改造
├── Task 3.1: 创建 thinking-links.json 数据
├── Task 3.2: 创建 ThinkingLinks.vue 组件
├── Task 3.3: 修改 index.ts 注册新组件
├── Task 3.4: 10 篇练习题添加复盘引导
├── Task 3.5: LearningPath.vue 微改造
├── Task 3.6: ContinueReading.vue 微改造
└── Task 3.7: custom.css 添加新样式
```

---

## 四、详细文件修改清单

### 4.1 Phase 1（P0）— 文章内容改造

每篇文章需要 **两次 Edit 操作**：
1. 在标题+`---`之后插入「思考锚点」
2. 在文末插入「复述自测」

#### Java 板块（15 篇 × 2 次编辑 = 30 次操作）

| # | 文件路径 | 锚点切入点 | 自测重点 |
|---|----------|-----------|----------|
| 1 | `java/concurrent/volatile-jmm.md` | CPU 多核缓存不一致 + 指令重排物理事实 | volatile 与 synchronized 区别；i++ 为什么不安全 |
| 2 | `java/concurrent/lock.md` | 多线程互斥的工程需求 + synchronized 演进史 | synchronized 锁升级路径；AQS 核心设计 |
| 3 | `java/concurrent/thread-pool.md` | 线程创建销毁的高昂开销 | 七大核心参数；拒绝策略选择 |
| 4 | `java/concurrent/threadlocal.md` | 线程上下文传递需求 + 内存泄漏风险 | ThreadLocal 内存泄漏原理；InheritableThreadLocal |
| 5 | `java/jvm/garbage-collection.md` | 内存溢出物理事实 + GC 暂停影响 | 三种 GC 对比；对象存活判定 |
| 6 | `java/jvm/class-loading.md` | 类加载的双亲委派机制 | 双亲委派破坏场景；SPI 机制 |
| 7 | `java/spring/ioc-aop.md` | 依赖注入本质 + 面向切面思想 | Bean 生命周期；循环依赖解决 |
| 8 | `java/spring/transaction.md` | 事务传播机制 + 隔离级别 | 7 种传播行为；@Transactional 失效场景 |
| 9 | `java/spring/circular-dependency.md` | 循环依赖检测与解决 | 三级缓存；构造器循环依赖 |
| 10 | `java/mysql/indexing.md` | 查找效率与更新效率的工程权衡 | B+ 树 vs 其他结构；索引失效场景 |
| 11 | `java/mysql/transaction-mvcc.md` | 并发读写冲突 + 快照读优化 | MVCC 实现；当前读 vs 快照读 |
| 12 | `java/mysql/lock.md` | 并发控制的必要性 | 表锁/行锁/间隙锁；死锁检测 |
| 13 | `java/redis/persistence-cache-problems.md` | 内存数据持久化 + 缓存穿透/击穿/雪崩 | 三种缓存问题对比；解决方案选择 |
| 14 | `java/redis/data-structures.md` | 不同数据结构的工程选型 | 跳表 vs 红黑树；应用场景 |
| 15 | `java/kafka/index.md` | 高吞吐消息队列的设计挑战 | ISR 机制；精确一次语义 |

#### 分布式板块（4 篇 × 2 次编辑 = 8 次操作）

| # | 文件路径 | 锚点切入点 | 自测重点 |
|---|----------|-----------|----------|
| 16 | `distributed/basics.md` | 单机→多机的数据一致性跃迁 | CAP 的 P 为什么不可避免；Raft 多数派 |
| 17 | `distributed/scenarios/gateway.md` | 接入层的流量入口职责 | 网关限流策略；服务发现机制 |
| 18 | `distributed/scenarios/service.md` | 业务服务的拆分与协作 | 分布式事务方案选择；幂等性设计 |
| 19 | `distributed/scenarios/storage.md` | 数据持久化的可靠性保证 | 最终一致 vs 强一致；补偿机制 |

#### 算法板块（8 篇 × 2 次编辑 = 16 次操作）

| # | 文件路径 | 锚点切入点 | 自测重点 |
|---|----------|-----------|----------|
| 20 | `algorithm/.../sliding-window/index.md` | 双指针优化暴力搜索 | 滑动窗口适用场景；模板代码 |
| 21 | `algorithm/.../dynamic-programming/index.md` | 重叠子问题与最优子结构 | 状态定义；转移方程推导 |
| 22 | `algorithm/.../binary-search/index.md` | 有序性带来的二分可能 | 搜索空间确定；左边界/右边界 |
| 23 | `algorithm/.../dfs-bfs/index.md` | 深度/广度遍历的系统性 | 回溯三要素；层序 vs 深搜选择 |
| 24 | `algorithm/.../greedy/index.md` | 局部最优→全局最优的条件 | 贪心正确性证明；与 DP 区别 |
| 25 | `algorithm/.../left-right-pointers/index.md` | 双指针的扫描优化 | 对撞指针；快慢指针适用场景 |
| 26 | `algorithm/.../union-find/index.md` | 连通性问题的高效判定 | 路径压缩；按秩合并 |
| 27 | `algorithm/.../consistent-hashing.md` | 节点增减时的最小数据迁移 | 虚拟节点作用；与取模对比 |

#### AI 板块（3 篇 × 2 次编辑 = 6 次操作）

| # | 文件路径 | 锚点切入点 | 自测重点 |
|---|----------|-----------|----------|
| 28 | `ai/02-agent/index.md` | LLM→Agent 的能力跃迁 | Agent 核心组件；规划vs执行 |
| 29 | `ai/03-mcp/index.md` | Agent 间通信的标准化需求 | MCP 协议设计；与 function calling 区别 |
| 30 | `ai/06-RAG/index.md` | LLM 知识截止日期的解决方案 | RAG 流程；向量检索原理 |

---

### 4.2 Phase 2（P1）— 读者思考微提示 + 模板扩展

#### Task 2.1：为 30 篇核心文章添加「🤔 停下来想想」

每篇文章挑选 1-2 个关键位置，用 `> 🤔 停下来想想：[问题]` 格式插入。

**示例位置：**
- `volatile-jmm.md`：讲完 `i++` 三步后 → "如果两个线程同时执行 i++，在什么条件下会丢失更新？CAS 是怎么解决的？"
- `basics.md`：讲完 Raft 日志复制 → "为什么只要多数派确认就够了？如果 3 节点集群，1 个慢节点落后，Leader 会阻塞吗？"
- `indexing.md`：讲完 B+ 树 vs B 树 → "为什么数据库不用红黑树或跳表做索引？B+ 树的叶子链表结构带来了什么好处？"
- `dynamic-programming/index.md`：讲完状态定义 → "如果状态定义错了（维度少了/多了），会导致什么问题？怎么验证状态定义的正确性？"

#### Task 2.2：扩展 feynman-template.md

在现有模板后面追加两个模板：
- **技术点复述模板**：用于读完八股文后的主动输出
- **系统设计复盘模板**：用于场景题后的总结

---

### 4.3 Phase 3（P2）— 前端组件 + 跨域关联 + 练习题

#### Task 3.1：创建 `thinking-links.json`

包含 10-15 条跨域关联，覆盖：
- Java ↔ 分布式（内存屏障 vs 顺序一致性）
- Java ↔ 算法（B+ 树 vs 跳表 vs 哈希表）
- 分布式 ↔ 算法（一致性哈希 vs 加权轮询 vs 取模分片）
- AI ↔ 算法（向量检索 vs B+ 树索引）
- Spring ↔ 分布式（IoC 控制反转 vs 服务注册发现）

#### Task 3.2：创建 `ThinkingLinks.vue`

```vue
<script setup>
import { computed } from 'vue'
import { useData } from 'vitepress'
import thinkingLinks from './thinking-links.json'

const { page } = useData()
const currentPath = computed(() => page.value?.path || '')

const relatedLinks = computed(() => {
  return thinkingLinks.links.filter(l => l.from === currentPath.value)
})
</script>

<template>
  <div v-if="relatedLinks.length" class="thinking-links">
    <h2 class="tl-title">💡 相关思考</h2>
    <div class="tl-list">
      <div v-for="(link, i) in relatedLinks" :key="i" class="tl-item">
        {{ link.text }}
        <div v-if="link.to?.length" class="tl-targets">
          <a v-for="t in link.to" :key="t" :href="t" class="tl-target">{{ t }}</a>
        </div>
      </div>
    </div>
  </div>
</template>
```

#### Task 3.3：修改 `index.ts`

在 `doc-after` 插槽中，`RelatedProblems` 之后添加 `ThinkingLinks`。

#### Task 3.4：10 篇练习题添加「复盘三步」

每篇练习题末尾追加 `## 做完之后试试` 段落。

#### Task 3.5：修改 `LearningPath.vue`

- 在 `lp-stage-name` 旁添加 💡 图标
- 在 `lp-hint` 位置替换为复述引导提示

#### Task 3.6：修改 `ContinueReading.vue`

- 在掌握状态 badge 旁添加 🧠 图标，提示"该做复述自测了"

#### Task 3.7：修改 `custom.css`

新增以下样式：
- `.thinking-anchor` — 思考锚点段落样式（左侧色条 + 浅色背景）
- `.self-test` — 复述自测段落样式（左侧色条 + 提问图标）
- `.thinking-links` — 跨域关联组件样式
- `.tl-item` — 关联条目卡片样式
- `.vp-doc blockquote.trigger-think` — 🤔 停下来想想特殊样式

---

## 五、新增样式规范

### 5.1 思考锚点样式
```css
.vp-doc h2:has-text("思考锚点") {
  border-left: 4px solid #38bdf8;
  padding-left: 12px;
}
```

### 5.2 复述自测样式
```css
.vp-doc h2:has-text("复述自测") {
  border-left: 4px solid #8b5cf6;
  padding-left: 12px;
}
```

### 5.3 🤔 停下来想想样式
```css
.vp-doc blockquote:has(> p:has-text("停下来想想")) {
  border-left: 4px solid #f59e0b;
  background: rgba(245, 158, 11, 0.05);
  border-radius: 4px;
  padding: 12px 16px;
}
```

### 5.4 ThinkingLinks 组件样式
```css
.thinking-links {
  margin-top: 24px;
  padding: 16px;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.05), rgba(56, 189, 248, 0.05));
  border: 1px solid rgba(139, 92, 246, 0.15);
}
.tl-title { font-size: 1.1rem; margin: 0 0 12px; color: #8b5cf6; }
.tl-item { padding: 10px 0; line-height: 1.7; }
.tl-targets { margin-top: 8px; display: flex; gap: 12px; flex-wrap: wrap; }
.tl-target { color: var(--vp-c-brand); font-size: 0.85rem; }
```

---

## 六、风险与注意事项

### 6.1 文章内容风险
- **风格一致性**：改造时需严格保持各板块原有风格（Java 八股→追问式；算法→实战式；分布式→工程式；AI→系统设计式）
- **不破坏现有结构**：思考锚点和复述自测是**追加**，不修改原有内容
- **思考锚点不超过 5 行**：避免过长导致阅读负担

### 6.2 前端组件风险
- **VitePress 插槽限制**：`doc-after` 插槽需确认在当前版本中可用
- **CSS `:has()` 兼容性**：部分浏览器可能不支持，需提供 fallback
- **localStorage 扩展**：新增的复习状态需向后兼容

### 6.3 跨域关联数据
- `thinking-links.json` 是静态数据，需手动维护
- 后续可考虑从文章 frontmatter 自动生成

### 6.4 执行建议
- Phase 1 可按板块分批执行，每完成一个板块即可预览效果
- Phase 2/3 依赖 Phase 1 的完成，但前端组件可并行开发
- 每完成一个文件的修改，建议立即 `npm run dev` 预览效果

---

## 七、完成验收标准

### Phase 1 验收
- [ ] 30 篇核心文章均有 `## 思考锚点` 段落
- [ ] 30 篇核心文章均有 `## 复述自测` 段落
- [ ] 每篇思考锚点 3-5 行，不包含结论
- [ ] 每篇复述自测 3 个问题，不提供答案
- [ ] 所有文章风格与原文一致

### Phase 2 验收
- [ ] 30 篇核心文章中至少 20 篇有 `> 🤔 停下来想想` 提示
- [ ] `feynman-template.md` 包含三个模板（算法/技术点/系统设计）

### Phase 3 验收
- [ ] `thinking-links.json` 包含 10+ 条跨域关联
- [ ] `ThinkingLinks.vue` 组件正常渲染
- [ ] `LearningPath.vue` 显示复述引导提示
- [ ] 10 篇练习题均有「复盘三步」
- [ ] 所有新样式在明暗主题下均正常