# AI 服务门面 + SSE 流式链路 实施计划

## 一、调研结论

### 1.1 AI 接入方案

经过对市面上免费 AI API 的详细调研，确定 **双轨策略**：

| 优先级 | 方案 | 免费额度 | 优点 | 缺点 |
|--------|------|----------|------|------|
| **首选** | 智谱 AI GLM-4.7-Flash | 2000万 Token 永久 | 中文优化好、编程强、30 QPS、兼容 OpenAI 格式 | 需注册获取 API Key |
| **备选** | Ollama 本地部署 Qwen2.5-7B | 完全免费无限 | 零成本、隐私安全、离线可用 | 需下载 ~4GB 模型、速度依硬件 |

**策略：** AI 服务门面设计为可插拔架构，默认使用智谱 AI（配置 `AI_PROVIDER=zhipu`），同时支持 Ollama 本地部署（`AI_PROVIDER=ollama`）作为兜底。开发阶段也保留 Mock 模式（`AI_PROVIDER=mock`）。

### 1.2 后端现状盘点

| 模块 | 文件 | 现状 | 需要改动 |
|------|------|------|----------|
| Flask 入口 | `backend/app.py` | 3个蓝图(auth/chat/analysis) | 新增 ai_bp 蓝图、配置管理 |
| 配置 | `backend/config.py` | 基础配置，无 AI 相关 | 添加 AI_PROVIDER、API Key、模型名 |
| 蓝图注册 | `backend/blueprints/__init__.py` | 3个蓝图 | 新增 ai_bp |
| 路由层 | `backend/blueprints/chat_routes.py` | 直接拼 SQL + 直接调 mock_data | 改为调用 Service 层 |
| 路由层 | `backend/blueprints/analysis_routes.py` | 直接调 mock_data | 改为调用 Service 层 |
| Mock 数据 | `backend/utils/mock_data.py` | keyword 匹配 | 保留，包装为 MockProvider |
| 依赖 | `backend/requirements.txt` | Flask + Flask-CORS | 新增 httpx（AI HTTP 客户端） |

### 1.3 前端现状盘点

| 模块 | 文件 | 现状 | 需要改动 |
|------|------|------|----------|
| 入口 | `src/App.vue` | 37行，布局骨架 | 不需要改 |
| 主区域 | `src/components/layout/AppMain.vue` | handleSend 内嵌（~70行） | 抽离到 composable |
| 状态 | `src/stores/chat.ts` | 基础 CRUD，无流式支持 | 添加流式状态管理 |
| API | `src/api/services.ts` | REST API，无 SSE | 添加 SSE 接口 |
| API | `src/api/http.ts` | Axios 实例 | 不需要改 |
| 类型 | `src/types/chat.ts` | Message/Chat/KGNode | 添加 SSEEvent 类型 |
| 消息 | `src/components/chat/ChatMessage.vue` | 静态渲染 | 支持流式增量渲染 |
| 图谱 | `src/components/panels/KnowledgeGraph.vue` | 简单列表 | 升级为 echarts 可视化 |
| 输入 | `src/components/chat/ChatInput.vue` | 基本输入 | 不需要改（后续加流式控制） |
| 面板 | `src/components/panels/ConfidencePanel.vue` | 仪表盘 | 后续优化 |
| 面板 | `src/components/panels/FollowUpPanel.vue` | 追问链 | 后续优化 |

---

## 二、实施步骤

### Step 1：后端基础设施（config + requirements + services 目录结构）

**改动文件：**
- 修改 `backend/requirements.txt` — 添加 `httpx`
- 修改 `backend/config.py` — 添加 AI 相关配置
- 新建 `backend/services/__init__.py`
- 新建 `backend/services/ai_service.py` — AI 服务门面
- 新建 `backend/services/chat_service.py` — 对话业务逻辑
- 新建 `backend/repositories/__init__.py`
- 新建 `backend/repositories/chat_repo.py` — 数据访问层

**核心设计：**

```python
# backend/config.py 新增配置
class Config:
    # ... 现有配置 ...
    AI_PROVIDER = os.environ.get('AI_PROVIDER', 'mock')  # mock | zhipu | ollama
    AI_API_KEY = os.environ.get('AI_API_KEY', '')
    AI_BASE_URL = os.environ.get('AI_BASE_URL', 'https://open.bigmodel.cn/api/paas/v4')
    AI_MODEL = os.environ.get('AI_MODEL', 'glm-4-flash')
    AI_TIMEOUT = int(os.environ.get('AI_TIMEOUT', '30'))
```

