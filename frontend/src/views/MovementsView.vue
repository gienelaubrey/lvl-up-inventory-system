<script setup lang="ts">
import {
  computed,
  onMounted,
  ref,
} from 'vue'

import {
  ArrowDownToLine,
  ArrowUpFromLine,
  Search,
} from 'lucide-vue-next'

import {
  getProducts,
  getStockMovements,
  type Product,
  type StockMovement,
} from '../services/api'


const movements = ref<StockMovement[]>([])
const products = ref<Product[]>([])
const loading = ref(true)
const searchQuery = ref('')


const filteredMovements = computed(() => {
  const query =
    searchQuery.value.trim().toLowerCase()

  if (!query) {
    return movements.value
  }

  return movements.value.filter((movement) => {
    const product =
      products.value.find(
        (item) =>
          item.id === movement.product_id
      )

    return (
      product?.name
        .toLowerCase()
        .includes(query) ||

      product?.sku
        .toLowerCase()
        .includes(query) ||

      movement.reference
        ?.toLowerCase()
        .includes(query)
    )
  })
})


function productName(id: number) {
  const product = products.value.find(
    (item) => item.id === id
  )

  return product
    ? `${product.sku} — ${product.name}`
    : `Product #${id}`
}


function formatDate(value: string) {
  return new Intl.DateTimeFormat(
    'en-PH',
    {
      dateStyle: 'medium',
      timeStyle: 'short',
    }
  ).format(new Date(value))
}


async function loadData() {
  loading.value = true

  try {
    const [
      movementData,
      productData,
    ] = await Promise.all([
      getStockMovements(),
      getProducts(),
    ])

    movements.value = movementData
    products.value = productData
  } finally {
    loading.value = false
  }
}


onMounted(loadData)
</script>

<template>
  <div class="inventory-page">

    <div class="page-header">
      <div>
        <h1>Stock Movements</h1>

        <p>
          Complete history of inventory
          received and released.
        </p>
      </div>
    </div>


    <section class="panel">

      <div class="products-toolbar">

        <div class="products-search">
          <Search :size="17" />

          <input
            v-model="searchQuery"
            placeholder="Search movements..."
          />
        </div>

        <div class="product-count">
          {{ filteredMovements.length }}
          movements
        </div>

      </div>


      <div class="table-wrapper">

        <table>

          <thead>
            <tr>
              <th>Product</th>
              <th>Type</th>
              <th>Quantity</th>
              <th>Stock After</th>
              <th>Reference</th>
              <th>Notes</th>
              <th>Date</th>
            </tr>
          </thead>

          <tbody>

            <tr v-if="loading">
              <td
                colspan="7"
                class="table-message"
              >
                Loading movements...
              </td>
            </tr>

            <tr
              v-for="movement in filteredMovements"
              v-else
              :key="movement.id"
            >

              <td>
                {{ productName(movement.product_id) }}
              </td>

              <td>
                <span
                  class="movement-type"
                  :class="
                    movement.movement_type === 'IN'
                      ? 'movement-in'
                      : 'movement-out'
                  "
                >

                  <ArrowDownToLine
                    v-if="
                      movement.movement_type === 'IN'
                    "
                    :size="14"
                  />

                  <ArrowUpFromLine
                    v-else
                    :size="14"
                  />

                  {{
                    movement.movement_type === 'IN'
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
                {{ movement.reference || '—' }}
              </td>

              <td>
                {{ movement.notes || '—' }}
              </td>

              <td>
                {{ formatDate(movement.created_at) }}
              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </section>

  </div>
</template>