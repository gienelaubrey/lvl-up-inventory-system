<script setup lang="ts">
import {
  LayoutDashboard,
  Package,
  Warehouse,
  ArrowDownToLine,
  ArrowUpFromLine,
  Truck,
  FileChartColumn,
  LogOut,
  Bell,
  Search,
} from 'lucide-vue-next'
</script>

<template>
  <div class="app-layout">

    <!-- Sidebar -->
    <aside class="sidebar">

      <div class="sidebar-brand">
        <div class="logo-container">
          <img
            src="/lvl-up-logo.png"
            alt="LVL UP Enterprises OPC"
            class="logo"
          />
        </div>

        <div class="brand-text">
          <strong>LVL UP</strong>
          <span>Inventory System</span>
        </div>
      </div>

      <nav class="sidebar-nav">

        <RouterLink to="/" class="nav-item">
          <LayoutDashboard :size="20" />
          <span>Dashboard</span>
        </RouterLink>

        <RouterLink to="/products" class="nav-item">
          <Package :size="20" />
          <span>Products</span>
        </RouterLink>
        
        <RouterLink to="/inventory" class="nav-item">
          <Warehouse :size="20" />
          <span>Inventory</span>
        </RouterLink>

        <RouterLink to="/stock-in" class="nav-item">
          <ArrowDownToLine :size="20" />
          <span>Stock In</span>
        </RouterLink>

        <RouterLink to="/stock-out" class="nav-item">
          <ArrowUpFromLine :size="20" />
          <span>Stock Out</span>
        </RouterLink>

        <RouterLink to="/suppliers" class="nav-item">
          <Truck :size="20" />
          <span>Suppliers</span>
        </RouterLink>

        <a href="#" class="nav-item">
          <FileChartColumn :size="20" />
          <span>Reports</span>
        </a>

        <div class="nav-divider"></div>

      </nav>

      <div class="sidebar-footer">
        <button class="logout-button">
          <LogOut :size="19" />
          <span>Logout</span>
        </button>
      </div>

    </aside>

    <!-- Main -->
    <div class="main-area">

      <header class="topbar">

        <div class="search-wrapper">
          <Search :size="19" />
          <input
            type="text"
            placeholder="Search products..."
          />
        </div>

        <div class="topbar-actions">

          <button class="icon-button">
            <Bell :size="21" />
            <span class="notification-dot"></span>
          </button>

          <div class="user-profile">
            <div class="avatar">
              A
            </div>

            <div class="user-details">
              <strong>Administrator</strong>
              <span>Admin</span>
            </div>
          </div>

        </div>

      </header>

      <main class="content">
        <slot />
      </main>

    </div>

  </div>
</template>