---
title: Redis 数据结构
---

# Redis 数据结构

> 面试高频。考察三层：**5 种基础类型怎么用、底层编码是什么、Zset 为什么用跳表**。很多人停在"5 种类型"，一问"String 底层有几种实现"就答不上。本文按问答，每题答 + 追问 + 易错点。

## 思考锚点

Redis 之所以快，一个关键原因是它针对不同场景设计了不同的数据结构——String、List、Hash、Set、Zset 各有各的底层编码，而且会根据数据量自动在「紧凑结构」和「标准结构」之间切换。

这种设计哲学很值得学习：不是用一个通用结构打天下，而是在小数据时用最省内存的方式，大数据时切换到最快的方式。理解了这一点，Redis 数据结构的知识就不是孤立的死记硬背，而是有统一的设计思路。

本文要讲清楚 5 种基础类型的底层编码、转码策略、跳表的原理，以及 Redis 特有的扩展数据结构。

## 5 种基础类型速览

| 类型 | 底层编码（7.0+） | 典型场景 |
|---|---|---|
| String | int / embstr / raw | 计数器、缓存对象、分布式锁 |
| List | quicklist（链表节点 + listpack） | 消息队列、最新列表 |
| Hash | listpack（小）/ hashtable（大） | 对象存储（比 String 存对象省空间） |
| Set | intset（纯整数）/ hashtable | 去重、交并集（共同好友） |
| Zset | listpack（小）/ skiplist + hashtable | 排行榜、延时队列 |

核心一句话：**类型是给用户的抽象，编码是 Redis 内部怎么存**。同一类型在不同数据量/元素大小下用不同编码——这是面试重点。

---

## Q1：String 的底层编码有几种？

**答**：3 种，按存的内容自动选：
- **int**：存的是长整型（≤ long 范围），直接 8 字节 long 存。
- **embstr**：≤ 44 字节的字符串，RedisObject 和 SDS **连续内存**一次分配（cache 友好）。
- **raw**：> 44 字节，RedisObject 和 SDS 分两次 malloc。

**追问**：embstr 和 raw 区别？→ embstr 是**只读**的。任何修改（append、incr）都会**先把 embstr 转成 raw** 再改。所以反复改一个短字符串，编码会从 embstr → raw。

**易错点**：很多人不知道 embstr 的 **44 字节**阈值。这是 Redis 面试筛人的细节题。

## Q2：Hash 什么时候从 listpack 转 hashtable？

**答**：两个条件任一满足：元素数 > `hash-max-listpack-entries`（默认 128），或任一元素长度 > `hash-max-listpack-value`（默认 64 字节）。

- **listpack（小 Hash）**：紧凑连续内存，省空间、小数据访问快，但插入/删除要重排。
- **hashtable（大 Hash）**：标准哈希表，O(1) 读写，但内存开销大。

**易错点**：这种"小用紧凑结构、大转标准结构"的策略在 Redis **所有类型**里都有（Hash/Set/Zset/List 都是）。面试可以一句话总结：**Redis 用渐进式转码来平衡"小数据省内存、大数据快访问"**——这是 Redis 数据结构设计的核心思想，比背 5 个类型显深度。

## Q3：Zset 底层为什么用跳表（skiplist）？

**答**：Zset 同时要满足两件事：
1. **按 score 排序**（排行榜）→ 需要有序结构
2. **按 member 查 score**（点查）→ 需要哈希

所以 Zset 底层是 **skiplist（按 score 排序 + 范围查询）+ dict（member→score，O(1) 点查）** 双结构。小 Zset 用 listpack；超阈值转 skiplist+dict。

**跳表原理**：多层有序链表，高层是低层的"快速车道"。查询从最高层往下一层层 narrowing，期望 O(logN)。节点层数靠**随机数**决定（不是平衡树那种严格平衡）。

**追问**：为什么不用红黑树 / B+ 树？→ 跳表相比红黑树：
- **实现简单**（几百行 vs 红黑树调平衡麻烦）
- **范围查询友好**（链表天然顺序，范围扫 O(logN + M)；红黑树要中序遍历）
- **并发改造容易**（跳表可做 ConcurrentSkipiList，红黑树调平衡涉及多节点难加锁）

