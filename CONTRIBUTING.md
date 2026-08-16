# 内容贡献指南

本文件规定「我是面试大王」知识库(`docs/`)的目录结构和命名约定。**新增或移动内容前请先读完**,目的是防止结构再次腐化。

> 历史教训:本项目曾出现根级与 `java-backend/` 下双重目录、`config.mts` 大量指向不存在文件的死链占位、`Spring/` 大小写不一、`Memory Project.md` 带空格等问题。本文件就是为避免重蹈覆辙。

---

## 一、顶层目录归属规则

`docs/` 下只允许以下顶层目录。**新增顶层目录前必须先讨论。**

| 目录 | 收录范围 | 不收录 |
|------|---------|--------|
| `java/` | Java 语言及 JVM 生态(基础、Spring、Redis、MySQL、Kafka、操作系统等) | 与 Java 无关的通用算法、纯分布式理论 |
| `distributed/` | 分布式理论与后端通用场景题(接入路由、业务逻辑、持久化异步层) | 具体语言的 API 细节 |
| `algorithm/` | 算法与数据结构(框架、方法论、数据结构、算法模式、系统算法、面试题) | 与算法无关的工程实践 |
| `ai/` | AI Agent 知识库(LLM、Agent、MCP、Skill、工程落地、RAG) | 非 AI 的后端话题 |
| `projects/` | 完整项目实战教程(每个子目录一个项目) | 零散知识点文章 |
| `public/` | 静态资源(图片等) | markdown 文档 |
| `.vitepress/` | VitePress 配置与主题 | 内容文档 |

**横跨多个领域时**:按"读者主要为什么而来"归类。例:「Redis 分布式锁」放 `java/redis/`(读者查 Redis),不放 `distributed/`。

---

## 二、命名规范

### 目录命名

- **全小写 kebab-case**:`my-topic`,不允许 `MyTopic`、`my_topic`、`Spring`(已修正为 `spring`)
- **数字前缀仅用于排序**:同层级需明确阅读顺序时用 `00-`、`01-`(如 `algorithm/00-algorithm-frameworks/`);无顺序要求的不用前缀(如 `java/redis/`)
- **单词简短**:目录名是 URL 的一部分,越短越好。`basics` 优于 `java-basics`(已在 `java/` 下,前缀冗余)

### 文件命名

- **全小写 kebab-case**,不允许空格、不允许中文文件名、不允许 PascalCase
- 反例:`Memory Project.md`(URL 编码为 `%20`,已修正为 `memory-project.md`)
- **栏目首页统一用 `index.md`**:每个目录必须有一个 `index.md` 作为入口

---

## 三、新增内容流程

1. **定位目录**:按第一节判断归属
2. **创建文件**:遵循命名规范(kebab-case,无空格)
3. **更新侧边栏**:在 `docs/.vitepress/config.mts` 对应 sidebar 加入条目
   - **只列真实存在的文件**,不要预先放占位条目(这是上次结构腐化的主因)
4. **更新栏目 index**(可选):重要内容在所属目录的 `index.md` 加导航链接

---

## 四、内部链接规范

- 指向**目录**的链接用尾斜杠:`/java/redis/`(VitePress 解析为该目录的 `index.md`)
- 指向**具体文件**的链接不带 `.md` 后缀、不带尾斜杠:`/java/redis/data-structures`
- **改动目录路径后,必须全局搜索旧路径并更新所有引用**,避免死链
  - 搜索命令(在仓库根):`grep -rn "/旧路径/" docs/`

---

## 五、index.md 用法

每个目录的 `index.md` 是该栏目的**门面**,应包含:
- 栏目简介(1 ~ 2 段)
- 子内容导航(链接到子页面)

不要用 `index.md` 堆砌完整文章(那是子页面的事)。

---

## 六、禁止事项

- 在 `docs/` 下放源码文件(`.py`、`.js` 等)。源码属于项目根的 `examples/` 或独立仓库
- 创建与现有目录语义重叠的新目录(如已有 `java/redis/` 又建一个根级 `redis/`)
- 在 `config.mts` 里列出不存在的页面作"占位"。要扩建骨架,请用 `// TODO:` 注释,不要放死链

---

## 七、相关文档

- [ROADMAP.md](./ROADMAP.md) — 项目架构与长期发展规划
