<template>
  <div class="followup-panel">
    <h3 class="panel-title">💡 智能追问</h3>
    <ul class="followup-list">
      <li
        v-for="(q, i) in questions"
        :key="i"
        class="followup-item"
        @click="emit('select', q)"
      >
        <span class="prefix">Q{{ i + 1 }}</span>
        <span class="text">{{ q }}</span>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  questions: string[]
}>()

const emit = defineEmits<{
  select: [question: string]
}>()
</script>

<style scoped>
.followup-panel {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 16px;
}

.panel-title {
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 12px;
}

.followup-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.followup-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 8px 10px;
  background: var(--bg-soft);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.85rem;
  line-height: 1.4;
}

.followup-item:hover {
  background: var(--user-bubble);
  border: 1px solid var(--primary-color);
}

.prefix {
  font-weight: 600;
  color: var(--primary-color);
  flex-shrink: 0;
}

.text {
  color: var(--text-2);
}
</style>
