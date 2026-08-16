---
title: Java 集合框架
---

# Java 集合框架

> Java 面试 TOP4。本文按问答组织（满足"面试前刷题"的查阅形态），每题给「答 + 面试官追问 + 常见误解」三层——比单背答案多一层深度。覆盖 HashMap、ConcurrentHashMap、ArrayList/LinkedList 四个高频考点。

## 集合体系速览

```
Collection
├── List（有序、可重复）：ArrayList / LinkedList / Vector(淘汰)
├── Set（无序、不重复）：HashSet(基于 HashMap) / LinkedHashSet / TreeSet(红黑树)
└── Queue：ArrayDeque / PriorityQueue(堆)

Map（键值对）
├── HashMap / LinkedHashMap / TreeMap(红黑树)
└── ConcurrentHashMap（线程安全）
```

一句话定位：**List 按位置存取、Set 去重、Queue 排队、Map 按 key 查 value**。下面挑面试最常问的 HashMap / ConcurrentHashMap / ArrayList vs LinkedList 展开。

---

## HashMap

### Q1：HashMap 的底层结构？

**答**：JDK 1.8 起是 **数组 + 链表 + 红黑树**。数组是主体（默认 16 桶），hash 冲突时同桶挂链表；链表长度 ≥8 且数组容量 ≥64 时转红黑树（退回链表阈值 6）。

**面试官追问**：为什么转树的阈值是 8？

**常见误解**：很多人以为 8 是"性能最优的拐点"——错。其实是泊松分布下链表长度到 8 的概率约 0.00000006（极低），是「概率 + 防御」的折中。真正目的是让正常情况下几乎不触发树化（树化开销大），只在极端冲突时才退化。阈值定 8 而不是 4 或 16，是空间（树节点比链表节点大）和最坏情况时间（O(log n) vs O(n)）的权衡。

### Q2：为什么容量必须是 2 的幂？

**答**：为了把取模 `hash % n` 换成位运算 `hash & (n-1)`（更快）。当 n 是 2 的幂时，两者结果等价。

**易错点**：`new HashMap<>(17)` 不会报错——HashMap 内部 `tableSizeFor` 会把 17 扩成 32（找 ≥17 的最近 2 幂）。所以传非 2 幂不会出错，但白做一次扩容计算。想精确控制容量，直接传 2 幂（如 16、32）。

### Q3：负载因子为什么是 0.75？

**答**：空间和时间的折中。负载因子越大（如 1.0），桶越满才扩容，空间省但冲突多查询慢；越小（如 0.5），早扩容，查询快但空间浪费。0.75 是基于「冲突概率与空间利用率」的经验折中——它在泊松分布假设下让冲突保持在合理水平，同时空间利用率 75% 不至于太浪费。

**常见误解**：以为 0.75 是拍脑袋定的——它实际上有数学依据（泊松分布下桶冲突的期望），但具体推导很少考，记住「空间时间折中」即可。

### Q4：扩容机制？

**答**：`size > capacity × loadFactor`（默认 `> 16 × 0.75 = 12`）时扩容，容量翻倍。JDK 1.8 优化：扩容后元素要么在原位置，要么在「原位置 + oldCap」——因为容量 ×2 后，`hash & (newCap-1)` 比 `hash & (oldCap-1)` 只多判一位（那一位为 0 留原位、为 1 移到原位+oldCap）。

**易错点**：JDK 1.7 扩容用**头插法**，多线程并发扩容可能形成环形链表导致 get 死循环（CPU 100%）。1.8 改**尾插法**解决了成环，但 HashMap 仍然**不是线程安全**的（put 仍可能丢数据）。

### Q5：HashMap 线程安全吗？怎么解决？

**答**：不安全。多线程 put 可能丢数据、size 不准；1.7 还有扩容成环死循环。解决：**ConcurrentHashMap（推荐）** / `Collections.synchronizedMap`（包一层 synchronized，性能差）/ `Hashtable`（整表锁，淘汰）。

---

## ConcurrentHashMap

### Q6：1.7 和 1.8 的区别？

**答**：
- **1.7**：`Segment[]` 分段锁（默认 16 段），每段是一个独立的小 HashMap，每段一把锁。put 时只锁对应段，并发度 = 段数（16）。
- **1.8**：去掉 Segment，回归「Node 数组 + 链表/红黑树」。锁粒度细化到**单个桶**（数组一个节点）：桶空用 CAS 插入（无锁）；桶非空用 `synchronized` 锁头节点。并发度 = 桶数，大幅提升。

