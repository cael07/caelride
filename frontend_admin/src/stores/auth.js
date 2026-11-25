import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '../api/auth'

export const useAuthStore = defineStore('auth', () => {
  function getStoredUser() {
    try {
      const stored = localStorage.getItem('user')
      if (!stored || stored === 'undefined') return null
      return JSON.parse(stored)
    } catch (e) {
      return null
    }
  }

  const token = ref(localStorage.getItem('access_token') || null)
  const user = ref(getStoredUser())

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => !!user.value?.role && user.value.role !== 'passenger' && user.value.role !== 'driver')

  function setAuth(data) {
    if (!data) return
    token.value = data.access_token
    user.value = data.user || null
    
    if (data.access_token) localStorage.setItem('access_token', data.access_token)
    if (data.user) localStorage.setItem('user', JSON.stringify(data.user))
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
  }

  async function login(username, password) {
    const data = await authApi.login(username, password)
    // Enforce employee or admin role check upon login
    const role = data.user?.role
    if (!role || role === 'passenger' || role === 'driver') {
      throw new Error('Access denied. Only employee and admin accounts are allowed to login.')
    }
    setAuth(data)
    return data
  }

  async function registerAdmin(formData) {
    // Calling API register for admin role
    return await authApi.registerAdmin(formData)
  }

  return { token, user, isAuthenticated, isAdmin, login, registerAdmin, logout }
})
