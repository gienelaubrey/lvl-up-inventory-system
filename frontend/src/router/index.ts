import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import ProductsView from '../views/ProductsView.vue'
import InventoryView from '../views/InventoryView.vue'
import StockInView from '../views/StockInView.vue'
import StockOutView from '../views/StockOutView.vue'
import MovementsView from '../views/MovementsView.vue'
import SupplierView from '../views/SupplierView.vue'
import ReportsView from '../views/ReportsView.vue'

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

    {
      path: '/movements',
      name: 'movements',
      component: MovementsView,
    },

    {
      path: '/suppliers',
      name: 'suppliers',
      component: SupplierView,
    },

    {
      path: '/reports',
      name: 'reports',
      component: ReportsView,
    },
  ],
})

export default router