**面试官追问**：为什么 1.8 弃用分段锁？

**常见误解**：以为分段锁"性能差"——不准确。真正原因是**分段锁粒度仍太粗**（锁一整段，段内多个桶串行）；1.8 锁单个桶，粒度更细，且引入 CAS 让「桶空」路径完全无锁。此外 1.8 和 HashMap 结构统一（数组+链表+树），维护成本低。

### Q7：1.8 的 put 流程？

**答**：
1. hash 找桶下标。
2. 桶空 → CAS 插入（无锁成功就完事）。
3. 桶非空 → `synchronized` 锁住头节点，链表尾插 / 红黑树插入。
4. 检查是否要扩容（扩容时多线程协助迁移，transfer）。

**易错点**：ConcurrentHashMap 的 `size()` 不是精确的——它用 `baseCount + CounterCell[]` 分段累加（类似 LongAdder），高并发下 `size()` 是个近似值。如果业务强依赖精确 size，要自己加锁或换数据结构。

### Q8：ConcurrentHashMap 的 key/value 能为 null 吗？

**答**：**不能**（HashMap 可以）。原因是 `get(key)` 返回 null 时无法区分「key 不存在」还是「value 就是 null」——HashMap 靠 `containsKey` 解决，但 ConcurrentHashMap 在并发场景下 `containsKey` 和 `get` 之间可能被改，二义性问题更严重，所以直接禁 null。

---

## ArrayList vs LinkedList

### Q9：底层和性能区别？

**答**：
- **底层**：ArrayList 是动态数组；LinkedList 是双向链表（同时实现 List 和 Deque）。
- **查找**：ArrayList `get(i)` O(1)（数组下标）；LinkedList O(n)（从头遍历）。
- **插入删除**：ArrayList 中间插删 O(n)（搬移后续元素）；LinkedList 在「已定位的节点」处插删 O(1)（改指针），但定位本身 O(n)。
- **内存**：LinkedList 每个节点额外存 prev/next 两个引用，比 ArrayList 费内存；ArrayList 内存连续，CPU 缓存友好。

### Q10：实际项目选哪个？

**答**：**几乎都选 ArrayList**。理由（不是"基础/进阶"分组，是具体取舍）：

1. **实际场景大多是随机访问**——ArrayList `get(i)` O(1) 完胜 LinkedList O(n)。
2. **LinkedList 的「插入 O(1)」是个陷阱**：它要求「已经定位到那个节点」，但 `list.add(index, e)` 这种调用要先遍历到 index（O(n)），再插（O(1)），整体仍 O(n)，并不比 ArrayList 的搬移快。
3. **CPU 缓存友好性**：ArrayList 数组连续，预取命中率高；LinkedList 节点散落堆里，缓存miss 多——实测即使理论复杂度相同，ArrayList 也快几倍。
4. **真要频繁头尾插删**：用 `ArrayDeque`（数组实现的双端队列），比 LinkedList 快且省内存；LinkedList 唯一比 ArrayDeque 强的「中间插 O(1)」在 List 语义里基本用不到。

**常见误解**：教科书说「频繁增删用 LinkedList」——这是理想化结论（假设定位免费 + 忽略缓存），实际工程里几乎总是 ArrayList。面试答「选 ArrayList，理由 1/2/3」比"看场景"显深度。

---

## 易错点速查表

| 知识点 | 关键值 / 注意 |
|---|---|
| HashMap 默认容量 | 16 |
| 负载因子 | 0.75（空间时间折中） |
| 树化 / 退树阈值 | 8 / 6 |
| 最小树化容量 | 64（容量 <64 时只扩容不树化） |
| HashMap 迭代顺序 | 无序；LinkedHashMap 维护插入/访问序 |
| ArrayList 默认容量 | 10（首次 add 才分配） |
| ArrayList 扩容倍数 | 1.5 倍（`oldCap + oldCap >> 1`） |
| fail-fast | 迭代时 modCount 变抛 `ConcurrentModificationException`；用 `Iterator.remove()` 避免 |
| ConcurrentHashMap key/value | 都不能为 null |

> 把这张表和上面的「常见误解」过一遍，集合的面试高频就覆盖了。后面要深入源码（HashMap 的 hash 扰动、resize 迁移、ConcurrentHashMap 的 CounterCell），等 `java/basics/` 拆出源码篇再展开。
