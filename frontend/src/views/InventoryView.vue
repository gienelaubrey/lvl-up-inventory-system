<script setup lang="ts">
import {
  computed,
  onMounted,
  reactive,
  ref,
} from 'vue'

import {
  ArrowDownToLine,
  ArrowUpFromLine,
  Search,
} from 'lucide-vue-next'

import {
  getCategories,
  getProducts,
  getStockMovements,
  stockIn,
  stockOut,
  type Category,
  type Product,
  type StockMovement,
} from '../services/api'

type MovementMode = 'IN' | 'OUT'

const products = ref<Product[]>([])
const categories = ref<Category[]>([])
const movements = ref<StockMovement[]>([])

const loading = ref(true)
const submitting = ref(false)
const searchQuery = ref('')
const message = ref('')
const errorMessage = ref('')
const mode = ref<MovementMode>('IN')

const form = reactive({
  product_id: '',
  quantity: 1,
  reason: 'RECEIPT',
  reference: '',
  notes: '',
})

const filteredProducts = computed(() => {
  const query =
    searchQuery.value.trim().toLowerCase()

  if (!query) {
    return products.value
  }

  return products.value.filter(
    (product) =>
      product.sku.toLowerCase().includes(query) ||
      product.name.toLowerCase().includes(query)
  )
})

const selectedProduct = computed(() =>
  products.value.find(
    (product) =>
      product.id === Number(form.product_id)
  )
)

const totalStock = computed(() =>
  products.value.reduce(
    (total, product) =>
      total + product.current_stock,
    0
  )
)

const lowStockCount = computed(() =>
  products.value.filter(
    (product) =>
      product.current_stock <=
      product.reorder_level
  ).length
)

const recentMovements = computed(
  () => movements.value.slice(0, 8)
)

function categoryName(
  categoryId: number | null
) {
  if (categoryId === null) {
    return 'Uncategorized'
  }

  return (
    categories.value.find(
      (category) =>
        category.id === categoryId
    )?.name ?? 'Unknown'
  )
}

function stockStatus(product: Product) {
  if (product.current_stock === 0) {
    return 'Out'
  }

  if (
    product.current_stock <=
    product.reorder_level
  ) {
    return 'Low'
  }

  return 'Healthy'
}

function setMode(value: MovementMode) {
  mode.value = value
  message.value = ''
  errorMessage.value = ''

  form.reason =
    value === 'IN'
      ? 'RECEIPT'
      : 'SALE'
}

async function loadData() {
  loading.value = true

  try {
    const [
      productData,
      categoryData,
      movementData,
    ] = await Promise.all([
      getProducts(),
      getCategories(),
      getStockMovements(),
    ])

    products.value = productData
    categories.value = categoryData
    movements.value = movementData
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to load inventory.'
  } finally {
    loading.value = false
  }
}

async function submitMovement() {
  message.value = ''
  errorMessage.value = ''

  if (!form.product_id) {
    errorMessage.value = 'Select a product.'
    return
  }

  if (Number(form.quantity) <= 0) {
    errorMessage.value =
      'Quantity must be greater than zero.'
    return
  }

  submitting.value = true

  const payload = {
    product_id: Number(form.product_id),
    quantity: Number(form.quantity),
    reason: form.reason,
    reference:
      form.reference.trim() || null,
    notes:
      form.notes.trim() || null,
  }

  try {
    const result =
      mode.value === 'IN'
        ? await stockIn(payload)
        : await stockOut(payload)

    message.value =
      mode.value === 'IN'
        ? `Stock received. New balance: ${result.stock_after}.`
        : `Stock released. Remaining balance: ${result.stock_after}.`

    form.quantity = 1
    form.reference = ''
    form.notes = ''

    await loadData()
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to save movement.'
  } finally {
    submitting.value = false
  }
}

onMounted(loadData)
</script>

