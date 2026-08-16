# 008 - Java 板块仿 JavaGuide 架构调整与文章建议

## 元信息

| 项 | 内容 |
|---|---|
| 编号 | 008 |
| 日期 | 2026-08-12 |
| 来源 | 对标 javaguide.cn（156K+ Star，Java 面试第一竞品）的 sitemap + 全站结构拆解 |
| 状态 | 待实施 |
| 适用范围 | `docs/java/`、`docs/distributed/`（连带 `docs/.vitepress/config.mts` 的 sidebar） |
| 关联 | `006 算法板块仿 labuladong`、`007 去味基线`、`.claude/rules/content.md`、`CLAUDE.md` 红线②④ |

## 背景

**目标用户**：Java 后端社招面试者。Java 是本站首屏卖点和主要入口词，是流量与可信度的根基。

**现状一句话诊断**：Java 板块是**全站最薄弱的核心板块**——10 个文件里有 4 个 0 字节空白，缺并发/JVM/网络三大高频目录，已有内容粒度太粗；与算法板块（35 篇成型）形成鲜明反差。这是阶段一上线前**必须优先补齐**的板块，否则用户点进"Java 集合"看到白板，第一印象即废（参见 `CLAUDE.md` 红线②：宣称属实——目录有链接但内容空白，比没有更糟）。

**竞品**：javaguide.cn。覆盖 Java 基础/集合/并发/JVM/MySQL/Redis/分布式/高并发/高可用/系统设计/消息队列/计算机基础/AI，200+ 篇，标志性组织方式是「八股分页（-questions-01/02/03）+ 源码深入（-source-code）+ 原理与最佳实践三件套」。

**核心目标**：用 JavaGuide 的**架构方法**（按知识领域分目录、八股分页、源码篇）重构 Java 板块结构并补齐核心缺口；同时放大本项目独有的**场景题深度**（`distributed/scenarios/`）作为差异化护城河。**不追他的体量**——他 200+ 篇是 8 年积累，阶段一目标是把"核心高频 + 无空白"做到位。

---

## 战略前提：仿什么 / 不仿什么 / 靠什么反超

| 类别 | 内容 | 决定 |
|---|---|---|
| ✅ **仿** | 架构方法：按知识领域分目录（java/concurrent、java/jvm、database/mysql 独立成域）、八股分页（`xxx-questions.md`）、源码深入（HashMap 等）、原理+最佳实践三件套 | 全盘学 |
| ✅ **仿** | 「问答式」八股文结构（问题 → 答 → 延伸），满足"面试前刷题"查阅需求 | 学形式，但按 `content.md` 去味 |
| ❌ **不仿** | 体量（200+ 篇）、每个 Java 版本一篇（new-features 26 篇）、设计模式 23 篇、安全/JWT/SSO、Git/Maven/Docker 工具、知识星球/PDF/付费专栏、Algolia 搜索 | 阶段一不做，会稀释核心 |
| 🏆 **反超** | `distributed/scenarios/` 场景题深度（gateway/storage/service 全链路）；单篇深度（他广而浅，我少而深）；与算法 `04-system-algorithms` 联动 | 放大成招牌 |

**一句话原则**：**学他的骨架（怎么组织 Java 面试知识），不学他的广度（什么都覆盖），用场景题深度和单篇厚实度反超。**

---

## JavaGuide 架构拆解（从 sitemap 提炼）

