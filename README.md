# 我是面试大王

> Java 后端面试全栈通关指南 —— 构建深度后端知识图谱,对齐大厂面试官架构思维。

[![VitePress](https://img.shields.io/badge/VitePress-1.6-646cff?logo=vitepress)](https://vitepress.dev)
[![Vue](https://img.shields.io/badge/Vue-3.5-42b883?logo=vue.js)](https://vuejs.org)

🚀 **在线站点**:即将上线 ｜ 📚 [知识库源码](docs/) ｜ 📋 [路线图](ROADMAP.md) ｜ 🤝 [贡献指南](CONTRIBUTING.md)

---

## 这是什么

一个面向 **Java 后端求职者**的体系化面试知识库,配套一个智能面试助手应用。

解决的痛点:

- ❌ **知识碎片化** —— 八股散落在收藏夹,形不成知识图谱
- ❌ **面试没体系** —— 基础 / 中间件 / 分布式 / 算法 / 场景题各自为战
- ❌ **场景题难练** —— 缺乏系统化的后端全链路场景训练

走 [labuladong](https://labuladong.online/) 那种 **「内容引流 + 工具服务」** 路线:免费知识做护城河,配套交互式工具做增值。长期规划见 [ROADMAP.md](ROADMAP.md)。

## 内容速览

| 板块 | 覆盖 | 目录 |
|------|------|------|
| ☕ **Java 后端** | 基础 / Spring / Redis / MySQL / Kafka / 操作系统 | [`docs/java/`](docs/java/) |
| 🌐 **分布式 & 场景** | 分布式理论 + 接入路由 / 业务逻辑 / 持久化异步层场景题 | [`docs/distributed/`](docs/distributed/) |
| 🧮 **算法 & 数据结构** | 算法框架 / 方法论 / 数据结构 / 算法模式 / 系统算法 / 面试 Top 100 | [`docs/algorithm/`](docs/algorithm/) |
| 🤖 **AI 实战** | LLM / Agent / MCP / Skill / 工程落地 / RAG | [`docs/ai/`](docs/ai/) |
| 🛠️ **项目实战** | 智能面试助手(LangChain Agent 完整项目) | [`docs/projects/`](docs/projects/) |

## 快速开始

本项目包含两部分:**知识库文档站**(VitePress)和 **智能面试助手应用**(Vue3 + Flask)。

### 1. 运行知识库文档站

```powershell
npm install
npm run docs:dev
```

浏览器打开 `http://localhost:5173` 浏览全部面试内容。

### 2. 运行智能面试助手应用(可选)

需要同时启动前端(Vite)和后端(Flask)两个终端:

```powershell
# 终端 A —— 后端(端口 5000)
cd frontend-interview-agent/backend
pip install -r requirements.txt
python server.py

# 终端 B —— 前端(端口 3000)
cd frontend-interview-agent
npm install
npm run dev
```

浏览器打开 `http://localhost:3000`。前端通过 Vite 代理把 `/api` 请求转发到后端 5000 端口。

## 目录结构

```
my-interview-king/
├── docs/                      # VitePress 知识库(主要内容)
│   ├── java/                  # Java 后端
│   ├── distributed/           # 分布式 & 场景题
│   ├── algorithm/             # 算法与数据结构
│   ├── ai/                    # AI Agent 知识库
│   ├── projects/              # 项目实战
│   └── .vitepress/            # 站点配置与主题
├── frontend-interview-agent/  # 智能面试助手(Vue3 前端 + Flask 后端)
├── ROADMAP.md                 # 架构与三阶段发展规划
├── CONTRIBUTING.md            # 内容贡献指南(目录归属 + 命名规范)
└── README.md
```

新增内容前请先读 [CONTRIBUTING.md](CONTRIBUTING.md),了解目录归属规则和命名规范。

## 路线图

三阶段演进(详见 [ROADMAP.md](ROADMAP.md)):

1. **静态引流期**(当前)—— VitePress 免费内容,积累 SEO 流量
2. **账号化工具期** —— 上线面试助手应用,沉淀用户、提供互动工具
3. **会员付费期** —— 内容继续全免费,工具 / 服务变现

## 参与贡献

- 发现内容错误或想补充:提 [Issue](https://github.com/handsomeyx/my-interview-king/issues) 或直接 PR
- 新增内容前请先读 [CONTRIBUTING.md](CONTRIBUTING.md)
- 欢迎在 GitHub 点 ⭐ Star 支持本项目

## 关于作者

Java 后端开发者,持续沉淀面试知识与工程实践。

---

> 本项目仅供学习交流,内容持续更新中。如有帮助,欢迎分享给同样在准备面试的朋友。
