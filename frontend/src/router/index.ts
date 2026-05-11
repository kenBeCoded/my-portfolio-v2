import { createRouter, createWebHistory } from 'vue-router'
import PublicPortfolio from '../views/PublicPortfolio.vue'

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
      component: () => import('../views/AdminLogin.vue')
    },
    {
      path: '/admin',
      name: 'admin-home',
      component: () => import('../views/AdminHome.vue')
    },
    {
      path: '/admin/projects',
      name: 'admin-projects',
      component: () => import('../views/AdminProjects.vue')
    },
    {
      path: '/admin/techstack',
      name: 'admin-techstack',
      component: () => import('../views/AdminTechStack.vue')
    },
    {
      path: '/admin/accounts',
      name: 'admin-accounts',
      component: () => import('../views/AdminAccounts.vue')
    }
  ]
})

export default router
