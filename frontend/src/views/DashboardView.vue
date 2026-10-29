<script setup lang="ts">
import {
  computed,
  onMounted,
  ref,
} from 'vue'

import {
  Boxes,
  Package,
  TriangleAlert,
  Truck,
  ArrowDownRight,
  ArrowUpRight,
  AlertCircle,
} from 'lucide-vue-next'

import {
  getProducts,
  getStockMovements,
  getSuppliers,
  type Product,
  type StockMovement,
  type Supplier,
} from '../services/api'

import SupplierSalesChart
  from '../components/SupplierSalesChart.vue'

import StockMovementTrendChart
  from '../components/StockMovementTrendChart.vue'


const products = ref<Product[]>([])
const suppliers = ref<Supplier[]>([])
const movements = ref<StockMovement[]>([])

const loading = ref(true)
const errorMessage = ref('')


const totalProducts = computed(
  () => products.value.length
)


const totalStock = computed(() => {
  return products.value.reduce(
    (total, product) =>
      total + product.current_stock,
    0
  )
})


const lowStockCount = computed(() => {
  return products.value.filter(
    (product) =>
      product.current_stock <=
      product.reorder_level
  ).length
})


const supplierCount = computed(
  () => suppliers.value.length
)


const recentMovements = computed(
  () => movements.value.slice(0, 5)
)


const todayStockIn = computed(() => {
  return movements.value
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
})


const todayStockOut = computed(() => {
  return movements.value
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
})


function isToday(
  value: string
) {
  const date = new Date(value)
  const today = new Date()

  return (
    date.getFullYear() ===
      today.getFullYear() &&

    date.getMonth() ===
      today.getMonth() &&

    date.getDate() ===
      today.getDate()
  )
}


function productName(
  productId: number
) {
  const product =
    products.value.find(
      (item) =>
        item.id === productId
    )

  return product
    ? `${product.sku} — ${product.name}`
    : `Product #${productId}`
}


function formatDate(
  value: string
) {
  return new Intl.DateTimeFormat(
    'en-PH',
    {
      dateStyle: 'medium',
      timeStyle: 'short',
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
        : 'Unable to load dashboard'
  } finally {
    loading.value = false
  }
}


onMounted(loadDashboard)
</script>


<template>
  <div class="dashboard">

    <div class="page-header">

      <div>
        <h1>Dashboard</h1>

        <p>
          Overview of LVL UP inventory
          operations.
        </p>
      </div>

    </div>


    <div
      v-if="errorMessage"
      class="alert error-alert"
    >
      <AlertCircle :size="17" />

      {{ errorMessage }}
    </div>


    <div class="stats-grid">

      <div class="stat-card">

        <div class="stat-icon red">
          <Package :size="23" />
        </div>

        <div>
          <span class="stat-label">
            Total Products
          </span>

          <h2>
            {{
              loading
                ? '—'
                : totalProducts
            }}
          </h2>

          <span class="stat-description">
            Registered products
          </span>
        </div>

      </div>


      <div class="stat-card">

        <div class="stat-icon red">
          <Boxes :size="23" />
        </div>

        <div>
          <span class="stat-label">
            Total Stock
          </span>

          <h2>
            {{
              loading
                ? '—'
                : totalStock
            }}
          </h2>

          <span class="stat-description">
            Units currently available
          </span>
        </div>

      </div>


      <div class="stat-card">

        <div class="stat-icon warning">
          <TriangleAlert :size="23" />
        </div>

        <div>
          <span class="stat-label">
            Low Stock
          </span>

          <h2>
            {{
              loading
                ? '—'
                : lowStockCount
            }}
          </h2>

          <span class="stat-description">
            Products requiring attention
          </span>
        </div>

      </div>


      <div class="stat-card">

        <div class="stat-icon red">
          <Truck :size="23" />
        </div>

        <div>
          <span class="stat-label">
            Suppliers
          </span>

          <h2>
            {{
              loading
                ? '—'
                : supplierCount
            }}
          </h2>

          <span class="stat-description">
            Registered suppliers
          </span>
        </div>

      </div>

    </div>
    
    <StockMovementTrendChart />
    <SupplierSalesChart />

    <div class="dashboard-grid">

      <section class="panel">

        <div class="panel-header">

          <div>
            <h2>
              Recent Stock Movements
            </h2>

            <p>
              Latest inventory activity
            </p>
          </div>

          <RouterLink
            to="/movements"
            class="text-button"
          >
            View All
          </RouterLink>

        </div>


        <div class="table-wrapper">

          <table>

            <thead>
              <tr>
                <th>Product</th>
                <th>Type</th>
                <th>Qty</th>
                <th>Stock After</th>
                <th>Date</th>
              </tr>
            </thead>

            <tbody>

              <tr v-if="loading">
                <td
                  colspan="5"
                  class="table-message"
                >
                  Loading activity...
                </td>
              </tr>


              <tr
                v-else-if="
                  recentMovements.length === 0
                "
              >
                <td
                  colspan="5"
                  class="table-message"
                >
                  No stock movements yet.
                </td>
              </tr>


              <tr
                v-for="
                  movement in
                  recentMovements
                "
                v-else
                :key="movement.id"
              >

                <td>
                  {{
                    productName(
                      movement.product_id
                    )
                  }}
                </td>


                <td>

                  <span
                    class="movement-type"
                    :class="
                      movement.movement_type ===
                      'IN'
                        ? 'movement-in'
                        : 'movement-out'
                    "
                  >

                    {{
                      movement.movement_type ===
                      'IN'
                        ? 'Stock In'
                        : 'Stock Out'
                    }}

                  </span>

                </td>


                <td>
                  {{ movement.quantity }}
                </td>


                <td>
                  <strong>
                    {{ movement.stock_after }}
                  </strong>
                </td>


                <td>
                  {{
                    formatDate(
                      movement.created_at
                    )
                  }}
                </td>

              </tr>

            </tbody>

          </table>

        </div>

      </section>


      <section class="panel">

        <div class="panel-header">

          <div>
            <h2>Today's Activity</h2>

            <p>
              Inventory movement today
            </p>
          </div>

        </div>


        <div class="summary-list">

          <div class="summary-item">

            <div
              class="
                summary-icon
                stock-in
              "
            >
              <ArrowDownRight
                :size="20"
              />
            </div>

            <div>
              <span>
                Stock In
              </span>

              <strong>
                {{
                  loading
                    ? '—'
                    : `${todayStockIn} units`
                }}
              </strong>
            </div>

          </div>


          <div class="summary-item">

            <div
              class="
                summary-icon
                stock-out
              "
            >
              <ArrowUpRight
                :size="20"
              />
            </div>

            <div>
              <span>
                Stock Out
              </span>

              <strong>
                {{
                  loading
                    ? '—'
                    : `${todayStockOut} units`
                }}
              </strong>
            </div>

          </div>

        </div>

      </section>

    </div>

  </div>
</template>