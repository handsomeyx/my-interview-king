#!/usr/bin/env python3
# 智能面试助手后端服务器
# 用于接收前端的请求并返回模拟数据

from flask import Flask, request, jsonify, session
from flask_cors import CORS
import sqlite3
import hashlib
import uuid
from datetime import datetime

# 创建 Flask 应用
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于会话管理
CORS(app, supports_credentials=True)  # 启用 CORS，允许前端跨域请求

# 初始化数据库
def init_db():
    conn = sqlite3.connect('interview_agent.db')
    cursor = conn.cursor()
    
    # 创建用户表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT,
        email TEXT UNIQUE,
        created_at TEXT,
        chat_count INTEGER DEFAULT 0
    )''')
    
    # 创建游客表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS guests (
        id TEXT PRIMARY KEY,
        chat_count INTEGER DEFAULT 0,
        created_at TEXT
    )''')
    
    conn.commit()
    conn.close()

# 初始化数据库
init_db()

# 辅助函数：密码哈希
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 辅助函数：获取或创建游客

def get_or_create_guest(guest_id):
    conn = sqlite3.connect('interview_agent.db')
    cursor = conn.cursor()
    
    if not guest_id:
        guest_id = str(uuid.uuid4())
        cursor.execute('INSERT INTO guests (id, chat_count, created_at) VALUES (?, ?, ?)', 
                      (guest_id, 0, datetime.now().isoformat()))
        conn.commit()
    else:
        cursor.execute('SELECT * FROM guests WHERE id = ?', (guest_id,))
        guest = cursor.fetchone()
        if not guest:
            guest_id = str(uuid.uuid4())
            cursor.execute('INSERT INTO guests (id, chat_count, created_at) VALUES (?, ?, ?)', 
                          (guest_id, 0, datetime.now().isoformat()))
            conn.commit()
    
    conn.close()
    return guest_id

