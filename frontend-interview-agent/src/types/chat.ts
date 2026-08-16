export type MessageRole = 'user' | 'assistant'

export interface Message {
  id: string
  chatId: string
  role: MessageRole
  content: string
  createdAt: string
  confidence?: number
  isStreaming?: boolean
}

export interface Chat {
  id: string
  title: string
  preview: string
  createdAt: string
  updatedAt: string
  messages: Message[]
}

export interface KGNode {
  name: string
  strength: 'strong' | 'medium' | 'weak'
}

export interface AnalysisResult {
  messageId: string
  confidenceScore: number
  knowledgeGraph: KGNode[]
  followUps: string[]
}

export interface SSEEvent {
  type: 'token' | 'meta' | 'done' | 'error'
  content?: string
  confidence?: number
  followUps?: string[]
  knowledgeGraph?: KGNode[]
  error?: string
}
