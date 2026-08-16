# 替换"中二"术语实施计划

## 背景
用户认为项目中部分术语过于"中二"（如"算法之魂"、"物理基石"、"实战通关"等），需要替换为更平实、专业的表达。

## 调研结论

### 需要修改的文件（共 9 个）

| # | 文件路径 | 修改内容 |
|---|---------|---------|
| 1 | `docs/algorithm/index.md` | 主标题、欢迎语、学习路线图 3 个阶段名称、目录结构注释 |
| 2 | `docs/algorithm/01-methodology/index.md` | 标题 + 简介段落 |
| 3 | `docs/algorithm/02-data-structures/index.md` | 标题 + 简介段落 |
| 4 | `docs/algorithm/03-algorithm-patterns/index.md` | 标题 + 简介段落 |
| 5 | `docs/algorithm/05-top-interview-100/index.md` | 标题 + 简介段落 |
| 6 | `docs/algorithm/00-algorithm-frameworks/index.md` | 一处引用 |
| 7 | `docs/index.md` | 首页 hero 标题 + alt |
| 8 | `docs/java/concurrent/index.md` | "天花板" → "重点和难点" |
| 9 | `docs/java/spring/ioc-aop.md` | "基石" → "核心" |
| 10 | `docs/algorithm/04-system-algorithms/consistent-hashing.md` | "基石" → "支撑" |
| 11 | `docs/algorithm/05-top-interview-100/arrays/index.md` | "大厂" 标签 |

### 具体替换映射

#### 核心术语替换（算法板块）

| 原词 | 替换为 | 出现位置 |
|------|--------|---------|
| 大厂面试手撕代码题 | 面试算法练习 | algorithm/index.md L1 |
| 欢迎来到大厂面试手撕代码题的学习专区！这里汇集了算法与数据结构的核心知识，帮助你在面试中脱颖而出。 | 欢迎来到面试算法练习专区！这里汇集了算法与数据结构的核心知识，帮助你系统地准备算法面试。 | algorithm/index.md L3 |
| 算法之魂 | 算法方法论 | algorithm/index.md L8, L238；01-methodology/index.md L1, L3 |
| 物理基石 | 数据结构基础 | algorithm/index.md L9, L243；02-data-structures/index.md L1, L3 |
| 逻辑模型 | 算法模式 | algorithm/index.md L12, L249；03-algorithm-patterns/index.md L1, L3 |
| 工程算法 | 系统算法 | algorithm/index.md L255 |
| 后端核心 (你的亮点) | 后端核心 | algorithm/index.md L255 |
| 实战通关 | 高频真题练习 | algorithm/index.md L15, L261；05-top-interview-100/index.md L1, L3；00-algorithm-frameworks/index.md L44 |
| 高频真题 | 真题训练 | algorithm/index.md L16 |

#### 首页标题

| 原词 | 替换为 | 出现位置 |
|------|--------|---------|
| Java 后端面试全栈通关指南 | Java 后端面试知识体系 | docs/index.md L6, L10 |

#### 其他散落位置

| 原词 | 替换为 | 出现位置 |
|------|--------|---------|
| 并发是 Java 面试的天花板 | 并发是 Java 面试的重点和难点 | java/concurrent/index.md L117 |
| Spring 两大基石 IoC + AOP | Spring 两大核心 IoC + AOP | java/spring/ioc-aop.md L7 |
| 底层基石（一致性哈希） | 底层支撑 | algorithm/04-system-algorithms/consistent-hashing.md L7 |
| `<span class="question-tag">大厂</span>` | `<span class="question-tag">高频</span>` | algorithm/05-top-interview-100/arrays/index.md L91 |

## 实施步骤

### Step 1：修改 `docs/algorithm/index.md`（改动最多）
- 替换主标题
- 替换欢迎语
- 替换学习路线图三个阶段的术语
- 替换目录结构注释中的术语

### Step 2：修改四个子板块 index.md
- `01-methodology/index.md`：标题 + 简介
- `02-data-structures/index.md`：标题 + 简介
- `03-algorithm-patterns/index.md`：标题 + 简介
- `05-top-interview-100/index.md`：标题 + 简介

### Step 3：修改引用处
- `00-algorithm-frameworks/index.md`：L44 "实战通关" → "高频真题练习"
- `algorithm/index.md` 目录结构注释同步更新

### Step 4：修改首页
- `docs/index.md`：hero text 和 alt

### Step 5：修改其他散落位置
- `java/concurrent/index.md`：天花板 → 重点和难点
- `java/spring/ioc-aop.md`：基石 → 核心
- `consistent-hashing.md`：基石 → 支撑
- `arrays/index.md`：大厂标签 → 高频

### Step 6：验证
- 运行 `npx vitepress build docs` 确保构建成功

## 不修改的内容
- `config.mts` 侧边栏文本已使用平实术语（方法论、数据结构、算法模式等），无需修改
- AI 板块的 "实战环节" 等用词不在本次范围（用户只提到算法板块的"算法之魂、物理基石"）
- "实战" 作为普通词汇出现在句子中时（如"通过解决高频面试题来实战练习"），保留不动
- "天花板" 在 AI 板块技术描述中（GOT 推理能力）保留不动
