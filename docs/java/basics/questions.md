---
title: Java 基础八股题集
---

# Java 基础八股题集

> 面试前刷题查阅。每题「答 + 易错」简洁版；深入版见 [Java 基础长文](./)。

---

## Q1：面向对象三大特性？

**答**：封装（隐藏实现细节，暴露接口）、继承（子类复用父类）、多态（同一调用不同行为）。

**易错**：多态「编译看左、运行看右」——`Animal a = new Dog(); a.eat()` 编译期看 Animal 有没有 eat，运行期执行 Dog 的 eat（重写了）。**成员变量不多态**（编译运行都看左），这是常考陷阱。

## Q2：重载 vs 重写？

**答**：重载（Overload）——同类同名、参数列表不同（返回类型无关）。重写（Override）——子类同名同参重写父类方法。

**易错**：重载是「**同类、编译期**」静态分派；重写是「**父子类、运行期**」动态分派。重写要求：方法签名相同 + 访问权限不缩小 + 抛出异常不扩大 + 返回类型协变兼容（JDK 5+）。

## Q3：接口 vs 抽象类？

**答**：
- 抽象类：单继承、有构造器、有成员变量、可含具体方法 + 抽象方法。
- 接口：多实现、无构造器、变量默认 `public static final`、方法默认 `public abstract`（JDK 8+ 可 `default`/`static`，9+ 可 `private`）。

**易错**：JDK 8 的 `default` 方法让接口看起来像抽象类，但本质区别仍在：**单继承 vs 多实现**、接口**无成员变量**（都是常量）、接口**无构造器**。

## Q4：== vs equals？

**答**：`==` 比较引用地址（对象）或值（基本类型）；`equals` 默认也是比地址（Object 里就是 ==），但 String/Integer 等重写了 equals 比内容。

**易错**：`Integer a = 127, b = 127; a == b` 是 **true**（缓存）；`Integer a = 128, b = 128; a == b` 是 **false**（超缓存）。包装类比较一律用 equals。

## Q5：hashCode 与 equals 契约？

**答**：equals 相等 → hashCode 必相等；hashCode 相等 → equals 不一定相等。HashMap 先比 hashCode（快，分桶），再 equals（准，定键）。

**易错**：重写 equals **必须**重写 hashCode——否则两个「逻辑相等」的对象 hashCode 不同，HashMap 存成两个 key，找不回。这是最经典的契约违反 bug。

## Q6：String / StringBuilder / StringBuffer？

**答**：String 不可变（每次改新建对象）；StringBuilder 可变、**非线程安全**（快）；StringBuffer 可变、**线程安全**（synchronized，慢）。

**易错**：单线程拼接用 StringBuilder（别用 String + 循环，每次 new）；多线程共享才用 StringBuffer（实际极少）。编译器优化 `"a" + "b"` 为 StringBuilder，但**循环内**拼接不优化，必须手写 StringBuilder。

## Q7：String 为什么不可变？

**答**：`final class`（不能继承）+ `private final char[] value`（JDK 9+ `byte[]`，不能改引用 + 不能改内容）。好处：字符串常量池（共享）、线程安全、hashCode 缓存、安全（防类加载器 / JNDI 注入点被篡改）。

**易错**：「不可变」是 value 数组内容不能改，**不是 value 引用不能改**。`s = s + "x"` 不是改 s，是新建对象把 s 引用指向新对象。

## Q8：异常体系？

**答**：`Throwable` → `Error`（不该 catch，如 OOM/StackOverflow）+ `Exception` → `RuntimeException`（unchecked，编译不查）+ 其他 Exception（checked，必须 catch/throws）。

**易错**：NullPointerException / ClassCastException 是 RuntimeException（unchecked）；IOException / SQLException 是 checked（必须处理）。checked 强制处理是双刃——业务异常常自定义 RuntimeException（Spring 的 DataAccessException 就是）。

## Q9：try-with-resources？

**答**：JDK 7+，自动关闭实现 `AutoCloseable` 的资源（编译成 try-finally）。资源在 `try()` 里声明，按声明**逆序**关闭。