**易错点**：跳表**不是**"随机化平衡的二叉树"——它是**多层链表**。别和 B 树、红黑树结构混为一谈。

## Q4：Set 的 intset 是什么？

**答**：Set 全是整数且元素数 < `set-max-intlist-entries`（默认 512）时，用 **intset**——一个**有序整数数组**（不是哈希表）。

**为什么**：纯整数 Set 用有序数组比 hashtable 省内存（没有哈希桶指针开销），二分查找 O(logN) 对小集合足够快。

**升级**：插入非整数或超阈值 → 转 hashtable。**不可逆**（不会退回 intset）。

**易错点**：intset 内部**有序**，但 Set 抽象**无序**——这是"抽象层"和"实现层"的区别。面试时说"Set 无序"对，但"intset 是有序数组"也对，别被绕。

## Q5：List 为什么从 ziplist 改成 quicklist？

**答**：Redis 7.0 起 List 底层是 **quicklist**：一个双向链表，每个节点里装一个 listpack（小段连续内存）。兼得"链表的快插删"和"listpack 的小内存紧凑"。

**历史**：老版本用 ziplist（纯连续内存），但 ziplist 有致命缺点——**级联更新（cascade update）**：一个 entry 的长度变化可能引发后续所有 entry 连锁扩容，最坏 O(n²)。**这就是 Redis 逐步用 listpack 替换 ziplist 的根本原因**：listpack 取消了前驱节点对后继的长度依赖，消除级联更新。

**易错点**：ziplist 级联更新是经典坑，面试问"ziplist 有什么问题"就是考这个。答出"级联更新最坏 O(n²)"是加分。

## Q6：特殊数据结构（Bitmap / HyperLogLog / Geo / Stream）

**答**（知道场景就够）：
- **Bitmap**：基于 String 的位操作。场景：**签到、活跃用户统计**（1 亿用户约 12MB）。
- **HyperLogLog**：基数估算（去重计数），误差 0.81%。场景：**UV 统计**（12KB 估算 2⁶⁴ 个 IP）。
- **Geo**：基于 Zset 的地理坐标。场景：**附近的人 / 店**。
- **Stream**：5.0+ 引入，类 Kafka 的消息流（消费者组、ACK）。场景：轻量消息队列。

**易错点**：HyperLogLog **不存原始数据**，只存概率结构——`pfcount` 是**估算值**，要精确 UV 还得用 Set（但费内存）。这是"用精度换内存"的典型取舍。

---

## 易错点速查表

| 知识点 | 关键 |
|---|---|
| String embstr 阈值 | ≤ 44 字节；embstr 只读，改后转 raw |
| 转码策略 | 所有类型通用：小用紧凑结构，大转标准结构 |
| Zset 底层 | 小 listpack；大 skiplist + dict 双结构 |
| 跳表本质 | 多层链表，非"随机平衡二叉树"；范围查询友好 |
| Set intset | 纯整数小集合用有序数组（实现有序 ≠ 抽象有序） |
| ziplist → listpack | listpack 消除级联更新（O(n²) 坑） |
| HyperLogLog | 估算不存原始数据，12KB 估算基数 |
| Bitmap | 1 亿用户约 12MB |

---

## 复述自测

读完这篇，试试用自己的话回答三个问题：

1. **一句话总结**：跳表相比平衡二叉搜索树的核心优势是什么？为什么 Redis 选择跳表实现 Zset？（提示：从「实现简单」和「范围查询友好」思考）

2. **讲给初学者听**：怎么用「多层地铁站」来类比跳表？为什么跳表的查找时间复杂度是 O(log n)？

3. **预判追问**：如果你是面试官，读完这篇你会追问什么？（比如 Redis 7.0 为什么用 listpack 替代 ziplist？embstr 和 raw 的转换时机是什么？）

> 数据结构是 Redis 内功。持久化与缓存三大问题见 [持久化与缓存问题](./persistence-cache-problems)，总览与「为什么快」见 [Redis 总览](./)。
