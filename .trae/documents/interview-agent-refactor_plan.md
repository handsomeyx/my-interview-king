# 面试助手 App 重构计划

> 基于 `需求变更/010-面试助手App重构需求-20260816.md`，采用「先 Demo → 再迭代」的分阶段策略。

---

## 一、现状总结

| 项 | 现状 |
|---|---|
| 代码位置 | `archive/frontend-interview-agent/`（旧版，需重构） |
| App.vue | 1150+ 行巨型单文件组件，无拆分 |
| 后端 | 单文件 `server.py`（570 行），Flask + SQLite，keyword mock |
| 状态管理 | 无 Pinia，全靠组件内 reactive/ref |
| HTTP | 无 Axios，原生 fetch |
| Markdown | 正则 replace 伪渲染 |
| 流式 | `setTimeout` 逐字模拟，非 SSE |
| 图表 | 无 echarts，知识图谱靠假数据 |

## 二、重构策略：4 阶段迭代

```
阶段 1：骨架 Demo（可跑起来的最小版本）
  → 工程基建 + 布局骨架 + 基础组件拆分
  → 验收：npm run dev 能启动，有侧边栏 + 聊天区 + 输入框

阶段 2：核心闭环（替换 Mock，真流式）
  → SSE 流式对话 + marked 渲染 + AI 服务门面
  → 验收：真实打字机效果，Markdown 正确渲染

阶段 3：功能完善（上传、图谱、持久化）
  → 文件/图片上传 + echarts 图谱 + 对话持久化
  → 验收：全链路跑通

阶段 4：体验打磨（响应式、动效、错误处理）
  → 移动端适配 + 加载状态 + 错误边界 + a11y
  → 验收：Definition of Done 全部通过
```

---

## 阶段 1：骨架 Demo（最小可运行版本）

### 1.1 目标
搭建新的前端项目结构，实现布局骨架，让 `npm run dev` 能跑起来，有基本的聊天界面。

### 1.2 文件变更清单

#### 新建目录结构
```
frontend-interview-agent/           ← 从 archive 搬到根目录
├── src/
│   ├── App.vue                     ← 瘦身为布局骨架（< 100 行）
│   ├── main.ts                     ← 引入 Pinia、样式
│   ├── style.css                   ← 全局样式（保留旧版设计变量）
│   ├── components/
│   │   ├── layout/
│   │   │   ├── AppSidebar.vue      ← 左侧导航 + 历史列表
│   │   │   ├── AppHeader.vue       ← 顶部标题 + 用户信息
│   │   │   └── AppMain.vue         ← 右侧主区域容器
│   │   ├── chat/
│   │   │   ├── ChatMessage.vue     ← 单条消息（用户/AI）
│   │   │   └── ChatInput.vue       ← 输入框 + 发送按钮
│   │   ├── panels/
│   │   │   ├── ConfidencePanel.vue ← 信心指数（占位）
│   │   │   ├── KnowledgeGraph.vue  ← 知识图谱（占位）
│   │   │   └── FollowUpPanel.vue   ← 追问链（占位）
│   │   ├── modals/
│   │   │   ├── LoginModal.vue
│   │   │   └── RegisterModal.vue
│   │   └── common/
│   │       └── MarkdownRenderer.vue ← marked + highlight.js 封装
│   ├── stores/
│   │   ├── chat.ts                 ← 对话状态
│   │   └── user.ts                 ← 用户/鉴权状态
│   ├── api/
│   │   └── http.ts                 ← Axios 实例 + 拦截器
│   ├── types/
│   │   ├── chat.ts
│   │   └── user.ts
│   └── App.vue
├── backend/                        ← 后端重构（蓝图拆分）
│   ├── app.py                      ← 入口，注册蓝图
│   ├── config.py                   ← 配置
│   ├── extensions.py               ← Flask 扩展
│   ├── models/
│   │   ├── user.py
│   │   └── chat.py
│   ├── blueprints/
│   │   ├── auth_bp.py
│   │   ├── chat_bp.py
│   │   ├── ai_bp.py
│   │   └── upload_bp.py
│   ├── services/
│   │   ├── ai_service.py
│   │   ├── chat_service.py
│   │   └── upload_service.py
│   └── requirements.txt
├── package.json                    ← 新增依赖
├── vite.config.ts                  ← 加路径别名
└── tsconfig.json                   ← 加路径映射
```

