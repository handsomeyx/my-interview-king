# 智能面试助手 Agent

一个面向小白的 LangChain Agent 实战项目，仅需填写 API Key 即可使用，1 天内就能跑通。

## 项目亮点

- **小白零门槛**：仅需填写 API Key，一键启动，无复杂配置
- **知识点全覆盖**：完整覆盖 Agent、MCP、Skill 三大核心知识点
- **可扩展性强**：小白可轻松写新技能，扩展 Agent 能力
- **贴合面试场景**：与「我是面试大王」知识库完美契合，用户可直接用它刷面试题

## 项目结构

```
interview-agent/
├── agent/              # Agent 核心实现
│   └── interview_agent.py  # 面试助手 Agent
├── mcp/                # MCP 协议实现
│   └── mcp_client.py    # MCP 客户端
├── skills/             # Skill 技能开发
│   ├── base_skill.py     # 技能基类
│   ├── interview_skill.py  # 面试题解答技能
│   └── plan_skill.py     # 学习计划生成技能
├── config.py           # 配置文件（填写 API Key）
├── main.py             # 项目入口
├── requirements.txt    # 依赖文件
└── README.md           # 项目说明文档
```

## 环境搭建（10 分钟搞定）

### 1. 安装 Python

确保你的电脑上安装了 Python 3.7 或更高版本。

- **Windows**：从 [Python 官网](https://www.python.org/downloads/) 下载并安装
- **Mac**：使用 Homebrew 安装 `brew install python`
- **Linux**：使用包管理器安装，如 `apt install python3`

### 2. 安装依赖

在项目目录下运行：

```bash
pip install -r requirements.txt
```

### 3. 填写 API Key

打开 `config.py` 文件，填写你的 OpenAI API Key：

```python
# OpenAI API Key
# 请在这里填写你的 OpenAI API Key
# 如何获取 API Key: https://platform.openai.com/account/api-keys
OPENAI_API_KEY = "your_api_key_here"  # 填写你的 API Key
```

## 运行项目（一键启动）

在项目目录下运行：

```bash
python main.py
```

然后你就可以与智能面试助手进行交互了！

### 示例对话

```
=== 智能面试助手 ===
你可以问我任何面试相关的问题，比如:
- 解释一下什么是 TCP/IP 协议？
- 如何实现一个线程安全的单例模式？
- 什么是分布式系统的 CAP 理论？
- 退出

你: 解释一下什么是面向对象编程？
面试助手: 正在思考...
...
面试助手: # 面向对象编程

## 核心知识点
- 知识点 1: 面向对象编程（OOP）是一种编程范式，它将数据和操作数据的方法封装在一起，形成对象。
- 知识点 2: 面向对象编程的核心概念包括封装、继承、多态。
- 知识点 3: 面向对象编程可以提高代码的可重用性、可维护性和可扩展性。

## 示例代码
```python
# 面向对象编程示例
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def say_hello(self):
        print(f"Hello, my name is {self.name}")

# 创建对象
person = Person("Alice", 25)
person.say_hello()  # 输出: Hello, my name is Alice
```

## 面试建议
- 保持思路清晰，分点回答
- 结合实际项目经验，举例说明
- 突出自己的优势，展示解决问题的能力
- 遇到不会的问题，诚实承认并表达学习意愿
```
```

## 扩展教程

### 如何添加新技能

1. 在 `skills` 目录下创建一个新的 Python 文件，如 `resume_skill.py`
2. 导入 `BaseSkill` 类并继承它
3. 实现 `run` 方法，处理具体的业务逻辑
4. 在 `agent/interview_agent.py` 中注册该技能

### 示例：创建简历优化技能

```python
# skills/resume_skill.py
from base_skill import BaseSkill

class ResumeSkill(BaseSkill):
    def run(self, **kwargs):
        position = kwargs.get("position", "")
        if not position:
            return "请提供目标职位"
        
        return f"# {position} 简历优化建议\n\n## 简历结构\n- 个人信息\n- 教育背景\n- 工作经历\n- 项目经验\n- 技能清单\n\n## 优化建议\n- 突出与目标职位相关的经验\n- 使用量化的成果展示\n- 避免使用模糊的描述\n- 保持简历简洁明了"
    
    def get_description(self):
        return "简历优化技能，根据目标职位提供简历优化建议"
```

然后在 `agent/interview_agent.py` 中注册该技能：

```python
from skills.resume_skill import ResumeSkill

# 初始化技能
self.resume_skill = ResumeSkill()

# 添加到工具列表
self.tools.append(
    Tool(
        name="ResumeSkill",
        func=self.resume_skill.run,
        description="用于简历优化，根据目标职位提供简历优化建议"
    )
)
```

### 如何对接本地大模型

如果你想使用本地大模型，而不是 OpenAI API，可以修改 `agent/interview_agent.py` 文件，将 `ChatOpenAI` 替换为本地大模型的接口。

### 如何部署到服务器

1. 确保服务器上安装了 Python 3.7+ 和所需依赖
2. 将项目文件上传到服务器
3. 填写 `config.py` 中的 API Key
4. 使用 `nohup` 命令后台运行：

```bash
nohup python main.py > interview-agent.log 2>&1 &
```

## 核心知识点讲解

### 1. Agent 是什么？

Agent 是一个能够自主决策、执行任务的智能实体。在 LangChain 中，Agent 可以理解用户的问题，决定使用哪些工具来解决问题，然后执行相应的操作并返回结果。

### 2. MCP 是什么？

MCP（Model Context Protocol）是一种标准化的通信协议，用于 Agent 和工具之间的通信。它定义了请求和响应的格式，使得 Agent 可以与不同的工具进行统一的交互。

### 3. Skill 怎么写？

Skill 是 Agent 可以调用的工具，用于扩展 Agent 的能力。要写一个 Skill，你需要：
1. 继承 `BaseSkill` 类
2. 实现 `run` 方法，处理具体的业务逻辑
3. 可选：重写 `get_description` 方法，提供更详细的技能描述
4. 在 Agent 中注册该技能

## 常见问题排查

### API Key 错误
- 确保你填写了正确的 OpenAI API Key
- 确保你的 API Key 有足够的余额
- 确保你的网络连接正常

### 依赖安装失败
- 确保你使用了正确的 pip 命令
- 确保你的 Python 版本符合要求
- 尝试使用 `pip install --upgrade pip` 升级 pip

### 运行时错误
- 检查你的 API Key 是否正确
- 检查你的网络连接是否正常
- 查看错误信息，根据错误提示进行排查

## 项目源码

你可以直接下载本项目的源码，按照上述步骤运行即可。

## 结语

智能面试助手 Agent 是一个面向小白的 LangChain Agent 实战项目，它涵盖了 Agent 基础、MCP 协议、Skill 技能开发三大核心知识点。通过这个项目，你可以了解 Agent 的工作原理，学习如何开发自定义技能，以及如何使用 MCP 协议进行标准化通信。

希望这个项目能帮助你更好地理解 Agent 技术，为你的面试准备提供帮助！