import { createRouter, createWebHistory } from 'vue-router'
import PublicPortfolio from '../views/PublicPortfolio.vue'
import { isAuthenticated } from '../services/authService'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'portfolio',
      component: PublicPortfolio
    },
    {
      path: '/admin/login',
      name: 'admin-login',
      component: () => import('../views/AdminLogin.vue'),
      meta: { public: true }
    },
    {
      path: '/admin',
      name: 'admin-home',
      component: () => import('../views/AdminHome.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/admin/projects',
      name: 'admin-projects',
      component: () => import('../views/AdminProjects.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/admin/techstack',
      name: 'admin-techstack',
      component: () => import('../views/AdminTechStack.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/admin/accounts',
      name: 'admin-accounts',
      component: () => import('../views/AdminAccounts.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

// ── Navigation guard ───────────────────────────────────────────
router.beforeEach((to) => {
  const authed = isAuthenticated()

  // Already logged in → skip the login page
  if (to.name === 'admin-login' && authed) {
    return { name: 'admin-home' }
  }

  // Protected route → require a token
  if (to.meta.requiresAuth && !authed) {
    return { name: 'admin-login', query: { redirect: to.fullPath } }
  }

  return true
})

export default router
