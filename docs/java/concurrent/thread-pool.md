---
title: 线程池实战（调参 / 监控 / 异常）
---

# 线程池实战（调参 / 监控 / 异常）

> 配套：[并发总览](./) 的 Q5/Q6 已讲 7 参数 + 执行流程 + 拒绝策略。本篇深入实战痛点：**大小怎么定、为什么禁用 Executors、异常怎么处理、怎么监控、怎么优雅关闭**。

---

## 思考锚点

Java 中创建一个线程的开销并不小——每次 new Thread() 都需要分配栈内存、创建内核线程、调度注册，线程销毁后这些资源才能回收。如果每个请求都创建新线程，高并发下系统资源会被快速耗尽。

线程池的核心思想是「复用」——提前创建一批线程放在池里，任务来了直接分配一个空闲线程执行，执行完线程不销毁，继续等下一个任务。但问题来了：池子该设多大？线程太多浪费资源，太少处理不过来。

本文就是要讲清楚线程池的核心参数、怎么定大小、怎么监控，以及生产中容易踩的坑。

## Q1：线程池大小怎么定？

**答**：不是拍脑袋，有公式（Brian Goetz）：

- **CPU 密集型**（计算为主，无 IO/锁等待）：`线程数 = CPU 核心数 + 1`。多出的 1 是为了在某个线程偶尔 page fault 等时不让 CPU 空闲。多了反而增加上下文切换开销。
- **IO 密集型**（网络/磁盘/数据库）：`线程数 = CPU 核心数 × (1 + 平均等待时间 / 平均计算时间)`。等待越长，线程越多（让 CPU 在等 IO 时切换跑别的线程）。简化版经验值 `2 × CPU 核心数`。
- **混合型**：拆成两个线程池（CPU 密集一个、IO 密集一个），各按公式定。

**易错点**：「CPU 核心数」用 `Runtime.getRuntime().availableProcessors()`，**不是写死**。容器/云环境下这个值反映 CPU 配额（Docker `--cpus`），不同环境不同。

**追问**：公式算完还要不要调？→ 要。公式是起点，实际要压测看 CPU 利用率 + 排队延迟 + GC 频率。线程太多会让 GC 压力大（每个线程栈占内存 + 对象多）。

## Q2：为什么阿里规约禁用 Executors？

**答**：`Executors` 工厂方法的隐患都在「无界」：

| 方法 | 隐患 |
|---|---|
| `newFixedThreadPool(n)` / `newSingleThreadExecutor()` | 队列用 `LinkedBlockingQueue`（默认 `Integer.MAX_VALUE` 无界）→ 任务堆积 OOM（任务对象撑爆堆） |
| `newCachedThreadPool()` | 最大线程数 `Integer.MAX_VALUE` → 突发请求创建海量线程 OOM（每个线程栈 ~1MB） |

**正确做法**：手 `new ThreadPoolExecutor(...)`，**明确** core/max/队列容量/拒绝策略 + 有界队列。

```java
new ThreadPoolExecutor(
    core, max, 60, TimeUnit.SECONDS,
    new ArrayBlockingQueue<>(1000),          // 有界队列
    new ThreadFactoryBuilder().setNameFormat("biz-%d").build(),  // 命名线程
    new ThreadPoolExecutor.CallerRunsPolicy() // 拒绝策略明确
);
```

**易错点**：「禁用 Executors」**不是**禁用线程池，是禁用「无界」的工厂方法。自己 `new ThreadPoolExecutor` 完全允许且是推荐。

## Q3：线程池里的任务抛异常会怎样？

**答**：分两种提交方式：

- **`execute(Runnable)`**：异常直接抛出 → 线程终止（`UncaughtExceptionHandler` 处理，默认打印栈到 stderr）。**线程池会新建一个线程顶上**，但你不知道任务失败了。
- **`submit(Runnable/Callable)`**：异常被**吞进 Future**，调用 `future.get()` 才抛 `ExecutionException`。不调 get 就永远不知道失败。

**易错点**：很多人用 `submit` 不调 `get`，任务静默失败，排查时一脸懵。两种解决：
1. 提交后一定要处理 Future（get + try/catch）。
2. 重写 `afterExecute` 统一记录异常；或用 `FutureTask` 包装 + try/finally。