<template>
  <div class="inventory-hub">
    <section class="inventory-heading">
      <div>
        <span class="eyebrow">Warehouse operations</span>
        <h1>Inventory</h1>
        <p>
          Monitor stock balances and record Stock In or
          Stock Out from one workspace.
        </p>
      </div>
    </section>

    <section class="inventory-stat-grid">
      <article>
        <span>Total Products</span>
        <strong>{{ products.length }}</strong>
      </article>

      <article>
        <span>Total Units</span>
        <strong>{{ totalStock.toLocaleString() }}</strong>
      </article>

      <article>
        <span>Low / Out of Stock</span>
        <strong>{{ lowStockCount }}</strong>
      </article>
    </section>

    <section class="inventory-work-grid">
      <article class="inventory-card transaction-card">
        <div class="inventory-card-head">
          <div>
            <span class="card-kicker">Stock transaction</span>
            <h2>Record Movement</h2>
          </div>
        </div>

        <div class="movement-toggle">
          <button
            type="button"
            :class="{ active: mode === 'IN' }"
            @click="setMode('IN')"
          >
            <ArrowDownToLine :size="16" />
            Stock In
          </button>

          <button
            type="button"
            :class="{ active: mode === 'OUT' }"
            @click="setMode('OUT')"
          >
            <ArrowUpFromLine :size="16" />
            Stock Out
          </button>
        </div>

        <form
          class="movement-form"
          @submit.prevent="submitMovement"
        >
          <label>
            Product
            <select
              v-model="form.product_id"
              required
            >
              <option value="">
                Select product
              </option>

              <option
                v-for="product in products"
                :key="product.id"
                :value="product.id"
              >
                {{ product.sku }} — {{ product.name }}
              </option>
            </select>
          </label>

          <div
            v-if="selectedProduct"
            class="selected-product-summary"
          >
            <div>
              <span>Current Stock</span>
              <strong>
                {{ selectedProduct.current_stock }}
              </strong>
            </div>

            <div>
              <span>Reorder Level</span>
              <strong>
                {{ selectedProduct.reorder_level }}
              </strong>
            </div>
          </div>

          <div class="movement-form-grid">
            <label>
              Quantity
              <input
                v-model.number="form.quantity"
                type="number"
                min="1"
                required
              />
            </label>

            <label>
              Reason
              <select v-model="form.reason">
                <template v-if="mode === 'IN'">
                  <option value="RECEIPT">Receipt</option>
                  <option value="RETURN">Return</option>
                  <option value="ADJUSTMENT">Adjustment</option>
                </template>

                <template v-else>
                  <option value="SALE">Sale</option>
                  <option value="DAMAGE">Damage</option>
                  <option value="RETURN">Return</option>
                  <option value="ADJUSTMENT">Adjustment</option>
                </template>
              </select>
            </label>
          </div>

          <label>
            Reference
            <input
              v-model="form.reference"
              type="text"
              placeholder="PO / DR / SALE reference"
            />
          </label>

          <label>
            Notes
            <textarea
              v-model="form.notes"
              rows="3"
              placeholder="Optional notes"
            ></textarea>
          </label>

          <div
            v-if="message"
            class="movement-message success"
          >
            {{ message }}
          </div>

          <div
            v-if="errorMessage"
            class="movement-message error"
          >
            {{ errorMessage }}
          </div>

          <button
            type="submit"
            class="movement-submit"
            :disabled="submitting"
          >
            <component
              :is="
                mode === 'IN'
                  ? ArrowDownToLine
                  : ArrowUpFromLine
              "
              :size="17"
            />

            {{
              submitting
                ? 'Saving...'
                : mode === 'IN'
                  ? 'Receive Stock'
                  : 'Release Stock'
            }}
          </button>
        </form>
      </article>

      <article class="inventory-card recent-movements-card">
        <div class="inventory-card-head">
          <div>
            <span class="card-kicker">Activity</span>
            <h2>Recent Movements</h2>
          </div>
        </div>

        <div class="movement-list">
          <div
            v-for="movement in recentMovements"
            :key="movement.id"
            class="movement-row"
          >
            <div
              class="movement-row-icon"
              :class="
                movement.movement_type === 'IN'
                  ? 'movement-row-in'
                  : 'movement-row-out'
              "
            >
              <ArrowDownToLine
                v-if="movement.movement_type === 'IN'"
                :size="15"
              />
              <ArrowUpFromLine
                v-else
                :size="15"
              />
            </div>

            <div>
              <strong>
                {{
                  products.find(
                    (product) =>
                      product.id === movement.product_id
                  )?.sku || `#${movement.product_id}`
                }}
              </strong>

              <span>
                {{ movement.movement_type }}
                · {{ movement.quantity }} units
              </span>
            </div>

            <b>{{ movement.stock_after }}</b>
          </div>
        </div>
      </article>
    </section>

    <section class="inventory-card inventory-table-card">
      <div class="inventory-table-toolbar">
        <div>
          <span class="card-kicker">Current balance</span>
          <h2>Stock Overview</h2>
        </div>

        <div class="inventory-search">
          <Search :size="16" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search SKU or product..."
          />
        </div>
      </div>

      <div class="inventory-table-wrap">
        <table>
          <thead>
            <tr>
              <th>SKU</th>
              <th>Product</th>
              <th>Category</th>
              <th>Unit</th>
              <th>Current Stock</th>
              <th>Reorder</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="product in filteredProducts"
              :key="product.id"
            >
              <td>
                <span class="sku-chip">
                  {{ product.sku }}
                </span>
              </td>

              <td>
                <strong>{{ product.name }}</strong>
              </td>

              <td>
                {{ categoryName(product.category_id) }}
              </td>

              <td>{{ product.unit }}</td>

              <td>
                <strong>{{ product.current_stock }}</strong>
              </td>

              <td>{{ product.reorder_level }}</td>

              <td>
                <span
                  class="status-chip"
                  :class="
                    `status-${stockStatus(product).toLowerCase()}`
                  "
                >
                  {{ stockStatus(product) }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<style scoped src="../styles/inventory-combined.css"></style>
