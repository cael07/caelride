import axios from 'axios'
import router from '../router'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || (typeof window !== 'undefined' && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') ? 'http://localhost:8000/auth' : 'https://pythonlogin-api.onrender.com/auth'),
  headers: { 'Content-Type': 'application/json' },
})

let isRedirecting = false

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (r) => r,
  (err) => {
    if (err.response?.status === 401) {
      // Clear Pinia store state dynamically to avoid circular dependency at static import time
      import('../stores/auth')
        .then(({ useAuthStore }) => {
          try {
            const auth = useAuthStore()
            auth.logout()
          } catch (e) {
            localStorage.removeItem('access_token')
            localStorage.removeItem('user')
          }
        })
        .catch(() => {
          localStorage.removeItem('access_token')
          localStorage.removeItem('user')
        })

      if (typeof window !== 'undefined') {
        const path = window.location.pathname
        if (path !== '/login' && !isRedirecting) {
          isRedirecting = true
          router.push('/login?error=session_expired').finally(() => {
            isRedirecting = false
          })
        }
      }
    }
    const msg = err.response?.data?.detail || err.message || 'Request failed'
    return Promise.reject(new Error(Array.isArray(msg) ? msg[0]?.msg || msg[0] : msg))
  }
)

export const authApi = {
  async login(username, password) {
    const { data } = await api.post('/login', { username, password })
    return data
  },

  async registerAdmin(formData) {
    const { data } = await api.post('/register', {
      user: {
        full_name: formData.full_name,
        username: formData.username,
        email: formData.email,
        password: formData.password,
        confirm_password: formData.confirm_password,
        role: formData.role || 'admin',
      }
    })
    return data
  },

  async addEmployee(employeeData) {
    const { data } = await api.post('/employees', employeeData)
    return data
  },

  async getMe() {
    const { data } = await api.get('/me')
    return data
  },

  async getUsers() {
    const { data } = await api.get('/users')
    return data
  },

  async toggleActive(userId) {
    const { data } = await api.post(`/users/${userId}/toggle-active`)
    return data
  },
  
  async toggleActivated(userId) {
    const { data } = await api.post(`/users/${userId}/toggle-activated`)
    return data
  },
  
  async updateBalance(userId, amount) {
    const { data } = await api.post(`/users/${userId}/update-balance`, { amount })
    return data
  },
  
  async getBalanceLogs(params = {}) {
    const { data } = await api.get('/balance-logs', { params })
    return data
  },
  
  async getBalanceStats() {
    const { data } = await api.get('/balance-stats')
    return data
  },
  
  async getBookings() {
    const { data } = await api.get('/bookings')
    return data
  },

  async verifyTopUp(logId) {
    const { data } = await api.post(`/topup/${logId}/verify`)
    return data
  },

  async unverifyTopUp(logId) {
    const { data } = await api.post(`/topup/${logId}/unverify`)
    return data
  },

  async getEmployees() {
    const { data } = await api.get('/employees')
    return data
  },

  async getRolePermissions() {
    const { data } = await api.get('/role-permissions')
    return data
  },

  async saveRolePermission(payload) {
    const { data } = await api.post('/role-permissions', payload)
    return data
  },

  async getSupportWaitingTickets() {
    const { data } = await api.get('/support/tickets/waiting')
    return data
  },

  async getSupportActiveTickets(agentName = null) {
    const params = agentName ? { agent_name: agentName } : {}
    const { data } = await api.get('/support/tickets/active', { params })
    return data
  },

  async getSupportHistory() {
    const { data } = await api.get('/support/tickets/history')
    return data
  },

  async claimSupportTicket(ticketId, agentName) {
    const { data } = await api.post(`/support/tickets/${ticketId}/claim`, { agent_name: agentName })
    return data
  },

  async getSupportTicketMessages(ticketId) {
    const { data } = await api.get(`/support/tickets/${ticketId}/messages`)
    return data
  },

  async sendSupportTicketMessage(ticketId, senderType, senderName, text) {
    const { data } = await api.post(`/support/tickets/${ticketId}/messages`, {
      sender_type: senderType,
      sender_name: senderName,
      text: text
    })
    return data
  },

  async resolveSupportTicket(ticketId) {
    const { data } = await api.post(`/support/tickets/${ticketId}/resolve`)
    return data
  },

  async createSupportTicket(userName, userRole, topic, message, userId = null) {
    const { data } = await api.post('/support/tickets', {
      user_name: userName,
      user_role: userRole,
      topic: topic,
      message: message,
      user_id: userId
    })
    return data
  },

  async getMyActiveSupportTicket(userName) {
    const { data } = await api.get('/support/tickets/my-active', { params: { user_name: userName } })
    return data
  }
}


