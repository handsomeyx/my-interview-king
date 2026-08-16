#!/usr/bin/env python3
# 智能面试助手 Agent 核心实现
# 直接使用 OpenAI 官方库调用千问模型
# 代码极简，仅保留核心逻辑，添加详细注释，小白能看懂每一行

from openai import OpenAI
from skills.interview_skill import InterviewSkill
from skills.plan_skill import PlanSkill

# 千问模型的 API Base URL
QIANWEN_API_BASE = "https://dashscope.aliyuncs.com/compatible-mode/v1"

class InterviewAgent:
    def __init__(self, api_key, model_name, system_prompt):
        """初始化面试助手 Agent
        
        Args:
            api_key: OpenAI API Key
            model_name: 模型名称，如 "qwen-max"
            system_prompt: 系统提示词
        """
        # 1. 初始化 OpenAI 客户端
        # 这是 Agent 的核心，负责与千问模型通信
        self.client = OpenAI(
            api_key=api_key,
            base_url=QIANWEN_API_BASE  # 千问模型的 API Base URL
        )
        
        # 2. 初始化技能
        # 技能是 Agent 可以调用的工具，扩展 Agent 的能力
        self.interview_skill = InterviewSkill()
        self.plan_skill = PlanSkill()
        
        # 3. 设置系统提示词和模型名称
        # 系统提示词告诉 Agent 它的角色和任务
        self.system_prompt = system_prompt
        self.model_name = model_name
        
        # 4. 初始化对话历史
        self.messages = [
            {"role": "system", "content": self.system_prompt}
        ]
    
    def chat(self, user_input):
        """与用户进行对话
        
        Args:
            user_input: 用户输入的问题
            
        Returns:
            str: Agent 的回答
        """
        # 添加用户输入到对话历史
        self.messages.append({"role": "user", "content": user_input})
        
        # 调用模型生成回答
        try:
            print("面试助手: 正在思考...")
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=self.messages,
                temperature=0.7  # 温度参数，控制回答的创造性
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

# 测试代码（小白可以忽略）
if __name__ == "__main__":
    from config import OPENAI_API_KEY, MODEL_NAME, SYSTEM_PROMPT
    
    if OPENAI_API_KEY:
        agent = InterviewAgent(
            api_key=OPENAI_API_KEY,
            model_name=MODEL_NAME,
            system_prompt=SYSTEM_PROMPT
        )
        
        # 测试对话
        test_question = "解释一下什么是面向对象编程？"
        response = agent.chat(test_question)
        print(f"问题: {test_question}")
        print(f"回答: {response}")
    else:
        print("请在 config.py 中填写你的 OpenAI API Key")