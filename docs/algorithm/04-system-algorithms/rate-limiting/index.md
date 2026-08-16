# 限流算法

限流是系统保护的重要技术，用于控制单位时间内的请求数量，防止系统过载。本文将介绍两种常见的限流算法：令牌桶算法和漏桶算法。

## 令牌桶算法

### 基本概念

令牌桶算法是一种基于令牌的限流算法，其核心思想是：系统以固定的速率向令牌桶中放入令牌，当请求到达时，需要从桶中获取令牌才能处理，否则拒绝请求或等待。

### 工作原理

1. **令牌生成**：以固定的速率向令牌桶中放入令牌
2. **令牌存储**：令牌桶有最大容量，当桶满时，多余的令牌会被丢弃
3. **请求处理**：当请求到达时，尝试从桶中获取令牌
   - 如果获取成功，处理请求
   - 如果获取失败，拒绝请求或等待

### 优缺点

**优点**：
- 可以处理突发流量，当桶中有令牌积累时，可以允许短时间内的高并发请求
- 实现相对简单
- 可以通过调整令牌生成速率和桶容量来适应不同的场景

**缺点**：
- 令牌桶的大小和令牌生成速率需要根据实际情况调整
- 对于严格的限流场景，可能不够精确

### 代码示例

```python
import time
import threading

class TokenBucket:
    def __init__(self, capacity, rate):
        """
        初始化令牌桶
        capacity: 令牌桶容量
        rate: 令牌生成速率（个/秒）
        """
        self.capacity = capacity  # 令牌桶容量
        self.rate = rate  # 令牌生成速率（个/秒）
        self.tokens = capacity  # 当前令牌数
        self.last_refill_time = time.time()  # 上次填充令牌的时间
        self.lock = threading.RLock()  # 线程锁
    
    def _refill(self):
        """填充令牌"""
        now = time.time()
        time_passed = now - self.last_refill_time
        new_tokens = time_passed * self.rate
        if new_tokens > 0:
            self.tokens = min(self.capacity, self.tokens + new_tokens)
            self.last_refill_time = now
    
    def consume(self, tokens=1):
        """
        消费令牌
        tokens: 需要的令牌数
        return: 是否成功获取令牌
        """
        with self.lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

# 使用示例
token_bucket = TokenBucket(capacity=10, rate=2)  # 容量10，每秒生成2个令牌

# 测试限流
print("Testing token bucket rate limiting...")
for i in range(15):
    if token_bucket.consume():
        print(f"Request {i+1}: Allowed")
    else:
        print(f"Request {i+1}: Rejected")
    time.sleep(0.2)  # 每0.2秒发送一个请求

# 测试突发流量
print("\nTesting burst traffic...")
token_bucket = TokenBucket(capacity=10, rate=1)  # 容量10，每秒生成1个令牌
# 等待令牌桶填满
time.sleep(10)
# 突发15个请求
for i in range(15):
    if token_bucket.consume():
        print(f"Burst request {i+1}: Allowed")
    else:
        print(f"Burst request {i+1}: Rejected")
```

### 应用场景

- **API 限流**：控制 API 的访问速率
- **服务器保护**：防止服务器过载
- **资源分配**：合理分配系统资源

## 漏桶算法

### 基本概念

漏桶算法是一种基于队列的限流算法，其核心思想是：请求进入漏桶后，以固定的速率处理，当漏桶满时，多余的请求会被丢弃。

### 工作原理

1. **请求入桶**：请求进入漏桶
2. **请求处理**：漏桶以固定的速率处理请求
3. **桶满处理**：当漏桶满时，新的请求被丢弃

### 优缺点

**优点**：
- 可以平滑处理流量，避免突发流量对系统的冲击
- 实现相对简单
- 适合对流量有严格控制的场景

**缺点**：
- 不能处理突发流量，即使系统有能力处理更多请求
- 漏桶的大小和处理速率需要根据实际情况调整

### 代码示例

