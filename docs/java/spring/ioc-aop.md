---
title: Spring IoC 与 AOP 原理
---

# Spring IoC 与 AOP 原理

> Spring 两大核心 IoC + AOP。很多人会用 `@Service`/`@Autowired`/`@Aspect`，但追问"BeanFactory 和 ApplicationContext 区别""AOP 用 JDK 还是 CGLIB"就答不全。本文按问答，每题答 + 易错点。AOP 代理原理也是理解 `@Transactional` 自调用失效的根（见 [Spring 事务](./transaction)）。---

## 思考锚点

传统 Java 开发中，一个对象需要另一个对象时，我们用 `new` 主动创建。但这样会导致对象之间耦合严重——改一个类可能要改所有依赖它的类。

Spring 的核心思想是「控制反转」：把对象的创建和依赖管理交给容器，开发者只需要声明「我要什么」，容器自动帮你注入。AOP 则更进一步，把「日志、事务、权限」等横切关注点从业务代码中剥离出来，动态织入。

本文要讲清楚 IoC/DI 的本质、Bean 的完整生命周期、AOP 的两种代理方式，以及为什么这些机制会导致 `@Transactional` 自调用失效。

## Q1：IoC 和 DI 是什么关系？

**答**：
- **IoC（控制反转）**：对象创建和依赖管理的权力**从代码交给 Spring 容器**。是一种**思想**。
- **DI（依赖注入）**：实现 IoC 的**方式**——容器主动把依赖"注入"对象（构造方法 / setter / 字段）。

关系：IoC 是思想，DI 是手段。说"IoC 容器"指的就是管这个的对象容器（ApplicationContext）。

**易错点**：IoC 不等于 DI。IoC 还可以用**依赖查找**（DL，主动 `getBean`）实现，只是 Spring 主推 DI。

## Q2：BeanFactory 和 ApplicationContext 区别？

**答**：两者都是 IoC 容器，ApplicationContext 继承 BeanFactory 并扩展：

| 维度 | BeanFactory | ApplicationContext |
|---|---|---|
| 定位 | 最底层容器接口 | 企业级增强容器（实际用的） |
| Bean 加载 | **懒加载**（getBean 时才创建） | **预加载**（启动时实例化单例） |
| 特性 | 只有核心 IoC | + 事件、国际化、AOP、注解扫描 |

**易错点**：平时说的"Spring 容器"基本都指 **ApplicationContext**。BeanFactory 是底层 SPI，业务代码很少直接用。

## Q3：Bean 生命周期？

**答**：核心 7 步（单例）：
1. **实例化**（new，构造方法）
2. **属性赋值**（依赖注入，`@Autowired`）
3. **Aware 回调**（如 `BeanNameAware`，注入容器元信息）
4. **BeanPostProcessor 前置处理**（`postProcessBeforeInitialization`）
5. **初始化**（`@PostConstruct` → `InitializingBean.afterPropertiesSet` → `init-method`）
6. **BeanPostProcessor 后置处理**（`postProcessAfterInitialization`——**AOP 代理就在这一步生成**）
7. **销毁**（`@PreDestroy` → `DisposableBean` → `destroy-method`）

**易错点**：AOP 代理在**第 6 步生成**（后置处理）。这意味着前 5 步里 `this` 引用是原始对象、没有代理——这也是为什么"构造方法里调 `@Transactional` 方法无效"（那时代理还没生成）。

> 🤔 停下来想想：AOP 代理在第 6 步才生成，那构造方法里调 @Transactional 为什么会失效？

## Q4：AOP 用 JDK 动态代理还是 CGLIB？

**答**：Spring AOP 两种都支持，按目标类自动选：
- **JDK 动态代理**：目标类**实现接口**时默认用。基于 `Proxy.newProxyInstance`，代理实现相同接口。
- **CGLIB**：目标类**没实现接口**时用。靠**生成子类**做代理（继承目标类，重写方法）。

**追问：SpringBoot 2.x 之后默认哪个？**→ **CGLIB**（`spring.aop.proxy-target-class=true` 默认开）。即使有接口也用 CGLIB，避免"代理类型和目标类型不一致"的歧义。

> 🤔 停下来想想：SpringBoot 2.x 为什么默认改用 CGLIB？

**易错点**：CGLIB 用**继承生成子类**，所以**final 类和 final 方法无法代理**（不能继承 / 覆写）。这是 `@Transactional` 加在 final 方法上失效的根因之一。

## Q5：AOP 的核心概念？

**答**（一张图理清）：
- **切面（Aspect）**：`@Aspect` 标注的类，包含一组增强。
- **切点（Pointcut）**：**where**——在哪些方法上增强（如 `execution(* com.xxx.*.*(..))`）。
- **通知（Advice）**：**when + what**——在切点的前 / 后 / 环绕做什么。
- **织入（Weaving）**：把切面应用到目标对象（Spring 用运行时代理织入）。

**通知 5 种类型**：
- `@Before`：方法前
- `@After`：方法后（无论正常 / 异常）
- `@AfterReturning`：方法正常返回后
- `@AfterThrowing`：方法抛异常后
- `@Around`：环绕（最强大，能控制是否执行原方法、改参数、改返回值）

**易错点**：`@After` 和 `@AfterReturning` 区别——前者**一定执行**（类似 finally），后者**只在正常返回时**执行。异常时 `@AfterReturning` 不触发，`@After` 触发。

## Q6：AOP 失效和 @Transactional 什么关系？

**答**：`@Transactional` 本质是 AOP（一个环绕切面）。所以**所有 AOP 失效场景 = @Transactional 失效场景**：
- 自调用（`this`，不走代理）
- 非 public / final 方法
- 类没被 Spring 管理

这解释了为什么"事务自调用失效"——根因是 AOP 代理原理。详见 [Spring 事务](./transaction)。

---

## 易错点速查表

| 知识点 | 关键 |
|---|---|
| IoC vs DI | IoC 是思想，DI 是手段；IoC 还能依赖查找实现 |
| BeanFactory vs ApplicationContext | 懒加载 vs 预加载；实际都用后者 |
| 生命周期 | AOP 代理在"后置处理"步生成（第 6 步） |
| JDK vs CGLIB | 有接口 JDK；无接口 CGLIB；SpringBoot 2.x 默认 CGLIB |
| CGLIB 限制 | 靠继承生成子类，final 类 / 方法不能代理 |
| @After vs @AfterReturning | 前者一定执行（finally）；后者仅正常返回时 |
| AOP = 事务根 | `@Transactional` 失效本质是 AOP 失效 |

---

## 复述自测

读完这篇，试试用自己的话回答三个问题：

1. **一句话总结**：IoC 和 AOP 的核心价值分别是什么？（提示：IoC 解决「对象创建和依赖管理」，AOP 解决「横切关注点剥离」）

2. **讲给初学者听**：怎么用「装修房子」来类比 IoC（你找装修公司，工人由公司安排）和 AOP（在不砸墙的情况下加电路）？

3. **预判追问**：如果你是面试官，读完这篇你会追问什么？（为什么 AOP 代理要在 Bean 生命周期的第 6 步生成？JDK 动态代理和 CGLIB 的本质区别是什么？）

> IoC 和 AOP 是 Spring 的地基。配合 [循环依赖](./circular-dependency)（三级缓存为什么为 AOP 设计）、[事务](./transaction)（AOP 代理失效）一起看，Spring 原理就通了。
