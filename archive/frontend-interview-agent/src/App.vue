<template>
  <!-- 动态弥散光晕背景 -->
  <div class="gradient-bg"></div>

  <!-- 顶部导航栏 -->
  <div class="top-nav">
    <div class="nav-left">
      <h1 class="app-title">智能面试助手</h1>
    </div>
    <div class="nav-right">
      <div v-if="user.is_logged_in" class="user-info">
        <span class="username">{{ user.username }}</span>
        <button @click="logout" class="logout-button">登出</button>
      </div>
      <div v-else class="auth-buttons">
        <button @click="showLoginModal = true" class="login-button">登录</button>
        <button @click="showRegisterModal = true" class="register-button">注册</button>
      </div>
    </div>
  </div>

  <div class="app-container">
    <!-- 左侧导航栏 -->
    <div class="sidebar">
      <div class="sidebar-item" :class="{ active: activeSidebar === 'new' }" @click="handleNewInterview">
        <span>✨</span>
        <span>新面试</span>
      </div>
      <div class="sidebar-item" :class="{ active: activeSidebar === 'history' }" @click="handleHistoryClick">
        <span>📚</span>
        <span>历史记录</span>
        <span class="sidebar-badge" v-if="chats.length > 0">{{ chats.length }}</span>
      </div>
      <div class="sidebar-item" :class="{ active: activeSidebar === 'career' }" @click="activeSidebar = 'career'">
        <span>💼</span>
        <span>职业建议</span>
      </div>
      <div class="sidebar-item" :class="{ active: activeSidebar === 'settings' }" @click="activeSidebar = 'settings'">
        <span>⚙️</span>
        <span>设置</span>
      </div>
      
      <!-- 历史记录列表 -->
      <div v-if="activeSidebar === 'history'" class="history-list">
        <div 
          v-for="chat in chats" 
          :key="chat.id"
          class="history-item"
          :class="{ active: currentChatId === chat.id }"
          @click="switchChat(chat.id)"
        >
          <div class="history-title">{{ chat.title }}</div>
          <div class="history-preview">{{ chat.preview }}</div>
          <div class="history-actions">
            <button class="history-delete" @click.stop="deleteChat(chat.id)">
              🗑️
            </button>
          </div>
        </div>
        <div v-if="chats.length === 0" class="history-empty">
          <span>暂无历史记录</span>
        </div>
      </div>
    </div>

    <!-- 右侧聊天区域 -->
    <div class="chat-container">
      <!-- 聊天头部 -->
      <div class="chat-header">
        <div class="chat-title">智能面试助手 (Mentor Mode)</div>
        <div class="flex gap-8 text-sm text-text-secondary">
          <span>快速</span>
          <span>专业</span>
          <span>个性化</span>
        </div>
      </div>

      <!-- 消息区域 -->
      <div class="message-area" ref="chatMessages">
        <!-- 空状态 -->
        <div v-if="!currentChat || currentChat.messages.length === 0" class="empty-state">
          <div class="empty-state-icon">
            <span class="text-4xl">🤖</span>
          </div>
          <div class="empty-state-title">您好啊，这里是智能的面试大王，A卷助手</div>
          <div class="empty-state-subtitle">请问你有什么想问的呢？我会为你提供结构化的面试建议和实战指导。</div>
          <div class="quick-questions">
            <div class="quick-question" @click="askQuestion('解释一下什么是 TCP/IP 协议？')">
              <span style="color: var(--primary-color)">→</span> 解释一下什么是 TCP/IP 协议？
            </div>
            <div class="quick-question" @click="askQuestion('如何实现线程安全的单例模式？')">
              <span style="color: var(--primary-color)">→</span> 如何实现线程安全的单例模式？
            </div>
            <div class="quick-question" @click="askQuestion('什么是分布式系统的 CAP 理论？')">
              <span style="color: var(--primary-color)">→</span> 什么是分布式系统的 CAP 理论？
            </div>
          </div>
        </div>

        <!-- 消息列表 -->
        <div v-for="(message, index) in currentChat?.messages || []" :key="index" class="message" :class="message.role">
          <div class="message-avatar" :class="message.role">
            {{ message.role === 'user' ? '👤' : '🤖' }}
          </div>
          <div class="message-content">
            <div v-if="message.role === 'user'" class="message-bubble">
              <div class="message-text">{{ message.content }}</div>
            </div>
            <div v-else class="ai-answer">
              <span class="answer-tag" v-if="message.tag">{{ message.tag }}</span>
              <div class="answer-content" v-html="renderMarkdown(message.content)"></div>
              <div class="feedback-icons">
                <div class="feedback-icon">👍 有用</div>
                <div class="feedback-icon">👎 没用</div>
                <div class="feedback-icon">📋 复制</div>
                <div class="feedback-icon">✏️ 重写</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 加载状态 -->
        <div v-if="isLoading" class="loading-state">
          <div class="thinking-animation">
            <span>🤖</span>
          </div>
          <div class="loading-text">智能面试助手正在思考中...</div>
        </div>
        
        <!-- AI回答控制 -->
        <div v-if="isStreaming" class="streaming-controls">
          <button class="streaming-control-button" @click="togglePauseStreaming">
            {{ isStreamingPaused ? '▶ 继续' : '⏸ 暂停' }}
          </button>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="input-area">
        <div class="input-toolbar">
          <button class="tool-button" @click="triggerFileUpload" title="上传文件">
            📁
          </button>
          <button class="tool-button" @click="triggerImageUpload" title="上传图片">
            🖼️
          </button>
          <div class="voice-recording-controls">
            <button class="tool-button" @click="toggleVoiceRecording" :title="isRecording ? '停止录音' : '开始录音'">
              <div v-if="isRecording" class="voice-wave">
                <span></span><span></span><span></span><span></span><span></span>
              </div>
              <span v-else>🎤</span>
            </button>
            <button v-if="isRecording" class="tool-button" @click="togglePauseRecording" :title="isPaused ? '继续录音' : '暂停录音'">
              {{ isPaused ? '▶' : '⏸' }}
            </button>
          </div>
        </div>
        <div class="input-container">
          <div class="input-box">
            <div v-if="recordingStatus" class="recording-status">
              {{ recordingStatus }}
            </div>
            <textarea
              v-model="userInput"
              @keyup.enter="isStreaming ? stopStreaming() : sendMessage()"
              placeholder="输入你的问题... (Enter 发送/终止)"
              class="input-textarea"
              rows="2"
              :disabled="isLoading"
            ></textarea>
          </div>
          <button @click="isStreaming ? stopStreaming() : sendMessage()" class="send-button" :disabled="isLoading && !isStreaming">
            {{ isStreaming ? '⏹' : '➤' }}
          </button>
        </div>
        
        <!-- 隐藏的文件输入 -->
        <input type="file" ref="fileInput" class="hidden" @change="handleFileUpload">
        <input type="file" ref="imageInput" class="hidden" accept="image/*" @change="handleImageUpload">
      </div>
    </div>

    <!-- 智能分析面板 -->
    <div class="analysis-panel">
      <div class="analysis-card">
        <div class="analysis-card-title">信心仪表盘</div>
        <div class="confidence-dashboard">
          <div class="flex justify-between items-center mb-4">
            <span>整体信心指数</span>
            <span class="text-primary-color font-medium">{{ confidenceScore }}%</span>
          </div>
          <div class="confidence-meter">
            <div class="confidence-fill" :style="{ width: confidenceScore + '%' }"></div>
          </div>
          <div class="mt-4 text-sm text-text-secondary">
            <p>基于您的回答质量和专业程度评估</p>
          </div>
        </div>
      </div>

      <div class="analysis-card">
        <div class="analysis-card-title">知识图谱</div>
        <div class="knowledge-graph">
          <div 
            v-for="(node, index) in knowledgeGraph" 
            :key="index"
            class="knowledge-node"
            :class="node.strength"
          >
            {{ node.name }}
          </div>
        </div>
      </div>

      <div class="analysis-card">
        <div class="analysis-card-title">智能追问链</div>
        <div class="text-sm text-text-secondary">
          <p>基于您的回答，AI 将重点关注以下方向：</p>
          <ul class="mt-2 space-y-2">
            <li v-for="(question, index) in followUpQuestions" :key="index">
              {{ index + 1 }}. {{ question }}
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- 登录模态框 -->
    <div v-if="showLoginModal" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h2>用户登录</h2>
          <button @click="showLoginModal = false" class="close-button">×</button>
        </div>
        <div class="modal-body">
          <div v-if="loginError" class="error-message">{{ loginError }}</div>
          <div class="form-group">
            <label>用户名</label>
            <input v-model="loginForm.username" type="text" class="form-input" placeholder="请输入用户名">
          </div>
          <div class="form-group">
            <label>密码</label>
            <input v-model="loginForm.password" type="password" class="form-input" placeholder="请输入密码">
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showLoginModal = false" class="btn-secondary">取消</button>
          <button @click="login" class="btn-primary">登录</button>
        </div>
      </div>
    </div>

    <!-- 注册模态框 -->
    <div v-if="showRegisterModal" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h2>用户注册</h2>
          <button @click="showRegisterModal = false" class="close-button">×</button>
        </div>
        <div class="modal-body">
          <div v-if="registerError" class="error-message">{{ registerError }}</div>
          <div class="form-group">
            <label>用户名</label>
            <input v-model="registerForm.username" type="text" class="form-input" placeholder="请输入用户名">
          </div>
          <div class="form-group">
            <label>密码</label>
            <input v-model="registerForm.password" type="password" class="form-input" placeholder="请输入密码">
          </div>
          <div class="form-group">
            <label>邮箱</label>
            <input v-model="registerForm.email" type="email" class="form-input" placeholder="请输入邮箱">
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showRegisterModal = false" class="btn-secondary">取消</button>
          <button @click="register" class="btn-primary">注册</button>
        </div>
      </div>
    </div>

    <!-- 智能工具盘 -->
    <div class="floating-toolbar">
      <button class="fab" @click="toggleFabMenu">
        {{ showFabMenu ? '✕' : '➕' }}
      </button>
      <div v-if="showFabMenu" class="fab-menu">
        <div class="fab-menu-item">常见面试题库</div>
        <div class="fab-menu-item">自我评价模板</div>
        <div class="fab-menu-item">面试技巧指南</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, onMounted } from 'vue';