#### 修改的文件

| 文件 | 变更内容 |
|---|---|
| `package.json` | 新增 pinia、axios、marked、highlight.js、echarts 依赖 |
| `vite.config.ts` | 添加 `@` → `src` 路径别名 |
| `tsconfig.json` | 添加 `paths` 映射 |
| `src/main.ts` | 引入 Pinia store |
| `src/App.vue` | 从 1150+ 行瘦身为布局骨架 |
| `backend/requirements.txt` | 新增 flask-cors、flask-sse、gunicorn |

#### 新增的依赖

```json
{
  "dependencies": {
    "pinia": "^2.2.0",
    "axios": "^1.7.0",
    "marked": "^14.0.0",
    "highlight.js": "^11.10.0",
    "echarts": "^5.5.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0"
  }
}
```

### 1.3 实施步骤

| 步骤 | 任务 | 产出 |
|---|---|---|
| 1 | 从 `archive/frontend-interview-agent/` 复制到根目录 `frontend-interview-agent/` | 新工作目录 |
| 2 | 更新 `package.json`，安装新依赖 | `npm install` 通过 |
| 3 | 配置 `vite.config.ts` + `tsconfig.json` 路径别名 | `@/components/...` 导入正常 |
| 4 | 创建 `types/` 类型定义文件 | 无 TS 错误 |
| 5 | 创建 `api/http.ts`（Axios 实例 + 拦截器） | 统一请求入口 |
| 6 | 创建 `stores/chat.ts` + `stores/user.ts` | Pinia store 可用 |
| 7 | 拆分 `AppSidebar.vue` | 侧边栏导航 + 历史列表 |
| 8 | 拆分 `AppHeader.vue` | 顶部栏 |
| 9 | 拆分 `ChatMessage.vue` | 单条消息组件 |
| 10 | 拆分 `ChatInput.vue` | 输入框组件 |
| 11 | 创建面板占位组件 | 3 个面板组件 |
| 12 | 创建 `LoginModal.vue` + `RegisterModal.vue` | 登录/注册模态框 |
| 13 | 重写 `App.vue` 为布局骨架 | < 100 行 |
| 14 | 后端目录结构搭建（蓝图骨架） | Flask 蓝图可启动 |
| 15 | `npm run dev` + `python app.py` 验证 | 前后端均启动成功 |

### 1.4 验收标准
- [x] `npm install` 无错误
- [x] `npm run dev` 前端启动成功（端口 3000）
- [x] `python app.py` 后端启动成功（端口 5000）
- [x] App.vue 行数 < 100 行
- [x] 页面有：侧边栏 + 聊天区 + 输入框 + 顶部栏
- [x] 点击"发送"按钮能发送消息，显示在对话区（Mock 回显即可）

---

## 阶段 2：核心闭环（SSE 流式 + Markdown）

### 2.1 目标
替换伪流式为真实 SSE，替换正则 Markdown 为 marked，打通 AI 服务门面。

### 2.2 文件变更清单

| 文件 | 变更内容 |
|---|---|
| `components/common/MarkdownRenderer.vue` | 新建，marked + highlight.js 封装 |
| `composables/useSSE.ts` | 新建，SSE 流式通信封装 |
| `composables/useMarkdown.ts` | 新建，Markdown 解析封装 |
| `components/chat/ChatStreaming.vue` | 新建，流式输出控制（暂停/停止） |
| `stores/chat.ts` | 扩展，支持流式状态管理 |
| `backend/services/ai_service.py` | 新建，AI 服务门面（mock/llm 可切换） |
| `backend/blueprints/ai_bp.py` | 新建，SSE 流式端点 |
| `backend/blueprints/chat_bp.py` | 新建，对话端点 |