```python
# backend/services/ai_service.py 架构
class AIService:
    """AI 服务门面，支持多提供者"""
    
    def __init__(self, provider: str = "mock"):
        self.provider = provider
    
    async def chat_stream(self, messages: list) -> AsyncGenerator[dict, None]:
        """流式对话"""
        if self.provider == "mock":
            async for chunk in self._mock_stream(messages):
                yield chunk
        elif self.provider == "zhipu":
            async for chunk in self._zhipu_stream(messages):
                yield chunk
        elif self.provider == "ollama":
            async for chunk in self._ollama_stream(messages):
                yield chunk
    
    async def analyze(self, question: str, answer: str) -> dict:
        """分析回答质量"""
        ...
    
    @classmethod
    def from_config(cls):
        """从 Flask config 创建"""
        ...
```

### Step 2：后端 SSE 端点 + 蓝图注册

**改动文件：**
- 新建 `backend/blueprints/ai_routes.py` — SSE 流式端点
- 修改 `backend/blueprints/__init__.py` — 注册 ai_bp
- 修改 `backend/app.py` — 注册蓝图

**核心 API：**

| Method | Path | 功能 |
|--------|------|------|
| POST | `/api/ai/chat/stream` | SSE 流式对话 |
| POST | `/api/ai/analyze` | 分析回答质量 |
| GET | `/api/ai/providers` | 获取可用 AI 提供者列表 |

**SSE 事件格式：**
```python
# 前端解析的事件
{
    "type": "token",      # token 文本片段
    "content": "你好"     # token 内容
}
{
    "type": "meta",       # 元数据
    "confidence": 85,     # 信心指数
    "followUps": ["..."], # 追问建议
    "knowledgeGraph": [...] # 知识图谱
}
{
    "type": "done"        # 结束
}
{
    "type": "error",      # 错误
    "error": "..."
}
```

### Step 3：后端重构（chat_routes + analysis_routes 调用 Service 层）

**改动文件：**
- 修改 `backend/blueprints/chat_routes.py` — 路由层改为调用 chat_service
- 修改 `backend/blueprints/analysis_routes.py` — 路由层改为调用 ai_service
- 修改 `backend/utils/mock_data.py` — 保留，供 MockProvider 使用

**重构原则：**
- 路由层只做：参数校验 → 调用 Service → 返回 JSON
- SQL 集中到 Repository 层
- 业务逻辑集中到 Service 层
- Mock 数据通过 AIService MockProvider 调用

### Step 4：前端 SSE composable + 类型定义

**改动文件：**
- 新建 `src/composables/useSSE.ts` — SSE 流式消费
- 新建 `src/composables/useChat.ts` — 聊天核心逻辑
- 修改 `src/types/chat.ts` — 添加 SSEEvent 类型
- 修改 `src/api/services.ts` — 添加 SSE API 方法

**useSSE 核心接口：**
```typescript
export function useSSE() {
    const events = ref<SSEEvent[]>([])
    const done = ref(false)
    const isStreaming = ref(false)
    
    async function connect(url: string, payload: object) { ... }
    function disconnect() { ... }
    function reset() { ... }
    
    return { events, done, isStreaming, connect, disconnect, reset }
}
```

### Step 5：前端组件改造

**改动文件：**
- 修改 `src/components/layout/AppMain.vue` — handleSend 改用 useChat composable
- 修改 `src/stores/chat.ts` — 添加流式消息增量更新
- 修改 `src/components/chat/ChatMessage.vue` — 支持 isStreaming 状态
- 修改 `src/components/panels/KnowledgeGraph.vue` — 升级为 echarts 可视化

**AppMain.vue 改造：**
- 移除 `handleSend` 函数实现 → 改用 `useChat()` composable
- 新增流式渲染逻辑：AI 回复逐 token 追加
- 保持现有 UI 布局不变

**KnowledgeGraph.vue echarts 升级：**
- 引入 echarts 力导向图
- 节点按 strength 显示不同颜色/大小
- 支持交互（点击高亮、拖拽）

### Step 6：集成测试 + 验证

**测试步骤：**
1. 启动后端：`python run.py`
2. 启动前端：`npm run dev`
3. 测试 Mock 模式对话（默认配置即可用）
4. 测试 SSE 流式打字机效果
5. 测试智谱 AI 接入（需配置 API Key）
6. 验证知识图谱 echarts 渲染
7. 验证历史对话持久化
8. 验证游客 3 次限制

