---
title: Spring 高频面试题速查
---

# Spring 高频面试题速查

> 15 道高频题，每题"2-4 行可直接答" + 深入链接。配合 [IoC 与 AOP](./ioc-aop)、[Spring 事务](./transaction)、[循环依赖](./circular-dependency) 深挖页。

## 整体

### Q1：Spring / SpringMVC / SpringBoot 区别？

- **Spring**：框架内核（IoC + AOP）。
- **SpringMVC**：Web 层（MVC，处理 HTTP 请求）。
- **SpringBoot**：**自动装配 + 起步依赖**，解决 Spring 配置繁琐（约定大于配置）。

关系：SpringBoot 内嵌 Tomcat + 自动装配，让你快速搭 Spring 应用。

### Q2：IoC 和 DI 是什么关系？

IoC 是**思想**（对象管理权交给容器），DI 是**手段**（容器把依赖注入对象）。详见 [IoC 与 AOP Q1](./ioc-aop)。

### Q3：AOP 用 JDK 动态代理还是 CGLIB？

有接口默认 JDK；无接口 CGLIB；SpringBoot 2.x 后**默认都走 CGLIB**。final 类 / 方法不能代理（CGLIB 靠继承）。详见 [IoC 与 AOP Q4](./ioc-aop)。

## Bean

### Q4：Bean 生命周期？

实例化 → 属性注入 → Aware 回调 → BeanPostProcessor 前置 → 初始化 → BeanPostProcessor 后置（**AOP 代理在此生成**）→ 销毁。详见 [IoC 与 AOP Q3](./ioc-aop)。

### Q5：Bean 作用域？

- **singleton**（默认）：容器单例。
- **prototype**：每次 getBean 新建。
- request / session / application：Web 场景。

### Q6：@Autowired vs @Resource？

- `@Autowired`（Spring）：**按类型**注入，多个同类型加 `@Qualifier` 指定名字。
- `@Resource`（JSR-250）：**按名字**注入，找不到再按类型。

**易错点**：构造方法注入推荐 `@Autowired`（Spring 4.3+ 单构造方法可省略注解）。

### Q7：@Component / @Service / @Repository / @Controller 区别？

功能上**都等价**（都是 @Component 的语义化别名）。区别只是**语义/分层**：Controller 控制层、Service 业务层、Repository 持久层。另外 `@Repository` 会把数据访问异常包装为统一的 `DataAccessException`。

## 事务（深入见专题页）

### Q8：Spring 事务传播行为？

7 种，常用 REQUIRED（默认，有就加入）/ REQUIRES_NEW（独立新事务）/ NESTED（嵌套保存点）。详见 [Spring 事务 Q2](./transaction)。

### Q9：@Transactional 失效场景？

自调用（`this` 不走代理）、非 public、异常被吞、checked 异常默认不回滚、final 方法。**根因都是"没走 AOP 代理"**。详见 [Spring 事务 Q3-Q4](./transaction)。

### Q10：循环依赖怎么解决？三级缓存为什么？

三级缓存（成品 / 半成品 / 对象工厂），靠"提前暴露半成品"。三级存对象工厂是为了 AOP 代理。构造方法循环依赖解决不了（卡在实例化前）。详见 [循环依赖](./circular-dependency)。

## SpringBoot

### Q11：SpringBoot 自动装配原理？

`@SpringBootApplication` 内含 `@EnableAutoConfiguration`，它通过 `spring.factories`（2.7+ 改 `META-INF/spring/...imports`）加载所有自动配置类，配合 `@Conditional`（满足条件才生效）实现"引入 starter 就自动配好"。

### Q12：@SpringBootApplication 包含什么？

`@SpringBootConfiguration`（就是 @Configuration）+ `@EnableAutoConfiguration`（自动装配）+ `@ComponentScan`（包扫描）。三个注解的组合。

### Q13：SpringBoot 启动流程？

1. `SpringApplication.run` 启动。
2. 创建 ApplicationContext（servlet 用 `ServletWebServerApplicationContext`）。
3. `refresh()`：加载 BeanDefinition、实例化单例 Bean、自动装配。
4. 内嵌 Tomcat 启动。
5. 发布 `ApplicationReadyEvent`。

## 其他

### Q14：Spring 用了哪些设计模式？

- **工厂**：BeanFactory。
- **单例**：Bean 默认 singleton。
- **代理**：AOP（JDK / CGLIB）。
- **模板方法**：JdbcTemplate、RestTemplate。
- **观察者**：ApplicationEvent / Listener。
- **责任链**：SpringMVC 的 HandlerInterceptor。

### Q15：SpringMVC 请求处理流程？

请求 → `DispatcherServlet` → `HandlerMapping`（找控制器）→ `HandlerAdapter`（执行）→ Controller 返回 ModelAndView → `ViewResolver` 渲染（或 `@ResponseBody` 走 `HttpMessageConverter` 返 JSON）。

---

> 速查够用版，深挖看 [IoC 与 AOP](./ioc-aop)、[Spring 事务](./transaction)、[循环依赖](./circular-dependency)。