# 辅助函数：检查对话次数限制
def check_chat_limit(user_id, is_guest):
    conn = sqlite3.connect('interview_agent.db')
    cursor = conn.cursor()
    
    if is_guest:
        cursor.execute('SELECT chat_count FROM guests WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        if result:
            chat_count = result[0]
            if chat_count >= 3:
                conn.close()
                return False, chat_count
    
    conn.close()
    return True, 0

# 辅助函数：增加对话次数
def increment_chat_count(user_id, is_guest):
    conn = sqlite3.connect('interview_agent.db')
    cursor = conn.cursor()
    
    if is_guest:
        cursor.execute('UPDATE guests SET chat_count = chat_count + 1 WHERE id = ?', (user_id,))
    else:
        cursor.execute('UPDATE users SET chat_count = chat_count + 1 WHERE id = ?', (user_id,))
    
    conn.commit()
    conn.close()

# 生成模拟响应（根据用户问题生成不同的回答）
def generate_mock_response(question):
    responses = {
        'who': '''# 关于我

我是你的智能面试助手，是基于先进的AI技术开发的面试辅导工具。

## 我的功能
- **面试问题回答**：为你提供专业、结构化的面试问题回答
- **技术知识讲解**：详细解释各种技术概念和原理
- **面试技巧指导**：分享有效的面试策略和技巧
- **智能追问**：根据你的回答进行针对性的追问
- **知识图谱**：展示相关知识点的关联关系
- **信心指数**：评估你的回答质量和专业程度

## 我的优势
- **专业**：覆盖后端、前端、算法等多个技术领域
- **快速**：实时生成详细的回答和分析
- **个性化**：根据你的问题提供定制化的内容
- **全面**：不仅提供答案，还提供相关的知识点和面试技巧

## 如何使用我
1. 输入你的面试问题或技术疑问
2. 查看我提供的详细回答
3. 参考智能追问链进行深入学习
4. 利用知识图谱了解相关知识点
5. 根据信心指数评估你的掌握程度

我随时准备帮助你提升面试技能，祝你面试成功！''',

        'tcp': '''# TCP/IP 协议详解

## 核心概念
TCP/IP 是互联网的基础协议套件，包含两个核心协议：

### 1. TCP（传输控制协议）
- **面向连接**：建立连接需要三次握手
- **可靠传输**：通过确认机制和重传机制保证数据完整性
- **流量控制**：使用滑动窗口机制
- **拥塞控制**：避免网络拥塞

### 2. IP（网际协议）
- **无连接**：不保证数据包的顺序和完整性
- **寻址**：使用 IP 地址标识网络设备
- **路由**：确定数据包传输路径

## 协议层次
```
应用层 → HTTP/FTP/DNS
传输层 → TCP/UDP
网络层 → IP/ICMP
链路层 → Ethernet/WiFi
```

## 面试要点
- 三次握手和四次挥手的过程
- TCP 和 UDP 的区别
- 滑动窗口机制
- TIME_WAIT 状态的作用''',

        'jvm': '''# JVM 内存模型详解

## 内存区域划分

### 1. 堆（Heap）
- 存放对象实例
- 分为年轻代和老年代
- 垃圾回收的主要区域

### 2. 栈（Stack）
- 存放局部变量
- 方法调用的上下文
- 线程私有

### 3. 方法区（Method Area）
- 类信息、常量、静态变量
- JDK 8 后改为元空间（Metaspace）

## 垃圾回收

### 垃圾回收算法
- **标记-清除**：简单但产生碎片
- **复制算法**：新生代使用，效率高
- **标记-整理**：老年代使用，避免碎片

### 垃圾回收器
```
Serial → 单线程，适合小应用
Parallel → 多线程，注重吞吐量
CMS → 低延迟，并发收集
G1 → 分区收集，平衡吞吐量和延迟
ZGC → 超低延迟，大堆内存
```

## 面试要点
- 内存泄漏排查方法
- OOM 异常处理
- JVM 调优参数
- 类加载机制''',

        'spring': '''# Spring Boot 核心原理

## 自动配置原理

### @SpringBootApplication
```java
@SpringBootConfiguration
@EnableAutoConfiguration
@ComponentScan
public @interface SpringBootApplication {}
```

### 自动配置流程
1. **读取 META-INF/spring.factories**
2. **条件判断**：@ConditionalOnClass, @ConditionalOnProperty
3. **配置加载**：加载默认配置
4. **用户配置覆盖**：application.properties

## 核心特性

### 1. 起步依赖（Starter）
- 简化 Maven 配置
- 自动版本管理

### 2. 内嵌服务器
- Tomcat/Jetty/Undertow
- 无需部署 WAR 包

### 3. Actuator 监控
- 健康检查
- 指标收集
- 端点暴露

## 面试要点
- IOC 容器原理
- AOP 实现机制
- 事务管理
- 微服务架构设计''',

        'default': '''# 智能面试助手回答

## 核心知识点
- **概念理解**：这个问题涉及的核心概念是...
- **实际应用**：在实际项目中，我们通常...
- **最佳实践**：建议采用以下最佳实践...

## 示例代码
```java
// 示例代码
public class Example {
    public void demonstrate() {
        // 核心逻辑实现
    }
}
```

## 面试技巧
1. **结构化回答**：先讲概念，再讲原理，最后讲应用
2. **结合实际**：举例说明在实际项目中的应用
3. **深入原理**：不仅要知道是什么，还要知道为什么
4. **举一反三**：展示你对相关技术的理解

## 追问准备
面试官可能会继续问：
- 这个技术的优缺点是什么？
- 在什么场景下使用？
- 与其他技术的对比？

建议提前准备这些问题的答案。'''
    }
    
    lower_question = question.lower()
    if '你是谁' in lower_question or 'who are you' in lower_question or '自我介绍' in lower_question:
        return responses['who']
    elif 'tcp' in lower_question or 'ip' in lower_question or '网络' in lower_question:
        return responses['tcp']
    elif 'jvm' in lower_question or '内存' in lower_question or 'gc' in lower_question:
        return responses['jvm']
    elif 'spring' in lower_question or 'boot' in lower_question:
        return responses['spring']
    else:
        return responses['default']

# 生成智能追问链
def generate_follow_up_questions(question):
    lower_question = question.lower()
    
    if '你是谁' in lower_question or 'who are you' in lower_question or '自我介绍' in lower_question:
        return [
            '你能帮我准备哪些类型的面试？',
            '你如何评估我的回答质量？',
            '你能提供哪些技术领域的面试指导？'
        ]
    elif 'tcp' in lower_question or 'ip' in lower_question or '网络' in lower_question:
        return [
            'TCP和UDP的区别是什么？',
            '三次握手的详细过程是什么？',
            'TIME_WAIT状态的作用是什么？'
        ]
    elif 'jvm' in lower_question or '内存' in lower_question or 'gc' in lower_question:
        return [
            '垃圾回收的原理是什么？',
            '如何排查内存泄漏问题？',
            'JVM调优的常用参数有哪些？'
        ]
    elif 'spring' in lower_question or 'boot' in lower_question:
        return [
            'Spring IOC容器的原理是什么？',
            'Spring AOP的实现机制是什么？',
            'Spring Boot自动配置的原理是什么？'
        ]
    else:
        return [
            '这个技术的优缺点是什么？',
            '在什么场景下使用这个技术？',
            '与其他类似技术的对比是什么？'
        ]

# 生成知识图谱
def generate_knowledge_graph(question):
    lower_question = question.lower()
    
    if '你是谁' in lower_question or 'who are you' in lower_question or '自我介绍' in lower_question:
        return [
            {'name': '面试技巧', 'strength': 'strong'},
            {'name': '技术知识', 'strength': 'strong'},
            {'name': '智能追问', 'strength': 'strong'},
            {'name': '知识图谱', 'strength': 'strong'},
            {'name': '信心指数', 'strength': 'strong'}
        ]
    elif 'tcp' in lower_question or 'ip' in lower_question or '网络' in lower_question:
        return [
            {'name': 'TCP/IP', 'strength': 'strong'},
            {'name': 'HTTP', 'strength': 'medium'},
            {'name': '网络协议', 'strength': 'strong'},
            {'name': '三次握手', 'strength': 'medium'},
            {'name': '四次挥手', 'strength': 'weak'}
        ]
    elif 'jvm' in lower_question or '内存' in lower_question or 'gc' in lower_question:
        return [
            {'name': 'JVM', 'strength': 'strong'},
            {'name': '内存模型', 'strength': 'strong'},
            {'name': '垃圾回收', 'strength': 'medium'},
            {'name': '类加载', 'strength': 'weak'},
            {'name': 'JVM调优', 'strength': 'weak'}
        ]
    elif 'spring' in lower_question or 'boot' in lower_question:
        return [
            {'name': 'Spring Boot', 'strength': 'strong'},
            {'name': 'IOC', 'strength': 'medium'},
            {'name': 'AOP', 'strength': 'weak'},
            {'name': '自动配置', 'strength': 'medium'},
            {'name': '微服务', 'strength': 'weak'}
        ]
    else:
        return [
            {'name': '技术概念', 'strength': 'medium'},
            {'name': '实际应用', 'strength': 'weak'},
            {'name': '最佳实践', 'strength': 'weak'},
            {'name': '面试技巧', 'strength': 'medium'},
            {'name': '相关技术', 'strength': 'weak'}
        ]

# 生成信心指数
def generate_confidence_score(question):
    # 模拟信心指数，实际项目中可以根据回答质量计算
    import random
    return random.randint(60, 95)

# 用户注册API
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        
        if not username or not password or not email:
            return jsonify({'error': '请提供用户名、密码和邮箱'}), 400
        
        conn = sqlite3.connect('interview_agent.db')
        cursor = conn.cursor()
        
        # 检查用户名是否已存在
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            conn.close()
            return jsonify({'error': '用户名已存在'}), 400
        
        # 检查邮箱是否已存在
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            conn.close()
            return jsonify({'error': '邮箱已存在'}), 400
        
        # 创建新用户
        user_id = str(uuid.uuid4())
        hashed_password = hash_password(password)
        created_at = datetime.now().isoformat()
        
        cursor.execute('INSERT INTO users (id, username, password, email, created_at, chat_count) VALUES (?, ?, ?, ?, ?, ?)', 
                      (user_id, username, hashed_password, email, created_at, 0))
        conn.commit()
        conn.close()
        
        # 设置会话
        session['user_id'] = user_id
        session['username'] = username
        session['is_guest'] = False
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'username': username
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'发生错误: {str(e)}'}), 500

