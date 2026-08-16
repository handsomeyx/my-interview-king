# Agent 基础

本章节将介绍 Agent 的核心概念和实现，帮助你理解智能面试助手的工作原理。

## 什么是 Agent？

Agent 是一个能够自主决策、执行任务的智能实体。在 AI 领域，Agent 通常指能够理解用户的问题，决定使用哪些工具来解决问题，然后执行相应的操作并返回结果的系统。

### Agent 的核心组件

1. **语言模型**：负责理解和生成回答，是 Agent 的大脑
2. **记忆系统**：用于记住对话历史，使 Agent 能够进行上下文连贯的对话
3. **工具调用**：Agent 可以调用外部工具来扩展自己的能力
4. **决策系统**：决定何时使用工具，使用哪些工具，以及如何处理工具的响应

## 智能面试助手的 Agent 实现

智能面试助手使用 OpenAI 官方库直接调用千问模型，实现了一个简单但功能完整的 Agent。

### 核心代码解析

```python
class InterviewAgent:
    def __init__(self, api_key, model_name, system_prompt):
        """初始化面试助手 Agent"""
        # 1. 初始化 OpenAI 客户端
        self.client = OpenAI(
            api_key=api_key,
            base_url=QIANWEN_API_BASE
        )
        
        # 2. 初始化技能
        self.interview_skill = InterviewSkill()
        self.plan_skill = PlanSkill()
        
        # 3. 设置系统提示词和模型名称
        self.system_prompt = system_prompt
        self.model_name = model_name
        
        # 4. 初始化对话历史
        self.messages = [
            {"role": "system", "content": self.system_prompt}
        ]
    
    def chat(self, user_input):
        """与用户进行对话"""
        # 添加用户输入到对话历史
        self.messages.append({"role": "user", "content": user_input})
        
        # 调用模型生成回答
        try:
            print("面试助手: 正在思考...")
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=self.messages,
                temperature=0.7
            )
            
            # 获取模型的回答
            answer = response.choices[0].message.content
            
            # 添加模型回答到对话历史
            self.messages.append({"role": "assistant", "content": answer})
            
            # 返回模型的回答
            return answer
        except Exception as e:
            print(f"错误: {str(e)}")
            return "抱歉，我遇到了一些问题，请稍后再试。"
```

### 代码分析

1. **初始化过程**：
   - 创建 OpenAI 客户端，连接到千问模型
   - 初始化技能，扩展 Agent 的能力
   - 设置系统提示词，告诉 Agent 它的角色和任务
   - 初始化对话历史，用于上下文管理

2. **对话过程**：
   - 接收用户输入
   - 将用户输入添加到对话历史
   - 调用千问模型生成回答
   - 将模型回答添加到对话历史
   - 返回模型的回答

## Agent 的工作流程

1. **接收输入**：获取用户的问题或指令
2. **理解上下文**：根据对话历史理解用户的意图
3. **生成响应**：调用语言模型生成回答
4. **执行工具**：如果需要，调用外部工具获取信息
5. **返回结果**：将最终答案返回给用户

## 为什么使用 Agent？

1. **能力扩展**：Agent 可以调用外部工具，扩展自己的能力
2. **上下文理解**：Agent 可以记住对话历史，提供连贯的对话体验
3. **自主决策**：Agent 可以根据用户的需求自主决定如何响应
4. **灵活性**：Agent 可以适应不同的场景和任务

## 实战练习

尝试修改 `agent/interview_agent.py` 文件，添加一个新的方法来处理特定类型的问题，比如技术面试题、简历建议等。

## 下一步

了解了 Agent 的基础概念和实现后，你可以继续学习 [MCP 协议](./../mcp-protocol/) 章节，了解标准化通信协议的实现。