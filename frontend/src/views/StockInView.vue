<script setup lang="ts">
import {
  onMounted,
  reactive,
  ref,
} from 'vue'

import {
  ArrowDownToLine,
} from 'lucide-vue-next'

import {
  getProducts,
  stockIn,
  type Product,
} from '../services/api'


const products = ref<Product[]>([])
const submitting = ref(false)
const message = ref('')
const error = ref('')


const form = reactive({
  product_id: '',
  quantity: 1,
  reason: 'RECEIPT',
  reference: '',
  notes: '',
})


async function loadProducts() {
  products.value = await getProducts()
}


async function submit() {
  message.value = ''
  error.value = ''

  if (!form.product_id) {
    error.value = 'Select a product.'
    return
  }

  submitting.value = true

  try {
    const result = await stockIn({
      product_id: Number(form.product_id),
      quantity: Number(form.quantity),
      reason: form.reason,
      reference: form.reference.trim() || null,
      notes: form.notes.trim() || null,
    })

    message.value =
      `Stock added successfully. ` +
      `New stock: ${result.stock_after}`

    form.quantity = 1
    form.reference = ''
    form.notes = ''

    await loadProducts()
  } catch (err) {
    error.value =
      err instanceof Error
        ? err.message
        : 'Unable to add stock'
  } finally {
    submitting.value = false
  }
}


onMounted(loadProducts)
</script>

<template>
  <div class="stock-page">

    <div class="page-header">
      <div>
        <h1>Stock In</h1>

        <p>
          Record inventory received by
          LVL UP Enterprises OPC.
        </p>
      </div>
    </div>


    <section class="panel stock-form-panel">

      <div class="panel-header">
        <div>
          <h2>Receive Stock</h2>
          <p>
            Add units to an existing product.
          </p>
        </div>

        <ArrowDownToLine :size="21" />
      </div>


      <form
        class="stock-form"
        @submit.prevent="submit"
      >

        <div
          v-if="message"
          class="alert success-alert"
        >
          {{ message }}
        </div>

        <div
          v-if="error"
          class="alert error-alert"
        >
          {{ error }}
        </div>


        <div class="form-field">
          <label>Product</label>

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
              {{ product.sku }}
              — {{ product.name }}
              (Stock: {{ product.current_stock }})
            </option>
          </select>
        </div>


        <div class="form-field">
          <label>Quantity</label>

          <input
            v-model.number="form.quantity"
            type="number"
            min="1"
            required
          />
        </div>


        <div class="form-field">
          <label>Reference</label>

          <input
            v-model="form.reference"
            placeholder="PO-001 / DR-001"
          />
        </div>


        <div class="form-field">
          <label>Notes</label>

          <textarea
            v-model="form.notes"
            rows="4"
            placeholder="Optional notes"
          />
        </div>


        <button
          class="primary-button"
          type="submit"
          :disabled="submitting"
        >
          {{
            submitting
              ? 'Saving...'
              : 'Receive Stock'
          }}
        </button>

      </form>

    </section>

  </div>
</template>