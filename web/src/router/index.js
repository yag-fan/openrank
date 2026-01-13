import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Screen',
      component: () => import('../App.vue')
    }
  ]
})

export default router

