<script setup lang="ts">
import {
  computed,
  onMounted,
  reactive,
  ref,
} from 'vue'

import {
  Package,
  Plus,
  Search,
  X,
  AlertCircle,
} from 'lucide-vue-next'

import {
  createProduct,
  getCategories,
  getProducts,
  type Category,
  type Product,
} from '../services/api'


const products = ref<Product[]>([])
const categories = ref<Category[]>([])

const loading = ref(true)
const submitting = ref(false)

const errorMessage = ref('')
const successMessage = ref('')

const searchQuery = ref('')

const showModal = ref(false)


const form = reactive({
  sku: '',
  name: '',
  category_id: '',
  unit: 'piece',
  cost_price: 0,
  selling_price: 0,
  reorder_level: 0,
})


const filteredProducts = computed(() => {
  const query = searchQuery.value
    .trim()
    .toLowerCase()

  if (!query) {
    return products.value
  }

  return products.value.filter((product) => {
    return (
      product.name
        .toLowerCase()
        .includes(query) ||

      product.sku
        .toLowerCase()
        .includes(query)
    )
  })
})


function getCategoryName(
  categoryId: number | null
) {
  if (categoryId === null) {
    return 'Uncategorized'
  }

  const category = categories.value.find(
    (item) => item.id === categoryId
  )

  return category?.name ?? 'Unknown'
}


function formatCurrency(
  value: number | string
) {
  const amount = Number(value)

  return new Intl.NumberFormat(
    'en-PH',
    {
      style: 'currency',
      currency: 'PHP',
    }
  ).format(amount)
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


function resetForm() {
  form.sku = ''
  form.name = ''
  form.category_id = ''
  form.unit = 'piece'
  form.cost_price = 0
  form.selling_price = 0
  form.reorder_level = 0
}


function openModal() {
  errorMessage.value = ''
  successMessage.value = ''

  resetForm()

  showModal.value = true
}


function closeModal() {
  if (submitting.value) {
    return
  }

  showModal.value = false
}


async function loadData() {
  loading.value = true
  errorMessage.value = ''

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
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to load products'
  } finally {
    loading.value = false
  }
}


async function submitProduct() {
  errorMessage.value = ''
  successMessage.value = ''

  if (
    !form.sku.trim() ||
    !form.name.trim()
  ) {
    errorMessage.value =
      'SKU and product name are required.'

    return
  }

  submitting.value = true

  try {
    await createProduct({
      sku: form.sku.trim(),
      name: form.name.trim(),

      category_id:
        form.category_id === ''
          ? null
          : Number(form.category_id),

      unit: form.unit.trim(),

      cost_price:
        Number(form.cost_price),

      selling_price:
        Number(form.selling_price),

      reorder_level:
        Number(form.reorder_level),
    })

    await loadData()

    showModal.value = false

    successMessage.value =
      'Product added successfully.'

    resetForm()
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to create product'
  } finally {
    submitting.value = false
  }
}


onMounted(loadData)
</script>