**易错**：资源必须实现 AutoCloseable（或 Closeable）。多个资源 `try (A a=...; B b=...) {}` 关闭顺序 B 先 A 后（逆序，防依赖）。比手写 finally 简洁且不漏关——手写 finally 漏关是常见 bug。

## Q10：泛型类型擦除？

**答**：JDK 泛型是「**编译期**」检查，编译后擦除（`List<String>` 和 `List<Integer>` 运行时都是 List）。靠桥接方法保证多态。

**易错**：因为擦除，运行时拿不到泛型类型（`list.getClass() == List.class`，无 String 信息）。要运行时泛型用 `TypeToken`（Gson）或 `ParameterizedType`（反射）。**基本类型不能做泛型参数**（`List<int>` 不行，要 Integer）。

## Q11：反射？

**答**：运行时获取类信息 + 操作对象（Field / Method / Constructor）。获取 Class 三种：`Xxx.class` / `obj.getClass()` / `Class.forName("全限定名")`。

**易错**：反射 `setAccessible(true)` 跳过访问检查（能调 private）。JDK 9+ 模块系统限制反射（要 `--add-opens`）。反射比直接调用慢（JIT 优化后差距缩小，但仍有开销）。

## Q12：JDK 动态代理 vs CGLIB？

**答**：JDK 动态代理——基于**接口**（`Proxy.newProxyInstance`），目标类必须实现接口。CGLIB——基于**继承**（生成子类），不要求接口，但不能代理 final 类/方法。

**易错**：Spring AOP 默认：有接口用 JDK 代理，没接口用 CGLIB（`spring.aop.proxy-target-class=true` 强制 CGLIB）。CGLIB 生成子类，**final 方法不代理**（静默跳过）。

## Q13：Java 是值传递还是引用传递？

**答**：**只有值传递**。基本类型传值的副本；对象传引用的**副本**（引用本身是值）。方法内改引用副本不影响外部引用。

**易错**：对象传进方法能改字段（通过引用副本找到堆对象），但**不能让外部引用指向新对象**——`void swap(Object a, Object b)` 在 Java 里 swap 不成功（改的是引用副本）。这就是「值传递」的体现。

## Q14：Integer 缓存？

**答**：`Integer a = 127` 走自动装箱（`Integer.valueOf(127)`），valueOf 缓存 **-128~127**（`IntegerCache`），范围内复用同一对象。

**易错**：`Integer a=127, b=127; a==b` true；`Integer a=128, b=128; a==b` **false**（超缓存，new 新对象）。Integer 比较一律 equals。缓存上限可配 `-XX:AutoBoxCacheMax=N`（下限 -128 不可改）。

## Q15：final / finally / finalize？

**答**：final（修饰符：变量不可改、方法不可重写、类不可继承）；finally（try-finally，异常时一定执行）；finalize（Object 方法，GC 前调用，**已弃用**）。

**易错**：finalize 不可靠（不保证执行时机 + 性能差 + 可能「复活」对象），JDK 9 弃用，用 try-with-resources 或 `Cleaner`。三个词只是名字像，**毫无关系**——面试经常当陷阱问。

---

## 易错点速查表

| 知识点 | 易错 |
|---|---|
| 多态 | 成员变量不多态（编译运行都看左） |
| 重载 vs 重写 | 同类静态 vs 父子运行 |
| 接口变量 | 默认 public static final（都是常量） |
| Integer 缓存 | -128~127 复用；超范围 `==` false |
| hashCode 契约 | 重写 equals 必须重写 hashCode |
| String 不可变 | value 内容不能改，不是引用 |
| checked vs unchecked | RuntimeException unchecked；IOException checked |
| 泛型擦除 | 运行时拿不到泛型；基本类型不能做参数 |
| JDK 代理 vs CGLIB | JDK 要接口；CGLIB 继承，final 不代理 |
| 值传递 | 只有值传递；对象传引用的副本 |
| finalize | 已弃用，用 try-with-resources / Cleaner |

> 本篇是 Java 基础的刷题集；深入源码/原理见 [基础长文](./)。concurrent / jvm / network 各自有总览 + 子页，刷题直接看总览问答即可，不另出 questions。
