import random


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

## 如何使用我
1. 输入你的面试问题或技术疑问
2. 查看我提供的详细回答
3. 参考智能追问链进行深入学习
4. 利用知识图谱了解相关知识点
5. 根据信心指数评估你的掌握程度''',

        'tcp': '''# TCP 三次握手

1. **第一次握手**：客户端发送 SYN 包，进入 SYN_SENT 状态
2. **第二次握手**：服务端回复 SYN+ACK 包，进入 SYN_RCVD 状态
3. **第三次握手**：客户端发送 ACK 包，连接建立

> 三次握手确保双方收发能力正常，防止已失效的连接请求报文突然又传送到了服务端。''',

        'jvm': '''# JVM 内存模型

### 主要区域
- **堆**：存放对象实例，GC 主战场
- **栈**：存放局部变量，线程私有
- **方法区**：类信息、常量池

### 垃圾回收
- **标记-清除**：产生碎片
- **复制算法**：新生代首选
- **标记-整理**：老年代使用''',

        'spring': '''# Spring IoC 原理

1. **Bean 定义**：通过 XML 或注解声明 Bean
2. **Bean 实例化**：反射创建对象
3. **依赖注入**：构造器/Setter/字段注入
4. **生命周期管理**：初始化、销毁回调''',

        'redis': '''# Redis 缓存穿透

### 解决方案
- **布隆过滤器**：拦截不存在的 key
- **缓存空对象**：缓存空值并设置较短 TTL
- **互斥锁**：查询时加锁，防止缓存雪崩'''
    }

    lower = question.lower()
    if '你是谁' in lower or 'who are you' in lower or '自我介绍' in lower:
        return responses['who']
    elif 'tcp' in lower or 'ip' in lower or '网络' in lower or '握手' in lower:
        return responses['tcp']
    elif 'jvm' in lower or '内存' in lower or 'gc' in lower:
        return responses['jvm']
    elif 'spring' in lower or 'ioc' in lower or 'boot' in lower:
        return responses['spring']
    elif 'redis' in lower or '缓存' in lower:
        return responses['redis']
    else:
        return f'''# 关于「{question}」的回答

## 核心知识点
- **概念理解**：这个问题涉及的核心概念需要深入掌握
- **实际应用**：在实际项目中，这个技术有广泛的应用场景
- **最佳实践**：建议采用标准化的实践方案

## 面试要点
1. **结构化回答**：先讲概念，再讲原理，最后讲应用
2. **结合实际**：举例说明在实际项目中的应用
3. **深入原理**：不仅要知道是什么，还要知道为什么

## 追问准备
- 这个技术的优缺点是什么？
- 在什么场景下使用？
- 与其他技术的对比是什么？'''


def generate_follow_ups(question):
    lower = question.lower()
    if '你是谁' in lower or 'who are you' in lower:
        return ['你能帮我准备哪些类型的面试？', '你如何评估我的回答质量？', '你能提供哪些技术领域的面试指导？']
    elif 'tcp' in lower or 'ip' in lower or '网络' in lower:
        return ['TCP和UDP的区别是什么？', '三次握手的详细过程是什么？', 'TIME_WAIT状态的作用是什么？']
    elif 'jvm' in lower or '内存' in lower:
        return ['垃圾回收的原理是什么？', '如何排查内存泄漏问题？', 'JVM调优的常用参数有哪些？']
    elif 'spring' in lower or 'boot' in lower:
        return ['Spring IOC容器的原理是什么？', 'Spring AOP的实现机制是什么？', 'Spring Boot自动配置的原理是什么？']
    elif 'redis' in lower or '缓存' in lower:
        return ['Redis为什么这么快？', 'Redis的持久化机制是什么？', '如何保证缓存和数据库的一致性？']
    else:
        return ['这个技术的优缺点是什么？', '在什么场景下使用？', '与其他类似技术的对比是什么？']


def generate_knowledge_graph(question):
    lower = question.lower()
    if '你是谁' in lower or 'who are you' in lower:
        return [
            {'name': '面试技巧', 'strength': 'strong'},
            {'name': '技术知识', 'strength': 'strong'},
            {'name': '智能追问', 'strength': 'strong'}
        ]
    elif 'tcp' in lower or 'ip' in lower or '网络' in lower:
        return [
            {'name': 'TCP/IP', 'strength': 'strong'},
            {'name': 'HTTP', 'strength': 'medium'},
            {'name': '网络协议', 'strength': 'strong'},
            {'name': '三次握手', 'strength': 'medium'}
        ]
    elif 'jvm' in lower or '内存' in lower:
        return [
            {'name': 'JVM', 'strength': 'strong'},
            {'name': '内存模型', 'strength': 'strong'},
            {'name': '垃圾回收', 'strength': 'medium'}
        ]
    elif 'spring' in lower or 'boot' in lower:
        return [
            {'name': 'Spring Boot', 'strength': 'strong'},
            {'name': 'IOC', 'strength': 'medium'},
            {'name': 'AOP', 'strength': 'weak'}
        ]
    elif 'redis' in lower or '缓存' in lower:
        return [
            {'name': 'Redis', 'strength': 'strong'},
            {'name': '缓存策略', 'strength': 'medium'},
            {'name': '持久化', 'strength': 'weak'}
        ]
    else:
        return [
            {'name': '技术概念', 'strength': 'medium'},
            {'name': '实际应用', 'strength': 'weak'},
            {'name': '最佳实践', 'strength': 'weak'}
        ]


def generate_confidence(question):
    return random.randint(60, 95)