### 2.3 实施步骤

| 步骤 | 任务 |
|---|---|
| 1 | 创建 `MarkdownRenderer.vue`（marked + highlight.js） |
| 2 | 创建 `useSSE.ts` composable |
| 3 | 创建 `useMarkdown.ts` composable |
| 4 | 扩展 `ChatMessage.vue` 使用 MarkdownRenderer |
| 5 | 创建 `ChatStreaming.vue`（暂停/继续/停止） |
| 6 | 扩展 `stores/chat.ts` 支持流式状态 |
| 7 | 后端：创建 `services/ai_service.py`（Mock 模式） |
| 8 | 后端：创建 `blueprints/ai_bp.py`（SSE 端点） |
| 9 | 后端：创建 `blueprints/chat_bp.py` |
| 10 | 前后端联调：SSE 流式对话跑通 |

### 2.4 验收标准
- [x] SSE 打字机效果真实流畅
- [x] 支持暂停/继续/停止
- [x] Markdown 渲染正确（代码块高亮、表格、列表嵌套）
- [x] AI Mock 模式正常返回

---

## 阶段 3：功能完善

### 3.1 目标
打通文件上传、知识图谱 echarts 渲染、对话持久化。

### 3.2 实施步骤

| 步骤 | 任务 |
|---|---|
| 1 | 后端：文件/图片上传 API + 存储服务 |
| 2 | 前端：上传组件对接后端 |
| 3 | 前端：`KnowledgeGraph.vue` 用 echarts 渲染 |
| 4 | 后端：对话持久化到 SQLite（Chat/Message 表） |
| 5 | 后端：对话次数限制逻辑修正 |
| 6 | 信心指数真实计算（替换 random） |

### 3.3 验收标准
- [x] 文件上传 → 后端存储 → 对话中展示，全链路跑通
- [x] 图片上传 → 预览 → 后端存储 → 对话中渲染
- [x] 知识图谱节点可交互
- [x] 刷新页面历史对话不丢失
- [x] 游客 3 次限制，登录后无限制

---

## 阶段 4：体验打磨

### 4.1 目标
响应式、动效、错误处理、无障碍。

### 4.2 实施步骤

| 步骤 | 任务 |
|---|---|
| 1 | 对话气泡样式优化 |
| 2 | 移动端响应式（375px） |
| 3 | 空状态引导 |
| 4 | 全局错误边界处理 |
| 5 | 加载骨架屏 |
| 6 | a11y 基础支持 |
| 7 | README 更新 |

### 4.3 验收标准
- [x] 移动端布局可用
- [x] API 失败有友好提示
- [x] 旧版功能无回归

---

## 三、技术决策记录

| 决策点 | 选择 | 理由 |
|---|---|---|
| 前端框架 | Vue 3.5 + TypeScript | 已有基础，保持一致 |
| 状态管理 | Pinia | 比 Vuex 轻，TS 支持好 |
| HTTP | Axios | 拦截器统一处理鉴权 |
| Markdown | marked + highlight.js | 业界标准 |
| 流式 | SSE | AI 场景比 WebSocket 简单 |
| 图表 | echarts | 轻量、中文文档好 |
| 后端 | Flask + 蓝图 | 渐进式重构 |
| 数据库 | SQLite（MVP） | 后续迁移 Postgres |
| AI 接入 | Mock 优先，可插拔 LLM | 先跑通，便于后续切换 |
| 代码位置 | 根目录 `frontend-interview-agent/` | 替代 `archive/` 旧版 |

## 四、风险与应对

| 风险 | 应对 |
|---|---|
| Tailwind CSS v4 alpha 兼容性 | 保留现有 Tailwind 配置，不升级到 v4 正式版 |
| SSE 跨域问题 | 后端 CORS 已配置，SSE 需额外设置 `Access-Control-Allow-Origin` |
| 旧版功能回归 | 每阶段完成后回归测试核心路径 |
| 依赖版本冲突 | 锁定版本号，使用 `package-lock.json` |
