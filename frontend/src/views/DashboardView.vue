<script setup lang="ts">
import {
  Package,
  Boxes,
  TriangleAlert,
  Truck,
  ArrowUpRight,
  ArrowDownRight,
} from 'lucide-vue-next'
</script>

<template>
  <div class="dashboard">

    <!-- Page heading -->
    <div class="page-header">
      <div>
        <h1>Dashboard</h1>
        <p>Welcome back. Here's an overview of your inventory.</p>
      </div>

      <button class="primary-button">
        + Add Product
      </button>
    </div>

    <!-- Statistics -->
    <div class="stats-grid">

      <div class="stat-card">
        <div class="stat-icon red">
          <Package :size="24" />
        </div>

        <div>
          <span class="stat-label">Total Products</span>
          <h2>0</h2>
          <span class="stat-description">
            Products registered
          </span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon red">
          <Boxes :size="24" />
        </div>

        <div>
          <span class="stat-label">Total Stock</span>
          <h2>0</h2>
          <span class="stat-description">
            Units available
          </span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon warning">
          <TriangleAlert :size="24" />
        </div>

        <div>
          <span class="stat-label">Low Stock</span>
          <h2>0</h2>
          <span class="stat-description">
            Requires attention
          </span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon red">
          <Truck :size="24" />
        </div>

        <div>
          <span class="stat-label">Suppliers</span>
          <h2>0</h2>
          <span class="stat-description">
            Active suppliers
          </span>
        </div>
      </div>

    </div>

    <!-- Dashboard panels -->
    <div class="dashboard-grid">

      <section class="panel recent-movements">

        <div class="panel-header">
          <div>
            <h2>Recent Stock Movements</h2>
            <p>Latest inventory transactions</p>
          </div>

          <button class="text-button">
            View All
          </button>
        </div>

        <div class="table-wrapper">

          <table>
            <thead>
              <tr>
                <th>Product</th>
                <th>Type</th>
                <th>Quantity</th>
                <th>Date</th>
              </tr>
            </thead>

            <tbody>
              <tr class="empty-row">
                <td colspan="4">
                  No stock movements yet.
                </td>
              </tr>
            </tbody>

          </table>

        </div>

      </section>

      <section class="panel quick-summary">

        <div class="panel-header">
          <div>
            <h2>Inventory Summary</h2>
            <p>Today's activity</p>
          </div>
        </div>

        <div class="summary-list">

          <div class="summary-item">

            <div class="summary-icon stock-in">
              <ArrowDownRight :size="20" />
            </div>

            <div>
              <span>Stock In</span>
              <strong>0 units</strong>
            </div>

          </div>

          <div class="summary-item">

            <div class="summary-icon stock-out">
              <ArrowUpRight :size="20" />
            </div>

            <div>
              <span>Stock Out</span>
              <strong>0 units</strong>
            </div>

          </div>

        </div>

      </section>

    </div>

  </div>
</template>