```
/java/                Java 语言
├── basis/            基础：java-basic-questions-01/02/03（八股分页）+ 泛型/反射/代理/SPI/序列化/BigDecimal/值传递
├── collection/       集合：java-collection-questions-01/02 + 各 -source-code（HashMap/ConcurrentHashMap/ArrayList/LinkedList/...）
├── concurrent/       并发：java-concurrent-questions-01/02/03 + AQS/CAS/JMM/线程池/ThreadLocal/虚拟线程/ReentrantLock
├── jvm/              JVM：内存区域/GC/类加载/class 文件结构/类加载器/JVM 参数/监控工具/实战
├── io/               IO：IO 基础/IO 模型/IO 设计模式/NIO
└── new-features/     新特性：Java 8 ~ 26 每版本一篇

/cs-basics/           计算机基础
├── network/          网络：OSI 与 TCP/IP、TCP 握手挥手、HTTP/HTTPS、HTTP1.0vs1.1、状态码、DNS、ARP、NAT、网络攻击、访问网页全流程...（14 篇）
├── operating-system/ 操作系统：基础题 01/02、Linux、Shell
├── data-structure/   数据结构原理：线性/树/红黑树/堆/图/布隆过滤器
└── algorithms/       算法题推荐

/database/            数据库（独立成域）
├── mysql/            MySQL：索引/索引失效/事务隔离/MVCC/SQL 执行/日志/查询计划/优化规范...（13 篇）
├── redis/            Redis：数据结构 01/02/持久化/集群/阻塞问题/跳表/缓存读写策略/缓存基础...（12 篇）
├── sql/              SQL 基础题 01~05 + 语法总结
├── elasticsearch/    ES
└── mongodb/          MongoDB

/system-design/       系统设计
├── framework/spring/ Spring：IoC&AOP/事务/常用注解/设计模式/知识点总结/SpringBoot 自动装配/SpringBoot 源码/异步
├── security/         安全：JWT/SSO/加密/脱敏/敏感词过滤...
├── basis/            RESTful/命名/重构/软件工程/单元测试
└── design-pattern/   23 种设计模式

/distributed-system/  分布式
├── protocol/         CAP&BASE/Paxos/Raft/ZAB/Gossip/一致性哈希
├── rpc/              RPC/Dubbo/HTTP_RPC
├── distributed-process-coordination/  ZooKeeper
└── （分布式锁/事务/ID/网关/配置中心 独立页）

/high-performance/    高性能：负载均衡/CDN/SQL 优化/读写分离/深分页/冷热分离/消息队列（Kafka/RabbitMQ/RocketMQ/Disruptor）
/high-availability/   高可用：限流/熔断降级/幂等/冗余/超时重试/高可用系统设计/压测
/interview-preparation/ 面试准备：后端面试计划/Java 路线/简历/项目经验/自测题/面试要点
```

**精髓**：
1. **八股分页**（`-questions-01/02/03`）——满足"面试前刷题"的查阅形态，这是 JavaGuide 流量最大的入口形态。
2. **按知识领域物理分目录**——java/cs-basics/database/system-design/distributed 不混。
3. **源码深入 + 原理 + 最佳实践三件套**（如线程池：summary 原理 + best-practices 实战）。

---

## 现状对标（实测）

### docs/java/（10 文件，4 空白）

| 文件 | 字数 | 状态 | 对标 JavaGuide |
|---|---|---|---|
| `basics/index.md` | 19936 | ✅ 实质 | 对标 basis，但应拆分 |
| `basics/collection.md` | **0** | ❌ **空白** |对标 collection（JavaGuide 11 篇）|
| `mysql/index.md` | 8251 | 🟡 偏薄 | 对标 mysql（JavaGuide 13 篇）|
| `mysql/indexing.md` | **0** | ❌ **空白** | 对标 mysql-index |
| `redis/index.md` | 8591 | 🟡 偏薄 | 对标 redis（JavaGuide 12 篇）|
| `redis/data-structures.md` | **0** | ❌ **空白** | 对标 redis-data-structures-01/02 |
| `kafka/index.md` | **0** | ❌ **空白** | 对标 high-performance/message-queue |
| `spring/index.md` | 7578 | 🟡 偏薄 | 对标 framework/spring（JavaGuide 8 篇）|
| `os/index.md` | 21345 | ✅ 实质 | 对标 operating-system（独有优势：单篇厚）|
| `index.md` | 1505 | 🟡 死目录 | 对标 interview-preparation 路线 |

### docs/distributed/（5 文件，2 空白）

| 文件 | 字数 | 状态 |
|---|---|---|
| `scenarios/storage.md` | 22770 | ✅ 招牌级 |
| `scenarios/gateway.md` | 13362 | ✅ 招牌级 |
| `scenarios/index.md` | 657 | 🟡 偏薄 |
| `index.md` | **0** | ❌ **空白** |
| `scenarios/service.md` | **0** | ❌ **空白** |

### 核心缺口（致命）

