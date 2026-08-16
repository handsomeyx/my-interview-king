---
title: MyBatis
---

# MyBatis

MyBatis 是 Java 后端最常用的半自动 ORM 框架。面试官爱问的不是「MyBatis 怎么用」，而是 **`#{}` 和 `${}` 的区别、一级 / 二级缓存的作用域与失效、Mapper 代理原理、插件拦截了谁、延迟加载怎么实现**。

## 为什么是 MyBatis 而不是 JPA/Hibernate

- **MyBatis 半自动**：SQL 自己写，框架负责参数映射 + 结果映射。SQL 可控、易调优。
- **JPA/Hibernate 全自动**：框架生成 SQL，开发快，但复杂查询难优化（N+1、生成的 SQL 啰嗦）。
- 取舍：CRUD 为主、业务简单 → JPA 快；报表、复杂 SQL、性能敏感 → MyBatis。
- 国内大厂主流是 MyBatis（+ MyBatis-Plus），因为 SQL 可控。

## 核心组件

| 组件 | 作用 |
|------|------|
| SqlSessionFactory | 全局单例，创建 SqlSession（重，启动建一次）|
| SqlSession | 一次 DB 会话（轻），含执行器，用完即关 |
| Mapper 接口 | 业务调用的接口，MyBatis 用**动态代理**生成实现 |
| Executor | 执行器，调度 StatementHandler / ParameterHandler / ResultSetHandler |

易错点：SqlSession **不是线程安全**的，不能跨线程共享。Spring 集成后由 SqlSessionTemplate 代理（线程安全），但你直接 `new SqlSession` 要自己管生命周期。

## `#{}` vs `${}` —— 高频中的高频

- **`#{}`**：**预编译参数**（PreparedStatement 的 `?` 占位），MyBatis 在 setParameter 时注入。**防 SQL 注入**。
- **`${}`**：**字符串拼接**，直接把值替换进 SQL。有 SQL 注入风险。

```xml
<!-- 安全：#{} 预编译 -->
<select id="getById">SELECT * FROM user WHERE id = #{id}</select>
<!-- 危险：${} 拼接，能被注入 -->
<select id="getByTable">SELECT * FROM ${tableName}</select>
```

- **什么时候只能用 `${}`**：**动态表名、列名、ORDER BY 字段**——这些 SQL 语法位置不接受 `?` 预编译。这时必须 `${}`，但必须**白名单校验**（只允许预期的值），不能直接拼用户输入。
- 易错点：`ORDER BY ${column}` 是常见坑——别让前端直接传 column，后端要用枚举 / 白名单映射。

## Mapper 代理原理

你只写接口（如 `UserMapper`），不写实现类，MyBatis 怎么跑起来的？

- **JDK 动态代理**：`MapperProxy` 实现 `InvocationHandler`，代理你的 Mapper 接口。
- 调用 `userMapper.getById(1)` → 进入 `MapperProxy.invoke()` → 解析方法对应的 SQL（XML / 注解）→ 走 Executor 执行 → 结果映射返回。
- 易错点：Mapper 接口和 XML 的 **namespace + id 必须对应**（namespace = 接口全限定名，id = 方法名），否则绑定失败。

## 一级 / 二级缓存

| 缓存 | 作用域 | 默认 | 失效条件 |
|------|--------|------|---------|
| 一级缓存 | **SqlSession** 级 | 开 | SqlSession 关闭 / commit / 对同表 update |
| 二级缓存 | **Mapper（namespace）** 级，跨 SqlSession | 关，需显式开 | 该 namespace 的 insert/update/delete |

- **一级缓存坑（Spring 下）**：Spring 默认每次方法用独立 SqlSession（一级缓存基本失效）。要跨方法共享，得 `@Transactional`（同事务同 SqlSession）。
- **二级缓存坑**：多表联查时，A 表 namespace 的二级缓存**不会因 B 表更新而失效** → 脏读。所以多表场景**别用二级缓存**，或用 Redis。
- 易错点：二级缓存要求实体可序列化（实现 Serializable），且缓存的是对象**副本**，读出来是新实例。

## 延迟加载（懒加载）

- 关联查询（`association` / `collection`）可配置懒加载——用到关联对象时才发 SQL。
- 实现：**cglib 代理**增强返回对象，调 getter 时触发加载。
- 配置：`lazyLoadingEnabled=true`（默认 false）。
- 易错点：懒加载要求 SqlSession **还没关闭**（关闭后再访问触发加载会报错）。Spring 下每次方法独立 session，跨方法懒加载会失败 → 解决：在 service 方法内完成所有数据访问。

## 插件（Interceptor）

- MyBatis 允许拦截**四大对象**的某些方法：
  - `Executor`（update / query / commit）
  - `StatementHandler`（prepare）
  - `ParameterHandler`（setParameters）
  - `ResultSetHandler`（handleResultSets）
- 用 `@Intercepts` 注解声明拦截签名。
- 场景：分页（PageHelper 拦 StatementHandler 改 SQL 加 LIMIT）、SQL 监控、慢日志、租户隔离。
- 易错点：插件是**责任链**，多个插件的顺序影响结果（外层先进入）。PageHelper 之类基础插件要在业务插件外层。

## 易错点速查

| 知识点 | 关键 |
|--------|------|
| `#{}` vs `${}` | `#{}` 预编译防注入；`${}` 拼接，仅用于表名 / 列名 / 排序且要白名单 |
| Mapper 代理 | JDK 动态代理；namespace + id 必须对应 |
| 一级缓存 | SqlSession 级；Spring 默认每次方法独立 session 基本失效 |
| 二级缓存 | namespace 级；多表联查会脏读；需 Serializable |
| 延迟加载 | cglib 代理；session 关闭后加载失败 |
| 插件 | 拦四大对象；责任链，顺序敏感 |
