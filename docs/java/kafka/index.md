---
title: Kafka
---

# Kafka

> 面试高频 MQ。Kafka 题考察四件事：**架构（分区/副本/消费组）、消息可靠性（怎么不丢）、顺序性、重复消费**。本文按问答，每题答 + 追问 + 易错点。

## 思考锚点

在分布式系统中，消息队列的核心价值是「解耦、异步、削峰」。但引入消息队列后，新的问题也来了：消息会不会丢？顺序怎么保证？重复消费怎么办？

Kafka 作为高吞吐的分布式消息系统，通过「分区 + 副本 + 消费组」的架构解决了这些问题。但它的保证不是绝对的——消息不丢需要生产端、Broker 端、消费端三端配合，顺序性只在单分区内保证，精确一次语义需要额外配置。

本文要讲清楚 Kafka 的核心架构、消息可靠性保证的三端配置、顺序性的实现方式，以及消费端幂等性的设计。

## 架构速览

```
Producer → Broker（Topic = 多 Partition，每 Partition 多副本）→ Consumer Group

Topic
├── Partition（并行单元；有序仅限单分区）
│   ├── Leader 副本（读写都走它）
│   └── Follower 副本（从 Leader 同步，ISR 集合）
└── Offset（消费位点，每个消费组各自维护）

Consumer Group：组内分区独占——一个分区同一时刻只被组内一个消费者消费
```

核心一句话：**Partition 是并行单元，也是顺序边界**。

---

## Q1：Kafka 怎么保证消息不丢？

**答**：三个环节都要配，漏一个就丢：

**生产端**（Producer → Broker）：
- `acks=all`（或 -1）：消息要等所有 ISR 副本写入才认为成功。
- `retries`：失败重试。
- `enable.idempotence=true`：开启幂等（防重试导致重复）。

**Broker 端**（存储）：
- `replication.factor ≥ 3`：副本数。
- `min.insync.replicas ≥ 2`：至少 2 个副本同步成功（配合 acks=all）。
- `unclean.leader.election.enable=false`：禁止非 ISR 副本当 Leader（否则丢数据）。

**消费端**（Consumer）：
- 关闭自动提交（`enable.auto.commit=false`），**业务处理完再手动提交 offset**。

**易错点**：很多人只配生产端 `acks=all` 就以为"不丢"。**消费端自动提交 offset 是隐性丢消息的常见元凶**——offset 先进了，但业务异常没处理，消费者崩溃重启后从新 offset 继续，这条消息没人再消费。

## Q2：Kafka 怎么保证消息顺序？

**答**：**Kafka 只保证单 Partition 内有序**，跨 Partition 无序。

- 要**全局有序**：整个 Topic 只建 1 个 Partition（牺牲并行，吞吐极低）。
- 要**局部有序**（常用）：`Producer` 发送时指定 `key`（如 `orderId`），**同 key 进同 partition**，保证同一业务对象的消息有序。

**追问**：为什么不全用 1 个分区？→ Kafka 的吞吐来自分区并行。1 个分区 = 1 个消费者 = 没有并行优势，等于白用 Kafka。所以工程上用"按 key 分区 + 局部有序"折中。

**易错点**：消息**重试可能打破顺序**。Producer 默认 `max.in.flight.requests.per.connection > 1` 时，重试可能把后发的消息先发成功。要严格顺序：设为 1，或开幂等（幂等开启时 Kafka 内部保序即使重试）。

## Q3：重复消费怎么处理？

**答**：Kafka 默认是 **at-least-once**（至少一次）——消息可能重复（生产端重试、消费端 offset 提交前崩溃重消费）。所以**消费端必须幂等**。

幂等实现：
- 业务层用唯一键去重（如 orderId，消费前查库 / Redis `SETNX`）
- 数据库唯一约束兜底
- 状态机（只处理"未处理"状态的消息）

**追问**：Kafka 能不能 exactly-once（精确一次）？→ 能。0.11+ 提供**事务 + 幂等生产**（`transactional.id` + `initTransactions`），保证"生产 → 消费 → 生产"链路精确一次。但有性能开销，且消费端 `read_committed` 只能看到已提交事务。大多数业务用 at-least-once + 业务幂等更实际。

**易错点**："Kafka 事务 = 一定不重复"——不准确。事务保证的是**生产端不重复 + 跨分区原子写入**，**消费端的重复仍要业务幂等**。

## Q4：消息积压怎么处理？

**答**：先定位再处理。

**定位**：
- 消费者 TPS < 生产者 TPS（消费太慢）
- 消费者挂了 / Rebalance 卡住
- 按 key 分区时**热点 key 数据倾斜**

**处理**：
- **临时扩消费者**——但受限于分区数：消费者数 > 分区数时，多余消费者空闲。所以要先**扩分区**才能真正扩并行。
- 紧急止血：把堆积消息转储到新 Topic，事后补偿。
- 优化消费逻辑（批量、异步、减少单条耗时）。

**易错点**：直接加消费者没用——**一个分区只能被一个消费者消费**。消费者数超过分区数，多余的不干活。要扩并行**必须先加分区**。

## Q5：Rebalance 是什么？为什么慢？

**答**：Consumer Group 成员变化（加消费者、消费者挂、订阅变化）时触发 **Rebalance**——重新分配分区给消费者。

**为什么慢**：Rebalance 期间**所有消费者暂停消费**（Stop The World），重新分配后才恢复。频繁 Rebalance = 频繁停顿。

**常见触发**：
- 消费者心跳超时（`session.timeout.ms`，网络抖动被误判挂了）
- 消费者处理太慢，poll 间隔超过 `max.poll.interval.ms`（被踢出组）

**优化**：
- `max.poll.interval.ms` 调大（给业务处理时间）
- `max.poll.records` 调小（一次少拉点，避免处理超时）
- 用 **Cooperative Rebalance**（增量 rebalance，2.4+，只重分配受影响分区，不全停）

**易错点**：消费者"处理慢被踢出"是生产高频坑。表现：消息堆、rebalance 不停循环。根因是 `max.poll.interval.ms` 太短 + 单条消息处理太慢。

---

## 易错点速查表

| 知识点 | 关键 |
|---|---|
| 不丢消息 | 三端都要配：生产 acks=all + 副本 ISR + 消费手动提交 offset |
| 顺序性 | 单 Partition 有序；按 key 路由做局部有序；幂等开启保重试不乱序 |
| 重复消费 | at-least-once，消费端业务幂等 |
| exactly-once | 事务有性能开销，消费端仍需幂等 |
| 消息积压 | 加消费者前必须先加分区（分区数 = 并行上限） |
| Rebalance | 期间 STW；处理慢超 `max.poll.interval.ms` 会被踢 |
| ISR | 落后太多的副本被踢出，影响 acks=all 的可用性 |

---

## 复述自测

读完这篇，试试用自己的话回答三个问题：

1. **一句话总结**：要保证 Kafka 消息不丢，生产端、Broker 端、消费端分别需要配置什么？（提示：acks=all + ISR 副本 + 手动提交 offset）

2. **讲给初学者听**：怎么用「公司邮件分发」来类比 Kafka 的「分区 + 副本 + 消费组」？多个秘书（消费者）怎么分工处理邮件（分区）？

3. **预判追问**：如果你是面试官，读完这篇你会追问什么？（比如 Rebalance 为什么会导致消息处理延迟？ exactly-once 语义是怎么实现的？）

> Kafka 是高吞吐 MQ。后续如需对比 RocketMQ / RabbitMQ，再起独立篇——按 `.claude/rules/content.md` 写满再挂链接。