| 缺口 | JavaGuide 对应 | 严重度 |
|---|---|---|
| **无并发目录** | concurrent/（14 篇） | 🔴 极高——面试 TOP1 |
| **无 JVM 目录** | jvm/（9 篇） | 🔴 极高——面试 TOP2 |
| **无网络目录** | cs-basics/network/（14 篇） | 🔴 高——面试必考 |
| **集合空白** | collection/（11 篇） | 🔴 高——面试 TOP4 |
| **4 个 0 字节文件** | — | 🔴 高——白板比没有更伤 |
| 无八股题集形态 | 所有 -questions-01/02/03 | 🟡 中——丢"刷题"流量 |

### 已有优势（要保留放大）

- `distributed/scenarios/gateway.md`（13362）、`storage.md`（22770）——**场景题招牌**，JavaGuide 有但分散，你集中深度，是反超点。
- `os/index.md`（21345）、`basics/index.md`（19936）——单篇厚实，质量基础在，重构时**保留+拆分**，不重写。

---

## 架构调整方案

### 方案选择：务实重构（推荐），不激进迁移

> 激进方案（把 mysql/redis 从 java/ 迁到 database/）会触发大面积链接断裂和 sidebar 重写，阻塞内容产出。阶段一**不推荐**。采用「保持 java/ 下结构 + 内部细化 + 补核心目录」。

### 终局目标目录（参考，非阶段一一期完成）

```
docs/java/
├── basics/              ← 已有 index(19936)，拆分 + 填 collection
│   ├── index.md
│   ├── collection.md    ← 填空白（HashMap/ConcurrentHashMap/ArrayList）
│   ├── java-basic-questions.md   ← 八股题集（仿 JavaGuide）
│   └── generics-reflection.md
├── concurrent/          ← 【新建·P0】面试 TOP1
│   ├── index.md
│   ├── thread-pool.md
│   ├── lock.md          (synchronized/ReentrantLock/AQS)
│   ├── volatile-jmm.md
│   ├── threadlocal.md
│   └── concurrent-questions.md
├── jvm/                 ← 【新建·P0】面试 TOP2
│   ├── index.md
│   ├── memory-area.md
│   ├── garbage-collection.md
│   ├── class-loading.md
│   └── jvm-questions.md
├── mysql/               ← 已有 index(8251)，拆分 + 填 indexing
│   ├── index.md
│   ├── indexing.md      ← 填空白
│   ├── transaction-mvcc.md
│   └── mysql-questions.md
├── redis/               ← 已有 index(8591)，拆分 + 填 data-structures
│   ├── index.md
│   ├── data-structures.md  ← 填空白
│   ├── persistence-cache-problems.md
│   └── redis-questions.md
├── spring/              ← 已有 index(7578)，拆分
│   ├── ioc-aop.md
│   ├── transaction.md
│   └── spring-questions.md
├── mq/
│   └── kafka.md         ← 填空白
└── os/                  ← 已有 index(21345)，保留

docs/cs-basics/          ← 【新建·P1】放网络
└── network/
    ├── tcp-http.md
    └── network-questions.md

docs/distributed/        ← 放大差异化招牌
├── index.md             ← 填空白
├── basics.md            ← CAP/Base（仿 protocol）
└── scenarios/           ← 招牌：全链路场景题
    ├── index.md
    ├── gateway.md       ✅ 已有
    ├── storage.md       ✅ 已有
    └── service.md       ← 填空白
```

### 迁移红线

- **已有实质内容的文件（basics 19936、os 21345、mysql 8251、redis 8591、spring 7578、gateway 13362、storage 22770）一律「保留 + 拆分」，不得删除重写。** 拆分时按考点切到子页，原 index 降为概述。
- 重构涉及 `config.mts` sidebar 改动，每批改完跑一次 `npm run docs:dev` 验证无死链。

---

## 文章层面建议

### 1. 强制遵循 `.claude/rules/content.md`（去 AI 味）

`CLAUDE.md` 红线④已规定：生成文章前必读 content.md 并过验收清单。Java 板块补缺口时会大量产新文，**这是去味的主战场**。重点：
- 每篇至少 1 个**具体**易错点（如 HashMap 负载因子为什么 0.75、ConcurrentHashMap 1.7 vs 1.8 分段锁差异、`synchronized` 锁升级过程）
- 禁空口承诺、禁结尾升华、禁 platitude、禁万能废话
- 见 007 去味基线

