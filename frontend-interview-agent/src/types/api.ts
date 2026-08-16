export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

export type SSEEventType = 'token' | 'done' | 'error' | 'meta'

export interface SSEEvent {
  type: SSEEventType
  content?: string
  confidence?: number
  followUps?: string[]
  knowledgeGraph?: import('./chat').KGNode[]
  error?: string
}
