import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  { path: '/', redirect: '/login' },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginView.vue'),
    meta: { guest: true },
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/DashboardView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/register-admin',
    name: 'RegisterAdmin',
    component: () => import('../views/RegisterView.vue'),
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth) {
    if (!auth.isAuthenticated) {
      return '/login'
    }
    if (!auth.isAdmin) {
      auth.logout()
      return '/login?error=access_denied'
    }
  }
  if (to.meta.guest && auth.isAuthenticated) {
    if (auth.isAdmin) {
      return '/dashboard'
    }
  }
})

export default router
