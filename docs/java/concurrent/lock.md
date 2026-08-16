---
title: 锁深入（synchronized 锁升级 / AQS / 公平非公平）
---

# 锁深入（synchronized 锁升级 / AQS / 公平非公平）

> 配套：[并发总览](./) Q3/Q4 已讲 synchronized vs ReentrantLock 区别 + 锁升级路径。本篇深入底层：**synchronized 对象头怎么记锁状态、AQS 怎么实现 ReentrantLock、公平非公平到底差在哪**。

---

## 思考锚点

多线程同时访问共享数据时，必须有一种机制保证同一时刻只有一个线程能操作——否则两个线程同时修改同一个变量，结果就不可预测了。

Java 提供了 synchronized 和 ReentrantLock 两种锁机制，但它们背后的实现原理差别很大：synchronized 依赖 JVM 的对象头 Mark Word 做锁状态记录，ReentrantLock 依赖 AQS 的双向队列管理等待线程。

本文就是要讲清楚这两种锁底层是怎么工作的，以及它们在不同场景下怎么选。

## Q1：synchronized 锁状态记在哪？对象头 Mark Word

**答**：JVM 给每个对象配一个「对象头」（Object Header），其中 **Mark Word** 记锁状态。64 位 JVM 的 Mark Word 在不同锁状态下复用同一块 bit：

| 锁状态 | Mark Word 关键内容 |
|---|---|
| 无锁 | hashCode、GC 分代年龄 |
| 偏向锁 | 线程 ID、epoch |
| 轻量级锁 | 指向栈中锁记录的指针 |
| 重量级锁 | 指向 Monitor（ObjectMonitor）的指针 |
| GC 标记 | （GC 用） |

锁升级就是 Mark Word 内容的改写：无锁 → 偏向（记线程 ID）→ 轻量级（CAS 自旋，记栈帧锁记录指针）→ 重量级（指向 OS Monitor）。

**易错点**：锁状态**不可降级**（轻量级不会退回偏向）。另外 JDK 15+ 偏向锁默认**禁用**（JEP 374，维护成本 > 收益），新版 JVM 直接从无锁跳轻量级。所以答锁升级要先问 JDK 版本。

> 🤔 停下来想想：偏向锁在 Java 15 被移除了——这说明了什么工程权衡？

## Q2：AQS 是什么？为什么是 ReentrantLock 的核心？

**答**：AQS（AbstractQueuedSynchronizer）是 `java.util.concurrent` 里大多数同步器的基类（ReentrantLock / Semaphore / CountDownLatch / ReentrantReadWriteLock 都基于它）。核心两件事：

1. **`volatile int state`**：同步状态。不同同步器赋予不同含义——ReentrantLock 里 state = 重入次数（0 无锁，>0 持有 + 重入数）；Semaphore 里 state = 剩余许可数；CountDownLatch 里 state = 剩余计数。
2. **CLH 双向队列**：获取不到锁的线程被包装成 Node 入队、park 挂起；前驱释放时 unpark 后继。

**模板方法模式**：AQS 定义了「入队 / 出队 / park / unpark」的骨架（`acquire`/`release`），子类只需实现「**试试能不能拿到**」（`tryAcquire`/`tryRelease`）。

**易错点**：`state` 是 `volatile` 但 AQS 不靠它单独保证原子性——`tryAcquire` 里用 CAS 改 state（`compareAndSetState`）。volatile 保证可见性，CAS 保证原子性，两者配合。

> 🤔 停下来想想：AQS 用 CAS + 队列实现公平锁，为什么非公平锁性能反而更好？

## Q3：ReentrantLock 的 tryAcquire 怎么实现？

**答**（非公平版，NonfairSync）：

```java
final boolean nonfairTryAcquire(int acquires) {
    final Thread current = Thread.currentThread();
    int c = getState();
    if (c == 0) {                                    // 无锁
        if (compareAndSetState(0, acquires)) {       // CAS 抢
            setExclusiveOwnerThread(current);
            return true;
        }
    } else if (current == getExclusiveOwnerThread()) { // 重入
        setState(c + acquires);                       // 不用 CAS（只有持有者能改）
        return true;
    }
    return false;                                     // 抢不到 → AQS 入队
}
```