---

## 三、AI Prompt 工程（嵌入式）

### 3.1 System Prompt 设计

AI 面试官的 System Prompt 基于项目知识库风格：

```
你是一个专业的 Java 后端面试官。你的特点：
1. 回答结构化：先给结论，再展开原理，最后讲实战
2. 紧扣 Java 后端生态：Spring、Redis、MySQL、Kafka、JVM、分布式
3. 主动追问：回答完后，给出 3 个可能的追问方向
4. 中文表达：使用清晰的中文，技术术语保留英文
5. 代码示例：涉及代码问题时，给出 Java 代码示例

回答格式：
## 核心回答
[结构化回答]

## 代码示例（如适用）
```java
// 代码
```

## 追问方向
- [追问1]
- [追问2]
- [追问3]
```

### 3.2 信心指数算法（MVP）

基于关键词匹配 + 回答长度 + 追问质量的简单评分：
- 关键词覆盖度（0-40分）：回答中包含的相关技术关键词比例
- 回答结构度（0-30分）：是否有结论/原理/代码/追问
- 回答深度（0-30分）：回答字数 + 代码块数量

---

## 四、文件变更清单

### 新增文件（9个）

| # | 路径 | 说明 |
|---|------|------|
| 1 | `backend/services/__init__.py` | Services 包初始化 |
| 2 | `backend/services/ai_service.py` | AI 服务门面（Mock/Zhipu/Ollama） |
| 3 | `backend/services/chat_service.py` | 对话业务逻辑（限次、持久化） |
| 4 | `backend/repositories/__init__.py` | Repositories 包初始化 |
| 5 | `backend/repositories/chat_repo.py` | 数据访问层（SQL 集中） |
| 6 | `backend/blueprints/ai_routes.py` | SSE 流式 AI 端点 |
| 7 | `src/composables/useSSE.ts` | SSE 消费 composable |
| 8 | `src/composables/useChat.ts` | 聊天逻辑 composable |
| 9 | `.env.example` | 环境变量示例 |

### 修改文件（10个）

| # | 路径 | 改动说明 |
|---|------|----------|
| 1 | `backend/requirements.txt` | 添加 `httpx` 依赖 |
| 2 | `backend/config.py` | 添加 AI_PROVIDER/API_KEY 等配置 |
| 3 | `backend/app.py` | 注册 ai_bp 蓝图、加载 AI 配置 |
| 4 | `backend/blueprints/__init__.py` | 新增 ai_bp 蓝图 |
| 5 | `backend/blueprints/chat_routes.py` | 改用 Service 层 |
| 6 | `backend/blueprints/analysis_routes.py` | 改用 Service 层 |
| 7 | `src/types/chat.ts` | 添加 SSEEvent 类型 |
| 8 | `src/api/services.ts` | 添加 SSE API 方法 |
| 9 | `src/stores/chat.ts` | 添加流式增量更新 |
| 10 | `src/components/layout/AppMain.vue` | 改用 useChat composable |
| 11 | `src/components/chat/ChatMessage.vue` | 支持流式状态 |
| 12 | `src/components/panels/KnowledgeGraph.vue` | echarts 升级 |

---

## 五、风险与应对

| 风险 | 概率 | 影响 | 应对 |
|------|------|------|------|
| 智谱 AI 注册/审核慢 | 中 | 低 | 先用 Mock 模式开发，拿到 Key 后切换 |
| httpx 异步与 Flask 同步冲突 | 中 | 中 | 在 Flask 同步路由中用 `loop.run_until_complete` 桥接 |
| SSE 断连 | 低 | 中 | 前端实现自动重连（指数退避） |
| echarts 与现有样式冲突 | 低 | 低 | echarts 容器独立 CSS 作用域 |
| Ollama 模型下载慢 | 低 | 低 | 备选方案，非必须 |

---

## 六、执行顺序

```
Step 1: 后端基础设施 → config.py + requirements.txt + services/ + repositories/
Step 2: 后端 SSE 端点 → ai_routes.py + __init__.py + app.py
Step 3: 后端重构 → chat_routes.py + analysis_routes.py 改用 Service 层
Step 4: 前端 SSE composable → useSSE.ts + useChat.ts + types + api
Step 5: 前端组件改造 → AppMain.vue + chat.ts + ChatMessage.vue + KnowledgeGraph.vue
Step 6: 集成测试 → 启动前后端、Mock 模式验证
```

每个 Step 完成后验证通过再进入下一个。
