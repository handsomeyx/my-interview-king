#!/usr/bin/env python3
# 测试千问模型 API 调用

from openai import OpenAI

# 千问模型的 API Base URL
QIANWEN_API_BASE = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# 你的 API Key
API_KEY = "sk-8addd5a64339484e8326882d0636abe6"

# 模型名称
MODEL_NAME = "qwen-max"

# 系统提示词
SYSTEM_PROMPT = "你是一个专业的面试助手，帮助用户准备技术面试。"

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key=API_KEY,
    base_url=QIANWEN_API_BASE
)

# 测试对话
try:
    print("正在测试千问模型 API 调用...")
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "什么是 TCP/IP 协议？"}
        ],
        temperature=0.7
    )
    
    # 输出回答
    print("测试成功！")
    print(f"回答: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"测试失败: {str(e)}")
    print("请检查 API Key 是否正确，或者网络连接是否正常。")