# 项目运行

本章节将介绍如何运行智能面试助手，开始使用它来帮助你准备面试。

## 1. 运行项目

在项目目录下运行以下命令启动智能面试助手：

```bash
python main.py
```

## 2. 交互式对话

启动后，你会看到以下界面：

```
正在初始化智能面试助手...
智能面试助手初始化完成！

=== 智能面试助手 ===
你可以问我任何面试相关的问题，比如:
- 解释一下什么是 TCP/IP 协议？
- 如何实现一个线程安全的单例模式？
- 什么是分布式系统的 CAP 理论？
- 退出

你: 
```

现在你可以输入你的问题，智能面试助手会为你提供详细的回答。

### 示例对话

```
你: 什么是 TCP/IP 协议？
面试助手: 正在思考...
TCP/IP（Transmission Control Protocol/Internet Protocol）是一组用于实现网络通信的协议族，是互联网的基础协议。它定义了计算机如何在网络中进行通信，包括数据如何打包、寻址、传输、路由和接收。

## 核心知识点
- **TCP（传输控制协议）**：提供可靠的、面向连接的通信服务，确保数据的有序传输和错误检测。
- **IP（网际协议）**：负责将数据包从源地址传输到目标地址，处理路由和寻址。
- **分层架构**：TCP/IP 协议族采用分层架构，包括应用层、传输层、网络层和网络接口层。

## 示例代码
```python
# 使用 Python 的 socket 模块实现 TCP 客户端
import socket

def tcp_client():
    # 创建 TCP 套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 连接到服务器
    server_address = ('localhost', 8080)
    client_socket.connect(server_address)
    
    # 发送数据
    message = 'Hello, TCP server!'
    client_socket.sendall(message.encode())
    
    # 接收响应
    data = client_socket.recv(1024)
    print(f"Received: {data.decode()}")
    
    # 关闭连接
    client_socket.close()

if __name__ == "__main__":
    tcp_client()
```

## 面试建议
- 理解 TCP/IP 的分层架构及其各层的功能
- 掌握 TCP 和 UDP 的区别及应用场景
- 了解常见的网络协议，如 HTTP、FTP、SMTP 等
- 熟悉网络故障排查的基本方法
```
```

## 3. 测试模式

智能面试助手还提供了测试模式，自动运行预设的测试问题，帮助你快速了解它的功能。

### 启用测试模式

修改 `main.py` 文件，将 `interactive_chat` 函数中的测试代码取消注释：

```python
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
```

## 4. 常见问题

### 运行时错误
- **API Key 错误**：确保你填写了正确的 API Key
- **网络连接错误**：确保你的网络连接正常
- **依赖缺失**：确保你安装了所有必要的依赖

### 回答质量问题
- **回答不够详细**：尝试更具体地描述你的问题
- **回答与问题无关**：尝试重新表述你的问题
- **代码示例错误**：检查代码示例是否符合你的编程语言

## 5. 项目配置

你可以修改 `config.py` 文件来调整项目的配置：

```python
# 千问模型 API Key
OPENAI_API_KEY = "your_api_key_here"  # 填写你的千问模型 API Key

# 模型配置
MODEL_NAME = "qwen-max"  # 使用千问模型

# 系统提示词
SYSTEM_PROMPT = "你是一个专业的面试助手，帮助用户准备技术面试。请提供详细、准确的回答，并给出示例代码。"
```

## 6. 性能优化

### 对话历史管理

智能面试助手会保存对话历史，这可能会导致内存使用增加。你可以修改 `interview_agent.py` 文件来限制对话历史的长度：

```python
# 限制对话历史长度
if len(self.messages) > 10:
    # 保留系统提示词和最近的 8 条消息
    self.messages = [self.messages[0]] + self.messages[-8:]
```

### 响应时间优化

如果响应时间过长，你可以尝试：
- 使用更轻量级的模型
- 减少系统提示词的长度
- 优化网络连接

## 实战练习

尝试运行智能面试助手，向它询问一些你感兴趣的面试问题，看看它的回答是否符合你的预期。

## 下一步

了解了如何运行智能面试助手后，你可以继续学习 [扩展教程](./../extension/) 章节，了解如何扩展项目的功能。