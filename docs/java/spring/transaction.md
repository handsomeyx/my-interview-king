---
title: Spring 事务（@Transactional 传播与失效）
---

# Spring 事务（@Transactional 传播与失效）

> Spring 事务面试两大核心：**传播行为（7 种）+ 失效场景（自调用、非 public、异常被吞等）**。很多人会用 `@Transactional` 但答不清"为什么自调用失效""REQUIRED 和 REQUIRES_NEW 区别"。本文按问答，每题答 + 易错点。---

## 思考锚点

数据库事务能保证一组操作要么全成功要么全失败，但在 Spring 应用中，一个业务方法往往会调用多个数据库操作，甚至调用其他带事务的方法。问题来了：这些事务之间怎么协作？如果内层方法回滚了，外层方法应该回滚还是继续？

Spring 事务的核心是「AOP 代理 + 传播行为」，它让开发者只需加一个 `@Transactional` 注解，框架自动处理事务的开启、提交和回滚。但这个机制有很多陷阱——自调用失效、checked 异常不回滚、非 public 方法不生效等。

本文要讲清楚 7 种事务传播行为的区别、所有常见的失效场景，以及隔离级别和传播行为的区别。

## Q1：@Transactional 的原理？

**答**：Spring 事务基于 **AOP 动态代理**。加了 `@Transactional` 的 Bean，Spring 生成一个**代理对象**，方法被调用时代理做三件事：
1. 开事务（`TransactionManager.getTransaction`）
2. 执行原方法
3. 正常返回 → 提交；抛异常 → 回滚

所以 `@Transactional` 只在**通过代理调用**时生效。这直接解释了为什么"自调用"会失效（见 Q3）。

**易错点**：`@Transactional` 不是"魔法注解"，本质是 AOP 环绕通知。**没有代理 = 没有事务**。

## Q2：7 种事务传播行为？

**答**：传播行为回答"一个事务方法被另一个事务方法调用时，怎么办"。7 种里前 3 个最常用：

| 传播行为 | 含义 | 场景 |
|---|---|---|
| **REQUIRED**（默认）| 有就加入，没有就新建 | 99% 场景 |
| **REQUIRES_NEW** | 不管有没有，新建一个；挂起当前事务 | 日志记录（不论业务成败都要落） |
| **NESTED** | 有就建嵌套事务（保存点），没有就新建 | 部分回滚 |
| SUPPORTS | 有就加入，没有就非事务跑 | 查询（不强求事务） |
| NOT_SUPPORTED | 非事务跑，挂起当前事务 | 耗时操作不想占事务连接 |
| MANDATORY | 必须在事务里，否则抛异常 | 强制调用方开事务 |
| NEVER | 不许在事务里，否则抛异常 | — |

**追问：REQUIRED vs REQUIRES_NEW vs NESTED 区别？**（最高频对比）
- **REQUIRED**：B 跟 A 用**同一个事务**。B 抛异常，A 也回滚（同一事务一损俱损）。
- **REQUIRES_NEW**：B 开**新事务**，A 的事务挂起。B 提交/回滚**与 A 无关**，A 后面还能继续自己的事务。
- **NESTED**：B 在 A 的事务里建**保存点**。B 失败回滚到保存点，A 可以 catch 掉 B 的异常选择继续，或一起回滚。依赖数据库的 savepoint。

**易错点**：NESTED 需要**数据库支持 savepoint**（InnoDB 支持）。REQUIRES_NEW 会**占两个数据库连接**（挂起的 A 占一个、新事务 B 占一个），连接池小可能死锁。

## Q3：@Transactional 自调用为什么失效？

**答**：这是**最高频失效场景**。

```java
@Service
public class UserService {
    public void methodA() {
        this.methodB();   // 直接 this 调用，不走代理
    }
    @Transactional
    public void methodB() { ... }
}
```

`methodA` 调 `methodB` 用的是 `this`（原始对象），**不是代理对象**。`@Transactional` 靠代理拦截生效，绕过代理 = 注解失效。

**解法**：
1. 把 `methodB` 拆到另一个类，注入后调用（跨 Bean 调用走代理）。
2. 注入自己：`@Autowired private UserService self; self.methodB();`
3. 从 ApplicationContext 拿代理：`applicationContext.getBean(UserService.class).methodB();`

