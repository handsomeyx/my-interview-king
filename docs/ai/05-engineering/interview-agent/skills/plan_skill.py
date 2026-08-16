#!/usr/bin/env python3
# 学习计划生成技能
# 用于生成学习计划，根据用户的需求制定合理的学习路线
# 代码极简，小白 5 分钟就能理解

from .base_skill import BaseSkill

class PlanSkill(BaseSkill):
    def __init__(self):
        """初始化学习计划生成技能"""
        super().__init__()
    
    def generate_plan(self, topic, time="1个月"):
        """生成学习计划
        
        Args:
            topic: 学习主题
            time: 学习时间，默认 1个月
            
        Returns:
            str: 详细的学习计划
        """
        # 这里我们模拟生成学习计划，实际项目中可以调用 MCP 客户端或其他服务
        # 小白可以在这里添加自己的计划生成逻辑
        
        # 构建学习计划
        plan = f"# {topic} 学习计划 ({time})\n\n"
        
        # 根据时间长度生成不同的学习计划
        if "周" in time:
            # 按周生成计划
            weeks = int(time.replace("周", ""))
            for i in range(1, weeks + 1):
                plan += f"## 第{i}周\n"
                plan += f"- 第{i}周第一天: 基础概念学习\n"
                plan += f"- 第{i}周第二天: 环境搭建\n"
                plan += f"- 第{i}周第三天: 核心知识点学习\n"
                plan += f"- 第{i}周第四天: 实战练习\n"
                plan += f"- 第{i}周第五天: 问题解决\n"
                plan += f"- 第{i}周第六天: 总结与复习\n"
                plan += f"- 第{i}周第七天: 休息\n\n"
        else:
            # 按月生成计划
            plan += "## 第一周\n"
            plan += "- 基础概念学习\n"
            plan += "- 环境搭建\n"
            plan += "- 简单示例练习\n\n"
            
            plan += "## 第二周\n"
            plan += "- 核心知识点深入\n"
            plan += "- 实战项目练习\n"
            plan += "- 问题解决\n\n"
            
            plan += "## 第三周\n"
            plan += "- 高级特性学习\n"
            plan += "- 性能优化\n"
            plan += "- 项目实战\n\n"
            
            plan += "## 第四周\n"
            plan += "- 复习与总结\n"
            plan += "- 模拟面试\n"
            plan += "- 简历准备\n"
        
        # 添加学习建议
        plan += "## 学习建议\n"
        plan += "- 每天保持固定的学习时间\n"
        plan += "- 理论与实践相结合\n"
        plan += "- 遇到问题及时解决，不要积累\n"
        plan += "- 定期回顾总结，巩固知识点\n"
        plan += "- 参与社区讨论，扩展人脉\n"
        
        return plan
    
    def run(self, **kwargs):
        """运行技能
        
        Args:
            **kwargs: 技能参数，包含 topic 和 time
            
        Returns:
            str: 技能执行结果
        """
        topic = kwargs.get("topic", "")
        time = kwargs.get("time", "1个月")
        
        if not topic:
            return "请提供学习主题"
        
        return self.generate_plan(topic, time)
    
    def get_description(self):
        """获取技能描述"""
        return "学习计划生成技能，根据用户的需求制定合理的学习路线"

# 测试代码（小白可以忽略）
if __name__ == "__main__":
    # 初始化技能
    skill = PlanSkill()
    
    # 测试生成学习计划
    test_topic = "Python 爬虫"
    test_time = "2周"
    result = skill.generate_plan(test_topic, test_time)
    print(f"主题: {test_topic}")
    print(f"时间: {test_time}")
    print(f"学习计划: {result}")
    
    # 测试 run 方法
    result = skill.run(topic="Java 基础", time="1个月")
    print(f"\n通过 run 方法调用:")
    print(result)