// 类型定义
interface Message {
  role: 'user' | 'assistant';
  content: string;
  tag?: string;
}

interface Chat {
  id: string;
  title: string;
  preview: string;
  messages: Message[];
}

// 状态管理
const chats = ref<Chat[]>([]);
const currentChatId = ref<string | null>(null);
const userInput = ref('');
const isLoading = ref(false);
const chatMessages = ref<HTMLElement | null>(null);
const streamingContent = ref('');
const isStreaming = ref(false);
const isStreamingPaused = ref(false);

// 智能分析相关状态
const followUpQuestions = ref<string[]>([]);
const knowledgeGraph = ref<Array<{name: string, strength: string}>>([]);
const confidenceScore = ref(75);

// 用户相关状态
const user = ref<{is_logged_in: boolean, user_id: string, username: string, is_guest: boolean}>({
  is_logged_in: false,
  user_id: '',
  username: '',
  is_guest: true
});
const guestId = ref('');
const chatCount = ref(0);
const limit = ref(3);

// 登录注册模态框状态
const showLoginModal = ref(false);
const showRegisterModal = ref(false);
const loginForm = ref({username: '', password: ''});
const registerForm = ref({username: '', password: '', email: ''});
const loginError = ref('');
const registerError = ref('');

// 新增：文件上传相关
const fileInput = ref<HTMLInputElement | null>(null);
const imageInput = ref<HTMLInputElement | null>(null);

