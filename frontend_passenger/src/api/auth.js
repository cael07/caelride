import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || (typeof window !== 'undefined' && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') ? 'http://localhost:8000/auth' : 'https://caelride-api.onrender.com/auth'),
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Silent token refresh: on 401, try refreshing the access token once
// before giving up. This keeps drivers/passengers logged in during long rides.
let _isRefreshing = false
let _refreshQueue = []

const processQueue = (error, token = null) => {
  _refreshQueue.forEach(p => error ? p.reject(error) : p.resolve(token))
  _refreshQueue = []
}

api.interceptors.response.use(
  (r) => r,
  async (err) => {
    const original = err.config
    if (err.response?.status === 401 && !original._retry) {
      const refreshToken = localStorage.getItem('refresh_token')
      // No refresh token stored — nothing we can do
      if (!refreshToken) {
        const msg = err.response?.data?.detail || err.message || 'Session expired'
        return Promise.reject(new Error(Array.isArray(msg) ? msg[0]?.msg || msg[0] : msg))
      }

      if (_isRefreshing) {
        // Queue this request until refresh completes
        return new Promise((resolve, reject) => {
          _refreshQueue.push({ resolve, reject })
        }).then(token => {
          original.headers.Authorization = `Bearer ${token}`
          return api(original)
        })
      }

      original._retry = true
      _isRefreshing = true

      try {
        const { data } = await api.post('/refresh', { refresh_token: refreshToken })
        const newToken = data.access_token
        localStorage.setItem('access_token', newToken)
        api.defaults.headers.common['Authorization'] = `Bearer ${newToken}`
        processQueue(null, newToken)
        original.headers.Authorization = `Bearer ${newToken}`
        return api(original)
      } catch (refreshErr) {
        processQueue(refreshErr, null)
        // Refresh also failed — token is truly dead; clear storage
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')
        return Promise.reject(refreshErr)
      } finally {
        _isRefreshing = false
      }
    }

    const msg = err.response?.data?.detail || err.message || 'Request failed'
    return Promise.reject(new Error(Array.isArray(msg) ? msg[0]?.msg || msg[0] : msg))
  }
)

export const authApi = {
  async register(formData, faceImage, appId) {
    const { data } = await api.post('/register', {
      user: formData,
      face_image: faceImage || null,
      app_id: appId || null,
    })
    return data
  },

  async login(credentials, appId) {
    const params = appId ? { app_id: appId } : {}
    const { data } = await api.post('/login', credentials, { params })
    return data
  },

  async getMe() {
    const { data } = await api.get('/me')
    return data
  },

  async refresh(refreshToken) {
    const { data } = await api.post('/refresh', { refresh_token: refreshToken })
    return data
  },

  async getBookings() {
    const { data } = await api.get('/bookings')
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
  },

  async sendSupportMessage(ticketId, senderType, senderName, text) {
    const { data } = await api.post(`/support/tickets/${ticketId}/messages`, {
      sender_type: senderType,
      sender_name: senderName,
      text: text
    })
    return data
  }
}

