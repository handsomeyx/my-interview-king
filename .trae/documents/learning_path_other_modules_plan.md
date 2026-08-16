# 为其他模块创建学习路径图计划

## 背景
算法模块已创建了 `learning-path.md` 学习路径图页面（含全景思维导图、三阶段学习路线、详细子图、跨域关联）。用户希望将此模式复制到 Java、分布式、AI、项目实战四个模块。

## 调研结论

### 当前状态
- `docs/algorithm/learning-path.md` — 已完成，含 5 张 Mermaid 图
- `docs/.vitepress/theme/thinking-links.json` — 已配置跨域关联
- `docs/.vitepress/config.mts` — 侧边栏各模块有独立分组
- 各模块 index.md 结构：Java 有分阶段列表、分布式有学习顺序建议、AI 有文字版路线图

### 需要创建的文件（4 个学习路径页面）

| # | 文件路径 | 覆盖模块 |
|---|---------|---------|
| 1 | `docs/java/learning-path.md` | Java 后端（语言→Spring→数据库→中间件） |
| 2 | `docs/distributed/learning-path.md` | 分布式（理论线→场景线） |
| 3 | `docs/ai/learning-path.md` | AI Agent（入门→进阶→高级） |
| 4 | `docs/projects/learning-path.md` | 项目实战（智能面试助手开发路径） |

### 需要修改的文件

| # | 文件路径 | 修改内容 |
|---|---------|---------|
| 5 | `docs/java/index.md` | 顶部添加学习路径图链接 |
| 6 | `docs/distributed/index.md` | 顶部添加学习路径图链接 |
| 7 | `docs/ai/index.md` | 顶部添加学习路径图链接 |
| 8 | `docs/projects/interview-agent/index.md` | 顶部添加学习路径图链接 |
| 9 | `docs/.vitepress/config.mts` | 4 个侧边栏分组各追加「🗺️ 学习路径图」条目 |

### 每个学习路径页面包含的内容

参照 `docs/algorithm/learning-path.md` 模板，每个页面包含：

1. **全景思维导图**（mindmap）— 展示模块完整知识体系
2. **阶段学习流程图**（flowchart TB）— 展示分阶段学习路径
3. **详细子图**（flowchart TB × 2-3）— 每个阶段展开详细节点
4. **跨域关联图**（flowchart LR）— 模块间知识关联
5. **推荐学习顺序** — 文字版总结

## 实施步骤

### Step 1：创建 Java 学习路径图
- 创建 `docs/java/learning-path.md`
- 覆盖：Java 语言基础 → Spring 框架 → 数据库（MySQL/Redis/MyBatis）→ 中间件（Kafka）
- 三阶段：打基础（语言+集合+并发）→ 进阶（JVM+Spring+MySQL+Redis）→ 实战（Kafka+OS+综合）
- 修改 `docs/java/index.md` 添加链接
- 修改 `config.mts` Java 侧边栏添加条目

### Step 2：创建分布式学习路径图
- 创建 `docs/distributed/learning-path.md`
- 两条线：理论线（CAP/BASE/共识）→ 场景线（网关/存储/业务）
- 修改 `docs/distributed/index.md` 添加链接
- 修改 `config.mts` 分布式侧边栏添加条目

### Step 3：创建 AI 学习路径图
- 创建 `docs/ai/learning-path.md`
- 三阶段：入门（LLM+Agent 概念）→ 进阶（框架+实战）→ 高级（多 Agent+RAG+工程化）
- 修改 `docs/ai/index.md` 添加链接
- 修改 `config.mts` AI 侧边栏添加条目

### Step 4：创建项目实战学习路径图
- 创建 `docs/projects/learning-path.md`
- 按智能面试助手项目的开发阶段组织
- 修改 `docs/projects/interview-agent/index.md` 添加链接
- 修改 `config.mts` 项目实战侧边栏添加条目

### Step 5：构建验证
- `npx vitepress build docs` 确保所有 Mermaid 图正确渲染、侧边栏链接有效

## Mermaid 图设计规范

每个页面的图表遵循以下规范：
- 使用 emoji 增强可读性
- 使用 subgraph 分组阶段
- 使用不同颜色区分阶段（蓝=基础、绿=进阶、橙=高级）
- 节点文字简洁（3-8 个字）
- 跨域关联图使用 LR 方向，展示模块间的知识流动