**易错点**：很多人以为 `@Transactional` 加上就一定生效——**自调用、非 public、同类内部调用**是最常见的"加了没效果"的坑，根因都是"没走代理"。

## Q4：@Transactional 还有别的失效场景吗？

**答**（高频背诵点）：

1. **自调用**（见 Q3）。
2. **非 public 方法**：Spring AOP 默认只代理 public 方法，protected/private 的 `@Transactional` 不生效。
3. **异常被 catch 吞掉**：`try { ... } catch { log }`——没抛异常，代理以为正常，提交不回滚。
4. **回滚类型不对**：默认只回滚 `RuntimeException` 和 `Error`；**checked 异常默认不回滚**。要么 `@Transactional(rollbackFor = Exception.class)`，要么抛 RuntimeException。
5. **类没被 Spring 管理**：`new` 出来的对象不是 Bean，没代理。
6. **final / static 方法**：final 不能被代理覆写；static 不走实例代理。
7. **数据库引擎不支持事务**：MyISAM 不支持事务（InnoDB 才支持）。

**易错点**：checked 异常默认不回滚是**最隐蔽**的坑。IO、SQL 异常是 checked，业务抛了 `IOException` 默认不回滚——数据写了一半。**生产建议统一 `@Transactional(rollbackFor = Exception.class)`**。

## Q5：声明式 vs 编程式事务？

**答**：
- **声明式**（`@Transactional`）：AOP 实现，代码无侵入，简单。缺点：粒度是方法级，灵活度低；自调用失效。
- **编程式**（`TransactionTemplate` / `PlatformTransactionManager`）：手动写事务边界，灵活（可方法内局部）。缺点：代码侵入。

**取舍**：默认用声明式。需要**方法内局部事务**（比如循环里每条独立事务）或**细粒度控制**时，用编程式。

## Q6：隔离级别怎么配？和传播是一回事吗？

**答**：`@Transactional(isolation = Isolation.DEFAULT)`，可选 DEFAULT / READ_UNCOMMITTED / READ_COMMITTED / REPEATABLE_READ / SERIALIZABLE。

Spring 只是透传给数据库，**真正实现隔离的是数据库**（MySQL InnoDB 默认 REPEATABLE_READ，Oracle 默认 READ_COMMITTED）。隔离级别 + MVCC 原理见 MySQL 板块（事务/MVCC 子页建设中）。

**易错点**：别混淆"Spring 事务传播"和"数据库隔离级别"——**传播**解决"多个事务方法之间怎么协作"，**隔离级别**解决"并发事务读写一致性"。两件事，面试常被混问。

---

## 易错点速查表

| 失效/坑 | 关键 |
|---|---|
| 原理 | AOP 代理；没代理就没事务 |
| 自调用 | `this` 调用不走代理；拆类 / 注入自己 / 拿 bean |
| 非 public | 默认只代理 public |
| 异常吞掉 | try-catch 不抛 = 提交不回滚 |
| checked 异常 | 默认不回滚；生产配 `rollbackFor = Exception.class` |
| REQUIRED vs REQUIRES_NEW | 同一事务 vs 独立新事务 |
| NESTED | 依赖 DB savepoint；REQUIRES_NEW 占两个连接 |
| 传播 vs 隔离 | 传播 = 方法间协作；隔离 = 并发一致性，两回事 |

---

## 复述自测

读完这篇，试试用自己的话回答三个问题：

1. **一句话总结**：`@Transactional` 自调用为什么会失效？（提示：从 AOP 代理的工作原理思考）

2. **讲给初学者听**：怎么用「剧场的幕后指挥」来类比 Spring 事务传播？REQUIRED 和 REQUIRES_NEW 像什么？

3. **预判追问**：如果你是面试官，读完这篇你会追问什么？（比如 NESTED 和 REQUIRES_NEW 的区别？为什么 checked 异常默认不回滚？）

> 事务失效是 Spring 高频坑题。后续拆 `ioc-aop`（IoC 容器原理 + AOP 的 JDK 动态代理 vs CGLIB）——AOP 代理原理是理解 `@Transactional` 失效的根。
