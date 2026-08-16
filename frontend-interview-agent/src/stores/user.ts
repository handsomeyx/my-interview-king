import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { AuthState, User, Guest } from '@/types/user'

export const useUserStore = defineStore('user', () => {
  const isLoggedIn = ref(false)
  const isGuest = ref(false)
  const user = ref<User | null>(null)
  const guestId = ref<string | null>(null)

  const state = computed<AuthState>(() => ({
    isLoggedIn: isLoggedIn.value,
    isGuest: isGuest.value,
    user: user.value,
    guestId: guestId.value
  }))

  function setUser(u: User) {
    user.value = u
    isLoggedIn.value = true
    isGuest.value = false
  }

  function setGuest(g: Guest) {
    guestId.value = g.id
    isGuest.value = true
    isLoggedIn.value = false
  }

  function logout() {
    user.value = null
    isLoggedIn.value = false
    isGuest.value = false
    guestId.value = null
  }

  function initFromStorage() {
    const saved = localStorage.getItem('auth')
    if (saved) {
      try {
        const data = JSON.parse(saved)
        if (data.user) setUser(data.user)
        else if (data.guestId) {
          guestId.value = data.guestId
          isGuest.value = true
        }
      } catch {}
    }
  }

  function persist() {
    localStorage.setItem('auth', JSON.stringify({
      user: user.value,
      guestId: guestId.value
    }))
  }

  return {
    state,
    isLoggedIn,
    isGuest,
    user,
    guestId,
    setUser,
    setGuest,
    logout,
    initFromStorage,
    persist
  }
})
