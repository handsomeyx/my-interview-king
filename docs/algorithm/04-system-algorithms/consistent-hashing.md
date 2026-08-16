---
title: 一致性哈希
---

# 一致性哈希

> **系统设计算法 · 后端面试高频**。解决「节点增删时大量请求漂移」问题，是 Redis 集群、分布式存储、负载均衡的底层支撑。
>
> 相关：[负载均衡](./load-balancing/)（一致性哈希是其中一种策略）、[Redis 集群](../../java/redis/)、[分布式 ID](./unique-id/)

## 一、为什么需要：普通哈希的痛

假设有 3 台缓存节点，用最朴素的哈希分流：

```java
int node = hash(key) % 3;
```

某天加一台节点（变成 4 台），`hash(key) % 4` 的结果和原来 `% 3` **几乎全不同**——意味着几乎所有 key 都要重新分配节点，缓存大面积失效，请求穿透到数据库，系统抖动。

**核心矛盾**：节点数变化时，希望只有「涉及变化节点的那部分 key」迁移，其余 key 不动。普通取模做不到。

## 二、核心思想：环形哈希空间

一致性哈希把整个哈希空间想象成一个 **0 ~ 2³² 的环**：

1. 把「节点」也用哈希映射到环上（节点 IP/名 哈希）
2. 把「key」也映射到环上
3. 每个 key **顺时针**找遇到的第一个节点，就是它的归属

```
        0
   N1   |    N2
    \   |   /
     \  |  /
      \ | /
       \|/
-------+-------- 2^32
       /|\
      / | \
     /  |  \
   N3   |   key→顺时针最近的 N1
        2^31
```

**节点增删时只影响相邻段**：加 N4 到 N1 和 N2 之间，只有原本归 N1（环上 N4~N1 段之外的 N1~N4 段）的部分 key 改归 N4，其余 key 不动。这就是「一致性」。

## 三、虚拟节点：解决倾斜

节点少时，环上分布不均（可能 N1 占了 60% 环，N2 只占 20%），导致负载倾斜。

**解法：虚拟节点**。每个真实节点对应 **多个虚拟节点**（如 150 个），分散在环上。统计时把虚拟节点的负载归到真实节点。

```
N1 → N1#1, N1#2, ..., N1#150   散落在环上
N2 → N2#1, N2#2, ..., N2#150
```

虚拟节点数足够多时，负载近似均匀（标准差随虚拟节点数下降）。

## 四、Java 实现（TreeMap 模拟环）

```java
public class ConsistentHash {
    private final TreeMap<Long, String> ring = new TreeMap<>();
    private final int VIRTUAL_COUNT = 150;

    // 哈希函数（演示用 FNV，生产用 MurmurHash3）
    private long hash(String key) {
        long h = 2166136261L;
        for (byte b : key.getBytes()) { h = (h ^ b) * 16777619L; }
        return h & 0xffffffffL;
    }

    public void addNode(String node) {
        for (int i = 0; i < VIRTUAL_COUNT; i++) {
            ring.put(hash(node + "#" + i), node);
        }
    }

    public void removeNode(String node) {
        for (int i = 0; i < VIRTUAL_COUNT; i++) {
            ring.remove(hash(node + "#" + i));
        }
    }

    public String route(String key) {
        if (ring.isEmpty()) return null;
        long h = hash(key);
        // 顺时针找第一个 >= h 的节点
        Map.Entry<Long, String> entry = ring.ceilingEntry(h);
        if (entry == null) entry = ring.firstEntry();   // 环绕回 0
        return entry.getValue();
    }
}
```

`TreeMap.ceilingEntry` O(log n) 找顺时针下一个节点，高效。

## 五、工程应用

| 系统 | 用法 |
|---|---|
| **Redis Cluster** | 用「哈希槽」变体（16384 槽分配到节点），思想同源 |
| **Memcached** | 客户端（如 Spymemcached）一致性哈希路由 |
| **Cassandra / DynamoDB** | 一致性哈希决定数据分片归属 |
| **CDN** | 用一致性哈希把 URL 路由到边缘节点 |
| **Dubbo / gRPC 负载均衡** | 一致性哈希策略，保证同 key 同节点 |

## 六、面试高频问

1. **为什么用虚拟节点**——解决节点少时的倾斜，让负载近似均匀
2. **一致性哈希 vs 哈希槽（Redis Cluster）**——一致性哈希是连续环，哈希槽是离散槽位（手动/自动分配到节点）；哈希槽迁移更可控，一致性哈希增删只影响相邻段
3. **节点故障时数据怎么办**——故障节点的 key 顺时针归下一节点；可配「虚拟节点副本数」控影响范围
4. **虚拟节点数怎么定**——经验值 150~200（Redis Cluster 用 16384 槽是等价思想）；越多越均匀，但内存/查找略增

## 七、相关阅读

- [负载均衡](./load-balancing/)：一致性哈希是负载均衡策略之一（对比轮询/最少连接）
- [Redis 集群原理](../../java/redis/)：哈希槽实战
- [分布式场景：接入与路由层](../../distributed/scenarios/gateway)：API 网关如何用一致性哈希做路由

> 这是**纯算法站（如 LeetCode 类）不覆盖**的内容——既是算法，也是后端系统设计，是 Java 后端面试的差异化加分项。
