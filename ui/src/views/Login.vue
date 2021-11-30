<script setup>
  import { ref } from 'vue'
  import { useStore } from 'vuex'
  import { useRouter } from 'vue-router'

  const store = useStore()
  const router = useRouter()
  const credentials = ref({username: '', password: ''})

  async function login() {
    await store.dispatch('user/login', credentials.value)
    router.push({ path: '/' })
  }
</script>

<template>
  <n-form :model="credentials">
    <n-form-item path="username" label="Username">
      <n-input v-model:value="credentials.username" autocomplete="username" @keydown.enter.prevent />
    </n-form-item>
    <n-form-item path="password" label="Password">
      <n-input v-model:value="credentials.password" autocomplete="current-password" type="password" @keydown.enter.prevent />
    </n-form-item>
  </n-form>
  <n-row :gutter="[0, 24]">
      <n-col :span="24">
        <div style="display: flex; justify-content: flex-end;">
          <n-button
            :disabled="credentials.username === '' && credentials.password === ''"
            @click="login"
            round
            type="primary"
          >
            Login
          </n-button>
        </div>
      </n-col>
    </n-row>
</template>