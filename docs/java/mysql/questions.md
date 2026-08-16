---
title: MySQL 高频面试题速查
---

# MySQL 高频面试题速查

> 15 道高频题，每题给"2-4 行可直接答"的版本 + 深入链接。面试前过一遍，配合 [索引](./indexing)、[事务 MVCC](./transaction-mvcc)、[锁](./lock) 三个深挖页。

## 基础

### Q1：三大范式？必须遵守吗？

1NF 字段原子、2NF 非主键完全依赖主键、3NF 非主键不传递依赖主键。**不必死守**——为了性能常**反范式**（加冗余字段避免 join）。范式是设计参考，不是铁律。

### Q2：drop / delete / truncate 区别？

- `drop`：删**表结构** + 数据，不可回滚。
- `truncate`：清空表数据、保留结构，**自增重置**，不可回滚（DDL）。
- `delete`：按条件删行，**可回滚**（DML），自增不重置。

速度：truncate > delete（不记 undo log）。

### Q3：InnoDB vs MyISAM？

InnoDB：支持事务、行锁、外键、崩溃恢复（redo log）。MyISAM：表锁、不支持事务、崩溃易损。**现代都用 InnoDB**，MyISAM 基本淘汰。

### Q4：为什么 InnoDB 推荐自增整型主键？

聚簇索引按主键有序，自增主键**顺序追加**避免页分裂；整型比 UUID 占空间小、比较快。详见 [索引 Q2（聚簇索引）](./indexing)。

## 查询与优化

### Q5：count(*) / count(1) / count(列) 区别？

- `count(*)` / `count(1)`：统计**所有行**（含 NULL）。
- `count(列)`：统计该列**非 NULL** 的行数。

**易错点**："count(1) 比 count(*) 快"是老黄历，MySQL 5.7+ 优化器把 `count(*)` 当最优，**两者性能基本一样，优先用 `count(*)`**。

### Q6：慢 SQL 优化思路？

1. `explain` 看执行计划（type / key / rows / Extra）——见 [索引 Q7](./indexing)。
2. 索引失效排查（函数、隐式转换、左模糊）——见 [索引 Q5](./indexing)。
3. 大表分页用游标 / 延迟关联（深分页，见 Q7）。
4. 减少 join 表数量、避免 `select *`。
5. 实在慢 → 分库分表 / 读写分离。

### Q7：深分页（LIMIT 1000000, 10）为什么慢？怎么优化？

OFFSET 会扫描前面所有行再丢弃。优化：
- **延迟关联**：先 `select id ... limit` 拿 id，再 join 取全字段。
- **游标分页**：`where id > last_id limit 10`（要求 id 连续有序）。

## 架构

### Q8：分库分表什么时候做？怎么选？

单表数据量超千万、DB CPU/IO 到瓶颈再做。**别过早分**。
- 垂直分库：按业务拆库（订单库 / 用户库）。
- 垂直分表：宽表拆窄表（冷热列分开）。
- 水平分表：按 hash / range / 时间拆到多表 / 多库。

**难点**：跨库 join、分布式事务、全局 ID（见 [算法 / 分布式 ID](/algorithm/04-system-algorithms/unique-id/)）。

### Q9：读写分离 + 主从延迟怎么办？

主写从读。主从复制异步，**从库有延迟**。解法：
- 关键写后读走主库（强制路由）
- 半同步复制（主等至少一个从收到才返回）
- 缓存兜底（写后写缓存，读先查缓存）

### Q10：MySQL 主从复制原理？

1. 主库写变更到 **binlog**。
2. IO 线程从主库拉 binlog，写从库 **relay log**。
3. SQL 线程回放 relay log。

三个日志区别见 Q11。

## 日志（高频易混）

### Q11：binlog / redo log / undo log 区别？

| 日志 | 归属 | 作用 |
|---|---|---|
| **redo log** | InnoDB 引擎层 | 崩溃恢复（持久性 D） |
| **undo log** | InnoDB 引擎层 | 回滚 + MVCC（原子性 A） |
| **binlog** | Server 层 | 主从复制 + 数据恢复 |

**易错点**：redo / undo 是 InnoDB 的，binlog 是 **Server 层**的（所有引擎都有）。两阶段提交（redo + binlog）保证两者一致。

## 事务与锁（深入见专题页）

### Q12：四种隔离级别？InnoDB 默认？

RU / RC / RR / Serializable，InnoDB 默认 **RR**。各级别解决的并发问题见 [事务 MVCC](./transaction-mvcc)。

### Q13：MVCC 怎么实现？

行隐藏列 + undo log 版本链 + ReadView。RC 每次 select 生成 ReadView，RR 事务首次 select 生成。详见 [事务 MVCC](./transaction-mvcc)。

### Q14：行锁 / 间隙锁 / Next-Key 区别？

Record 锁行、Gap 锁间隙（仅 RR）、Next-Key 锁区间（RR 默认）。详见 [锁](./lock)。

### Q15：怎么排查死锁？

`SHOW ENGINE INNODB STATUS` 看最近死锁详情（两个事务各持什么锁、等什么）。预防：统一加锁顺序、事务短。详见 [锁 Q5](./lock)。

---

> 速查只给"够用版"，深挖看三个专题页：[索引](./indexing)、[事务 MVCC](./transaction-mvcc)、[锁](./lock)。
