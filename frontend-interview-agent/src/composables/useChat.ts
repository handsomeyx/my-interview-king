import { ref, computed } from 'vue'
import { useSSE } from './useSSE'
import type { SSEEvent, KGNode } from '@/types/chat'

export function useChat() {
  const { events, isStreaming, connect, disconnect, reset } = useSSE()

  const assistantContent = ref('')
  const assistantConfidence = ref<number | null>(null)
  const assistantFollowUps = ref<string[]>([])
  const assistantKnowledgeGraph = ref<KGNode[]>([])
  const chatId = ref('')
  const error = ref<string | null>(null)

  const META_EVENT = computed<SSEEvent | null>(() => {
    const metas = events.value.filter(e => e.type === 'meta')
    return metas.length > 0 ? metas[metas.length - 1] : null
  })

  function handleEvent(event: SSEEvent) {
    switch (event.type) {
      case 'token':
        if (event.content) {
          assistantContent.value += event.content
        }
        break
      case 'meta':
        assistantConfidence.value = event.confidence ?? null
        assistantFollowUps.value = event.followUps ?? []
        assistantKnowledgeGraph.value = event.knowledgeGraph ?? []
        break
      case 'error':
        error.value = event.error || 'AI 服务异常'
        break
    }
  }

  async function sendMessage(
    message: string,
    opts: { guestId?: string; existingChatId?: string } = {}
  ) {
    assistantContent.value = ''
    assistantConfidence.value = null
    assistantFollowUps.value = []
    assistantKnowledgeGraph.value = []
    error.value = null

    const payload: Record<string, unknown> = { message }
    if (opts.guestId) payload.guest_id = opts.guestId
    if (opts.existingChatId) {
      payload.chat_id = opts.existingChatId
    }

    await connect('/api/ai/chat/stream', payload)

    for (const event of events.value) {
      handleEvent(event)
    }

    const doneEvent = events.value.find(e => e.type === 'done')
    if (doneEvent && opts.existingChatId) {
      chatId.value = opts.existingChatId
    } else {
      const metaEvent = META_EVENT.value
      if (metaEvent) {
        // chat_id might come from first token
      }
    }

    return {
      content: assistantContent.value,
      confidence: assistantConfidence.value ?? 0,
      followUps: assistantFollowUps.value,
      knowledgeGraph: assistantKnowledgeGraph.value,
      error: error.value
    }
  }

  function stopStreaming() {
    disconnect()
  }

  function resetState() {
    assistantContent.value = ''
    assistantConfidence.value = null
    assistantFollowUps.value = []
    assistantKnowledgeGraph.value = []
    error.value = null
    chatId.value = ''
    reset()
  }

  function processEventStream(newEvents: SSEEvent[]) {
    for (const event of newEvents) {
      handleEvent(event)
    }
  }

  return {
    // State
    assistantContent,
    assistantConfidence,
    assistantFollowUps,
    assistantKnowledgeGraph,
    chatId,
    error,
    isStreaming,
    events,

    // Actions
    sendMessage,
    stopStreaming,
    resetState,
    processEventStream
  }
}
