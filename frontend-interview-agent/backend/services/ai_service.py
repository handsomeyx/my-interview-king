import json
import random
from datetime import datetime

import httpx


SYSTEM_PROMPT = """你是一个专业的 Java 后端面试官。你的特点：
1. 回答结构化：先给结论，再展开原理，最后讲实战
2. 紧扣 Java 后端生态：Spring、Redis、MySQL、Kafka、JVM、分布式
3. 主动追问：回答完后，给出 3 个可能的追问方向
4. 中文表达：使用清晰的中文，技术术语保留英文
5. 代码示例：涉及代码问题时，给出 Java 代码示例

回答格式：
## 核心回答
[结构化回答]

## 代码示例（如适用）
```java
// 代码
```

## 追问方向
- [追问1]
- [追问2]
- [追问3]"""


class AIService:
    def __init__(self, provider: str = "mock", api_key: str = "",
                 base_url: str = "", model: str = "", timeout: int = 30):
        self.provider = provider
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.timeout = timeout

    async def chat_stream(self, messages: list):
        if self.provider == "mock":
            async for chunk in self._mock_stream(messages):
                yield chunk
        elif self.provider == "zhipu":
            async for chunk in self._zhipu_stream(messages):
                yield chunk
        elif self.provider == "ollama":
            async for chunk in self._ollama_stream(messages):
                yield chunk
        else:
            yield {"type": "error", "error": f"未知的 AI 提供者: {self.provider}"}

    async def analyze(self, question: str, answer: str) -> dict:
        if self.provider == "mock":
            return self._mock_analyze(question)
        else:
            return await self._llm_analyze(question, answer)

    def _mock_stream(self, messages: list):
        question = messages[-1].get("content", "") if messages else ""
        response = self._mock_response(question)
        for token in self._tokenize(response):
            yield {"type": "token", "content": token}
        yield {"type": "meta", **self._mock_analyze(question)}
        yield {"type": "done"}

    def _mock_response(self, question: str) -> str:
        responses = {
            "tcp": self._response_tcp(),
            "jvm": self._response_jvm(),
            "spring": self._response_spring(),
            "redis": self._response_redis(),
            "mysql": self._response_mysql(),
            "kafka": self._response_kafka(),
            "分布式": self._response_distributed(),
            "算法": self._response_algo(),
        }
        lower = question.lower()
        for keyword, resp in responses.items():
            if keyword in lower or keyword in question:
                return resp
        return self._response_generic(question)

    def _response_tcp(self):
        return """## 核心回答

TCP 三次握手是建立可靠连接的过程：

1. **第一次握手**：客户端发送 SYN 包（seq=x），进入 SYN_SENT 状态
2. **第二次握手**：服务端回复 SYN+ACK 包（seq=y, ack=x+1），进入 SYN_RCVD
3. **第三次握手**：客户端发送 ACK 包（ack=y+1），连接建立

三次握手的原因：
- 确认双方收发能力正常
- 同步初始序列号
- 防止已失效的连接请求报文突然传送到服务端

## 代码示例（如适用）

```java
// 不需要代码
```

## 追问方向
- 为什么不是两次或四次握手？
- TIME_WAIT 状态的作用是什么？
- SYN 洪水攻击怎么防御？"""

    def _response_jvm(self):
        return """## 核心回答

JVM 内存模型主要包含以下区域：

**线程私有区：**
- 程序计数器：记录当前线程执行的字节码行号
- 虚拟机栈：存储局部变量、操作数栈，方法调用时入栈出栈
- 本地方法栈：为 Native 方法服务

**线程共享区：**
- 堆：存放对象实例和数组，GC 主战场
- 方法区/元空间：类信息、常量池、静态变量

**GC 算法：**
- 标记-清除：产生碎片
- 复制算法：新生代首选，Eden+Survivor
- 标记-整理：老年代使用
- 分代收集：新生代高频回收，老年代低频回收

## 追问方向
- 什么情况下对象会直接进入老年代？
- CMS 和 G1 收集器的区别？
- 如何排查 OOM？"""

    def _response_spring(self):
        return """## 核心回答

Spring IoC 控制反转的核心原理：

1. **Bean 定义**：通过 XML 配置或 @Component/@Service 注解声明 Bean
2. **Bean 扫描**：ClassPathBeanDefinitionScanner 扫描指定包下的注解类
3. **Bean 实例化**：通过反射创建对象实例（`BeanUtils.instantiateClass`）
4. **依赖注入**：构造器注入 > Setter 注入 > 字段注入
5. **生命周期管理**：初始化回调 → 使用 → 销毁回调

**循环依赖解决：**
- 构造器注入：无法解决，直接报错
- 字段/Setter 注入：通过三级缓存（singletonFactories）解决

## 追问方向
- Bean 的生命周期回调有哪些？
- AOP 的代理机制（JDK vs CGLib）？
- Spring Boot 自动装配原理？"""

    def _response_redis(self):
        return """## 核心回答

Redis 缓存三大问题及解决方案：

**缓存穿透**（查不存在的 key）：
- 布隆过滤器拦截
- 缓存空对象（设较短 TTL）

**缓存击穿**（热点 key 失效瞬间大量请求）：
- 互斥锁（分布式锁保证单线程重建）
- 热点数据永不过期 + 异步更新

**缓存雪崩**（大量 key 同时失效）：
- 过期时间加随机偏移
- 多级缓存（本地缓存 + Redis）
- 熔断降级

**Redis 为什么快？**
- 纯内存操作（纳秒级）
- 单线程模型（无锁竞争）
- IO 多路复用（epoll）
- 高效数据结构（跳表、哈希表）

## 追问方向
- Redis 持久化机制（RDB vs AOF）？
- Redis 集群模式（主从/哨兵/Cluster）？
- 如何保证缓存与数据库的一致性？"""

    def _response_mysql(self):
        return """## 核心回答

MySQL 索引与事务核心：

**索引类型：**
- B+ 树索引：最常用，范围查询效率高
- 哈希索引：等值查询、O(1) 查找
- 全文索引：全文检索

**事务 ACID 特性：**
- 原子性（Atomicity）：通过 Undo Log 回滚
- 一致性（Consistency）：通过 Redo Log + Undo Log 保证
- 隔离性（Isolation）：通过 MVCC + 锁实现
- 持久性（Durability）：通过 Redo Log 刷盘保证

**MVCC 实现：**
- 每行数据两个版本号：创建版本、删除版本
- Read View 判断哪些版本可见
- 快照读不加锁，提升并发性能

## 追问方向
- 间隙锁（GAP Lock）是什么？解决什么问题？
- InnoDB 和 MyISAM 的区别？
- 如何分析慢查询？"""

    def _response_kafka(self):
        return """## 核心回答

Kafka 核心架构：

**核心概念：**
- Producer：消息生产者
- Broker：Kafka 服务器（多个 Broker 组成集群）
- Topic：消息分类，类似文件夹
- Partition：Topic 的物理分片，有序性保证
- Consumer Group：消费者组，同一组内消费者分摊 Partition

**高可用原理：**
- 多副本（Leader + Follower）
- ISR（In-Sync Replicas）同步副本集
- ACK 机制：acks=all 保证最强一致性

**消息不丢失保证：**
1. 生产者：设置 acks=all + retries
2. Broker：unclean.leader.election.enable=false
3. 消费者：手动提交 offset（enable.auto.commit=false）

## 追问方向
- 如何保证消息不重复消费？
- 如何保证消息有序？
- Kafka vs RocketMQ vs RabbitMQ 选型？"""

    def _response_distributed(self):
        return """## 核心回答

分布式系统核心理论：

**CAP 定理：**
- 一致性（Consistency）：所有节点数据同步
- 可用性（Availability）：每个节点都能响应
- 分区容错性（Partition Tolerance）：网络分区必须接受
→ 只能在 CP 和 AP 之间选择

**BASE 理论（最终一致性）：**
- 基本可用、软状态、最终一致
- 适用于对实时一致性要求不高的场景

**共识算法：**
- Paxos：理论完备，实现复杂
- Raft：易于理解和实现，Leader 选举 + 日志复制
- ZAB：ZooKeeper 使用的原子广播协议

## 追问方向
- 分布式锁的实现方式？
- 分布式事务解决方案（2PC/TCC/Seata）？
- 一致性哈希原理？"""

    def _response_algo(self):
        return """## 核心回答

算法学习方法论：

**解题三板斧：**
1. 识别模式：滑动窗口/双指针/DFS/BFS/动态规划
2. 确定状态：定义状态变量和转移方程
3. 验证边界：空输入/单元素/极端值

**高频算法模式：**
- 滑动窗口：解决连续子串/子数组问题
- 二叉树遍历：前序/中序/后序/层序
- 动态规划：最优子结构 + 重叠子问题
- 回溯：选择/不选择 × 剪枝优化
- 二分查找：搜索空间二分 + 条件判断

## 追问方向
- 动态规划如何确定状态？
- BFS 和 DFS 的使用场景？
- 如何分析时间和空间复杂度？"""

    def _response_generic(self, question: str) -> str:
        return f"""## 核心回答

关于「{question}」的回答：

这是一个很好的问题。让我从几个角度来分析：

1. **概念层面**：理解这个技术/问题的核心定义和设计目标
2. **原理层面**：深入底层机制，理解其工作原理
3. **实践层面**：在真实项目中的应用场景和最佳实践
4. **对比层面**：与同类技术的优劣对比

## 追问方向
- 这个技术的核心设计理念是什么？
- 在什么场景下选择它？不选择它？
- 有哪些常见的坑？如何避免？"""

    def _tokenize(self, text: str):
        tokens = []
        for paragraph in text.split('\n'):
            if paragraph.strip():
                tokens.append(paragraph + '\n')
        if tokens:
            tokens[-1] = tokens[-1].rstrip('\n')
        return tokens

    def _mock_analyze(self, question: str) -> dict:
        lower = question.lower()

        keywords_map = {
            'tcp': ['TCP', '三次握手', 'SYN', 'ACK', '连接'],
            'jvm': ['JVM', '内存', 'GC', '堆', '栈', '类加载'],
            'spring': ['Spring', 'IoC', 'AOP', 'Bean', '自动装配'],
            'redis': ['Redis', '缓存', '持久化', '集群', '穿透'],
            'mysql': ['MySQL', '索引', '事务', 'MVCC', '锁', 'B+树'],
            'kafka': ['Kafka', '消息队列', 'Broker', 'Topic', 'Partition'],
            '分布式': ['分布式', 'CAP', '一致性', '共识', 'Raft'],
            '算法': ['算法', '复杂度', '动态规划', '排序', '查找'],
        }

        matched_keywords = []
        for key, kws in keywords_map.items():
            if key in lower or key in question:
                matched_keywords.extend(kws)

        if not matched_keywords:
            matched_keywords = ['核心概念', '设计原理', '实践应用']

        knowledge_graph = [
            {"name": kw, "strength": "strong" if i < 2 else "medium"}
            for i, kw in enumerate(matched_keywords[:4])
        ]

        follow_ups = [
            f"「{matched_keywords[0]}」在实际项目中怎么应用？",
            f"如果让你设计「{matched_keywords[0]}」的替代方案，你会怎么做？",
            f"「{matched_keywords[0]}」和相关技术的区别是什么？"
        ]

        confidence = random.randint(65, 92)

        return {
            "confidence": confidence,
            "followUps": follow_ups,
            "knowledgeGraph": knowledge_graph
        }

    async def _zhipu_stream(self, messages: list):
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + messages,
            "stream": True
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream("POST", url, headers=headers, json=payload) as response:
                    if response.status_code != 200:
                        error_text = await response.aread()
                        yield {"type": "error", "error": f"AI 服务错误 ({response.status_code}): {error_text.decode()}"}
                        return
                    async for line in response.aiter_lines():
                        line = line.strip()
                        if not line or line == "data: [DONE]":
                            continue
                        if line.startswith("data: "):
                            try:
                                data = json.loads(line[6:])
                                delta = data.get("choices", [{}])[0].get("delta", {})
                                content = delta.get("content", "")
                                if content:
                                    yield {"type": "token", "content": content}
                            except json.JSONDecodeError:
                                continue
                    question = messages[-1].get("content", "") if messages else ""
                    yield {"type": "meta", **(await self._llm_analyze(question, ""))}
                    yield {"type": "done"}
        except Exception as e:
            yield {"type": "error", "error": f"AI 调用失败: {str(e)}"}

    async def _ollama_stream(self, messages: list):
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + messages,
            "stream": True
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream("POST", url, json=payload) as response:
                    if response.status_code != 200:
                        error_text = await response.aread()
                        yield {"type": "error", "error": f"Ollama 错误 ({response.status_code}): {error_text.decode()}"}
                        return
                    async for line in response.aiter_lines():
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            data = json.loads(line)
                            if "message" in data:
                                content = data["message"].get("content", "")
                                if content:
                                    yield {"type": "token", "content": content}
                            if data.get("done", False):
                                break
                        except json.JSONDecodeError:
                            continue
                    question = messages[-1].get("content", "") if messages else ""
                    yield {"type": "meta", **self._mock_analyze(question)}
                    yield {"type": "done"}
        except Exception as e:
            yield {"type": "error", "error": f"Ollama 调用失败: {str(e)}"}

    async def _llm_analyze(self, question: str, answer: str) -> dict:
        analysis_prompt = f"""分析以下面试回答的质量：

问题：{question}
回答：{answer[:2000]}

请输出：
1. 信心指数（0-100分）
2. 3个相关的追问方向
3. 4个相关的知识图谱节点（标注 strength: strong/medium/weak）

以JSON格式输出：
{{"confidence": 85, "followUps": ["追问1", "追问2", "追问3"], "knowledgeGraph": [{{"name": "知识点", "strength": "strong"}}]}}"""

        if self.provider == "zhipu":
            url = f"{self.base_url}/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": analysis_prompt}],
                "temperature": 0.3,
                "response_format": {"type": "json_object"}
            }
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    resp = await client.post(url, headers=headers, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                        return json.loads(content)
            except Exception:
                pass

        return self._mock_analyze(question)

    @classmethod
    def from_config(cls, app) -> "AIService":
        return cls(
            provider=app.config.get("AI_PROVIDER", "mock"),
            api_key=app.config.get("AI_API_KEY", ""),
            base_url=app.config.get("AI_BASE_URL", ""),
            model=app.config.get("AI_MODEL", ""),
            timeout=app.config.get("AI_TIMEOUT", 30)
        )