// 新增：浮动工具栏
const showFabMenu = ref(false);

// 新增：侧边栏
const activeSidebar = ref('new');

// 计算属性：当前聊天
const currentChat = computed(() => {
  return chats.value.find(chat => chat.id === currentChatId.value) || null;
});

// 初始化聊天记录
const initChats = () => {
  const savedChats = localStorage.getItem('interview-agent-chats');
  if (savedChats) {
    chats.value = JSON.parse(savedChats);
    if (chats.value.length > 0) {
      currentChatId.value = chats.value[0].id;
    }
  } else {
    newChat();
  }
};

// 保存聊天记录到本地存储
const saveChats = () => {
  localStorage.setItem('interview-agent-chats', JSON.stringify(chats.value));
};

// 新建对话
const newChat = () => {
  const newChatId = Date.now().toString();
  const newChat: Chat = {
    id: newChatId,
    title: '新对话',
    preview: '',
    messages: []
  };
  
  chats.value.unshift(newChat);
  currentChatId.value = newChatId;
  saveChats();
};



// 渲染 Markdown
const renderMarkdown = (content: string) => {
  if (!content) return '';
  // 简单的 Markdown 渲染，实际项目中可以使用 marked 库
  return content
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/\n\* (.*$)/gim, '<li>$1</li>')
    .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
    .replace(/`(.*?)`/gim, '<code>$1</code>')
    .replace(/```([\s\S]*?)```/gim, '<pre><code>$1</code></pre>');
};

