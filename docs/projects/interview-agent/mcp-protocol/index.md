# MCP 协议

本章节将介绍 MCP 协议的概念和实现，帮助你理解 Agent 如何与工具进行标准化通信。

## 什么是 MCP 协议？

MCP（Model Context Protocol）是一种标准化的通信协议，用于 Agent 和工具之间的通信。它定义了请求和响应的格式，使得 Agent 可以与不同的工具进行统一的交互。

### MCP 协议的核心概念

1. **工具调用**：Agent 调用工具的请求
2. **工具响应**：工具执行后的返回结果
3. **上下文管理**：维护对话历史和状态

## MCP 协议的实现

智能面试助手实现了一个简单的 MCP 客户端，用于与工具进行通信。

### 核心代码解析

```python
class MCPClient:
    def __init__(self, base_url="http://localhost:8000"):
        """初始化 MCP 客户端"""
        self.base_url = base_url
    
    def call_tool(self, tool_name, params):
        """调用 MCP 工具"""
        # 1. 构建 MCP 请求格式
        request_data = {
            "toolcall": {
                "thought": f"调用 {tool_name} 工具",
                "name": tool_name,
                "params": params
            }
        }
        
        print(f"发送 MCP 请求: {json.dumps(request_data, indent=2, ensure_ascii=False)}")
        
        # 2. 发送请求到 MCP 服务器
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
```

### 代码分析

1. **初始化过程**：
   - 设置 MCP 服务器的基础 URL

2. **工具调用过程**：
   - 构建 MCP 请求格式，包含工具名称和参数
   - 发送 HTTP 请求到 MCP 服务器
   - 处理响应，如果请求失败则返回模拟响应

## MCP 协议的请求格式

```json
{
  "toolcall": {
    "thought": "调用工具的思考过程",
    "name": "工具名称",
    "params": {
      "参数1": "值1",
      "参数2": "值2"
    }
  }
}
```

## MCP 协议的响应格式

```json
{
  "toolcall_result": {
    "thought": "工具执行的思考过程",
    "content": "工具执行的结果"
  }
}
```

## 为什么使用 MCP 协议？

1. **标准化**：提供统一的通信格式，便于不同工具的集成
2. **灵活性**：支持不同类型的工具和服务
3. **可扩展性**：易于添加新的工具和功能
4. **可测试性**：便于模拟和测试工具的行为

## 实战练习

尝试修改 `mcp/mcp_client.py` 文件，添加一个新的方法来处理不同类型的工具调用，比如文件操作、网络请求等。

## 下一步

了解了 MCP 协议的概念和实现后，你可以继续学习 [Skill 开发](./../skill-development/) 章节，了解如何开发自定义技能。