# 用户登录API
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': '请提供用户名和密码'}), 400
        
        conn = sqlite3.connect('interview_agent.db')
        cursor = conn.cursor()
        
        # 查找用户
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        if not user or hash_password(password) != user[2]:
            conn.close()
            return jsonify({'error': '用户名或密码错误'}), 401
        
        conn.close()
        
        # 设置会话
        session['user_id'] = user[0]
        session['username'] = user[1]
        session['is_guest'] = False
        
        return jsonify({
            'success': True,
            'user_id': user[0],
            'username': user[1]
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'发生错误: {str(e)}'}), 500

# 用户登出API
@app.route('/logout', methods=['POST'])
def logout():
    try:
        session.clear()
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'发生错误: {str(e)}'}), 500

# 获取用户信息API
@app.route('/user', methods=['GET'])
def get_user():
    try:
        if 'user_id' in session:
            return jsonify({
                'is_logged_in': True,
                'user_id': session['user_id'],
                'username': session['username'],
                'is_guest': session.get('is_guest', False)
            })
        else:
            # 检查是否有游客ID
            guest_id = request.cookies.get('guest_id')
            if not guest_id:
                guest_id = get_or_create_guest(None)
            
            return jsonify({
                'is_logged_in': False,
                'guest_id': guest_id,
                'is_guest': True
            })
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'发生错误: {str(e)}'}), 500

