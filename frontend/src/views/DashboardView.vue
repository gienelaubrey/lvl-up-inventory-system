<script setup lang="ts">
import {
  computed,
  onMounted,
  ref,
} from 'vue'

import {
  AlertTriangle,
  ArrowDownToLine,
  ArrowUpFromLine,
  Boxes,
  FileDown,
  Package,
  Truck,
} from 'lucide-vue-next'

import SupplierSalesChart
  from '../components/SupplierSalesChart.vue'

import StockMovementTrendChart
  from '../components/StockMovementTrendChart.vue'

import {
  getProducts,
  getStockMovements,
  getSuppliers,
  type Product,
  type StockMovement,
  type Supplier,
} from '../services/api'

const products = ref<Product[]>([])
const suppliers = ref<Supplier[]>([])
const movements = ref<StockMovement[]>([])
const loading = ref(true)
const errorMessage = ref('')

const totalProducts = computed(
  () => products.value.length
)

const totalStock = computed(() =>
  products.value.reduce(
    (total, product) =>
      total + product.current_stock,
    0
  )
)

const lowStockProducts = computed(() =>
  products.value.filter(
    (product) =>
      product.current_stock <=
      product.reorder_level
  )
)

const supplierCount = computed(
  () => suppliers.value.length
)

const todayStockIn = computed(() =>
  movements.value
    .filter(
      (movement) =>
        movement.movement_type === 'IN' &&
        isToday(movement.created_at)
    )
    .reduce(
      (total, movement) =>
        total + movement.quantity,
      0
    )
)

const todayStockOut = computed(() =>
  movements.value
    .filter(
      (movement) =>
        movement.movement_type === 'OUT' &&
        isToday(movement.created_at)
    )
    .reduce(
      (total, movement) =>
        total + movement.quantity,
      0
    )
)

const recentMovements = computed(
  () => movements.value.slice(0, 5)
)

const topStockProducts = computed(() =>
  [...products.value]
    .sort(
      (a, b) =>
        b.current_stock - a.current_stock
    )
    .slice(0, 5)
)

function isToday(value: string) {
  const date = new Date(value)
  const today = new Date()

  return (
    date.getFullYear() === today.getFullYear() &&
    date.getMonth() === today.getMonth() &&
    date.getDate() === today.getDate()
  )
}

function productFor(id: number) {
  return products.value.find(
    (product) => product.id === id
  )
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat(
    'en-PH',
    {
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
    }
  ).format(new Date(value))
}

async function loadDashboard() {
  loading.value = true
  errorMessage.value = ''

  try {
    const [
      productData,
      supplierData,
      movementData,
    ] = await Promise.all([
      getProducts(),
      getSuppliers(),
      getStockMovements(),
    ])

    products.value = productData
    suppliers.value = supplierData
    movements.value = movementData
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to load dashboard.'
  } finally {
    loading.value = false
  }
}

onMounted(loadDashboard)
</script>