// 滚动到最新消息
const scrollToBottom = () => {
  nextTick(() => {
    if (chatMessages.value) {
      // 强制滚动到最底部
      chatMessages.value.scrollTop = chatMessages.value.scrollHeight;
      // 确保滚动生效
      setTimeout(() => {
        if (chatMessages.value) {
          chatMessages.value.scrollTop = chatMessages.value.scrollHeight;
        }
      }, 100);
    }
  });
};

// 流式输出模拟
const streamResponse = async (fullContent: string, messageIndex: number) => {
  isStreaming.value = true;
  isStreamingPaused.value = false;
  streamingContent.value = '';
  
  const chars = fullContent.split('');
  for (let i = 0; i < chars.length; i++) {
    // 检查是否暂停
    if (isStreamingPaused.value) {
      // 等待直到继续
      await new Promise(resolve => {
        const checkInterval = setInterval(() => {
          if (!isStreamingPaused.value) {
            clearInterval(checkInterval);
            resolve(null);
          }
        }, 100);
      });
    }
    
    streamingContent.value += chars[i];
    if (currentChat.value && currentChat.value.messages[messageIndex]) {
      currentChat.value.messages[messageIndex].content = streamingContent.value;
    }
    
    // 每10个字符滚动一次，避免过于频繁
    if (i % 10 === 0) {
      scrollToBottom();
    }
    
    // 模拟打字速度
    await new Promise(resolve => setTimeout(resolve, 20));
  }
  
  isStreaming.value = false;
  isStreamingPaused.value = false;
  scrollToBottom();
  saveChats();
};

