import { ref, readonly } from 'vue'
import type { SSEEvent } from '@/types/chat'

export function useSSE() {
  const events = ref<SSEEvent[]>([])
  const done = ref(false)
  const isStreaming = ref(false)
  const error = ref<string | null>(null)

  let controller: AbortController | null = null

  async function connect(url: string, payload: Record<string, unknown>) {
    reset()
    controller = new AbortController()
    isStreaming.value = true

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        signal: controller.signal
      })

      if (!response.ok) {
        error.value = `请求失败: ${response.status}`
        isStreaming.value = false
        return
      }

      const reader = response.body!.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done: streamDone, value } = await reader.read()
        if (streamDone) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          const trimmed = line.trim()
          if (!trimmed || !trimmed.startsWith('data: ')) continue

          const dataStr = trimmed.slice(6)
          try {
            const event: SSEEvent = JSON.parse(dataStr)
            events.value.push(event)

            if (event.type === 'error') {
              error.value = event.error || '未知错误'
            }
          } catch {
            // skip malformed data
          }
        }
      }

      done.value = true
    } catch (e) {
      if ((e as Error).name === 'AbortError') {
        // intentionally aborted
      } else {
        error.value = (e as Error).message
      }
    } finally {
      isStreaming.value = false
    }
  }

  function disconnect() {
    controller?.abort()
    isStreaming.value = false
  }

  function reset() {
    events.value = []
    done.value = false
    isStreaming.value = false
    error.value = null
  }

  return {
    events: readonly(events),
    done: readonly(done),
    isStreaming: readonly(isStreaming),
    error: readonly(error),
    connect,
    disconnect,
    reset
  }
}