**生产实践**：用 `submit` 时，建议封装一层，把 Future 的异常在完成回调里强制 log，避免静默。

## Q4：线程池怎么监控？

**答**：`ThreadPoolExecutor` 自带一堆 getter，重点监控：

| 指标 | 方法 | 含义 / 告警 |
|---|---|---|
| 活跃线程数 | `getActiveCount()` | 接近 max 说明在排队 |
| 队列积压 | `getQueue().size()` | 接近队列容量说明要扩容/降流 |
| 已完成任务 | `getCompletedTaskCount()` | 吞吐量参考 |
| 当前线程数 | `getPoolSize()` | 接近 max 说明忙 |
| 拒绝次数 | 自己在 RejectedExecutionHandler 里计数 | 持续增长说明过载 |

**易错点**：这些 `getXxx` 不是为精确统计设计的（并发下瞬时值），看**趋势**而非单点。接 Prometheus/Micrometer 做时序监控更靠谱。

## Q5：shutdown 和 shutdownNow 区别？

**答**：
- **`shutdown()`**：不再接新任务，但**已提交的任务会跑完**。温和。
- **`shutdownNow()`**：不再接新任务 + **中断正在跑的任务**（`interrupt`），返回还没开始的任务列表。粗暴。

**优雅关闭**：先 `shutdown` + `awaitTermination(超时)`，超时再 `shutdownNow` 强制。

```java
pool.shutdown();
if (!pool.awaitTermination(60, TimeUnit.SECONDS)) {
    pool.shutdownNow();
}
```

**易错点**：`shutdownNow` 的 `interrupt` 只是「设中断标志」，**任务里要主动检查 `Thread.currentThread().isInterrupted()`** 或响应 `InterruptedException` 才会真的停。任务里死循环不检查中断，`shutdownNow` 也停不下来。

## Q6：Spring @Async / Tomcat 线程池注意什么？

**答**：
- **Spring `@Async`**：默认用 `SimpleAsyncTaskExecutor`——**每次新建线程，不复用**（不是真正的线程池）。生产必须自定义 `TaskExecutor`（`@Bean` 配 ThreadPoolTaskExecutor），否则高并发下线程爆炸。
- **Tomcat**：自带线程池（`maxThreads` 默认 200，`minSpareThreads` 默认 10，`acceptCount` 默认 100）。调参看 QPS 和请求耗时——请求慢（DB 慢）时 maxThreads 要调大；纯计算时调大没用（CPU 满了）。

**易错点**：Spring `@Async` 默认非线程池是个**经典坑**——很多人以为「@Async = 异步线程池」，实际默认每次 new 线程。务必自定义。

---

## 易错点速查表

| 知识点 | 关键 |
|---|---|
| 大小公式 | CPU 密集 N+1；IO 密集 N×(1+等待/计算)；用 availableProcessors 不写死 |
| Executors 禁用 | 因为无界（队列/线程），不是禁线程池；手 new + 有界队列 |
| submit 吞异常 | 不调 get 不知道失败；封装回调强制 log |
| 监控看趋势 | getXxx 是瞬时值，接 Prometheus 看时序 |
| shutdownNow | interrupt 只是设标志，任务要主动检查才停 |
| @Async 默认 | SimpleAsyncTaskExecutor 每次 new 线程，必须自定义 |
| Tomcat 默认 | maxThreads 200，慢请求场景要调大 |

---

## 复述自测

读完这篇，试试用自己的话回答三个问题：

1. **一句话总结**：线程池的核心设计思想是什么？（提示：从「资源复用」的角度思考）

2. **讲给初学者听**：如果把线程池比作「公司食堂」，怎么解释「核心线程数 + 最大线程数 + 队列」的关系？可以用「正式员工 + 临时工 + 排队等位」之类的类比。

3. **预判追问**：如果你是面试官，读完这篇你会追问什么？（比如 CPU 密集型和 IO 密集型的线程数公式为什么不同？submit 的异常为什么会被吞？）

> 本篇是 [并发总览](./) Q5/Q6 的实战深化。后续 `lock` 子页讲 synchronized 锁升级 + AQS 源码、`volatile-jmm` 讲 happens-before + 内存屏障。
