#!/usr/bin/env python3
# 智能面试助手 Agent 项目入口
# 小白一键启动，实现交互对话

from config import OPENAI_API_KEY, MODEL_NAME, SYSTEM_PROMPT
from agent.interview_agent import InterviewAgent

# 检查 API Key 是否填写
if not OPENAI_API_KEY:
    print("错误: 请在 config.py 中填写你的 OpenAI API Key")
    print("获取 API Key 的方法: https://platform.openai.com/account/api-keys")
    exit(1)

# 初始化 Agent
def init_agent():
    """初始化面试助手 Agent"""
    print("正在初始化智能面试助手...")
    try:
        agent = InterviewAgent(
            api_key=OPENAI_API_KEY,
            model_name=MODEL_NAME,
            system_prompt=SYSTEM_PROMPT
        )
        print("智能面试助手初始化完成！")
        return agent
    except Exception as e:
        print(f"初始化失败: {str(e)}")
        exit(1)

# 交互对话
def interactive_chat(agent):
    """与面试助手进行交互对话"""
    print("\n=== 智能面试助手 ===")
    print("你可以问我任何面试相关的问题，比如:")
    print("- 解释一下什么是 TCP/IP 协议？")
    print("- 如何实现一个线程安全的单例模式？")
    print("- 什么是分布式系统的 CAP 理论？")
    print("- 退出\n")
    
    # 测试问题，自动运行
    test_questions = [
        "什么是 TCP/IP 协议？",
        "如何实现一个线程安全的单例模式？",
        "什么是分布式系统的 CAP 理论？"
    ]
    
    for question in test_questions:
        print(f"你: {question}")
        try:
            print("面试助手: 正在思考...")
            response = agent.chat(question)
            print(f"面试助手: {response}")
            print()
        except Exception as e:
            print(f"错误: {str(e)}")
            print("请检查你的 API Key 是否正确，或者网络连接是否正常")
            print()
    
    print("测试完成！你可以修改 main.py 文件，添加更多测试问题，或者启用交互式对话。")

if __name__ == "__main__":
    # 初始化 Agent
    agent = init_agent()
    # 开始交互对话
    interactive_chat(agent)