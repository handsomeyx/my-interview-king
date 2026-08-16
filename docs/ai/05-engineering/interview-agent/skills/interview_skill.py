#!/usr/bin/env python3
# 面试题解答技能
# 用于回答面试问题，提供详细的技术解释和示例代码
# 代码极简，小白 5 分钟就能理解

from .base_skill import BaseSkill

class InterviewSkill(BaseSkill):
    def __init__(self):
        """初始化面试题解答技能"""
        super().__init__()
    
    def answer_question(self, question):
        """回答面试问题
        
        Args:
            question: 面试问题
            
        Returns:
            str: 详细的回答
        """
        # 这里我们模拟回答，实际项目中可以调用 MCP 客户端或其他服务
        # 小白可以在这里添加自己的回答逻辑
        
        # 构建回答
        answer = f"# {question}\n\n"
        
        # 添加核心知识点
        answer += "## 核心知识点\n"
        answer += "- 知识点 1: 这是第一个核心知识点的详细解释\n"
        answer += "- 知识点 2: 这是第二个核心知识点的详细解释\n"
        answer += "- 知识点 3: 这是第三个核心知识点的详细解释\n\n"
        
        # 添加示例代码
        answer += "## 示例代码\n"
        answer += "```python\n"
        answer += "# 这里是示例代码\n"
        answer += "def example_function():\n"
        answer += "    # 函数实现\n"
        answer += "    pass\n"
        answer += "```\n\n"
        
        # 添加面试建议
        answer += "## 面试建议\n"
        answer += "- 保持思路清晰，分点回答\n"
        answer += "- 结合实际项目经验，举例说明\n"
        answer += "- 突出自己的优势，展示解决问题的能力\n"
        answer += "- 遇到不会的问题，诚实承认并表达学习意愿\n"
        
        return answer
    
    def run(self, **kwargs):
        """运行技能
        
        Args:
            **kwargs: 技能参数，包含 question
            
        Returns:
            str: 技能执行结果
        """
        question = kwargs.get("question", "")
        if not question:
            return "请提供面试问题"
        
        return self.answer_question(question)
    
    def get_description(self):
        """获取技能描述"""
        return "面试题解答技能，提供详细的技术解释和示例代码"

# 测试代码（小白可以忽略）
if __name__ == "__main__":
    # 初始化技能
    skill = InterviewSkill()
    
    # 测试回答问题
    test_question = "什么是面向对象编程？"
    result = skill.answer_question(test_question)
    print(f"问题: {test_question}")
    print(f"回答: {result}")
    
    # 测试 run 方法
    result = skill.run(question="什么是 HTTP 协议？")
    print(f"\n通过 run 方法调用:")
    print(result)