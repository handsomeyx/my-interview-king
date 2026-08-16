---
title: Java 并发
---

# Java 并发

> Java 面试 TOP1。并发题考察的核心就三件事：**可见性/有序性（JMM、volatile）、互斥（锁）、调度（线程池、工具）**。本文按问答组织，每题给「答 + 面试官追问 + 易错点」。后续会拆 thread-pool、lock、volatile-jmm、threadlocal 子页深入。

## 体系速览

```
并发要解决的问题
├── 可见性 / 有序性 → JMM、volatile、synchronized
├── 原子性 / 互斥   → synchronized、ReentrantLock、CAS
└── 协作 / 调度     → 线程池、wait/notify、LockSupport、CountDownLatch/CyclicBarrier/Semaphore

底层支撑
├── CAS（Compare-And-Swap）→ AtomicXxx 的基础
├── AQS（AbstractQueuedSynchronizer）→ ReentrantLock/Semaphore/CountDownLatch 的基类
└── happens-before → 可见性保证的形式化规则
```

---

## Q1：JMM（Java 内存模型）是什么？

**答**：JMM 规定每个线程有自己的工作内存（CPU 缓存/寄存器的抽象），共享变量在主内存；线程不直接读写主存，而是工作内存 ↔ 主存交互。这导致两个问题：**可见性**（一个线程改了，另一个看不到）和**有序性**（编译器/CPU 重排序）。

**面试官追问**：happens-before 是什么？

**易错点**：JMM **不是**「JVM 内存结构」（堆/栈/方法区）——那是运行时数据区。JMM 是「多线程下内存访问的可见性/有序性规则」。两个概念名字像但完全不同，面试经常混问。

## Q2：volatile 的作用？

**答**：两个保证——**可见性**（写立即刷主存、读强制从主存读）+ **有序性**（禁止重排序，靠内存屏障）。**不保证原子性**：`volatile int i; i++` 仍不安全（i++ 是读-改-写三步，非原子）。

**易错点**：要原子用 `AtomicInteger`（基于 CAS）或 `synchronized`。volatile 单独保不了复合操作。

## Q3：synchronized 和 ReentrantLock 区别？

**答**：
| 维度 | synchronized | ReentrantLock |
|---|---|---|
| 性质 | JVM 关键字（monitorenter/monitorexit） | API 类（AQS 实现） |
| 公平性 | 非公平，不可配 | 可配公平/非公平 |
| 可中断 | 抢锁时被 interrupt 不响应 | `lockInterruptibly()` 可响应 |
| 试锁 | 无 | `tryLock()` 非阻塞试抢 |
| 多条件 | 一个 wait/notify | `Condition` 可多个等待队列 |
| 自动释放 | 是（出块/异常自动） | 否（必须 finally unlock，漏了死锁） |

**选哪个**：简单互斥用 synchronized（自动释放、JVM 偏向锁/轻量级锁优化后性能不差）；需要「可中断/试锁/多条件/公平」用 ReentrantLock。

**易错点**：ReentrantLock 必须 `try { lock(); ... } finally { unlock(); }`。漏了 finally，异常时锁不释放 → 死锁。

## Q4：synchronized 的锁升级？

**答**：JDK 1.6+ 优化，synchronized 不再总是重量级锁，升级路径：
1. **无锁** → **偏向锁**（第一个线程进来，对象头记线程 ID，下次该线程直接进，无 CAS）。
2. 偏向锁 → **轻量级锁**（出现竞争，CAS 自旋）。
3. 轻量级锁 → **重量级锁**（自旋失败/竞争激烈，OS 互斥量，线程挂起）。

**易错点**：升级**不可降级**（重量级不会退回轻量级）。另外偏向锁在 JDK 15+ 默认禁用（维护成本 > 收益），所以新版 JVM 你可能看不到偏向锁。

## Q5：线程池 7 个核心参数？

**答**：`ThreadPoolExecutor(int corePoolSize, int maximumPoolSize, long keepAliveTime, TimeUnit unit, BlockingQueue<Runnable> workQueue, ThreadFactory threadFactory, RejectedExecutionHandler handler)`

