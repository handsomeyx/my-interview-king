# Redis

Redis 是内存型 KV 数据库。面试官爱问的不是"Redis 是什么"，而是**为什么快、每种类型的底层结构是什么、持久化怎么取舍、缓存三大问题怎么解**。这篇是总览，每个主题点到面试官追问的深度，细节展开在子页。

## 为什么快

三个原因，缺一不可：

1. **全内存**：数据在内存，读写是内存速度（纳秒～微秒级），这是基础。
2. **单线程 + IO 多路复用**：Redis 6 之前命令执行单线程，避免锁竞争和上下文切换；用一个线程走 epoll 监听多个 socket，非阻塞 IO。
   - 易错点：Redis 6 引入的多线程只用在**网络读写**（读 socket / 写 socket），命令执行仍是单线程。别误以为"Redis 6 多线程了所以并发安全"——命令还是串行执行。
3. **高效数据结构**：每种类型都有针对场景优化的底层结构（跳表、压缩列表等），操作复杂度低。

## 五大类型与底层结构

| 类型 | 底层结构 | 关键追问 |
|------|---------|---------|
| String | SDS（简单动态字符串） | 为什么不用 C 字符串？—— O(1) 取长度、二进制安全、防缓冲区溢出 |
| List | quicklist（3.2+）；旧版 ziplist / linkedlist | 数据量小、元素短时用 ziplist，省内存 |
| Hash | ziplist / hashtable | 元素数或单个大小超过阈值才升级 hashtable |
| Set | intset / hashtable | 全是整数时用 intset 省内存 |
| ZSet | ziplist / skiplist + hashtable | 为什么用跳表不用红黑树？—— 范围查询友好、实现简单、内存可调 |

底层实现细节展开见 [Redis 数据结构底层](/java/redis/data-structures)。

## 持久化：RDB vs AOF

两种方案，核心取舍是**性能 vs 可靠性**：

- **RDB**（快照）：某时刻全量数据的二进制文件。体积小、恢复快，但宕机可能丢失最近一次快照之后的数据。
- **AOF**（追加日志）：每条写命令追加到日志。数据全，但体积大、恢复慢。
  - `appendfsync` 三档（面试高频）：
    - `always`：每条命令都 fsync，最可靠但最慢。
    - `everysec`：每秒 fsync 一次（默认），宕机最多丢 1 秒。**生产首选**。
    - `no`：交给 OS，Redis 不主动 fsync，性能最好但丢失量看 OS。
  - 易错点：`everysec` 不是定时器硬触发，而是后台线程每秒检查"上次 fsync 是否超过 1 秒"，超过就再 fsync。

Redis 4.0+ 支持**混合持久化**（RDB 全量 + AOF 增量），兼顾两者。

细节见 [持久化与缓存问题](/java/redis/persistence-cache-problems)。

## 缓存三大问题

| 问题 | 现象 | 解法 |
|------|------|------|
| 穿透 | 查一个**根本不存在**的 key，每次打到 DB | 布隆过滤器（有误判但不漏判）；或缓存空值 |
| 击穿 | **热点 key 过期瞬间**，大量请求打 DB | 互斥锁（只放一个去查 DB 回填）；或热点 key 永不过期 |
| 雪崩 | **大量 Key 同时过期**，全打 DB | 过期时间加随机抖动；多级缓存；熔断 |

易错点：穿透 vs 击穿 vs 雪崩 别混。穿透是 key **根本不存在**（恶意请求或代码 bug），击穿是 key **存在但过期了**，雪崩是**大批量 key 同时过期**。

细节见 [持久化与缓存问题](/java/redis/persistence-cache-problems)。

## 高可用

- **主从复制**：读写分离，主写从读。复制是异步的，存在延迟。
- **哨兵 Sentinel**：主挂了自动选从为主。承担监控 + 通知 + 自动故障转移。
- **分片集群**：数据按 hash slot 分布（共 16384 个 slot），水平扩展，客户端按 slot 路由。

## 过期与淘汰

- **过期策略**：惰性删除（访问时检查）+ 定期删除（后台抽样扫描）。
- **淘汰策略**（`maxmemory-policy`，8 种）：
  - `noeviction`（默认）：内存满了写操作报错。
  - `allkeys-lru` / `volatile-lru`：最近最少使用。
  - `allkeys-lfu` / `volatile-lfu`：最不经常使用（4.0+）。
  - `allkeys-random` / `volatile-random`：随机。
  - 易错点：LRU（最近最少用）vs LFU（最不经常用）。LFU 更适合"偶尔被访问的冷 key 不该污染 LRU"的场景。

## 子页索引

- [Redis 数据结构底层](/java/redis/data-structures)：SDS、跳表、压缩列表、渐进式 rehash 的实现细节
- [持久化与缓存问题](/java/redis/persistence-cache-problems)：RDB/AOF 全流程、缓存三问题真解法
- [Redis 面试题集](/java/redis/questions)：高频题与追问
