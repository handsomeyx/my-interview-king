import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Chat, Message } from '@/types/chat'

export const useChatStore = defineStore('chat', () => {
  const chats = ref<Chat[]>([])
  const currentChatId = ref<string | null>(null)
  const isLoading = ref(false)
  const isStreaming = ref(false)

  const currentChat = computed(() =>
    chats.value.find((c) => c.id === currentChatId.value) ?? null
  )

  function createChat(): Chat {
    const chat: Chat = {
      id: crypto.randomUUID(),
      title: '新面试',
      preview: '',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      messages: []
    }
    chats.value.unshift(chat)
    currentChatId.value = chat.id
    persist()
    return chat
  }

  function switchChat(id: string) {
    currentChatId.value = id
    persist()
  }

  function deleteChat(id: string) {
    const idx = chats.value.findIndex((c) => c.id === id)
    if (idx > -1) {
      chats.value.splice(idx, 1)
      if (currentChatId.value === id) {
        currentChatId.value = chats.value[0]?.id ?? null
      }
      persist()
    }
  }

  function addMessage(chatId: string, message: Message) {
    const chat = chats.value.find((c) => c.id === chatId)
    if (chat) {
      chat.messages.push(message)
      chat.preview = message.content.slice(0, 60)
      chat.updatedAt = new Date().toISOString()
      if (message.role === 'user') {
        chat.title = message.content.slice(0, 20) || chat.title
      }
      persist()
    }
  }

  function updateMessage(chatId: string, messageId: string, content: string) {
    const chat = chats.value.find((c) => c.id === chatId)
    const msg = chat?.messages.find((m) => m.id === messageId)
    if (msg) {
      msg.content = content
      persist()
    }
  }

  function appendMessageContent(chatId: string, messageId: string, delta: string) {
    const chat = chats.value.find((c) => c.id === chatId)
    const msg = chat?.messages.find((m) => m.id === messageId)
    if (msg) {
      msg.content += delta
      msg.isStreaming = true
      chat!.preview = msg.content.slice(0, 60)
      persist()
    }
  }

  function finalizeMessage(chatId: string, messageId: string, content: string) {
    const chat = chats.value.find((c) => c.id === chatId)
    const msg = chat?.messages.find((m) => m.id === messageId)
    if (msg) {
      msg.content = content
      msg.isStreaming = false
      chat!.preview = content.slice(0, 60)
      chat!.updatedAt = new Date().toISOString()
      persist()
    }
  }

  function setMessageConfidence(chatId: string, messageId: string, confidence: number) {
    const chat = chats.value.find((c) => c.id === chatId)
    const msg = chat?.messages.find((m) => m.id === messageId)
    if (msg) {
      msg.confidence = confidence
      persist()
    }
  }

  function setLoading(val: boolean) {
    isLoading.value = val
  }

  function setStreaming(val: boolean) {
    isStreaming.value = val
  }

  function updateChatId(oldId: string, newId: string) {
    const chat = chats.value.find((c) => c.id === oldId)
    if (chat) {
      chat.id = newId
      if (currentChatId.value === oldId) {
        currentChatId.value = newId
      }
      persist()
    }
  }

  function loadFromStorage() {
    const saved = localStorage.getItem('chats')
    if (saved) {
      try {
        chats.value = JSON.parse(saved)
        const lastId = localStorage.getItem('currentChatId')
        if (lastId && chats.value.find((c) => c.id === lastId)) {
          currentChatId.value = lastId
        }
      } catch {}
    }
  }

  function persist() {
    localStorage.setItem('chats', JSON.stringify(chats.value))
    if (currentChatId.value) {
      localStorage.setItem('currentChatId', currentChatId.value)
    }
  }

  return {
    chats,
    currentChatId,
    currentChat,
    isLoading,
    isStreaming,
    createChat,
    switchChat,
    deleteChat,
    addMessage,
    updateMessage,
    appendMessageContent,
    finalizeMessage,
    setMessageConfidence,
    updateChatId,
    setLoading,
    setStreaming,
    loadFromStorage,
    persist
  }
})