**执行流程**：任务来了 → 核心线程没满就开核心线程 → 满了进队列 → 队列满了开非核心线程（到 max）→ 还满执行拒绝策略。

**易错点**：顺序是**核心 → 队列 → 非核心**，**不是「核心 → 非核心 → 队列」**。所以用 `LinkedBlockingQueue`（默认 Integer.MAX_VALUE 无界）时，队列永远不满，max 永远不生效——线程数停在 core。这正是 `Executors.newFixedThreadPool` 的隐患（无界队列 OOM）。

## Q6：线程池拒绝策略？

**答**：4 种内置：
- `AbortPolicy`（默认）：抛 `RejectedExecutionException`。
- `CallerRunsPolicy`：谁提交谁执行（背压降速，生产常用）。
- `DiscardPolicy`：默默丢弃（慎用，问题难查）。
- `DiscardOldestPolicy`：丢队列最老的，再 submit。

**易错点**：阿里规约禁止用 `Executors.newXxx`（队列/线程数无界 OOM），要求手 `new ThreadPoolExecutor` + 明确参数 + 有界队列 + 命名线程（便于排查）。

## Q7：ThreadLocal 原理和内存泄漏？

**答**：每个 Thread 持有 `ThreadLocalMap`，key 是 ThreadLocal 的**弱引用**、value 是**强引用**。`get()` 拿当前线程的 map，按 `this`（ThreadLocal 实例）查 value。

**内存泄漏**：ThreadLocal 实例被回收后 key 变 null，但 value 仍强引用。如果线程长期活着（线程池），这些 null-key 的 value 永远回收不掉 → 泄漏。

**解决**：用完 `remove()`，尤其在线程池场景。

**易错点**：ThreadLocal **不是**「让对象线程安全」，是「让每个线程有自己的副本」。它解决的是「线程间隔离」，不是「共享同步」。

---

## Q8：CAS 和 ABA 问题？

**答**：CAS（Compare-And-Swap）三个操作数：内存值 V、预期旧值 A、新值 B；当 V==A 时把 V 改成 B，返回 true，否则 false（重试）。硬件级原子指令（cmpxchg）。是 `AtomicXxx`、`AQS`、`ConcurrentHashMap` 桶空插入的基础。

**ABA 问题**：值从 A→B→A，CAS 以为没变过，实际变过两次。对「只关心最终值」的场景无害，对「关心是否变过」的场景（如栈操作）有 bug。

**解决**：`AtomicStampedReference`（加版本号，CAS 比对值+版本）。

---

## 易错点速查表

| 知识点 | 关键 |
|---|---|
| volatile | 不保证原子性（i++ 仍不安全） |
| ReentrantLock | 必须 finally unlock，否则异常时死锁 |
| synchronized 锁升级 | 不可降级；JDK 15+ 偏向锁默认禁用 |
| 线程池执行顺序 | 核心 → 队列 → 非核心（队列无界则 max 不生效） |
| 线程池创建 | 禁用 Executors，手 new + 有界队列（防 OOM） |
| ThreadLocal | 用完 remove（线程池场景防泄漏） |
| CAS ABA | 用 AtomicStampedReference（版本号） |
| happens-before | 不等于「时间上前发生」，是「可见性保证」的规则 |

> 并发是 Java 面试的重点和难点。本文是总览，下面 4 个子页按场景深入实战：

## 子页深入

- [线程池实战](./thread-pool)——大小公式 / Executors 为什么禁用 / 异常处理 / 监控 / 优雅关闭
- [锁深入](./lock)——synchronized 对象头 Mark Word / AQS 源码 / 公平 vs 非公平 / Condition
- [volatile 与 JMM](./volatile-jmm)——happens-before 8 条 / 内存屏障 / DCL 单例
- [ThreadLocal](./threadlocal)——泄漏根因 / InheritableThreadLocal / TransmittableThreadLocal