<template>
  <div class="products-page">

    <div class="page-header">

      <div>
        <h1>Products</h1>

        <p>
          Manage the products registered in
          LVL UP inventory.
        </p>
      </div>

      <button
        class="primary-button"
        @click="openModal"
      >
        <Plus :size="17" />
        Add Product
      </button>

    </div>


    <div
      v-if="successMessage"
      class="alert success-alert"
    >
      {{ successMessage }}
    </div>


    <div
      v-if="errorMessage && !showModal"
      class="alert error-alert"
    >
      <AlertCircle :size="17" />
      {{ errorMessage }}
    </div>


    <section class="panel products-panel">

      <div class="products-toolbar">

        <div class="products-search">
          <Search :size="17" />

          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search by name or SKU..."
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
              <th>Cost</th>
              <th>Selling Price</th>
              <th>Stock</th>
              <th>Status</th>
            </tr>
          </thead>


          <tbody>

            <tr v-if="loading">
              <td
                colspan="8"
                class="table-message"
              >
                Loading products...
              </td>
            </tr>


            <tr
              v-else-if="
                filteredProducts.length === 0
              "
            >
              <td
                colspan="8"
                class="table-message"
              >
                <div class="empty-products">

                  <Package :size="30" />

                  <strong>
                    No products found
                  </strong>

                  <span>
                    Add your first inventory product.
                  </span>

                </div>
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
                  getCategoryName(
                    product.category_id
                  )
                }}
              </td>

              <td>
                {{ product.unit }}
              </td>

              <td>
                {{
                  formatCurrency(
                    product.cost_price
                  )
                }}
              </td>

              <td>
                {{
                  formatCurrency(
                    product.selling_price
                  )
                }}
              </td>

              <td>
                <strong>
                  {{ product.current_stock }}
                </strong>
              </td>

              <td>

                <span
                  class="stock-badge"
                  :class="
                    `stock-${stockStatus(product)}`
                  "
                >

                  <template
                    v-if="
                      stockStatus(product) ===
                      'healthy'
                    "
                  >
                    In Stock
                  </template>

                  <template
                    v-else-if="
                      stockStatus(product) ===
                      'low'
                    "
                  >
                    Low Stock
                  </template>

                  <template v-else>
                    Out of Stock
                  </template>

                </span>

              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </section>


    <!-- ADD PRODUCT MODAL -->

    <div
      v-if="showModal"
      class="modal-backdrop"
      @click.self="closeModal"
    >

      <div class="modal-card">

        <div class="modal-header">

          <div>
            <h2>Add Product</h2>

            <p>
              Register a new product in the
              LVL UP inventory.
            </p>
          </div>

          <button
            class="modal-close"
            type="button"
            @click="closeModal"
          >
            <X :size="20" />
          </button>

        </div>


        <form
          class="product-form"
          @submit.prevent="submitProduct"
        >

          <div
            v-if="errorMessage"
            class="alert error-alert"
          >
            <AlertCircle :size="17" />
            {{ errorMessage }}
          </div>


          <div class="form-grid">

            <div class="form-field">
              <label for="sku">
                SKU
              </label>

              <input
                id="sku"
                v-model="form.sku"
                type="text"
                placeholder="LVL-003"
                required
              />
            </div>


            <div class="form-field">
              <label for="name">
                Product Name
              </label>

              <input
                id="name"
                v-model="form.name"
                type="text"
                placeholder="Product name"
                required
              />
            </div>


            <div class="form-field">
              <label for="category">
                Category
              </label>

              <select
                id="category"
                v-model="form.category_id"
              >

                <option value="">
                  No category
                </option>

                <option
                  v-for="category in categories"
                  :key="category.id"
                  :value="category.id"
                >
                  {{ category.name }}
                </option>

              </select>
            </div>


            <div class="form-field">
              <label for="unit">
                Unit
              </label>

              <select
                id="unit"
                v-model="form.unit"
              >
                <option value="piece">
                  Piece
                </option>

                <option value="box">
                  Box
                </option>

                <option value="pack">
                  Pack
                </option>

                <option value="set">
                  Set
                </option>

                <option value="case">
                  Case
                </option>
              </select>
            </div>


            <div class="form-field">
              <label for="cost">
                Cost Price
              </label>

              <input
                id="cost"
                v-model.number="
                  form.cost_price
                "
                type="number"
                min="0"
                step="0.01"
              />
            </div>


            <div class="form-field">
              <label for="selling">
                Selling Price
              </label>

              <input
                id="selling"
                v-model.number="
                  form.selling_price
                "
                type="number"
                min="0"
                step="0.01"
              />
            </div>


            <div class="form-field">
              <label for="reorder">
                Reorder Level
              </label>

              <input
                id="reorder"
                v-model.number="
                  form.reorder_level
                "
                type="number"
                min="0"
                step="1"
              />
            </div>

          </div>


          <div class="modal-actions">

            <button
              type="button"
              class="secondary-button"
              :disabled="submitting"
              @click="closeModal"
            >
              Cancel
            </button>

            <button
              type="submit"
              class="primary-button"
              :disabled="submitting"
            >
              {{
                submitting
                  ? 'Adding...'
                  : 'Add Product'
              }}
            </button>

          </div>

        </form>

      </div>

    </div>

  </div>
</template>