<template>
  <main class="app-main">
    <div class="chat-area">
      <div class="messages-container" ref="messagesContainer">
        <div v-if="!chatStore.currentChat || chatStore.currentChat.messages.length === 0" class="empty-state">
          <div class="empty-icon">💬</div>
          <div class="empty-text">
            <h2>开始你的面试之旅</h2>
            <p>输入一个面试问题，AI 将为你提供专业的回答</p>
          </div>
          <div class="suggestions">
            <button
              v-for="s in suggestions"
              :key="s"
              class="suggestion-btn"
              @click="sendSuggestion(s)"
            >
              {{ s }}
            </button>
          </div>
        </div>
        <template v-else>
          <ChatMessage
            v-for="msg in chatStore.currentChat.messages"
            :key="msg.id"
            :message="msg"
          />
          <div v-if="chatStore.isStreaming" class="streaming-indicator">
            <span class="cursor">▍</span>
            <span class="streaming-text">AI 正在思考...</span>
          </div>
        </template>
      </div>

      <ChatInput
        :disabled="chatStore.isStreaming"
        @send="handleSend"
      />
    </div>

    <div class="panels-area">
      <ConfidencePanel :score="confidenceScore" />
      <FollowUpPanel :questions="followUps" @select="handleFollowUp" />
      <KnowledgeGraph :nodes="knowledgeNodes" />
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { useChatStore } from '@/stores/chat'
import { useUserStore } from '@/stores/user'
import { useSSE } from '@/composables/useSSE'
import ChatMessage from '@/components/chat/ChatMessage.vue'
import ChatInput from '@/components/chat/ChatInput.vue'
import ConfidencePanel from '@/components/panels/ConfidencePanel.vue'
import FollowUpPanel from '@/components/panels/FollowUpPanel.vue'
import KnowledgeGraph from '@/components/panels/KnowledgeGraph.vue'
import type { KGNode } from '@/types/chat'

const chatStore = useChatStore()
const userStore = useUserStore()
const { connect, isStreaming } = useSSE()

const confidenceScore = ref(0)
const followUps = ref<string[]>([])
const knowledgeNodes = ref<KGNode[]>([])
const messagesContainer = ref<HTMLElement | null>(null)

const suggestions = [
  'TCP 三次握手过程？',
  'JVM 内存模型是怎样的？',
  'Spring IoC 原理是什么？',
  'Redis 缓存穿透怎么解决？'
]

async function handleSend(message: string) {
  if (!chatStore.currentChatId) {
    chatStore.createChat()
  }
  const chatId = chatStore.currentChatId!

  chatStore.addMessage(chatId, {
    id: crypto.randomUUID(),
    chatId,
    role: 'user',
    content: message,
    createdAt: new Date().toISOString()
  })

  const assistantId = crypto.randomUUID()
  chatStore.addMessage(chatId, {
    id: assistantId,
    chatId,
    role: 'assistant',
    content: '',
    createdAt: new Date().toISOString(),
    isStreaming: true
  })

  chatStore.setStreaming(true)
  scrollToBottom()

  const payload: Record<string, unknown> = { message }
  payload.chat_id = chatId
  if (userStore.guestId) {
    payload.guest_id = userStore.guestId
  }

  try {
    const events = await connect('/api/ai/chat/stream', payload)

    for (const event of events) {
      if (event.type === 'token' && event.content) {
        chatStore.appendMessageContent(chatId, assistantId, event.content)
        scrollToBottom()
      } else if (event.type === 'meta') {
        if (event.confidence !== undefined) {
          confidenceScore.value = event.confidence
          chatStore.setMessageConfidence(chatId, assistantId, event.confidence)
        }
        if (event.followUps) followUps.value = event.followUps
        if (event.knowledgeGraph) knowledgeNodes.value = event.knowledgeGraph
      } else if (event.type === 'error') {
        chatStore.finalizeMessage(chatId, assistantId, `⚠️ ${event.error}`)
        break
      } else if (event.type === 'done') {
        const msg = chatStore.currentChat?.messages.find(m => m.id === assistantId)
        chatStore.finalizeMessage(chatId, assistantId, msg?.content || '（空回复）')
      }
    }
  } catch (err: any) {
    chatStore.finalizeMessage(chatId, assistantId, `⚠️ 请求失败：${err?.message || '请检查后端服务是否启动'}`)
  } finally {
    chatStore.setStreaming(false)
    chatStore.persist()
    scrollToBottom()
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

function sendSuggestion(text: string) {
  handleSend(text)
}

function handleFollowUp(question: string) {
  handleSend(question)
}
</script>

<style scoped>
.app-main {
  flex: 1;
  display: flex;
  overflow: hidden;
  min-width: 0;
}

.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-width: 0;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 40px;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 16px;
}

.empty-text h2 {
  font-size: 1.5rem;
  margin-bottom: 8px;
}

.empty-text p {
  color: var(--text-secondary);
  margin-bottom: 24px;
}

.suggestions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  max-width: 500px;
}

.suggestion-btn {
  padding: 8px 16px;
  background: var(--glass-bg);
  border: 1px solid var(--border-color);
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.85rem;
}

.suggestion-btn:hover {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.streaming-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
  color: var(--text-secondary);
  font-size: 0.85rem;
}

.streaming-indicator .cursor {
  animation: blink 0.8s step-end infinite;
  color: var(--primary-color);
}

@keyframes blink {
  50% { opacity: 0; }
}

.panels-area {
  width: 280px;
  flex-shrink: 0;
  padding: 16px;
  background: var(--bg-soft);
  border-left: 1px solid var(--border-color);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
</style>
