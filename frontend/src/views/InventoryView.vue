<script setup lang="ts">
import {
  computed,
  onMounted,
  ref,
} from 'vue'

import {
  Boxes,
  Search,
  TriangleAlert,
} from 'lucide-vue-next'

import {
  getCategories,
  getProducts,
  type Category,
  type Product,
} from '../services/api'


const products = ref<Product[]>([])
const categories = ref<Category[]>([])

const loading = ref(true)
const searchQuery = ref('')


const filteredProducts = computed(() => {
  const query =
    searchQuery.value.trim().toLowerCase()

  if (!query) {
    return products.value
  }

  return products.value.filter((product) =>
    product.name.toLowerCase().includes(query) ||
    product.sku.toLowerCase().includes(query)
  )
})


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
    return 'out'
  }

  if (
    product.current_stock <=
    product.reorder_level
  ) {
    return 'low'
  }

  return 'healthy'
}


async function loadInventory() {
  loading.value = true

  try {
    const [
      productData,
      categoryData,
    ] = await Promise.all([
      getProducts(),
      getCategories(),
    ])

    products.value = productData
    categories.value = categoryData
  } finally {
    loading.value = false
  }
}


onMounted(loadInventory)
</script>

<template>
  <div class="inventory-page">

    <div class="page-header">
      <div>
        <h1>Inventory</h1>

        <p>
          Monitor current stock levels across
          all LVL UP products.
        </p>
      </div>
    </div>

    <div class="inventory-summary">

      <div class="inventory-summary-card">
        <Boxes :size="22" />

        <div>
          <span>Total Units</span>

          <strong>
            {{
              products.reduce(
                (total, product) =>
                  total + product.current_stock,
                0
              )
            }}
          </strong>
        </div>
      </div>

      <div class="inventory-summary-card">
        <TriangleAlert :size="22" />

        <div>
          <span>Low / Out of Stock</span>

          <strong>
            {{
              products.filter(
                (product) =>
                  product.current_stock <=
                  product.reorder_level
              ).length
            }}
          </strong>
        </div>
      </div>

    </div>


    <section class="panel">

      <div class="products-toolbar">

        <div class="products-search">
          <Search :size="17" />

          <input
            v-model="searchQuery"
            placeholder="Search inventory..."
          />
        </div>

        <div class="product-count">
          {{ filteredProducts.length }}
          products
        </div>

      </div>


      <div class="table-wrapper">

        <table class="products-table">

          <thead>
            <tr>
              <th>SKU</th>
              <th>Product</th>
              <th>Category</th>
              <th>Unit</th>
              <th>Current Stock</th>
              <th>Reorder Level</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>

            <tr v-if="loading">
              <td
                colspan="7"
                class="table-message"
              >
                Loading inventory...
              </td>
            </tr>

            <tr
              v-for="product in filteredProducts"
              v-else
              :key="product.id"
            >

              <td>
                <span class="sku">
                  {{ product.sku }}
                </span>
              </td>

              <td>
                <strong class="product-name">
                  {{ product.name }}
                </strong>
              </td>

              <td>
                {{
                  categoryName(
                    product.category_id
                  )
                }}
              </td>

              <td>
                {{ product.unit }}
              </td>

              <td>
                <strong>
                  {{ product.current_stock }}
                </strong>
              </td>

              <td>
                {{ product.reorder_level }}
              </td>

              <td>
                <span
                  class="stock-badge"
                  :class="
                    `stock-${stockStatus(product)}`
                  "
                >
                  {{
                    stockStatus(product) ===
                    'healthy'
                      ? 'In Stock'
                      : stockStatus(product) ===
                        'low'
                        ? 'Low Stock'
                        : 'Out of Stock'
                  }}
                </span>
              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </section>

  </div>
</template>