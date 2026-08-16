# 扩展教程

本章节将介绍如何扩展智能面试助手的功能，包括添加新技能、对接本地大模型、部署到服务器等。

## 1. 添加新技能

智能面试助手的一个重要特性是可以轻松添加新技能，扩展其能力。

### 步骤 1：创建技能文件

在 `skills` 目录下创建一个新的 Python 文件，如 `resume_skill.py`。

### 步骤 2：实现技能类

继承 `BaseSkill` 类并实现 `run` 方法：

```python
from .base_skill import BaseSkill

class ResumeSkill(BaseSkill):
    def run(self, **kwargs):
        position = kwargs.get("position", "")
        if not position:
            return "请提供目标职位"
        
        return f"# {position} 简历优化建议\n\n## 简历结构\n- 个人信息\n- 教育背景\n- 工作经历\n- 项目经验\n- 技能清单\n\n## 优化建议\n- 突出与目标职位相关的经验\n- 使用量化的成果展示\n- 避免使用模糊的描述\n- 保持简历简洁明了"
    
    def get_description(self):
        return "简历优化技能，根据目标职位提供简历优化建议"
```

### 步骤 3：注册技能

在 `agent/interview_agent.py` 中注册该技能：

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

### 示例：创建代码调试技能

```python
# skills/debug_skill.py
from .base_skill import BaseSkill

class DebugSkill(BaseSkill):
    def run(self, **kwargs):
        code = kwargs.get("code", "")
        error = kwargs.get("error", "")
        
        if not code:
            return "请提供代码"
        
        if not error:
            return "请提供错误信息"
        
        return f"# 代码调试建议\n\n## 代码\n```python\n{code}\n```\n\n## 错误信息\n{error}\n\n## 可能的原因\n- 语法错误\n- 逻辑错误\n- 变量未定义\n- 类型不匹配\n\n## 修复建议\n1. 检查语法是否正确\n2. 检查变量是否正确定义\n3. 检查类型是否匹配\n4. 增加错误处理\n\n## 优化建议\n- 代码风格优化\n- 性能优化\n- 可读性优化"
    
    def get_description(self):
        return "代码调试技能，帮助用户调试代码问题"
```

## 2. 对接本地大模型

如果你想使用本地大模型，而不是千问模型，可以修改 `agent/interview_agent.py` 文件：

### 步骤 1：安装本地大模型接口

安装相应的本地大模型接口库，如 `llama-cpp-python`：

```bash
pip install llama-cpp-python
```

### 步骤 2：修改代码

```python
# 使用本地大模型
from llama_cpp import Llama

class InterviewAgent:
    def __init__(self, model_path, system_prompt):
        """初始化面试助手 Agent"""
        # 初始化本地大模型
        self.llm = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_threads=4
        )
        
        # 设置系统提示词
        self.system_prompt = system_prompt
        
        # 初始化对话历史
        self.messages = [
            {"role": "system", "content": self.system_prompt}
        ]
    
    def chat(self, user_input):
        """与用户进行对话"""
        # 添加用户输入到对话历史
        self.messages.append({"role": "user", "content": user_input})
        
        # 构建提示词
        prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.messages])
        prompt += "\nassistant: "
        
        # 调用模型生成回答
        try:
            print("面试助手: 正在思考...")
            response = self.llm(prompt, max_tokens=1024, stop=["\nuser:"])
            
            # 获取模型的回答
            answer = response["choices"][0]["text"].strip()
            
            # 添加模型回答到对话历史
            self.messages.append({"role": "assistant", "content": answer})
            
            # 返回模型的回答
            return answer
        except Exception as e:
            print(f"错误: {str(e)}")
            return "抱歉，我遇到了一些问题，请稍后再试。"
```

### 步骤 3：运行项目

```bash
python main.py --model_path /path/to/your/model.gguf
```

## 3. 部署到服务器

### 步骤 1：准备服务器

- 确保服务器上安装了 Python 3.7+ 和所需依赖
- 配置好网络连接和防火墙

### 步骤 2：上传代码

将项目代码上传到服务器：

```bash
scp -r interview-agent user@server:/path/to/project/
```

### 步骤 3：安装依赖

```bash
cd /path/to/project/interview-agent
pip install -r requirements.txt
```

### 步骤 4：配置 API Key

修改 `config.py` 文件，填写你的 API Key。

### 步骤 5：后台运行

使用 `nohup` 命令后台运行：

```bash
nohup python main.py > interview-agent.log 2>&1 &
```

### 步骤 6：监控运行状态

```bash
tail -f interview-agent.log
```

## 4. 构建 Web 界面

你可以为智能面试助手构建一个 Web 界面，使其更易于使用。

### 步骤 1：安装 Flask

```bash
pip install flask
```

### 步骤 2：创建 Web 应用