**两个分支**：state==0 → CAS 抢（成功设持有者）；state>0 但持有者是自己 → 重入（state+1，不需 CAS，因为别人改不了）。

**易错点**：重入分支**不用 CAS**——因为只有持有锁的线程能走到这里（`current == getExclusiveOwnerThread`），没有竞争，直接 setState。新手常见错误是重入也加 CAS，多余。

## Q4：公平和非公平到底差在哪？

**答**：只差一行——`tryAcquire` 开头查不查队列。

- **非公平**（默认）：`tryAcquire` 直接 CAS 抢（上面 Q3 的代码）。即使队列里有线程在等，新来的线程也能"插队"抢到。
- **公平**：`tryAcquire` 先 `hasQueuedPredecessors()`（队列里有没有前驱），有则不抢、乖乖排队。

```java
// FairSync.tryAcquire
if (c == 0) {
    if (!hasQueuedPredecessors() && compareAndSetState(0, acquires)) {
        setExclusiveOwnerThread(current);
        return true;
    }
}
```

**为什么默认非公平**：吞吐量高。公平锁要求严格 FIFO，线程切换开销大；非公平允许新线程直接抢（可能前一个刚释放的线程通过 CAS 又抢到），少了挂起/唤醒的开销。代价是「队列中线程可能长时间拿不到锁」（饥饿），但概率低。

**易错点**：公平锁的「公平」是「**进入顺序**」公平，不保证「执行顺序」绝对 FIFO（CAS 失败的细微窗口）。但实际效果接近 FIFO。

## Q5：AQS 的 Condition 怎么工作？

**答**：Condition 是「**等待队列**」（对比 synchronized 的 wait/notify 只有一个等待队列）。`await()`/`signal()` 流程：

- **`await()`**：当前线程**释放锁**（AQS state 归 0）+ 包装成 Node 进入该 Condition 的**条件队列** + park。
- **`signal()`**：把条件队列的首节点**移到 AQS 主队列**（sync queue），等它被前驱唤醒后重新 `acquire` 锁。

**用在哪**：生产者-消费者（notEmpty / notFull 两个 Condition，比 synchronized 的单一 wait/notify 灵活）、阻塞队列（ArrayBlockingQueue 的实现）。

**易错点**：`await()` 会**释放锁**（不像 `Thread.sleep` 持有锁）——这是「协作」语义（让别的线程能改条件）。忘了这点会死锁（持有锁等条件，条件改变需要别的线程改，但别的线程拿不到锁）。

---

## 易错点速查表

| 知识点 | 关键 |
|---|---|
| Mark Word | 记锁状态；锁升级 = Mark Word 改写；不可降级 |
| 偏向锁 | JDK 15+ 默认禁用，答锁升级先问版本 |
| AQS state | volatile + CAS（不是 volatile 单独保证原子） |
| 重入 | state>0 且持有者是自己 → state+1，**不用 CAS** |
| 公平 vs 非公平 | 只差 hasQueuedPredecessors 一行；默认非公平（吞吐高） |
| Condition await | 释放锁（区别于 sleep 持锁） |
| synchronized vs AQS | synchronized 是 JVM 关键字（Monitor）；AQS 是 API 层（队列同步器） |

---

## 复述自测

读完这篇，试试用自己的话回答三个问题：

1. **一句话总结**：synchronized 和 ReentrantLock 本质区别是什么？（提示：一个是 JVM 层面的，一个是 API 层面的）

2. **讲给初学者听**：如果把锁比作"公共厕所的门锁"，synchronized 的锁升级过程是怎样的？可以用"一个人用→熟人直接进→陌生人排队"之类的类比。

3. **预判追问**：如果你是面试官，读完这篇你会追问什么？（比如 AQS 的同步队列和等待队列是怎么切换的？公平锁和非公平锁的性能差多少？）

> 本篇是 [并发总览](./) Q3/Q4 的源码级深化。后续 `volatile-jmm` 子页讲 happens-before + 内存屏障、`threadlocal` 讲泄漏 + InheritableThreadLocal / TransmittableThreadLocal。