// 发送消息
const sendMessage = async () => {
  const message = userInput.value.trim();
  if (!message || isLoading.value) return;
  
  // 如果没有当前聊天，自动创建一个
  if (!currentChat.value) {
    newChat();
  }
  
  // 添加用户消息
  currentChat.value!.messages.push({
    role: 'user',
    content: message
  });
  
  // 更新对话预览和标题
  currentChat.value!.preview = message.length > 50 ? message.substring(0, 50) + '...' : message;
  if (currentChat.value!.title === '新对话') {
    currentChat.value!.title = currentChat.value!.preview;
  }
  
  // 清空输入框
  userInput.value = '';
  
  // 滚动到最新消息
  scrollToBottom();
  
  // 保存聊天记录
  saveChats();
  
  // 显示加载状态
  isLoading.value = true;
  
  try {
    // 调用后端 API
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include', // 包含cookie
      body: JSON.stringify({ message, guest_id: guestId.value })
    });
    
    if (response.ok) {
      const data = await response.json();
      
      // 更新对话次数
      if (data.chat_count !== undefined) {
        chatCount.value = data.chat_count;
      }
      
      // 更新智能分析相关状态
      if (data.follow_up_questions) {
        followUpQuestions.value = data.follow_up_questions;
      }
      if (data.knowledge_graph) {
        knowledgeGraph.value = data.knowledge_graph;
      }
      if (data.confidence_score) {
        confidenceScore.value = data.confidence_score;
      }
      
      // 添加 AI 消息（初始为空）
      const messageIndex = currentChat.value!.messages.length;
      currentChat.value!.messages.push({
        role: 'assistant',
        content: ''
      });
      
      // 流式输出
      await streamResponse(data.response, messageIndex);
      
    } else if (response.status === 403) {
      // 对话次数限制
      const data = await response.json();
      alert(data.error);
      showLoginModal.value = true;
    } else {
      // API 错误，使用模拟数据
      const mockResponse = generateMockResponse(message);
      const messageIndex = currentChat.value!.messages.length;
      currentChat.value!.messages.push({
        role: 'assistant',
        content: ''
      });
      await streamResponse(mockResponse, messageIndex);
    }
  } catch (error) {
    console.error('Error:', error);
    // 网络错误，使用模拟数据
    const mockResponse = generateMockResponse(message);
    const messageIndex = currentChat.value!.messages.length;
    currentChat.value!.messages.push({
      role: 'assistant',
      content: ''
    });
    await streamResponse(mockResponse, messageIndex);
  } finally {
    isLoading.value = false;
    scrollToBottom();
    saveChats();
  }
};

// 生成模拟响应（根据用户问题生成不同的回答）
const generateMockResponse = (question: string) => {
  const responses: Record<string, string> = {
    'tcp': `# TCP/IP 协议详解

## 核心概念
TCP/IP 是互联网的基础协议套件，包含两个核心协议：

### 1. TCP（传输控制协议）
- **面向连接**：建立连接需要三次握手
- **可靠传输**：通过确认机制和重传机制保证数据完整性
- **流量控制**：使用滑动窗口机制
- **拥塞控制**：避免网络拥塞

### 2. IP（网际协议）
- **无连接**：不保证数据包的顺序和完整性
- **寻址**：使用 IP 地址标识网络设备
- **路由**：确定数据包传输路径

## 协议层次
\`\`\`
应用层 → HTTP/FTP/DNS
传输层 → TCP/UDP
网络层 → IP/ICMP
链路层 → Ethernet/WiFi
\`\`\`

## 面试要点
- 三次握手和四次挥手的过程
- TCP 和 UDP 的区别
- 滑动窗口机制
- TIME_WAIT 状态的作用`,

    'jvm': `# JVM 内存模型详解

## 内存区域划分

### 1. 堆（Heap）
- 存放对象实例
- 分为年轻代和老年代
- 垃圾回收的主要区域

### 2. 栈（Stack）
- 存放局部变量
- 方法调用的上下文
- 线程私有

### 3. 方法区（Method Area）
- 类信息、常量、静态变量
- JDK 8 后改为元空间（Metaspace）

## 垃圾回收

### 垃圾回收算法
- **标记-清除**：简单但产生碎片
- **复制算法**：新生代使用，效率高
- **标记-整理**：老年代使用，避免碎片

### 垃圾回收器
\`\`\`
Serial → 单线程，适合小应用
Parallel → 多线程，注重吞吐量
CMS → 低延迟，并发收集
G1 → 分区收集，平衡吞吐量和延迟
ZGC → 超低延迟，大堆内存
\`\`\`

## 面试要点
- 内存泄漏排查方法
- OOM 异常处理
- JVM 调优参数
- 类加载机制`,

    'spring': `# Spring Boot 核心原理

## 自动配置原理

### @SpringBootApplication
\`\`\`java
@SpringBootConfiguration
@EnableAutoConfiguration
@ComponentScan
public @interface SpringBootApplication {}
\`\`\`

### 自动配置流程
1. **读取 META-INF/spring.factories**
2. **条件判断**：@ConditionalOnClass, @ConditionalOnProperty
3. **配置加载**：加载默认配置
4. **用户配置覆盖**：application.properties

## 核心特性

### 1. 起步依赖（Starter）
- 简化 Maven 配置
- 自动版本管理

### 2. 内嵌服务器
- Tomcat/Jetty/Undertow
- 无需部署 WAR 包

### 3. Actuator 监控
- 健康检查
- 指标收集
- 端点暴露

## 面试要点
- IOC 容器原理
- AOP 实现机制
- 事务管理
- 微服务架构设计`,

    'default': `# 智能面试助手回答

## 核心知识点
- **概念理解**：这个问题涉及的核心概念是...
- **实际应用**：在实际项目中，我们通常...
- **最佳实践**：建议采用以下最佳实践...

## 示例代码
\`\`\`java
// 示例代码
public class Example {
    public void demonstrate() {
        // 核心逻辑实现
    }
}
\`\`\`

## 面试技巧
1. **结构化回答**：先讲概念，再讲原理，最后讲应用
2. **结合实际**：举例说明在实际项目中的应用
3. **深入原理**：不仅要知道是什么，还要知道为什么
4. **举一反三**：展示你对相关技术的理解

## 追问准备
面试官可能会继续问：
- 这个技术的优缺点是什么？
- 在什么场景下使用？
- 与其他技术的对比？

建议提前准备这些问题的答案。`
  };
  
  const lowerQuestion = question.toLowerCase();
  if (lowerQuestion.includes('tcp') || lowerQuestion.includes('ip') || lowerQuestion.includes('网络')) {
    return responses['tcp'];
  } else if (lowerQuestion.includes('jvm') || lowerQuestion.includes('内存') || lowerQuestion.includes('gc')) {
    return responses['jvm'];
  } else if (lowerQuestion.includes('spring') || lowerQuestion.includes('boot')) {
    return responses['spring'];
  } else {
    return responses['default'];
  }
};

