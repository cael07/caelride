<template>
  <div class="auth-page">
    <div class="auth-card glass" style="padding: 2.5rem;">
      <!-- Header -->
      <div class="auth-header">
        <div class="auth-logo">
          <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>
        </div>
        <h1 class="auth-title">Admin Console</h1>
        <p class="auth-subtitle">CAEL User Management Services</p>
      </div>

      <!-- Error message -->
      <Transition name="fade">
        <div v-if="error" class="alert alert-error" role="alert">
          <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>
          <div style="flex: 1;">{{ error }}</div>
        </div>
      </Transition>

      <form @submit.prevent="handleLogin" novalidate>
        <div class="form-group">
          <label class="form-label" for="username">Username</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            class="form-input"
            :class="{ error: touched.username && !form.username }"
            placeholder="Enter admin username"
            autocomplete="username"
            required
            @blur="touched.username = true"
          />
        </div>

        <div class="form-group" style="margin-bottom: 1.5rem;">
          <label class="form-label" for="password">Password</label>
          <div class="input-wrap">
            <input
              id="password"
              v-model="form.password"
              :type="showPwd ? 'text' : 'password'"
              class="form-input"
              :class="{ error: touched.password && !form.password }"
              placeholder="Enter password"
              autocomplete="current-password"
              required
              @blur="touched.password = true"
            />
            <button type="button" class="eye-btn" @click="showPwd = !showPwd">
              <svg v-if="!showPwd" viewBox="0 0 24 24" fill="currentColor"><path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg>
              <svg v-else viewBox="0 0 24 24" fill="currentColor"><path d="M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.43-4.75-1.73-4.39-6-7.5-11-7.5-1.4 0-2.74.25-3.98.7l2.16 2.16C10.74 7.13 11.35 7 12 7zM2 4.27l2.28 2.28.46.46C3.08 8.3 1.78 10.02 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42L19.73 22 21 20.73 3.27 3 2 4.27zM7.53 9.8l1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2zm4.31-.78l3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01z"/></svg>
            </button>
          </div>
        </div>

        <button type="submit" class="btn btn-primary" :disabled="loading">
          <span v-if="loading" class="spinner spinner-sm"></span>
          <span>Log in</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route  = useRoute()
const auth   = useAuthStore()

const form = ref({ username: '', password: '' })
const touched = ref({ username: false, password: false })
const error = ref('')
const loading = ref(false)
const showPwd = ref(false)

onMounted(() => {
  if (route.query.error === 'access_denied') {
    error.value = 'Access denied. You must be an administrator to access this area.'
  } else if (route.query.error === 'session_expired') {
    error.value = 'Your session has expired. Please log in again.'
  }
})

async function handleLogin() {
  touched.value.username = true
  touched.value.password = true

  if (!form.value.username || !form.value.password) {
    error.value = 'Please enter both fields.'
    return
  }

  error.value = ''
  loading.value = true
  try {
    await auth.login(form.value.username, form.value.password)
    router.push('/dashboard')
  } catch (err) {
    error.value = err.message || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.input-wrap { position: relative; }
.input-wrap .form-input { padding-right: 2.75rem; }

.eye-btn {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-3);
  padding: 0.25rem;
  display: flex;
}
.eye-btn:hover { color: var(--text-1); }
.eye-btn svg { width: 18px; height: 18px; }
</style>
