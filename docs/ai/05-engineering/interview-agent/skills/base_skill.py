#!/usr/bin/env python3
# Skill 基类定义
# 统一所有技能的规范，小白可通过继承此类快速开发新技能

class BaseSkill:
    def __init__(self):
        """初始化技能"""
        self.name = self.__class__.__name__  # 技能名称
    
    def run(self, **kwargs):
        """运行技能
        
        Args:
            **kwargs: 技能参数
            
        Returns:
            str: 技能执行结果
        """
        raise NotImplementedError("子类必须实现 run 方法")
    
    def get_description(self):
        """获取技能描述
        
        Returns:
            str: 技能描述
        """
        return f"{self.name} 技能"

# 示例：如何创建一个新技能
"""
# 1. 导入 BaseSkill
from base_skill import BaseSkill

# 2. 继承 BaseSkill 类
class MySkill(BaseSkill):
    def run(self, **kwargs):
        # 实现技能逻辑
        return "技能执行结果"
    
    def get_description(self):
        return "我的自定义技能"

# 3. 使用技能
skill = MySkill()
result = skill.run(param1="value1", param2="value2")
print(result)
"""

# 技能开发指南
"""
技能开发步骤：
1. 创建一个新的 Python 文件，如 my_skill.py
2. 导入 BaseSkill 类
3. 创建一个继承自 BaseSkill 的子类
4. 实现 run 方法，处理具体的业务逻辑
5. 可选：重写 get_description 方法，提供更详细的技能描述
6. 在 agent/interview_agent.py 中注册该技能

技能命名规范：
- 类名：驼峰命名法，如 MySkill
- 文件名：小写加下划线，如 my_skill.py

技能参数规范：
- 使用 **kwargs 接收参数，提高灵活性
- 在 run 方法中使用 get 方法获取参数，设置默认值

技能返回值规范：
- 返回字符串类型的结果
- 结果应该清晰、详细，包含解决问题的步骤和建议
"""