---
layout: home

hero:
  name: "我是面试大王"
  text: "Java 后端面试知识体系" 
  tagline: 每篇都写到面试官追问的深度 —— Redis 的 fsync、MySQL 的 MVCC、一致性哈希的虚拟节点
  image:
    src: /images/hero.jpg
    alt: Java 后端面试知识体系
  actions:
    - theme: brand
      text: 开始学习
      link: /java/basics/
    - theme: alt
      text: 算法刷题
      link: /algorithm/
    - theme: alt
      text: AI Agent 实战
      link: /ai/
    - theme: alt
      text: 在 GitHub 上查看
      link: https://github.com/handsomeyx/my-interview-king

features:
  - icon: 💻
    title: Java 基础
    details: JVM 内存与 GC、并发（volatile / synchronized / CAS / 线程池）、集合源码。
  - icon: 📚
    title: 中间件深度
    details: Redis 持久化与底层数据结构、MySQL B+ 树与 MVCC、Kafka 副本与 ISR。
  - icon: 🏗️
    title: 分布式架构
    details: CAP / Base、Raft 共识、分布式事务（2PC / TCC / 本地消息表）。
  - icon: 🤖
    title: AI Agent 实战
    details: ReAct / Plan-Execute、MCP 协议、Function Calling、RAG 检索增强。
  - icon: 🧠
    title: 算法与数据结构
    details: 滑动窗口 / 动规 / DFS 套路框架 + 面试 Top 100 精讲。
  - icon: 💡
    title: 场景题专栏
    details: 接入路由 / 业务逻辑 / 持久化异步 三层全链路场景题。
  - icon: 🎯
    title: 系统设计算法
    details: 一致性哈希、限流、LRU/LFU 等后端面试高频——纯算法站不覆盖的差异化招牌。

---

# 数据看板

<SiteStats />

<ContinueReading />

# 热门推荐

<div class="recommendations-container">
  <div class="recommendation-section">
    <h3 class="recommendation-title">高频面试题</h3>
    <div class="recommendation-list">
      <a href="/algorithm/05-top-interview-100/arrays/" class="recommendation-item">
        <span class="recommendation-icon">🧮</span>
        <span class="recommendation-text">数组类 Top 题</span>
      </a>
      <a href="/algorithm/05-top-interview-100/linked-list/" class="recommendation-item">
        <span class="recommendation-icon">🔗</span>
        <span class="recommendation-text">链表类 Top 题</span>
      </a>
      <a href="/algorithm/05-top-interview-100/dynamic-programming/" class="recommendation-item">
        <span class="recommendation-icon">📊</span>
        <span class="recommendation-text">动态规划 Top 题</span>
      </a>
    </div>
  </div>
  <div class="recommendation-section">
    <h3 class="recommendation-title">热门项目</h3>
    <div class="recommendation-list">
      <a href="/ai/" class="recommendation-item">
        <span class="recommendation-icon">🤖</span>
        <span class="recommendation-text">AI Agent 知识库</span>
      </a>
      <a href="/distributed/scenarios/" class="recommendation-item">
        <span class="recommendation-icon">🎯</span>
        <span class="recommendation-text">场景题专栏</span>
      </a>
      <a href="/algorithm/00-algorithm-frameworks/" class="recommendation-item">
        <span class="recommendation-icon">📋</span>
        <span class="recommendation-text">算法框架学习</span>
      </a>
    </div>
  </div>
  <div class="recommendation-section">
    <h3 class="recommendation-title">推荐入门</h3>
    <div class="recommendation-list">
      <a href="/java/basics/" class="recommendation-item">
        <span class="recommendation-icon">💻</span>
        <span class="recommendation-text">Java 基础语法</span>
      </a>
      <a href="/java/redis/" class="recommendation-item">
        <span class="recommendation-icon">📚</span>
        <span class="recommendation-text">Redis 核心原理</span>
      </a>
      <a href="/distributed/" class="recommendation-item">
        <span class="recommendation-icon">🏗️</span>
        <span class="recommendation-text">分布式基础</span>
      </a>
    </div>
  </div>
</div>

<LearningPath />

## 关于作者

作为一名 Java 后端开发者，我希望通过分享自己的学习经验和面试心得，帮助更多人顺利通过面试，获得理想的工作机会。这个指南是我对 Java 后端面试知识的系统总结，希望能够为你提供有价值的帮助。
