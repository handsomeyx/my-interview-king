import { withMermaid } from 'vitepress-plugin-mermaid'

export default withMermaid({
  title: "我是面试大王",
  description: "沉淀知识，对齐面试逻辑",
  appearance: true,
  ignoreDeadLinks: true,
  markdown: {
    lineNumbers: true
  },
  themeConfig: {
    // 顶部导航栏：只放主类目入口，子项交给侧边栏
    nav: [
      { text: '首页', link: '/' },
      {
        text: 'Java 后端',
        items: [
          { text: '总览', link: '/java/' },
          { text: 'Java 基础', link: '/java/basics/' },
          { text: 'Java 并发', link: '/java/concurrent/' }
        ]
      },
      {
        text: '分布式 & 场景',
        items: [
          { text: '总览', link: '/distributed/' },
          { text: '场景题专栏', link: '/distributed/scenarios/' }
        ]
      },
      {
        text: '算法',
        items: [
          { text: '总览', link: '/algorithm/' },
          { text: '面试 Top 100', link: '/algorithm/05-top-interview-100/' }
        ]
      },
      {
        text: 'AI 实战',
        items: [
          { text: '总览', link: '/ai/' }
        ]
      },
      {
        text: '项目实战',
        items: [
          { text: '智能面试助手', link: '/projects/interview-agent/' }
        ]
      },
      {
        text: '计算机基础',
        items: [
          { text: '计算机网络', link: '/cs-basics/network/' }
        ]
      },
      { text: '更新日志', link: '/changelog' },
      { text: '我的学习', link: '/my-progress' }
    ],
    search: {
      provider: 'local',
      options: {
        translations: {
          button: {
            buttonText: '搜索',
            buttonAriaLabel: '搜索'
          },
          modal: {
            noResultsText: '没有找到结果',
            resetButtonTitle: '清除查询',
            footer: {
              selectText: '选择',
              navigateText: '导航'
            }
          }
        },
        searchOptions: {
          fuzzy: 0.3,
          prefix: true,
          boost: {
            title: 4,
            text: 2,
            tags: 3,
            category: 3
          }
        }
      }
    },

    // 侧边栏：每条 link 均指向真实存在的文件，无占位死链
    sidebar: {
      '/java/': [
        {
          text: 'Java 后端',
          items: [
            { text: '总览', link: '/java/' },
            { text: '🗺️ 学习路径图', link: '/java/learning-path' },
            {
              text: 'Java 语言',
              collapsed: false,
              items: [
                { text: 'Java 基础', link: '/java/basics/' },
                { text: '集合框架', link: '/java/basics/collection' },
                { text: 'Java 并发', link: '/java/concurrent/' },
                { text: 'JVM', link: '/java/jvm/' }
              ]
            },
            {
              text: 'Spring 框架',
              collapsed: false,
              items: [
                { text: 'Spring 总览', link: '/java/spring/' },
                { text: 'IoC 与 AOP', link: '/java/spring/ioc-aop' },
                { text: 'Spring 事务', link: '/java/spring/transaction' },
                { text: '循环依赖', link: '/java/spring/circular-dependency' }
              ]
            },
            {
              text: '数据库',
              collapsed: false,
              items: [
                { text: 'MySQL', link: '/java/mysql/' },
                { text: '索引', link: '/java/mysql/indexing' },
                { text: '事务与 MVCC', link: '/java/mysql/transaction-mvcc' },
                { text: '锁', link: '/java/mysql/lock' },
                { text: 'Redis', link: '/java/redis/' },
                { text: 'Redis 数据结构', link: '/java/redis/data-structures' },
                { text: '持久化与缓存问题', link: '/java/redis/persistence-cache-problems' },
                { text: 'MyBatis', link: '/java/mybatis/' }
              ]
            },
            {
              text: '中间件',
              collapsed: false,
              items: [
                { text: 'Kafka', link: '/java/kafka/' }
              ]
            },
            { text: '操作系统', link: '/java/os/' }
          ]
        }
      ],

      '/distributed/': [
        {
          text: '分布式 & 场景',
          items: [
            { text: '分布式总览', link: '/distributed/' },
            { text: '🗺️ 学习路径图', link: '/distributed/learning-path' },
            { text: '理论基础（CAP/Base/共识）', link: '/distributed/basics' },
            {
              text: '场景题',
              collapsed: false,
              items: [
                { text: '场景题概述', link: '/distributed/scenarios/' },
                { text: '接入与路由层', link: '/distributed/scenarios/gateway' },
                { text: '业务逻辑与处理层', link: '/distributed/scenarios/service' },
                { text: '数据持久化与异步层', link: '/distributed/scenarios/storage' }
              ]
            }
          ]
        }
      ],

      '/cs-basics/': [
        {
          text: '计算机基础',
          items: [
            { text: '计算机网络', link: '/cs-basics/network/' }
          ]
        }
      ],

      '/algorithm/': [
        {
          text: '算法与数据结构',
          items: [
            { text: '总览', link: '/algorithm/' },
            { text: '🗺️ 学习路径图', link: '/algorithm/learning-path' },
            { text: '算法框架', link: '/algorithm/00-algorithm-frameworks/' },
            { text: '方法论', link: '/algorithm/01-methodology/' },
            { text: '数据结构', link: '/algorithm/02-data-structures/' },
            { text: '算法模式', link: '/algorithm/03-algorithm-patterns/' },
            { text: '系统算法', link: '/algorithm/04-system-algorithms/' },
            { text: '面试 Top 100', link: '/algorithm/05-top-interview-100/' },
            { text: '专项练习', link: '/algorithm/06-practice/' }
          ]
        }
      ],

      '/algorithm/06-practice/': [
        {
          text: '专项练习（框架→习题）',
          collapsed: true,
          items: [
            { text: '总览', link: '/algorithm/06-practice/' },
            { text: '滑动窗口', link: '/algorithm/06-practice/sliding-window-practice' },
            { text: '二分查找', link: '/algorithm/06-practice/binary-search-practice' },
            { text: '二叉树 I（基础遍历）', link: '/algorithm/06-practice/binary-tree-practice-i' },
            { text: 'DFS/BFS I（网格与图）', link: '/algorithm/06-practice/dfs-bfs-practice-i' },
            { text: '动态规划 I（一维入门）', link: '/algorithm/06-practice/dynamic-programming-practice-i' },
            { text: '回溯 I（排列组合子集）', link: '/algorithm/06-practice/backtrack-practice-i' },
            { text: '二叉树 II（构造与路径）', link: '/algorithm/06-practice/binary-tree-practice-ii' },
            { text: 'DFS/BFS II（状态与组合）', link: '/algorithm/06-practice/dfs-bfs-practice-ii' },
            { text: '动态规划 II（二维背包）', link: '/algorithm/06-practice/dynamic-programming-practice-ii' }
          ]
        }
      ],

      '/algorithm/00-algorithm-frameworks/': [
        {
          text: '算法框架',
          items: [
            { text: '框架总览', link: '/algorithm/00-algorithm-frameworks/' },
            { text: '左右指针', link: '/algorithm/00-algorithm-frameworks/left-right-pointers/' },
            { text: '滑动窗口', link: '/algorithm/00-algorithm-frameworks/sliding-window/' },
            { text: 'DFS / BFS', link: '/algorithm/00-algorithm-frameworks/dfs-bfs/' },
            { text: '动态规划', link: '/algorithm/00-algorithm-frameworks/dynamic-programming/' },
            { text: '贪心算法', link: '/algorithm/00-algorithm-frameworks/greedy/' },
            { text: '并查集', link: '/algorithm/00-algorithm-frameworks/union-find/' },
            { text: '二分查找', link: '/algorithm/00-algorithm-frameworks/binary-search/' },
            { text: '最短路径', link: '/algorithm/00-algorithm-frameworks/shortest-path/' }
          ]
        }
      ],

      '/algorithm/01-methodology/': [
        {
          text: '方法论',
          items: [
            { text: '总览', link: '/algorithm/01-methodology/' },
            { text: '费曼技巧模板', link: '/algorithm/01-methodology/feynman-template' },
            { text: '时空复杂度指南', link: '/algorithm/01-methodology/complexity-guide' },
            { text: '工程化编码习惯', link: '/algorithm/01-methodology/coding-habits' }
          ]
        }
      ],

      '/algorithm/02-data-structures/': [
        {
          text: '数据结构',
          items: [
            { text: '总览', link: '/algorithm/02-data-structures/' },
            { text: '线性结构', link: '/algorithm/02-data-structures/linear/' },
            { text: '树形结构', link: '/algorithm/02-data-structures/tree/' },
            { text: '图论', link: '/algorithm/02-data-structures/graph/' },
            { text: '堆与前缀树', link: '/algorithm/02-data-structures/heap-and-trie/' }
          ]
        }
      ],

      '/algorithm/03-algorithm-patterns/': [
        {
          text: '算法模式',
          items: [
            { text: '总览', link: '/algorithm/03-algorithm-patterns/' },
            { text: '搜索', link: '/algorithm/03-algorithm-patterns/search/' },
            { text: '动态规划', link: '/algorithm/03-algorithm-patterns/dynamic-programming/' },
            { text: '优化', link: '/algorithm/03-algorithm-patterns/optimization/' },
            { text: '数学逻辑', link: '/algorithm/03-algorithm-patterns/math-logic/' }
          ]
        }
      ],

      '/algorithm/04-system-algorithms/': [
        {
          text: '系统算法',
          items: [
            { text: '总览', link: '/algorithm/04-system-algorithms/' },
            { text: '缓存', link: '/algorithm/04-system-algorithms/caching/' },
            { text: '负载均衡', link: '/algorithm/04-system-algorithms/load-balancing/' },
            { text: '限流', link: '/algorithm/04-system-algorithms/rate-limiting/' },
            { text: '分布式 ID', link: '/algorithm/04-system-algorithms/unique-id/' },
            { text: '一致性哈希', link: '/algorithm/04-system-algorithms/consistent-hashing' }
          ]
        }
      ],

      '/algorithm/05-top-interview-100/': [
        {
          text: '面试 Top 100',
          items: [
            { text: '总览', link: '/algorithm/05-top-interview-100/' },
            { text: '数组', link: '/algorithm/05-top-interview-100/arrays/' },
            { text: '链表', link: '/algorithm/05-top-interview-100/linked-list/' },
            { text: '动态规划', link: '/algorithm/05-top-interview-100/dynamic-programming/' },
            { text: 'DFS / BFS', link: '/algorithm/05-top-interview-100/dfs-bfs/' },
            { text: '智力题', link: '/algorithm/05-top-interview-100/logic-puzzles/' }
          ]
        }
      ],

      '/ai/': [
        {
          text: 'AI Agent 知识库',
          items: [
            { text: '知识库总览', link: '/ai/' },
            { text: '🗺️ 学习路径图', link: '/ai/learning-path' },
            { text: '基础入门', link: '/ai/00-basics/' },
            { text: 'LLM 底座', link: '/ai/01-llm/' },
            { text: 'Agent 核心', link: '/ai/02-agent/' },
            { text: 'Memory Project', link: '/ai/02-agent/memory-project' },
            { text: 'MCP 协议', link: '/ai/03-mcp/' },
            { text: 'Skill 技能', link: '/ai/04-skills/' },
            { text: '工程落地', link: '/ai/05-engineering/' },
            { text: '系统设计', link: '/ai/05-engineering/system-design' },
            { text: '数据工程', link: '/ai/05-engineering/data-pipeline' },
            { text: '部署', link: '/ai/05-engineering/deployment' },
            { text: '监控与可观测性', link: '/ai/05-engineering/monitoring' },
            { text: '安全工程', link: '/ai/05-engineering/security' },
            { text: 'RAG', link: '/ai/06-RAG/' }
          ]
        }
      ],

      '/projects/': [
        {
          text: '项目实战',
          items: [
            { text: '智能面试助手', link: '/projects/interview-agent/' },
            { text: '🗺️ 学习路径图', link: '/projects/learning-path' },
            { text: '环境搭建', link: '/projects/interview-agent/setup/' },
            { text: 'Agent 基础', link: '/projects/interview-agent/agent-basics/' },
            { text: 'MCP 协议', link: '/projects/interview-agent/mcp-protocol/' },
            { text: 'Skill 开发', link: '/projects/interview-agent/skill-development/' },
            { text: '项目运行', link: '/projects/interview-agent/run/' },
            { text: '扩展教程', link: '/projects/interview-agent/extension/' }
          ]
        }
      ]
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/handsomeyx/my-interview-king' }
    ]
  }
})