// 新增：文件上传功能
const triggerFileUpload = () => {
  fileInput.value?.click();
};

const handleFileUpload = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (file) {
    // 这里可以添加文件上传逻辑
    console.log('Uploading file:', file.name);
    // 模拟文件上传成功
    if (currentChat.value) {
      currentChat.value.messages.push({
        role: 'user',
        content: `📁 上传了文件：${file.name}`
      });
      saveChats();
      scrollToBottom();
    }
  }
  // 重置文件输入
  target.value = '';
};

// 新增：图片上传功能
const triggerImageUpload = () => {
  imageInput.value?.click();
};

const handleImageUpload = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (file) {
    // 创建图片预览
    const reader = new FileReader();
    reader.onload = (e) => {
      const imageUrl = e.target?.result as string;
      if (currentChat.value) {
        currentChat.value.messages.push({
          role: 'user',
          content: `![图片](${imageUrl})`
        });
        saveChats();
        scrollToBottom();
      }
    };
    reader.readAsDataURL(file);
  }
  // 重置文件输入
  target.value = '';
};

// 语音输入相关状态
const isRecording = ref(false);
const isPaused = ref(false);
const recordingStatus = ref('');
const mediaStream = ref<MediaStream | null>(null);
const audioContext = ref<any>(null);
const processor = ref<any>(null);
const audioData = ref<Float32Array[]>([]);
const recordingTimer = ref<number | null>(null);
const speechRecognition = ref<any>(null);

// 新增：语音输入功能
const toggleVoiceRecording = () => {
  if (!isRecording.value) {
    startRecording();
  } else {
    stopRecording();
  }
};

// 开始录音
const startRecording = () => {
  console.log('开始录音...');
  recordingStatus.value = '正在录入...';
  
  // 检查浏览器是否支持Web Speech API
  if (!('SpeechRecognition' in window || 'webkitSpeechRecognition' in window)) {
    recordingStatus.value = '';
    alert('您的浏览器不支持语音识别功能，请使用Chrome、Edge等现代浏览器。');
    return;
  }
  
  // 清空输入框
  userInput.value = '';
  
  // 开始语音识别
  speechRecognition.value = startSpeechRecognition();
  isRecording.value = true;
  isPaused.value = false;
};

