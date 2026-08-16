# Skill 开发

本章节将介绍如何开发自定义技能，帮助你扩展智能面试助手的能力。

## 什么是 Skill？

Skill（技能）是 Agent 可以调用的工具，用于扩展 Agent 的能力。技能可以是简单的函数，也可以是复杂的服务，它们可以执行特定的任务，如回答问题、生成计划、查询信息等。

### Skill 的核心组件

1. **技能基类**：定义技能的基本结构和接口
2. **技能实现**：具体的技能逻辑
3. **技能注册**：将技能注册到 Agent 中

## 技能基类

智能面试助手提供了一个 `BaseSkill` 基类，所有技能都继承自这个基类。

### 核心代码解析

```python
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
```

### 代码分析

1. **初始化过程**：
   - 设置技能名称为类名

2. **核心方法**：
   - `run`：执行技能的核心逻辑，子类必须实现
   - `get_description`：获取技能描述，返回默认描述

## 技能实现

智能面试助手实现了两个示例技能：`InterviewSkill`（面试题解答）和 `PlanSkill`（学习计划生成）。

### InterviewSkill 代码解析

```python
class InterviewSkill(BaseSkill):
    def __init__(self):
        """初始化面试题解答技能"""
        super().__init__()
    
    def answer_question(self, question):
        """回答面试问题"""
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
        """运行技能"""
        question = kwargs.get("question", "")
        if not question:
            return "请提供面试问题"
        
        return self.answer_question(question)
```

### PlanSkill 代码解析

```python
class PlanSkill(BaseSkill):
    def __init__(self):
        """初始化学习计划生成技能"""
        super().__init__()
    
    def generate_plan(self, topic, time="1个月"):
        """生成学习计划"""
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
        """运行技能"""
        topic = kwargs.get("topic", "")
        time = kwargs.get("time", "1个月")
        
        if not topic:
            return "请提供学习主题"
        
        return self.generate_plan(topic, time)
```

## 技能注册

在 `InterviewAgent` 类中，技能被注册到 Agent 中：

```python
# 初始化技能
self.interview_skill = InterviewSkill()
self.plan_skill = PlanSkill()

# 定义工具列表
self.tools = [
    Tool(
        name="InterviewSkill",
        func=self.interview_skill.answer_question,
        description="用于回答面试问题，提供详细的技术解释和示例代码"
    ),
    Tool(
        name="PlanSkill",
        func=self.plan_skill.generate_plan,
        description="用于生成学习计划，根据用户的需求制定合理的学习路线"
    )
]
```

## 如何创建新技能

1. **创建技能文件**：在 `skills` 目录下创建一个新的 Python 文件，如 `resume_skill.py`

2. **继承 BaseSkill**：导入 `BaseSkill` 类并继承它

3. **实现 run 方法**：实现 `run` 方法，处理具体的业务逻辑

4. **注册技能**：在 `agent/interview_agent.py` 中注册该技能

### 示例：创建简历优化技能

```python
# skills/resume_skill.py
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

## 技能开发最佳实践

1. **单一职责**：每个技能只负责一个特定的任务
2. **参数验证**：对输入参数进行验证，确保技能能够正常运行
3. **错误处理**：处理可能的错误，返回友好的错误信息
4. **文档说明**：为技能添加详细的文档，说明技能的功能和使用方法
5. **测试**：为技能编写测试，确保技能能够正常工作

## 实战练习

创建一个新的技能，比如「代码调试技能」，用于帮助用户调试代码问题。

## 下一步

了解了 Skill 开发的方法后，你可以继续学习 [项目运行](./../run/) 章节，了解如何运行智能面试助手。