# 处理聊天请求
@app.route('/chat', methods=['POST'])
def chat():
    try:
        # 获取前端发送的消息
        data = request.json
        message = data.get('message', '')
        guest_id = data.get('guest_id', '')
        
        if not message:
            return jsonify({'response': '请提供有效的消息'}), 400
        
        # 检查用户状态
        is_guest = True
        user_id = guest_id
        
        if 'user_id' in session:
            is_guest = False
            user_id = session['user_id']
        else:
            # 获取或创建游客
            user_id = get_or_create_guest(guest_id)
        
        # 检查对话次数限制
        can_chat, chat_count = check_chat_limit(user_id, is_guest)
        if not can_chat:
            return jsonify({
                'error': '游客模式对话次数已达上限，请登录后继续使用',
                'chat_count': chat_count,
                'limit': 3
            }), 403
        
        # 生成模拟回答
        response = generate_mock_response(message)
        
        # 生成智能追问链
        follow_up_questions = generate_follow_up_questions(message)
        
        # 生成知识图谱
        knowledge_graph = generate_knowledge_graph(message)
        
        # 生成信心指数
        confidence_score = generate_confidence_score(message)
        
        # 增加对话次数
        increment_chat_count(user_id, is_guest)
        
        # 返回回答和相关信息
        return jsonify({
            'response': response,
            'follow_up_questions': follow_up_questions,
            'knowledge_graph': knowledge_graph,
            'confidence_score': confidence_score,
            'chat_count': chat_count + 1,
            'is_guest': is_guest
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'response': f'发生错误: {str(e)}'}), 500

# 健康检查
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    # 启动服务器
    app.run(host='0.0.0.0', port=5000, debug=True)