// 停止录音
const stopRecording = () => {
  console.log('停止录音');
  recordingStatus.value = '';
  
  // 停止语音识别
  if (speechRecognition.value) {
    speechRecognition.value.stop();
    speechRecognition.value = null;
  }
  
  if (mediaStream.value) {
    mediaStream.value.getTracks().forEach(track => track.stop());
    mediaStream.value = null;
  }
  
  if (processor.value) {
    processor.value.disconnect();
    processor.value = null;
  }
  
  if (audioContext.value) {
    audioContext.value.close();
    audioContext.value = null;
  }
  
  if (recordingTimer.value) {
    clearInterval(recordingTimer.value);
    recordingTimer.value = null;
  }
  
  isRecording.value = false;
  isPaused.value = false;
  
  // 获取语音识别结果
  const transcript = userInput.value.trim();
  console.log('语音识别结果:', transcript);
  
  // 将识别结果添加到聊天记录
  if (currentChat.value && transcript) {
    currentChat.value.messages.push({
      role: 'user',
      content: `🎤 语音输入：${transcript}`
    });
    saveChats();
    scrollToBottom();
    
    // 自动发送消息
    sendMessage();
  }
};

// 暂停/继续录音
const togglePauseRecording = () => {
  if (isRecording.value) {
    isPaused.value = !isPaused.value;
    recordingStatus.value = isPaused.value ? '已暂停' : '正在录入...';
    console.log(isPaused.value ? '暂停录音' : '继续录音');
    
    // 由于Web Speech API不直接支持暂停，我们通过停止并重新开始来模拟
    if (isPaused.value) {
      if (speechRecognition.value) {
        speechRecognition.value.stop();
        speechRecognition.value = null;
      }
    } else {
      speechRecognition.value = startSpeechRecognition();
    }
  }
};

// 暂停/继续AI回答
const togglePauseStreaming = () => {
  if (isStreaming.value) {
    isStreamingPaused.value = !isStreamingPaused.value;
    console.log(isStreamingPaused.value ? '暂停AI回答' : '继续AI回答');
  }
};

// 停止AI回答
const stopStreaming = () => {
  if (isStreaming.value) {
    isStreamingPaused.value = false;
    isStreaming.value = false;
    console.log('停止AI回答');
    // 这里可以添加额外的停止逻辑，比如取消网络请求等
  }
};

// 实现真正的语音识别
const startSpeechRecognition = () => {
  // 检查浏览器是否支持Web Speech API
  if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || (window as any).webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    
    // 配置语音识别
    recognition.lang = 'zh-CN'; // 设置为中文
    recognition.continuous = true; // 持续识别
    recognition.interimResults = true; // 返回中间结果
    
    // 识别结果回调
    recognition.onresult = (event: any) => {
      let transcript = '';
      for (let i = event.resultIndex; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript;
      }
      userInput.value = transcript;
      console.log('语音识别结果:', transcript);
    };
    
    // 识别结束的回调
    recognition.onend = () => {
      console.log('语音识别结束');
    };
    
    // 识别错误的回调
    recognition.onerror = (event: any) => {
      console.error('语音识别错误:', event.error);
    };
    
    // 开始识别
    recognition.start();
    return recognition;
  } else {
    alert('您的浏览器不支持语音识别功能，请使用Chrome、Edge等现代浏览器。');
    return null;
  }
};

// 新增：快速问题点击
const askQuestion = (question: string) => {
  userInput.value = question;
  sendMessage();
};

// 新增：浮动工具栏切换
const toggleFabMenu = () => {
  showFabMenu.value = !showFabMenu.value;
};

// 处理新面试点击
const handleNewInterview = () => {
  activeSidebar.value = 'new';
  newChat();
};

// 处理历史记录点击
const handleHistoryClick = () => {
  activeSidebar.value = 'history';
};

// 切换对话
const switchChat = (chatId: string) => {
  currentChatId.value = chatId;
  activeSidebar.value = 'new'; // 切换到聊天界面
};

