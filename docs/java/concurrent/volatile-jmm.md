---
title: volatile 与 JMM（happens-before / 内存屏障 / DCL）
---

# volatile 与 JMM（happens-before / 内存屏障 / DCL）

> 配套：[并发总览](./) Q1/Q2 已讲 JMM 三大问题 + volatile 两个保证。本篇深入：**happens-before 8 条规则、内存屏障 4 种、volatile 的 i++ 为什么不安全、双重检查锁单例**。

---

## 思考锚点

现代 CPU 都是多核的，每个核心有自己的缓存。当一个核心修改了变量值，其他核心不会自动看到——因为每个核心的缓存里存的还是旧值。

同时，编译器和 CPU 为了性能会调整指令执行顺序，只要单线程结果不变就行。但在多线程环境下，这种重排可能导致一个线程还没初始化完对象，另一个线程就开始使用它了。

volatile 就是 JVM 层面给程序员的一个"开关"，告诉编译器和 CPU："这个变量不要缓存、不要重排"。

## Q1：happens-before 是什么？8 条规则

**答**：happens-before 是 JMM 的核心规则——如果 A happens-before B，那么 A 的操作结果对 B 可见（且 A 的执行顺序在前，除非有重排序但不改变结果）。8 条：

1. **程序顺序规则**：同一线程内，前面的操作 happens-before 后面的（as-if-serial）。
2. **监视器锁规则**：unlock happens-before 后续对同一把锁的 lock。
3. **volatile 规则**：volatile 写 happens-before 后续读。
4. **线程启动规则**：`Thread.start()` happens-before 该线程的所有操作。
5. **线程终止规则**：线程所有操作 happens-before `Thread.join()` 返回。
6. **线程中断规则**：`Thread.interrupt()` happens-before 被中断线程检测到中断。
7. **对象终结规则**：构造函数执行完 happens-before `finalize()`。
8. **传递性**：A happens-before B，B happens-before C → A happens-before C。

**易错点**：happens-before **不是**「时间上先发生」。它的本质是「**可见性 + 有序性保证**」——即使指令重排序，结果上要等价于按 happens-before 顺序执行。两者经常混淆。

## Q2：什么是指令重排序？哪些会重排？

**答**：编译器（JIT）、CPU、内存 Cache 都会为性能重排指令顺序。分三类：
- **编译器重排序**：JIT 优化代码，调整指令顺序（不改变单线程语义）。
- **CPU 重排序**：指令级并行（流水线、乱序执行）。
- **内存重排序**：CPU 写 Store Buffer + Cache 不一致导致「写顺序」被其他核心看到的不一致。

**as-if-serial**：重排序的前提是「不改变单线程执行结果」。单线程下重排序无害；多线程下重排序会破坏可见性/有序性——这就是为什么要 volatile/synchronized。

**易错点**：「单线程无害」是关键。很多人看到「重排序会导致 bug」就以为哪里都会重排——不，单线程下你永远观察不到重排序（as-if-serial 保证）。只有多线程共享变量才暴露。

> 🤔 停下来想想：单线程下重排序永远观察不到——这是为什么？

## Q3：内存屏障（Memory Barrier）4 种

**答**：内存屏障是 CPU/JVM 指令，禁止屏障前后的指令越过屏障重排。4 种：

| 屏障 | 作用 |
|---|---|
| LoadLoad | Load1; LoadLoad; Load2 → Load1 必须在 Load2 前完成 |
| StoreStore | Store1; StoreStore; Store2 → Store1 必须在 Store2 前刷主存 |
| LoadStore | Load1; LoadStore; Store2 → Load1 必须在 Store2 前 |
| StoreLoad | Store1; StoreLoad; Load2 → Store1 刷主存，Load2 才能读。**开销最大**，全能屏障 |

**volatile 怎么用屏障**：
- volatile **写**前插 StoreStore（保证前面普通写先刷出）；写后插 StoreLoad（保证写对后续读可见）。
- volatile **读**后插 LoadLoad（保证后续普通读不重排到 volatile 读前）；读后插 LoadStore。

