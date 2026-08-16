<template>
  <Teleport to="body">
    <div v-if="visible" class="modal-overlay" @click.self="handleClose">
      <div class="modal-content">
        <h2>注册</h2>
        <form @submit.prevent="handleRegister">
          <div class="form-group">
            <label>用户名</label>
            <input v-model="form.username" type="text" required />
          </div>
          <div class="form-group">
            <label>邮箱</label>
            <input v-model="form.email" type="email" required />
          </div>
          <div class="form-group">
            <label>密码</label>
            <input v-model="form.password" type="password" required minlength="6" />
          </div>
          <div v-if="error" class="error">{{ error }}</div>
          <button type="submit" class="submit-btn" :disabled="loading">
            {{ loading ? '注册中...' : '注册' }}
          </button>
          <p class="switch-link">
            已有账号？<a @click="goLogin">去登录</a>
          </p>
        </form>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useUserStore } from '@/stores/user'

defineProps<{ visible: boolean }>()
const emit = defineEmits<{
  'update:visible': [value: boolean]
  'register-success': []
}>()

const userStore = useUserStore()

const form = reactive({ username: '', email: '', password: '' })
const error = ref('')
const loading = ref(false)

function handleClose() {
  emit('update:visible', false)
}

async function handleRegister() {
  error.value = ''
  loading.value = true
  try {
    await new Promise((resolve) => setTimeout(resolve, 500))
    userStore.setUser({
      id: crypto.randomUUID(),
      username: form.username,
      email: form.email,
      createdAt: new Date().toISOString(),
      chatCount: 0
    })
    userStore.persist()
    emit('register-success')
    handleClose()
  } catch (e: any) {
    error.value = e?.message || '注册失败'
  } finally {
    loading.value = false
  }
}

function goLogin() {
  handleClose()
  window.dispatchEvent(new CustomEvent('auth:show-login'))
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: var(--bg-surface);
  border-radius: 16px;
  padding: 32px;
  width: 400px;
  max-width: 90%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-content h2 {
  margin: 0 0 24px;
  font-size: 1.3rem;
  text-align: center;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
  font-size: 0.9rem;
}

.form-group input {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 0.95rem;
  background: var(--bg-soft);
  color: var(--text-1);
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: var(--primary-color);
}

.error {
  color: #ef4444;
  font-size: 0.85rem;
  margin-bottom: 12px;
}

.submit-btn {
  width: 100%;
  padding: 12px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.submit-btn:hover:not(:disabled) {
  background: var(--primary-dark);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.switch-link {
  text-align: center;
  margin: 16px 0 0;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.switch-link a {
  color: var(--primary-color);
  cursor: pointer;
}
</style>
