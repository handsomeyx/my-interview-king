# 学习体系剩余任务实施计划

> 基于 `需求变更/011-学习体系剩余实施清单-20260816.md`，共 5 个任务。

---

## 任务 1：核心文章加入「读者思考」微提示

### 目标
在 8 篇核心文章的关键推导步骤中间插入 `> 🤔 停下来想想：[引导性问题]` 引用块，每篇 2-3 处。

### 实施清单

| # | 文件 | 插入位置 | 内容 |
|---|------|---------|------|
| 1.1 | `docs/java/concurrent/volatile-jmm.md` | Q2 讲完 "as-if-serial" 后 | `> 🤔 停下来想想：单线程下重排序永远观察不到——这是为什么？` |
| 1.1 | 同上 | Q3 讲完 "volatile 写的 StoreLoad 最贵" 后 | `> 🤔 停下来想想：为什么 volatile 写比读慢这么多？` |
| 1.1 | 同上 | Q5 讲完 "DCL 为什么要 volatile" 后 | `> 🤔 停下来想想：如果没有 volatile，2 和 3 重排序后会发生什么？` |
| 1.2 | `docs/java/mysql/transaction-mvcc.md` | Q2 讲完四种隔离级别后 | `> 🤔 停下来想想：不可重复读和幻读的本质区别是什么？` |
| 1.2 | 同上 | Q3 讲完 MVCC 三件套后 | `> 🤔 停下来想想：为什么快照读能不加锁？` |
| 1.2 | 同上 | Q4 讲完 RC 和 RR 的区别后 | `> 🤔 停下来想想：ReadView 在 RC 和 RR 下生成时机不同，这带来了什么行为差异？` |
| 1.3 | `docs/java/spring/ioc-aop.md` | Q3 讲完 Bean 生命周期 7 步后 | `> 🤔 停下来想想：AOP 代理在第 6 步才生成，那构造方法里调 @Transactional 为什么会失效？` |
| 1.3 | 同上 | Q4 讲完 JDK vs CGLIB 对比后 | `> 🤔 停下来想想：SpringBoot 2.x 为什么默认改用 CGLIB？` |
| 1.4 | `docs/distributed/basics.md` | Q1 讲完 "CAP 不是任何时候三选二" 后 | `> 🤔 停下来想想：没有网络分区时，CAP 三选二还成立吗？` |
| 1.4 | 同上 | Q5 讲完 "多数派 Quorum" 后 | `> 🤔 停下来想想：为什么多数派能保证一致性？任意两个多数派必有交集——这是为什么？` |
| 1.5 | `docs/algorithm/00-algorithm-frameworks/sliding-window/index.md` | 框架模板前 | `> 🤔 停下来想想：为什么滑动窗口能把 O(n²) 降到 O(n)？` |
| 1.5 | 同上 | 四种类型讲完后 | `> 🤔 停下来想想：什么时候该扩大窗口、什么时候该缩小？判断依据是什么？` |
| 1.6 | `docs/java/jvm/garbage-collection.md` | GC 种类对比讲解处 | `> 🤔 停下来想想：为什么 G1 用 Region 而不是传统的连续分代？` |
| 1.6 | 同上 | 可达性分析讲解处 | `> 🤔 停下来想想：三色标记法中，为什么需要写屏障来处理并发标记？` |
| 1.6 | 同上 | GC 调优思路处 | `> 🤔 停下来想想：线上 OOM 了，你会怎么一步步排查是内存泄漏还是内存溢出？` |
| 1.7 | `docs/java/redis/persistence-cache-problems.md` | AOF 重写讲解处 | `> 🤔 停下来想想：AOF 重写和 MySQL purge binlog 解决的是同一类空间问题吗？` |
| 1.7 | 同上 | 缓存穿透/击穿/雪崩讲解处 | `> 🤔 停下来想想：三者的核心区别是什么？各自的解法思路有什么本质不同？` |
| 1.8 | `docs/java/concurrent/lock.md` | synchronized 锁升级过程讲解处 | `> 🤔 停下来想想：偏向锁在 Java 15 被移除了——这说明了什么工程权衡？` |
| 1.8 | 同上 | AQS 核心流程讲解处 | `> 🤔 停下来想想：AQS 用 CAS + 队列实现公平锁，为什么非公平锁性能反而更好？` |

### 操作方法
读取每篇文章 → 定位到对应的 H2/H3 标题段落末尾 → 在该段落后插入引用块 → 用 Edit 工具精确替换。

---

## 任务 2：练习题文章追加「复盘三步」

### 目标
在 9 篇练习题文章末尾追加复盘引导段落。

### 实施清单

以下 9 个文件，在文件最末尾追加统一内容：

```markdown
## 做完之后试试

1. **盖住答案重新做一遍**：不看本文的解法提示，你能在 20 分钟内独立写出来吗？
2. **用一句话讲清楚**：如果让你给面试官讲这道题的思路，你会怎么说？（不能直接念代码）
3. **举一反三**：这道题的思路可以用来解决哪些其他题？（可以回头看看对应框架章节的内容）
```

### 文件列表

