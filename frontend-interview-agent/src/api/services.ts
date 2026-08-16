import http from './http'
import type { ApiResponse } from '@/types/api'
import type { KGNode } from '@/types/chat'

export interface ChatResponse {
  chat_id: string
  response: string
  follow_up_questions: string[]
  knowledge_graph: KGNode[]
  confidence_score: number
  is_guest: boolean
}

export interface HistoryItem {
  id: string
  title: string
  preview: string
  created_at: string
  updated_at: string
}

export interface HistoryResponse {
  chats: HistoryItem[]
}

export interface MessagesResponse {
  messages: {
    id: string
    role: 'user' | 'assistant'
    content: string
    created_at: string
  }[]
}

export interface AnalyzeResponse {
  follow_up_questions: string[]
  knowledge_graph: KGNode[]
  confidence_score: number
}

export interface AIProvidersResponse {
  current: string
  available: string[]
  models: Record<string, { name: string; description: string }>
}

export const authApi = {
  register(data: { username: string; password: string; email: string }) {
    return http.post<ApiResponse<{ user_id: string; username: string }>>('/auth/register', data)
  },
  login(data: { username: string; password: string }) {
    return http.post<ApiResponse<{ user_id: string; username: string }>>('/auth/login', data)
  },
  logout() {
    return http.post<ApiResponse<{ success: boolean }>>('/auth/logout')
  },
  getUser() {
    return http.get<ApiResponse<{ is_logged_in: boolean; user_id?: string; username?: string; is_guest: boolean }>>('/auth/user')
  }
}

export const chatApi = {
  send(data: { message: string; chat_id?: string; guest_id?: string }) {
    return http.post<ChatResponse>('/chat/send', data)
  },
  getHistory() {
    return http.get<HistoryResponse>('/chat/history')
  },
  getMessages(chatId: string) {
    return http.get<MessagesResponse>(`/chat/${chatId}/messages`)
  }
}

export const analysisApi = {
  analyze(message: string) {
    return http.post<AnalyzeResponse>('/analysis/analyze', { message })
  }
}

export const aiApi = {
  chatStream(data: { message: string; chat_id?: string; guest_id?: string }) {
    return fetch('/api/ai/chat/stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(data)
    })
  },
  analyze(message: string) {
    return http.post<AnalyzeResponse>('/ai/analyze', { message })
  },
  getProviders() {
    return http.get<AIProvidersResponse>('/ai/providers')
  }
}

export const healthApi = {
  check() {
    return http.get<{ status: string; ai_provider?: string }>('/health')
  }
}
