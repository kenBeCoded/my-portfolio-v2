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
    }
  ]
})

export default router
