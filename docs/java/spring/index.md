# Spring

Spring 是 Java 后端事实标准框架。面试官爱问的不是“Spring 是什么”，而是**IoC 容器怎么启动、Bean 生命周期、三级缓存怎么解循环依赖、AOP 用 JDK 还是 CGLIB、@Transactional 为什么会失效**。这篇是总览，每个主题点到面试官追问的深度，细节在子页。

## IoC 与 AOP 的本质

- **IoC（控制反转）**：对象创建和依赖管理的权力**从业务代码反转到容器**。本质是把“new 对象 + 设依赖”集中交给容器，解耦。
  - 易错点：IoC 不是“代码里没有 new”，而是“由容器决定何时创建、创建什么”。`new` 还在，只是写在容器里。
- **DI（依赖注入）**：IoC 的实现方式——容器主动把依赖塞进 Bean（构造器 / setter / 字段注入）。
- **AOP（面向切面）**：把横切逻辑（日志、事务、权限）从业务代码抽出来，通过**动态代理**织入。
  - 底层：目标类有接口 → JDK 动态代理（`Proxy.newProxyInstance`）；没有接口 → CGLIB（生成子类）。
  - 易错点：**同类内部方法调用不走代理**（`this.method()` 不经过代理对象），导致 `@Transactional`、缓存注解等失效。这是 Spring 面试高频坑。

细节见 [IoC 与 AOP](/java/spring/ioc-aop)。

## Bean 生命周期

核心阶段（面试常让背）：

1. **实例化**：调用构造方法 new 出对象（“毛坯 Bean”）。
2. **属性填充**：注入依赖（`@Autowired`）。
3. **初始化**：
   - 各种 Aware 回调（BeanNameAware、ApplicationContextAware）
   - `BeanPostProcessor.postProcessBeforeInitialization`
   - `@PostConstruct` / `InitializingBean.afterPropertiesSet` / init-method
   - `BeanPostProcessor.postProcessAfterInitialization`（**AOP 代理就在这一步生成**）
4. **使用**。
5. **销毁**：`@PreDestroy` / `DisposableBean` / destroy-method。

易错点：`BeanPostProcessor` 的 after 钩子是 AOP 代理生成的时机——理解这点就理解了“循环依赖为什么要三级缓存”。

## 循环依赖与三级缓存

Spring 用**三级缓存**解决 setter / 字段注入的循环依赖：

- **一级 singletonObjects**：完整的单例 Bean（成品）。
- **二级 earlySingletonObjects**：提前暴露的半成品（已实例化，未初始化）。
- **三级 singletonFactories**：ObjectFactory（能产出 Bean 或其代理）。

流程（A 依赖 B、B 依赖 A）：A 实例化后把自己的 ObjectFactory 放入三级缓存，去注入 B；B 实例化时需要 A，从三级缓存拿到 A 的工厂产出半成品 A（存入二级），B 完成；A 继续完成。

易错点：
- **构造器注入解决不了循环依赖**（实例化阶段就需要对方，但对方还没创建）。改用 setter 注入或 `@Lazy`。
- 为什么三级而不是两级：**为了 AOP**。三级缓存的 ObjectFactory 决定是否返回代理对象，保证循环依赖下代理也只生成一次。

细节见 [循环依赖](/java/spring/circular-dependency)。

## 事务

- **@Transactional 本质**：AOP 代理 + try-catch + commit/rollback。
- **失效场景**（面试高频）：
  - 方法不是 public（AOP 默认只代理 public）。
  - **同类内部调用**（不走代理，见 AOP 易错点）。
  - 异常被 catch 吞掉（代理看不到异常，不回滚）。
  - 抛 checked 异常默认不回滚（要 `rollbackFor = Exception.class`）。
  - 数据库引擎不支持事务（MyISAM）。

细节见 [Spring 事务](/java/spring/transaction)。

## 常用注解速查

| 注解 | 作用 |
|------|------|
| @Component / @Service / @Controller / @Repository | 注册 Bean（语义不同，本质都是 Bean） |
| @Configuration + @Bean | 配置类里手动定义 Bean |
| @Autowired | 按类型注入（配 @Qualifier 按名）|
| @Primary | 多候选时标记优先 |
| @Scope("prototype") | 作用域（默认 singleton）|

## 子页索引

- [IoC 与 AOP](/java/spring/ioc-aop)：容器启动、动态代理、AOP 失效
- [Spring 事务](/java/spring/transaction)：@Transactional 原理与失效场景
- [循环依赖](/java/spring/circular-dependency)：三级缓存详解
- [Spring 面试题集](/java/spring/questions)
