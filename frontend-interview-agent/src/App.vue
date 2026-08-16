<template>
  <div class="app">
    <AppHeader />
    <div class="app-body">
      <AppSidebar />
      <AppMain />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useChatStore } from '@/stores/chat'
import { useUserStore } from '@/stores/user'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppMain from '@/components/layout/AppMain.vue'

const chatStore = useChatStore()
const userStore = useUserStore()

onMounted(() => {
  chatStore.loadFromStorage()
  userStore.initFromStorage()
  if (!userStore.isLoggedIn && !userStore.isGuest) {
    userStore.setGuest({
      id: crypto.randomUUID(),
      chatCount: 0,
      createdAt: new Date().toISOString()
    })
    userStore.persist()
  }
  if (!chatStore.currentChatId) {
    chatStore.createChat()
  }
})
</script>