**易错点**：StoreLoad 是**最贵**的屏障（强制 CPU 把 Store Buffer 刷出 + 清空流水线）。volatile 写的开销主要就在 StoreLoad，所以 volatile 写比读慢。

> 🤔 停下来想想：为什么 volatile 写比读慢这么多？

## Q4：volatile 的 i++ 为什么不安全？

**答**：`i++` 是三步：**读 i → +1 → 写 i**。volatile 保证「读读到最新值」+「写立即可见」，但**不保证这三步的原子性**。两个线程同时读 i=0 → 都 +1 → 都写 1 → 丢一次。

**解决**：
- `AtomicInteger`（基于 CAS，read-modify-write 原子）。
- `synchronized`（互斥）。
- `LongAdder`（高并发累加，比 AtomicXxx 快——分段累加 reduce 竞争）。

**易错点**：volatile 适合「一个线程写、多个线程读」的场景（如状态标志位 `volatile boolean stopped`）。**不适合复合操作**（i++、check-then-act）。判断标准：操作是单步读写 → volatile 够；多步 → CAS 或锁。

## Q5：双重检查锁（DCL）单例

**答**：懒加载 + 线程安全 + 性能的经典写法：

```java
public class Singleton {
    private static volatile Singleton instance;   // ← volatile 必须！
    private Singleton() {}
    public static Singleton getInstance() {
        if (instance == null) {                    // 第一次检查（无锁，快）
            synchronized (Singleton.class) {
                if (instance == null) {             // 第二次检查（锁内，防重复）
                    instance = new Singleton();     // 非原子：分配内存 → 初始化 → 赋值
                }
            }
        }
        return instance;
    }
}
```

**为什么 instance 必须 volatile**：`instance = new Singleton()` 不是原子操作，分三步：
1. 分配内存
2. 初始化对象
3. 把内存地址赋给 instance

如果 2 和 3 重排序（编译器/CPU 可能），线程 A 执行到 3（instance 非空但还没初始化完），线程 B 第一次检查看到 instance 非空 → 直接用 → 用到**半初始化的对象**（字段是默认值），bug。

**volatile 的作用**：禁止 2、3 重排序（StoreStore 屏障），保证 instance 赋值时对象已初始化完。

> 🤔 停下来想想：如果没有 volatile，2 和 3 重排序后会发生什么？

**易错点**：DCL 不加 volatile 在 JDK 1.5 前是有 bug 的（JMM 不完善）；1.5+ JMM 修复 volatile 语义后 DCL 才可靠。现在写 DCL **volatile 必须加**。不过更推荐「静态内部类」或「枚举」单例（无锁、JVM 保证、代码简单）。

---

## 易错点速查表

| 知识点 | 关键 |
|---|---|
| happens-before | 是「可见性 + 有序性保证」，不是「时间先后」 |
| 重排序 | 单线程观察不到（as-if-serial）；多线程共享才暴露 |
| 内存屏障 | StoreLoad 最贵；volatile 写主要开销在这 |
| volatile i++ | 不安全（read-modify-write 非原子）；用 AtomicXxx |
| volatile 场景 | 单写多读（标志位）；不适合复合操作 |
| DCL volatile | 禁止「初始化」和「赋值」重排序，防半初始化对象 |
| 单例更优解 | 静态内部类（JVM 类加载保证）或枚举 |

---

## 复述自测

读完这篇，试试用自己的话回答三个问题：

1. **一句话总结**：volatile 到底是做什么的？（提示：别只说"可见性和有序性"，想想它解决的物理事实是什么）

2. **讲给初学者听**：如果让你给一个大一新生解释"为什么需要 volatile"，你会怎么说？可以用"多人协作时信息不同步"、"传话游戏传错顺序"之类的类比。

3. **预判追问**：如果你是面试官，看完这篇你会追问候选人什么？（比如 volatile 和 synchronized 有什么区别？为什么 volatile 的 i++ 不安全？）

> 本篇是 [并发总览](./) Q1/Q2 的底层深化。后续 `threadlocal` 子页讲泄漏原理 + InheritableThreadLocal / TransmittableThreadLocal（线程池下传值）。
