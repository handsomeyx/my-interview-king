import { defineConfig } from 'vitepress'

export default defineConfig({
  title: "我是面试大王",
  description: "沉淀知识，对齐面试逻辑",
  themeConfig: {
    // 顶部导航栏
    nav: [
      { text: '首页', link: '/' },
      {
        text: '后端开发',
        items: [
          { text: 'Java 基础', link: '/java-basics/' },
          { 
            text: '分布式与中间件', 
            items: [
              { text: 'Redis', link: '/redis/' },
              { text: 'MySQL', link: '/mysql/' },
              { text: 'Kafka', link: '/kafka/' },
              { text: '分布式理论', link: '/distributed/' }
            ]
          }
        ]
      },
// 预留 AI Agent 位置
      {
        text: 'AI 实验室',
        items: [
          { text: 'Agent 开发指南', link: '/agent/' },
          { text: 'RAG 实战', link: '/rag/' }
        ]
      },

      { text: '关于我', link: '/about' }
    ],

    // 侧边栏
    sidebar: {
      '/java-basics/': [
        {
          text: 'Java 基础专栏',
          items: [
            { text: '基础语法', link: '/java-basics/index' },
            { text: '集合框架', link: '/java-basics/collection' },
          ]
        }
      ],
      '/redis/': [
        {
          text: 'Redis 深度解析',
          items: [
            { text: '核心原理', link: '/redis/index' },
            { text: '数据结构', link: '/redis/data-structures' },
          ]
        }
      ],
      '/mysql/': [
        {
          text: 'MySQL 详解',
          items: [
            { text: 'MySQL 基础', link: '/mysql/index' },
            { text: '索引原理', link: '/mysql/indexing' },
          ]
        }
      ],
      '/kafka/': [
        {
          text: 'Kafka 消息队列',
          items: [{ text: '入门指南', link: '/kafka/index' }]
        }
      ],
      '/distributed/': [
        {
          text: '分布式核心',
          items: [{ text: '分布式基础', link: '/distributed/index' }]
        }
      ]
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/handsomeyx/my-interview-king' }
    ]
  }
})