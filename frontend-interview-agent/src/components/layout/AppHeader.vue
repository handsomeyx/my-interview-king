<template>
  <header class="app-header">
    <div class="header-left">
      <h1 class="app-title">🤖 智能面试助手</h1>
    </div>
    <div class="header-right">
      <div v-if="userStore.isLoggedIn && userStore.user" class="user-info">
        <span class="username">{{ userStore.user.username }}</span>
        <button class="logout-btn" @click="handleLogout">登出</button>
      </div>
      <div v-else-if="userStore.isGuest" class="guest-info">
        <span>游客模式</span>
        <button class="login-btn" @click="showLogin = true">登录</button>
      </div>
      <div v-else class="auth-buttons">
        <button class="login-btn" @click="showLogin = true">登录</button>
        <button class="register-btn" @click="showRegister = true">注册</button>
      </div>
    </div>

    <LoginModal v-model:visible="showLogin" @login-success="onLoginSuccess" />
    <RegisterModal v-model:visible="showRegister" @register-success="onRegisterSuccess" />
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useUserStore } from '@/stores/user'
import LoginModal from '@/components/modals/LoginModal.vue'
import RegisterModal from '@/components/modals/RegisterModal.vue'

const userStore = useUserStore()

const showLogin = ref(false)
const showRegister = ref(false)

function handleLogout() {
  userStore.logout()
  userStore.persist()
}

function onLoginSuccess() {
  showLogin.value = false
}

function onRegisterSuccess() {
  showRegister.value = false
}

function showLoginModal() {
  showRegister.value = false
  showLogin.value = true
}

function showRegisterModal() {
  showLogin.value = false
  showRegister.value = true
}

onMounted(() => {
  window.addEventListener('auth:show-login', showLoginModal)
  window.addEventListener('auth:show-register', showRegisterModal)
})

onUnmounted(() => {
  window.removeEventListener('auth:show-login', showLoginModal)
  window.removeEventListener('auth:show-register', showRegisterModal)
})
</script>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: 60px;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-backdrop);
  border-bottom: 1px solid var(--border-color);
}

.app-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--primary-color);
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-info,
.guest-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.username {
  font-weight: 500;
}

.auth-buttons {
  display: flex;
  gap: 8px;
}

.login-btn,
.register-btn,
.logout-btn {
  padding: 6px 16px;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.login-btn {
  background: transparent;
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
}

.login-btn:hover {
  background: var(--primary-color);
  color: white;
}

.register-btn {
  background: var(--primary-color);
  color: white;
}

.register-btn:hover {
  background: var(--primary-dark);
}

.logout-btn {
  background: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.logout-btn:hover {
  background: var(--background-mute);
}
</style>
