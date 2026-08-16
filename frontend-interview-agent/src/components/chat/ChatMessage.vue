<template>
  <div class="chat-message" :class="[message.role, { streaming: message.isStreaming }]">
    <div class="avatar">
      {{ message.role === 'user' ? '🧑' : '🤖' }}
    </div>
    <div class="message-body">
      <div class="message-meta">
        <span class="role">{{ message.role === 'user' ? '你' : 'AI 助手' }}</span>
        <span class="time">{{ formatTime(message.createdAt) }}</span>
        <span v-if="message.isStreaming" class="streaming-badge">● 输出中</span>
      </div>
      <div class="message-content">
        <template v-if="message.content">
          <MarkdownRenderer :content="message.content" />
        </template>
        <div v-else class="empty-content">
          <span class="thinking-dot" />
          <span class="thinking-dot" />
          <span class="thinking-dot" />
        </div>
        <span v-if="message.isStreaming && message.content" class="typing-cursor">▍</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Message } from '@/types/chat'
import MarkdownRenderer from '@/components/common/MarkdownRenderer.vue'

defineProps<{
  message: Message
}>()

function formatTime(iso: string) {
  const d = new Date(iso)
  return d.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.chat-message {
  display: flex;
  gap: 12px;
  max-width: 85%;
}

.chat-message.streaming .message-content {
  border-color: var(--primary-color);
  box-shadow: 0 0 12px rgba(59, 130, 246, 0.15);
}

.user {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.assistant {
  align-self: flex-start;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.user .avatar {
  background: var(--primary-color);
}

.assistant .avatar {
  background: var(--secondary-color);
}

.message-body {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.user .message-body {
  align-items: flex-end;
}

.message-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.role {
  font-weight: 600;
}

.streaming-badge {
  color: var(--primary-color);
  font-size: 0.7rem;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.message-content {
  padding: 12px 16px;
  border-radius: 12px;
  line-height: 1.6;
  max-width: 100%;
  overflow-x: auto;
  position: relative;
}

.user .message-content {
  background: var(--user-bubble);
  border: 1px solid var(--primary-color);
  border-top-right-radius: 4px;
}

.assistant .message-content {
  background: var(--glass-bg);
  border: 1px solid var(--border-color);
  border-top-left-radius: 4px;
}

.empty-content {
  display: flex;
  gap: 4px;
  padding: 4px 0;
}

.thinking-dot {
  width: 8px;
  height: 8px;
  background: var(--primary-color);
  border-radius: 50%;
  animation: thinking 1.4s infinite ease-in-out both;
}

.thinking-dot:nth-child(1) { animation-delay: -0.32s; }
.thinking-dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes thinking {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

.typing-cursor {
  display: inline-block;
  margin-left: 2px;
  color: var(--primary-color);
  animation: blink 0.8s step-end infinite;
}

@keyframes blink {
  50% { opacity: 0; }
}
</style>