```python
# app.py
from flask import Flask, render_template, request, jsonify
from agent.interview_agent import InterviewAgent
from config import OPENAI_API_KEY, MODEL_NAME, SYSTEM_PROMPT

app = Flask(__name__)

# 初始化 Agent
agent = InterviewAgent(
    api_key=OPENAI_API_KEY,
    model_name=MODEL_NAME,
    system_prompt=SYSTEM_PROMPT
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = agent.chat(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### 步骤 3：创建 HTML 模板

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>智能面试助手</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .chat-container {
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            height: 400px;
            overflow-y: scroll;
        }
        .message {
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 5px;
        }
        .user-message {
            background-color: #e3f2fd;
            align-self: flex-end;
        }
        .agent-message {
            background-color: #f5f5f5;
            align-self: flex-start;
        }
        .input-container {
            display: flex;
        }
        input {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px 0 0 5px;
        }
        button {
            padding: 10px 20px;
            background-color: #2196f3;
            color: white;
            border: none;
            border-radius: 0 5px 5px 0;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>智能面试助手</h1>
    <div class="chat-container" id="chat-container">
        <div class="message agent-message">你好！我是智能面试助手，有什么我可以帮助你的吗？</div>
    </div>
    <div class="input-container">
        <input type="text" id="message-input" placeholder="输入你的问题...">
        <button onclick="sendMessage()">发送</button>
    </div>

    <script>
        function sendMessage() {
            const input = document.getElementById('message-input');
            const message = input.value;
            if (!message) return;

            // 添加用户消息
            const chatContainer = document.getElementById('chat-container');
            chatContainer.innerHTML += `<div class="message user-message">${message}</div>`;
            input.value = '';

            // 发送请求
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                // 添加助手消息
                chatContainer.innerHTML += `<div class="message agent-message">${data.response}</div>`;
                // 滚动到底部
                chatContainer.scrollTop = chatContainer.scrollHeight;
            });
        }

        // 回车发送
        document.getElementById('message-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
```

### 步骤 4：运行 Web 应用

```bash
python app.py
```

现在你可以通过浏览器访问 `http://localhost:5000` 使用智能面试助手了。

## 5. 集成到其他系统

### 集成到 Discord

```python
# discord_bot.py
import discord
from agent.interview_agent import InterviewAgent
from config import OPENAI_API_KEY, MODEL_NAME, SYSTEM_PROMPT

# 初始化 Agent
agent = InterviewAgent(
    api_key=OPENAI_API_KEY,
    model_name=MODEL_NAME,
    system_prompt=SYSTEM_PROMPT
)

# 创建 Discord 机器人
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!interview'):
        # 提取问题
        question = message.content[10:].strip()
        if not question:
            await message.channel.send('请提供面试问题')
            return

        # 获取回答
        response = agent.chat(question)
        await message.channel.send(response)

# 运行机器人
client.run('YOUR_DISCORD_TOKEN')
```

### 集成到 Slack

```python
# slack_bot.py
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from flask import Flask, request, jsonify
from agent.interview_agent import InterviewAgent
from config import OPENAI_API_KEY, MODEL_NAME, SYSTEM_PROMPT

app = Flask(__name__)

# 初始化 Agent
agent = InterviewAgent(
    api_key=OPENAI_API_KEY,
    model_name=MODEL_NAME,
    system_prompt=SYSTEM_PROMPT
)

# 初始化 Slack 客户端
client = WebClient(token="YOUR_SLACK_TOKEN")

@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json
    
    # 验证请求
    if data.get('type') == 'url_verification':
        return jsonify({'challenge': data.get('challenge')})
    
    # 处理消息事件
    if data.get('event') and data['event'].get('type') == 'message' and not data['event'].get('bot_id'):
        channel_id = data['event']['channel']
        user_id = data['event']['user']
        text = data['event']['text']
        
        # 提取问题
        if text.startswith('!interview'):
            question = text[10:].strip()
            if question:
                # 获取回答
                response = agent.chat(question)
                
                # 发送回答
                try:
                    client.chat_postMessage(
                        channel=channel_id,
                        text=response
                    )
                except SlackApiError as e:
                    print(f"Error sending message: {e}")
    
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(port=3000)
```

## 6. 最佳实践

### 代码组织

- **模块化**：将不同功能的代码放在不同的模块中
- **文档**：为代码添加详细的文档和注释
- **测试**：为关键功能编写测试

### 性能优化

- **缓存**：缓存频繁使用的结果
- **批处理**：批量处理请求
- **异步**：使用异步编程提高并发性能

### 安全性

- **API Key 保护**：不要在代码中硬编码 API Key
- **输入验证**：验证用户输入，防止注入攻击
- **错误处理**：妥善处理错误，不要暴露敏感信息

### 可维护性

- **版本控制**：使用 Git 进行版本控制
- **代码风格**：遵循 PEP8 代码风格
- **日志**：添加适当的日志记录

## 7. 常见问题

### 技能开发问题
- **技能不被调用**：检查技能的描述是否清晰，确保 Agent 能够理解何时使用该技能
- **技能执行失败**：检查技能的实现是否正确，确保它能够处理各种输入情况

### 部署问题
- **服务器配置**：确保服务器配置足够运行模型
- **网络连接**：确保服务器能够访问模型 API
- **权限问题**：确保应用有足够的权限访问文件和资源

### 集成问题
- **API 兼容性**：确保集成的系统与智能面试助手的 API 兼容
- **数据格式**：确保数据格式符合集成系统的要求
- **错误处理**：确保集成系统能够妥善处理智能面试助手的错误

## 8. 总结

智能面试助手是一个功能强大、易于扩展的 AI 面试辅助工具。通过本教程，你已经了解了如何：

- **添加新技能**：扩展智能面试助手的能力
- **对接本地大模型**：使用本地模型提高隐私性和响应速度
- **部署到服务器**：让更多人使用智能面试助手
- **构建 Web 界面**：提供更友好的用户体验
- **集成到其他系统**：与 Discord、Slack 等系统集成

现在，你可以根据自己的需求和创意，进一步扩展智能面试助手的功能，为用户提供更好的面试准备体验。