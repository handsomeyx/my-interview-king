<template>
  <aside class="app-sidebar">
    <div class="sidebar-section">
      <div
        class="sidebar-item"
        :class="{ active: !chatStore.currentChatId }"
        @click="handleNewInterview"
      >
        <span class="icon">✨</span>
        <span>新面试</span>
      </div>
    </div>

    <div class="sidebar-section history-section">
      <div class="sidebar-header">历史记录</div>
      <div v-if="chatStore.chats.length === 0" class="empty-hint">暂无历史对话</div>
      <div v-else class="history-list">
        <div
          v-for="chat in chatStore.chats"
          :key="chat.id"
          class="history-item"
          :class="{ active: chat.id === chatStore.currentChatId }"
          @click="chatStore.switchChat(chat.id)"
        >
          <span class="history-title">{{ chat.title }}</span>
          <span class="history-preview">{{ chat.preview || '暂无消息' }}</span>
          <button
            class="delete-btn"
            @click.stop="handleDelete(chat.id)"
            title="删除对话"
          >
            ✕
          </button>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { useChatStore } from '@/stores/chat'

const chatStore = useChatStore()

function handleNewInterview() {
  chatStore.createChat()
  chatStore.persist()
}

function handleDelete(id: string) {
  chatStore.deleteChat(id)
  chatStore.persist()
}
</script>

<style scoped>
.app-sidebar {
  width: 260px;
  height: 100%;
  background: var(--sidebar-color);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar-section {
  padding: 12px;
}

.sidebar-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
}

.sidebar-item:hover {
  background: var(--glass-bg);
  border: 1px solid var(--border-color);
}

.sidebar-item.active {
  background: var(--primary-color);
  color: white;
}

.sidebar-item .icon {
  font-size: 1.1rem;
}

.history-section {
  flex: 1;
  overflow-y: auto;
  border-top: 1px solid var(--border-color);
}

.sidebar-header {
  font-size: 0.85rem;
  color: var(--text-secondary);
  font-weight: 600;
  padding: 8px 14px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.empty-hint {
  text-align: center;
  color: var(--text-secondary);
  font-size: 0.85rem;
  padding: 30px 10px;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.history-item {
  position: relative;
  padding: 10px 14px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.history-item:hover {
  background: var(--glass-bg);
  border-color: var(--border-color);
}

.history-item.active {
  background: var(--user-bubble);
  border-color: var(--primary-color);
}

.history-title {
  display: block;
  font-weight: 500;
  font-size: 0.9rem;
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.history-preview {
  display: block;
  font-size: 0.8rem;
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.delete-btn {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 2px 6px;
  border-radius: 4px;
  opacity: 0;
  transition: all 0.2s ease;
}

.history-item:hover .delete-btn {
  opacity: 1;
}

.delete-btn:hover {
  background: var(--accent-color);
  color: white;
}
</style>
