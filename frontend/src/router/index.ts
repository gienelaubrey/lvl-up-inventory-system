import {
  createRouter,
  createWebHistory,
} from 'vue-router'

import DashboardView
  from '../views/DashboardView.vue'

import ProductsView
  from '../views/ProductsView.vue'

import InventoryView
  from '../views/InventoryView.vue'

import SupplierHubView
  from '../views/SupplierHubView.vue'

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
      path: '/suppliers-reports',
      name: 'suppliers-reports',
      component: SupplierHubView,
    },

    /* Backward-compatible redirects */
    {
      path: '/stock-in',
      redirect: '/inventory',
    },

    {
      path: '/stock-out',
      redirect: '/inventory',
    },

    {
      path: '/suppliers',
      redirect: '/suppliers-reports',
    },

    {
      path: '/reports',
      redirect: '/suppliers-reports?tab=reports',
    },
  ],
})

export default router