<template>
  <div class="executive-dashboard">
    <section class="dashboard-intro">
      <div>
        <span class="eyebrow">Inventory overview</span>
        <h1>Welcome back, Admin</h1>
        <p>
          Track inventory health, supplier performance,
          stock movement, and warehouse activity.
        </p>
      </div>

      <RouterLink
        to="/suppliers-reports?tab=reports"
        class="export-report-button"
      >
        <FileDown :size="17" />
        Export Supplier Report
      </RouterLink>
    </section>

    <div
      v-if="errorMessage"
      class="dashboard-alert"
    >
      {{ errorMessage }}
    </div>

    <section class="metric-grid">
      <article class="metric-card">
        <div class="metric-top">
          <span>Total Products</span>
          <div class="metric-icon">
            <Package :size="19" />
          </div>
        </div>

        <strong>{{ loading ? '—' : totalProducts }}</strong>
        <p>Registered inventory items</p>
      </article>

      <article class="metric-card">
        <div class="metric-top">
          <span>Total Stock</span>
          <div class="metric-icon">
            <Boxes :size="19" />
          </div>
        </div>

        <strong>{{ loading ? '—' : totalStock.toLocaleString() }}</strong>
        <p>Units currently available</p>
      </article>

      <article class="metric-card">
        <div class="metric-top">
          <span>Low Stock Items</span>
          <div class="metric-icon metric-icon-warning">
            <AlertTriangle :size="19" />
          </div>
        </div>

        <strong>{{ loading ? '—' : lowStockProducts.length }}</strong>
        <p>Items requiring attention</p>
      </article>

      <article class="metric-card">
        <div class="metric-top">
          <span>Suppliers</span>
          <div class="metric-icon">
            <Truck :size="19" />
          </div>
        </div>

        <strong>{{ loading ? '—' : supplierCount }}</strong>
        <p>Registered supplier partners</p>
      </article>
    </section>

    <section class="dashboard-content-grid">
      <div class="dashboard-primary-column">
        <StockMovementTrendChart />

        <SupplierSalesChart />

        <div class="dashboard-two-column">
          <article class="executive-card">
            <div class="executive-card-head">
              <div>
                <span class="card-kicker">Warehouse flow</span>
                <h2>Today’s Movement</h2>
              </div>
            </div>

            <div class="movement-summary-grid">
              <div class="movement-summary-item movement-in-summary">
                <div class="summary-icon">
                  <ArrowDownToLine :size="18" />
                </div>

                <div>
                  <span>Stock In</span>
                  <strong>{{ todayStockIn.toLocaleString() }}</strong>
                  <small>units received today</small>
                </div>
              </div>

              <div class="movement-summary-item movement-out-summary">
                <div class="summary-icon">
                  <ArrowUpFromLine :size="18" />
                </div>

                <div>
                  <span>Stock Out</span>
                  <strong>{{ todayStockOut.toLocaleString() }}</strong>
                  <small>units released today</small>
                </div>
              </div>
            </div>
          </article>

          <article class="executive-card">
            <div class="executive-card-head">
              <div>
                <span class="card-kicker">Stock balance</span>
                <h2>Highest Stock</h2>
              </div>
            </div>

            <div class="ranking-list">
              <div
                v-for="(product, index) in topStockProducts"
                :key="product.id"
                class="ranking-row"
              >
                <div class="rank-number">
                  {{ String(index + 1).padStart(2, '0') }}
                </div>

                <div class="rank-copy">
                  <strong>{{ product.sku }}</strong>
                  <span>{{ product.name }}</span>
                </div>

                <b>{{ product.current_stock }}</b>
              </div>
            </div>
          </article>
        </div>
      </div>

      <aside class="dashboard-secondary-column">
        <article class="executive-card recent-card">
          <div class="executive-card-head">
            <div>
              <span class="card-kicker">Latest activity</span>
              <h2>Recent Movements</h2>
            </div>

            <RouterLink
              to="/inventory"
              class="card-link"
            >
              View inventory
            </RouterLink>
          </div>

          <div
            v-if="!recentMovements.length && !loading"
            class="empty-state"
          >
            No stock movements yet.
          </div>

          <div class="recent-list">
            <div
              v-for="movement in recentMovements"
              :key="movement.id"
              class="recent-item"
            >
              <div
                class="recent-icon"
                :class="
                  movement.movement_type === 'IN'
                    ? 'recent-in'
                    : 'recent-out'
                "
              >
                <ArrowDownToLine
                  v-if="movement.movement_type === 'IN'"
                  :size="16"
                />

                <ArrowUpFromLine
                  v-else
                  :size="16"
                />
              </div>

              <div class="recent-copy">
                <strong>
                  {{
                    productFor(movement.product_id)?.sku
                      || `Product #${movement.product_id}`
                  }}
                </strong>

                <span>
                  {{
                    movement.movement_type === 'IN'
                      ? 'Stock In'
                      : 'Stock Out'
                  }}
                  · {{ movement.quantity }} units
                </span>

                <small>
                  {{ formatDate(movement.created_at) }}
                </small>
              </div>

              <b>{{ movement.stock_after }}</b>
            </div>
          </div>
        </article>

        <article class="executive-card low-stock-card">
          <div class="executive-card-head">
            <div>
              <span class="card-kicker">Attention needed</span>
              <h2>Low Stock</h2>
            </div>

            <span class="count-chip">
              {{ lowStockProducts.length }}
            </span>
          </div>

          <div
            v-if="!lowStockProducts.length && !loading"
            class="empty-state"
          >
            All products are above reorder level.
          </div>

          <div class="low-stock-list">
            <div
              v-for="product in lowStockProducts.slice(0, 5)"
              :key="product.id"
              class="low-stock-row"
            >
              <div>
                <strong>{{ product.sku }}</strong>
                <span>{{ product.name }}</span>
              </div>

              <b>
                {{ product.current_stock }}
                / {{ product.reorder_level }}
              </b>
            </div>
          </div>
        </article>
      </aside>
    </section>
  </div>
</template>

<style scoped src="../styles/dashboard-executive.css"></style>
