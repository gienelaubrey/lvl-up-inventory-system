<script setup lang="ts">
import {
  LayoutDashboard,
  Package,
  Warehouse,
  Building2,
} from 'lucide-vue-next'

const navItems = [
  {
    label: 'Dashboard',
    to: '/',
    icon: LayoutDashboard,
  },
  {
    label: 'Products',
    to: '/products',
    icon: Package,
  },
  {
    label: 'Inventory',
    to: '/inventory',
    icon: Warehouse,
  },
  {
    label: 'Suppliers & Reports',
    to: '/suppliers-reports',
    icon: Building2,
  },
]
</script>

<template>
  <div class="app-shell">
    <header class="app-topnav">
      <RouterLink to="/" class="brand-area">
        <div class="brand-mark">
          <img src="/lvl-up-logo.png" alt="LVL UP logo" />
        </div>
      </RouterLink>

      <nav class="nav-pill-group" aria-label="Primary navigation">
        <RouterLink
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="topnav-link"
        >
          <component :is="item.icon" :size="16" />
          <span>{{ item.label }}</span>
        </RouterLink>
      </nav>

      <div class="topnav-actions">

        <div class="owner-chip">
          <div class="owner-avatar">A</div>

          <div class="owner-copy">
            <strong>Administrator</strong>
            <span>Owner</span>
          </div>
        </div>
      </div>
    </header>

    <main class="app-main">
      <RouterView />
    </main>
  </div>
</template>

<style scoped src="../styles/app-layout-topnav.css"></style>