```python
import time
import threading
from collections import deque

class LeakyBucket:
    def __init__(self, capacity, rate):
        """
        初始化漏桶
        capacity: 漏桶容量
        rate: 处理速率（个/秒）
        """
        self.capacity = capacity  # 漏桶容量
        self.rate = rate  # 处理速率（个/秒）
        self.queue = deque()  # 请求队列
        self.last_process_time = time.time()  # 上次处理请求的时间
        self.lock = threading.RLock()  # 线程锁
    
    def _process(self):
        """处理请求"""
        now = time.time()
        time_passed = now - self.last_process_time
        process_count = int(time_passed * self.rate)
        
        if process_count > 0:
            for _ in range(process_count):
                if self.queue:
                    self.queue.popleft()
                else:
                    break
            self.last_process_time = now
    
    def add(self, request):
        """
        添加请求
        request: 请求
        return: 是否成功添加到漏桶
        """
        with self.lock:
            self._process()
            if len(self.queue) < self.capacity:
                self.queue.append(request)
                return True
            return False

# 使用示例
leaky_bucket = LeakyBucket(capacity=5, rate=1)  # 容量5，每秒处理1个请求

# 测试限流
print("Testing leaky bucket rate limiting...")
for i in range(10):
    if leaky_bucket.add(f"Request {i+1}"):
        print(f"Request {i+1}: Added to bucket")
    else:
        print(f"Request {i+1}: Rejected")
    time.sleep(0.2)  # 每0.2秒发送一个请求

# 等待处理
print("\nWaiting for processing...")
time.sleep(10)
print(f"Remaining requests in bucket: {len(leaky_bucket.queue)}")
```

### 应用场景

- **流量平滑**：平滑突发流量，避免系统过载
- **网络流量控制**：控制网络流量的速率
- **消息队列**：控制消息处理的速率

## 令牌桶与漏桶的对比

| 特性 | 令牌桶 | 漏桶 |
|------|-------|------|
| 处理方式 | 以固定速率生成令牌，请求需要获取令牌 | 以固定速率处理请求，请求进入队列 |
| 突发流量 | 可以处理突发流量，当有令牌积累时 | 不能处理突发流量，请求会被队列缓冲或丢弃 |
| 实现复杂度 | 中等 | 简单 |
| 适用场景 | API 限流，服务器保护 | 流量平滑，网络流量控制 |

## 其他限流算法

### 1. 计数器算法

**工作原理**：在单位时间内计数，超过阈值则拒绝请求。

**优点**：实现简单
**缺点**：可能存在边界问题，如在时间窗口的边界可能允许两倍的请求

### 2. 滑动窗口算法

**工作原理**：使用滑动窗口来计数，避免计数器算法的边界问题。

**优点**：解决了计数器算法的边界问题
**缺点**：实现相对复杂

## 限流策略

### 1. 拒绝策略

- **直接拒绝**：直接返回错误
- **排队等待**：将请求放入队列等待处理
- **降级处理**：返回降级内容，如缓存数据
- **熔断**：暂时停止服务，稍后恢复

### 2. 限流粒度

- **全局限流**：限制整个系统的请求速率
- **接口限流**：限制特定接口的请求速率
- **用户限流**：限制特定用户的请求速率
- **IP 限流**：限制特定 IP 的请求速率

## 应用场景

### 1. API 限流

控制 API 的访问速率，防止 API 被滥用。

### 2. 服务器保护

防止服务器过载，保证系统的稳定性。

### 3. 资源分配

合理分配系统资源，确保关键服务的正常运行。

### 4. 网络流量控制

控制网络流量的速率，避免网络拥塞。

## 总结

限流是系统保护的重要技术，令牌桶和漏桶是两种常见的限流算法：

- **令牌桶**：通过生成令牌来控制请求速率，可以处理突发流量，适合 API 限流和服务器保护
- **漏桶**：通过队列来平滑流量，避免突发流量对系统的冲击，适合流量平滑和网络流量控制
- **计数器**：简单但可能存在边界问题
- **滑动窗口**：解决了计数器算法的边界问题，但实现相对复杂

在实际应用中，应根据具体的场景选择合适的限流算法和策略，以确保系统的稳定性和可靠性。