### 2. 仿 JavaGuide「问答式」结构，但去味

JavaGuide 的八股分页是"问题 → 答 → 延伸"。建议 `xxx-questions.md` 用此结构，但每题加**一句"面试官追问"或"常见误解"**，比 JavaGuide 多一层深度——这是反超点。例：

```markdown
## Q: HashMap 为什么用红黑树阈值 8？
**答**：泊松分布下链表长度到 8 的概率极低（约 0.00000006）...
**面试官追问**：那为什么退回链表的阈值是 6 不是 7？
**常见误解**：很多人以为 8 是性能最优解，其实是"概率+防御性"的折中。
```

### 3. 源码篇要讲"为什么"，不是 Wikipedia

JavaGuide 的 `-source-code` 篇容易写成"代码翻译"。要求：每个设计决策回答**为什么**（HashMap 为什么 2 次幂容量、为什么 0.75、ConcurrentHashMap 为什么 1.8 弃用分段锁）。没"为什么"的源码篇 = 抄源码，无价值。

### 4. 招牌场景题（distributed/scenarios）做成深于 JavaGuide 的招牌

- 补 `service.md`（业务逻辑层场景题）、`distributed/index.md`、`basics.md`（CAP/Base）
- 每篇做"算法 ↔ 后端场景"双向链接：scenarios/gateway 链算法 `04-system-algorithms/rate-limiting`；scenarios/storage 链 `04-system-algorithms/caching`。这是 JavaGuide 做不到的网状结构（他算法和后端是分开的两个站区）。

### 5. 诚实化首页与学习路线

- `java/index.md`（1505 字死目录）和首页 LearningPath 一样的问题——按 001 第 4 条 / 006 批 3 处理：要么配置化、要么改成可点的真实链接清单，别写"企业级应用开发""高并发系统设计"等空话。

---

## 优先级总览与实施顺序

| # | 任务 | 优先级 | 工作量 | 类型 |
|---|---|---|---|---|
| 1 | 填 4 个空白文件（collection/indexing/data-structures/kafka） | P0 | 中 | 补缺口 |
| 2 | 新建 `java/concurrent/`（5–6 篇） | P0 | 大 | 补缺口 |
| 3 | 新建 `java/jvm/`（4–5 篇） | P0 | 大 | 补缺口 |
| 4 | 填 distributed 空白（index/basics/service） | P0 | 中 | 补缺口 |
| 5 | 拆分厚 index（basics/mysql/redis/spring → 子页） | P1 | 中 | 重构 |
| 6 | 新建 `cs-basics/network/`（3 篇） | P1 | 中 | 补缺口 |
| 7 | 各域补 `xxx-questions.md` 八股题集 | P1 | 中 | 增量 |
| 8 | 招牌深化：scenarios 双向链接 + service.md 厚写 | P1 | 中 | 反超 |
| 9 | 首页/学习路线诚实化 | P2 | 小 | 体验 |

### 建议分批

- **第一批 · 补空白 + 建核心**（~2 周，P0）：任务 1+2+3+4。完成后 Java 板块从"残缺"变"核心齐全"，达上线门槛。
- **第二批 · 拆分 + 题集**（~2 周，P1）：任务 5+6+7。
- **第三批 · 招牌与体验**（持续）：任务 8+9。

每批改完跑 `docs:dev` 验链接；每篇按 `content.md` 验收清单过；完成在 `docs/changelog.md` 记录。

---

## 规则呼应

- 本计划**纯内容工作**，0 后端代码、不碰判题/可视化，符合 `CLAUDE.md` 阶段一与 `phase-gate.md`。
- 所有新文章强制走 `.claude/rules/content.md`（红线④），用 007 作为去味基线。
- 目录重构遵循红线②：拆分时不得宣称"已覆盖 X" unless 子页真的写完了——**先写完再挂 sidebar 链接，杜绝新的空白页**。
- 与 `006 算法板块`共享同一战略框架：仿架构方法、不仿体量、放大独占场景题。

> 首推动手项：第一批任务 1 的 `java/basics/collection.md`（填空白）——它是面试 TOP4、首页第一个 feature 卡的目标、且 basics/index 已有上下文可承接。写完即验证「JavaGuide 式八股 + content.md 去味」的产出长什么样。