// 删除对话
const deleteChat = (chatId: string) => {
  const index = chats.value.findIndex(chat => chat.id === chatId);
  if (index !== -1) {
    chats.value.splice(index, 1);
    saveChats();
    
    if (currentChatId.value === chatId) {
      currentChatId.value = chats.value.length > 0 ? chats.value[0].id : null;
    }
  }
};

// 生成气泡效果


// 加载用户信息
const loadUserInfo = async () => {
  try {
    const response = await fetch('/api/user', {
      method: 'GET',
      credentials: 'include' // 包含cookie
    });
    
    if (response.ok) {
      const data = await response.json();
      if (data.is_logged_in) {
        user.value = {
          is_logged_in: true,
          user_id: data.user_id,
          username: data.username,
          is_guest: data.is_guest
        };
      } else {
        user.value = {
          is_logged_in: false,
          user_id: '',
          username: '',
          is_guest: true
        };
        guestId.value = data.guest_id;
      }
    }
  } catch (error) {
    console.error('加载用户信息失败:', error);
  }
};

// 用户登录
const login = async () => {
  try {
    loginError.value = '';
    const response = await fetch('/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include', // 包含cookie
      body: JSON.stringify(loginForm.value)
    });
    
    if (response.ok) {
      const data = await response.json();
      user.value = {
        is_logged_in: true,
        user_id: data.user_id,
        username: data.username,
        is_guest: false
      };
      showLoginModal.value = false;
      loginForm.value = {username: '', password: ''};
    } else {
      const data = await response.json();
      loginError.value = data.error || '登录失败';
    }
  } catch (error) {
    console.error('登录失败:', error);
    loginError.value = '网络错误，请稍后重试';
  }
};

// 用户注册
const register = async () => {
  try {
    registerError.value = '';
    const response = await fetch('/api/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include', // 包含cookie
      body: JSON.stringify(registerForm.value)
    });
    
    if (response.ok) {
      const data = await response.json();
      user.value = {
        is_logged_in: true,
        user_id: data.user_id,
        username: data.username,
        is_guest: false
      };
      showRegisterModal.value = false;
      registerForm.value = {username: '', password: '', email: ''};
    } else {
      const data = await response.json();
      registerError.value = data.error || '注册失败';
    }
  } catch (error) {
    console.error('注册失败:', error);
    registerError.value = '网络错误，请稍后重试';
  }
};

// 用户登出
const logout = async () => {
  try {
    const response = await fetch('/api/logout', {
      method: 'POST',
      credentials: 'include' // 包含cookie
    });
    
    if (response.ok) {
      user.value = {
        is_logged_in: false,
        user_id: '',
        username: '',
        is_guest: true
      };
      // 重新加载用户信息获取新的guest_id
      await loadUserInfo();
    }
  } catch (error) {
    console.error('登出失败:', error);
  }
};

// 生命周期钩子
onMounted(() => {
  initChats();
  loadUserInfo();
  
  // 添加语音波形动画样式
  const style = document.createElement('style');
  style.textContent = `
    .voice-wave {
      display: flex;
      align-items: center;
      gap: 2px;
      height: 20px;
    }
    
    .voice-wave span {
      width: 2px;
      background: var(--primary-color);
      animation: voiceWave 1s ease-in-out infinite;
    }
    
    .voice-wave span:nth-child(1) { height: 10px; animation-delay: 0s; }
    .voice-wave span:nth-child(2) { height: 15px; animation-delay: 0.1s; }
    .voice-wave span:nth-child(3) { height: 20px; animation-delay: 0.2s; }
    .voice-wave span:nth-child(4) { height: 15px; animation-delay: 0.3s; }
    .voice-wave span:nth-child(5) { height: 10px; animation-delay: 0.4s; }
    
    @keyframes voiceWave {
      0%, 100% { transform: scaleY(0.5); }
      50% { transform: scaleY(1); }
    }
  `;
  document.head.appendChild(style);
});
</script>

<style scoped>
.hidden {
  display: none;
}
</style>