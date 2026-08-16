#!/usr/bin/env python3
# MCP 协议客户端实现
# 用最简单的方式实现标准化通信，添加详细注释，小白能理解 MCP 原理
# 模拟工具响应，小白可直接扩展对接真实服务

import json
import requests

class MCPClient:
    def __init__(self, base_url="http://localhost:8000"):
        """初始化 MCP 客户端
        
        Args:
            base_url: MCP 服务器的基础 URL
        """
        self.base_url = base_url
    
    def call_tool(self, tool_name, params):
        """调用 MCP 工具
        
        Args:
            tool_name: 工具名称
            params: 工具参数（字典格式）
            
        Returns:
            dict: 工具的响应结果
        """
        # 1. 构建 MCP 请求格式
        # MCP (Model Context Protocol) 是一种标准化的通信协议
        # 用于 Agent 和工具之间的通信
        request_data = {
            "toolcall": {
                "thought": f"调用 {tool_name} 工具",
                "name": tool_name,
                "params": params
            }
        }
        
        print(f"发送 MCP 请求: {json.dumps(request_data, indent=2, ensure_ascii=False)}")
        
        # 2. 发送请求到 MCP 服务器
        # 这里我们模拟服务器响应，实际项目中可以替换为真实的 HTTP 请求
        try:
            # 尝试发送真实的 HTTP 请求
            response = requests.post(
                f"{self.base_url}/mcp",
                json=request_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                # 如果请求失败，返回模拟响应
                return self._mock_response(tool_name, params)
                
        except Exception as e:
            # 如果连接失败，返回模拟响应
            print(f"连接 MCP 服务器失败: {str(e)}")
            print("返回模拟响应...")
            return self._mock_response(tool_name, params)
    
    def _mock_response(self, tool_name, params):
        """模拟 MCP 工具响应
        
        Args:
            tool_name: 工具名称
            params: 工具参数
            
        Returns:
            dict: 模拟的响应结果
        """
        # 根据不同的工具名称返回不同的模拟响应
        if tool_name == "InterviewSkill":
            # 模拟面试题回答工具的响应
            question = params.get("question", "")
            return {
                "toolcall_result": {
                    "thought": f"回答面试问题: {question}",
                    "content": f"这是关于 '{question}' 的详细回答。\n\n**核心知识点:**\n- 知识点 1\n- 知识点 2\n- 知识点 3\n\n**示例代码:**\n```python\n# 示例代码\ndef example():\n    pass\n```\n\n**面试建议:**\n- 保持思路清晰\n- 结合实际项目经验\n- 突出自己的优势"
                }
            }
        elif tool_name == "PlanSkill":
            # 模拟学习计划生成工具的响应
            topic = params.get("topic", "")
            time = params.get("time", "1个月")
            return {
                "toolcall_result": {
                    "thought": f"为 {topic} 生成 {time} 的学习计划",
                    "content": f"# {topic} 学习计划 ({time})\n\n## 第一周\n- 基础概念学习\n- 环境搭建\n- 简单示例练习\n\n## 第二周\n- 核心知识点深入\n- 实战项目练习\n- 问题解决\n\n## 第三周\n- 高级特性学习\n- 性能优化\n- 项目实战\n\n## 第四周\n- 复习与总结\n- 模拟面试\n- 简历准备"
                }
            }
        else:
            # 未知工具的默认响应
            return {
                "toolcall_result": {
                    "thought": f"调用未知工具: {tool_name}",
                    "content": f"工具 {tool_name} 暂未实现"
                }
            }

# 测试代码（小白可以忽略）
if __name__ == "__main__":
    # 初始化 MCP 客户端
    mcp_client = MCPClient()
    
    # 测试调用 InterviewSkill 工具
    print("测试调用 InterviewSkill 工具:")
    response = mcp_client.call_tool(
        "InterviewSkill",
        {"question": "什么是 Python 的装饰器？"}
    )
    print(f"响应: {json.dumps(response, indent=2, ensure_ascii=False)}")
    print()
    
    # 测试调用 PlanSkill 工具
    print("测试调用 PlanSkill 工具:")
    response = mcp_client.call_tool(
        "PlanSkill",
        {"topic": "Python 爬虫", "time": "2周"}
    )
    print(f"响应: {json.dumps(response, indent=2, ensure_ascii=False)}")