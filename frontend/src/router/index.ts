import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import ProductsView from '../views/ProductsView.vue'
import InventoryView from '../views/InventoryView.vue'
import StockInView from '../views/StockInView.vue'
import StockOutView from '../views/StockOutView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView,
    },

    {
      path: '/products',
      name: 'products',
      component: ProductsView,
    },

    {
      path: '/inventory',
      name: 'inventory',
      component: InventoryView,
    },

    {
      path: '/stock-in',
      name: 'stock-in',
      component: StockInView,
    },

    {
      path: '/stock-out',
      name: 'stock-out',
      component: StockOutView,
    },
  ],
})

export default router