1. `docs/algorithm/06-practice/sliding-window-practice.md`
2. `docs/algorithm/06-practice/dynamic-programming-practice-i.md`
3. `docs/algorithm/06-practice/dynamic-programming-practice-ii.md`
4. `docs/algorithm/06-practice/dfs-bfs-practice-i.md`
5. `docs/algorithm/06-practice/dfs-bfs-practice-ii.md`
6. `docs/algorithm/06-practice/binary-tree-practice-i.md`
7. `docs/algorithm/06-practice/binary-tree-practice-ii.md`
8. `docs/algorithm/06-practice/binary-search-practice.md`
9. `docs/algorithm/06-practice/backtrack-practice-i.md`

### 操作方法
读取文件末尾 → 在最后一行后追加内容 → 用 Edit 工具替换。

---

## 任务 3：补齐 thinking-links.json 跨域关联配置

### 目标
在现有 9 个条目的基础上，追加 8 个新页面的跨域关联配置。

### 追加内容

在 `docs/.vitepress/theme/thinking-links.json` 的最后一个对象（`algorithm/00-algorithm-frameworks/dynamic-programming`）之后，追加以下 8 个条目（注意 JSON 逗号分隔）：

3.1 `java/redis/persistence-cache-problems` — 关联 MySQL/Kafka/缓存问题，2 个思考问题
3.2 `java/jvm/garbage-collection` — 关联内存区域/Redis/MySQL，2 个思考问题
3.3 `java/spring/transaction` — 关联 AOP/MySQL 事务/分布式基础，2 个思考问题
3.4 `java/mysql/indexing` — 已存在，跳过（当前 json 已有此条目）
3.5 `distributed/scenarios/gateway` — 关联一致性哈希/限流算法/服务治理，2 个思考问题
3.6 `algorithm/04-system-algorithms/caching` — 关联 Redis 数据结构/缓存问题/JVM，2 个思考问题
3.7 `algorithm/04-system-algorithms/rate-limiting` — 关联分布式基础/网关/Kafka，2 个思考问题
3.8 `algorithm/00-algorithm-frameworks/binary-search` — 关联 MySQL 索引/Redis/复杂度分析，2 个思考问题

注意：3.4 `java/mysql/indexing` 在当前 json 中已存在，跳过。实际追加 7 个条目。

### 操作方法
读取完整 JSON → 在最后一个 `}` 前插入新条目 → 验证 JSON 格式正确。

---

## 任务 4：首页学习路径追加引导文案

### 目标
在 `LearningPath.vue` 第 52 行现有 hint 后追加一行复述自测引导。

### 操作
编辑 `docs/.vitepress/theme/LearningPath.vue`，在第 52 行 `<p class="lp-hint">点圆点切换...</p>` 后追加：

```html
<p class="lp-hint">💡 建议每学完一个节点，回到对应文章末尾做一下「复述自测」——能讲出来才算真正掌握。</p>
```

---

## 任务 5：实现间隔重复提醒（纯前端）

### 目标
用户标记"已掌握"后，系统在 1/3/7 天后提醒回来复习。

### 实施步骤

#### 5.1 在 `study-storage.ts` 中追加间隔重复功能

- 新增 `reviewReminders` key
- 新增 `ReviewReminder` 类型
- 新增 `INTERVALS = [1, 3, 7]` 常量
- 新增 4 个函数：`scheduleReview`、`getReviewReminders`、`getDueReviews`、`advanceReview`、`cancelReview`

#### 5.2 修改 `LearningPath.vue`

- 在 `cycle` 函数中，当状态切换到 `mastered` 时调用 `scheduleReview(path, title)`
- 当从 `mastered` 切回其他状态时调用 `cancelReview(path)`

#### 5.3 修改 `MyProgressPanel.vue`

- 引入 `getReviewReminders`、`advanceReview`、`cancelReview`
- 计算 `dueReviews`（到期提醒列表）
- 追加"复习提醒"板块 UI
- 实现 `markReviewed`（推进到下一间隔）和 `skipReview`（取消）

#### 5.4 修改 `ContinueReading.vue`

- 引入 `getReviewReminders`
- 计算每个 item 是否有到期复习提醒
- 在卡片中显示 `⏰ 该复习了` 图标

### 验收标准
- 所有新增函数 TypeScript 类型正确
- Vue 组件引入和使用正确
- 刷新页面后功能正常

---

## 执行顺序

| 顺序 | 任务 | 文件数 |
|------|------|--------|
| 1 | 任务 2：复盘三步 | 9 个 practice .md |
| 2 | 任务 1：读者思考微提示 | 8 个核心 .md |
| 3 | 任务 4：学习路径引导文案 | 1 个 .vue |
| 4 | 任务 3：thinking-links.json | 1 个 .json |
| 5 | 任务 5：间隔重复提醒 | 4 个 .ts/.vue |

任务 1-4 互相独立，任务 5 放最后。

---

## 验收总清单

- [ ] 8 篇核心文章各有 2-3 个 `> 🤔 停下来想想：` 引用块
- [ ] 9 篇练习题末尾有「复盘三步」段落
- [ ] `thinking-links.json` 包含 16 个页面的跨域关联配置（原 9 + 新 7）
- [ ] `LearningPath.vue` 底部有复述自测引导文案
- [ ] `study-storage.ts` 新增间隔重复相关函数
- [ ] `LearningPath.vue` 掌握状态切换时触发/取消复习提醒
- [ ] `MyProgressPanel.vue` 显示到期复习提醒
- [ ] `ContinueReading.vue` 显示复习提醒图标
- [ ] `npx vitepress build docs` 构建成功
