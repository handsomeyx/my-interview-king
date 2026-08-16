export interface User {
  id: string
  username: string
  email: string
  createdAt: string
  chatCount: number
}

export interface Guest {
  id: string
  chatCount: number
  createdAt: string
}

export interface AuthState {
  isLoggedIn: boolean
  isGuest: boolean
  user: User | null
  guestId: string | null
}
