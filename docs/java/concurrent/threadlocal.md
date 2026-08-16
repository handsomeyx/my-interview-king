---
title: ThreadLocal（泄漏 / InheritableThreadLocal / TransmittableThreadLocal）
---

# ThreadLocal（泄漏 / InheritableThreadLocal / TransmittableThreadLocal）

> 配套：[并发总览](./) Q7 已讲 ThreadLocal 原理 + 内存泄漏。本篇深入：**泄漏的精确根因、父子线程传值为什么失效、线程池下用 TransmittableThreadLocal**。

---

## 思考锚点

在多线程应用中，我们经常需要在同一个线程的不同方法间传递数据——比如用户 ID、事务 ID、trace ID 等。如果每个方法都加一个参数传递，代码会变得非常冗长。

ThreadLocal 就是解决这个问题的：它像一个「线程本地的 Map」，每个线程有自己独立的一份数据，互不干扰。但用不好会导致内存泄漏，而且在线程池场景下还会有数据错乱的风险。

本文要讲清楚 ThreadLocal 的底层结构、泄漏的精确根因，以及线程池下正确传值的方案。

## Q1：ThreadLocalMap 的精确结构？

**答**：每个 Thread 对象有个字段 `ThreadLocal.ThreadLocalMap threadLocals`。ThreadLocalMap 是 ThreadLocal 的静态内部类，类似 Map 但**不是 HashMap**：

- **key**：ThreadLocal 的**弱引用**（`WeakReference<ThreadLocal>`）。
- **value**：用户的值，**强引用**（Object）。
- **结构**：开放寻址的数组（不是链表法），hash 冲突线性探测。

**为什么 key 弱引用**：ThreadLocal 实例本身（业务里的 `static final ThreadLocal<X> TL = ...`）如果被回收（比如不是 static、方法栈弹出），key 不应该阻止 GC。弱引用让 key 可被回收。

**易错点**：ThreadLocalMap 的 key 弱引用是**设计上为了防「ThreadLocal 实例泄漏」**，但它没防「value 泄漏」——这正是 Q2 的根因。

## Q2：内存泄漏的精确根因

**答**：泄漏链路：
1. ThreadLocal 实例被回收（弱引用，GC 后 key = null）。
2. 但 value 是强引用，且 ThreadLocalMap 还在 → value 引用链：`Thread → ThreadLocalMap → Entry → value`。
3. 如果线程长期不死（**线程池的核心线程**），这个 null-key 的 value **永远回收不掉** → 泄漏。

**ThreadLocal 的自救**：`get()`/`set()`/`remove()` 时会顺带清理 key==null 的 Entry（expungeStaleEntry）。但这是「机会性清理」，如果线程跑完不再调这些方法，value 就漏了。

**根治**：用完 `remove()`。尤其在**线程池**场景，线程复用，上一次任务的 ThreadLocal 残留会被下一次任务看到（数据错乱）+ 泄漏。

**易错点**：自救（机会性清理）**不能依赖**——它只在 get/set/remove 时触发。线程池的线程跑完一个任务不一定会调这些，value 漏。`finally { TL.remove(); }` 是唯一可靠做法。

## Q3：InheritableThreadLocal——父子传值

**答**：普通 ThreadLocal **父子线程不共享**（子线程新建自己的 ThreadLocalMap）。`InheritableThreadLocal` 解决：子线程创建时，会**复制父线程的 InheritableThreadLocal 值**。

原理：Thread 创建时（`new Thread()`），如果父线程有 InheritableThreadLocal 的值，子线程的 `inheritableThreadLocals` 会复制一份（`Thread.parent.inheritableThreadLocals`）。

**致命限制**：只在**`new Thread()` 时复制一次**。**线程池场景失效**——线程池的线程是预先创建/复用的，提交任务时不重新 `new Thread()`，所以父线程（提交任务的主线程）的 InheritableThreadLocal 值**传不进**线程池的工作线程。

**易错点**：「InheritableThreadLocal 解决线程池传值」——**错**。它只解决 `new Thread()` 的父子传值。线程池要用 Q4 的 TransmittableThreadLocal。

## Q4：TransmittableThreadLocal（TTL）——线程池下正确传值

**答**：阿里开源 [TransmittableThreadLocal](https://github.com/alibaba/transmittable) 解决「线程池 + ThreadLocal 传值」。原理：

1. 提交任务时，**装饰 Runnable**：抓取当前线程的所有 TTL 值，快照。
2. 任务执行前，把快照**set 到工作线程**的 TTL。
3. 任务执行后，**恢复工作线程**原来的 TTL 值（避免污染下个任务）。

**使用**：用 `TtlRunnable.get(runnable)` 包装任务，或用 `TtlExecutors.getTtlExecutorService(executor)` 包装线程池。

```java
// 阿里 TTL 典型用法
TransmittableThreadLocal<String> context = new TransmittableThreadLocal<>();
context.set("userId-123");

ExecutorService pool = TtlExecutors.getTtlExecutorService(Executors.newFixedThreadPool(4));
pool.submit(() -> {
    System.out.println(context.get());   // 能拿到 "userId-123"（普通 ThreadLocal / InheritableThreadLocal 拿不到）
});
```

**典型场景**：链路追踪（traceId 跨线程池传递）、日志 MDC、用户上下文（userId/tenantId 在异步任务里取）。

**易错点**：TTL 不是 JDK 自带，是阿里的库（需引入 `com.alibaba:transmittable-thread-local`）。Spring Cloud Sleuth 的 traceId 传播底层就是类似的 TTL 机制（或 agent 字节码增强）。

---

## 易错点速查表

| 知识点 | 关键 |
|---|---|
| ThreadLocalMap | key 弱引用（防 TL 实例泄漏）、value 强引用（泄漏根源） |
| 泄漏根因 | 线程长期存活（线程池）+ null-key 的 value 强引用 |
| 自救 | get/set/remove 机会性清理，**不能依赖** |
| remove | finally 里 remove 是唯一可靠防泄漏 |
| InheritableThreadLocal | 只在 new Thread 时复制；**线程池失效** |
| TransmittableThreadLocal | 阿里 TTL，线程池下正确传值（装饰 Runnable） |
| 场景 | 链路追踪 traceId、MDC、用户上下文 |

---

## 复述自测

读完这篇，试试用自己的话回答三个问题：

1. **一句话总结**：ThreadLocal 内存泄漏的根因是什么？（提示：从「弱引用 key + 强引用 value + 线程长期存活」三个要素思考）

2. **讲给初学者听**：怎么用「每个人有自己的储物柜」来类比 ThreadLocal？用了之后为什么「离开时必须把东西取走（remove）」？

3. **预判追问**：如果你是面试官，读完这篇你会追问什么？（比如 InheritableThreadLocal 为什么在线程池下失效？TTL 的工作原理是什么？）

> 本篇是 [并发总览](./) Q7 的深化，concurrent 子页到此（thread-pool / lock / volatile-jmm / threadlocal）写完。这四篇加上总览，覆盖了 Java 并发面试的核心——从「面试八股」到「源码 + 实战」逐层深入。
