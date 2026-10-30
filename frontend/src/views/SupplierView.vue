<script setup lang="ts">
import {
  computed,
  onMounted,
  reactive,
  ref,
} from 'vue'

import {
  AlertCircle,
  Pencil,
  Plus,
  Search,
  Trash2,
  Truck,
  X,
} from 'lucide-vue-next'

import {
  createSupplier,
  deleteSupplier,
  getSuppliers,
  updateSupplier,
  type Supplier,
} from '../services/api'


const suppliers = ref<Supplier[]>([])

const loading = ref(true)
const submitting = ref(false)

const searchQuery = ref('')

const errorMessage = ref('')
const successMessage = ref('')

const showModal = ref(false)
const editingSupplierId = ref<number | null>(null)


const form = reactive({
  name: '',
  contact_person: '',
  phone: '',
  email: '',
  address: '',
  notes: '',
})


const filteredSuppliers = computed(() => {
  const query =
    searchQuery.value.trim().toLowerCase()

  if (!query) {
    return suppliers.value
  }

  return suppliers.value.filter((supplier) => {
    return (
      supplier.name
        .toLowerCase()
        .includes(query) ||

      supplier.contact_person
        ?.toLowerCase()
        .includes(query) ||

      supplier.email
        ?.toLowerCase()
        .includes(query) ||

      supplier.phone
        ?.toLowerCase()
        .includes(query)
    )
  })
})


function resetForm() {
  form.name = ''
  form.contact_person = ''
  form.phone = ''
  form.email = ''
  form.address = ''
  form.notes = ''
}


function openAddModal() {
  editingSupplierId.value = null

  errorMessage.value = ''
  successMessage.value = ''

  resetForm()

  showModal.value = true
}


function openEditModal(
  supplier: Supplier
) {
  editingSupplierId.value =
    supplier.id

  errorMessage.value = ''
  successMessage.value = ''

  form.name =
    supplier.name

  form.contact_person =
    supplier.contact_person ?? ''

  form.phone =
    supplier.phone ?? ''

  form.email =
    supplier.email ?? ''

  form.address =
    supplier.address ?? ''

  form.notes =
    supplier.notes ?? ''

  showModal.value = true
}


function closeModal() {
  if (submitting.value) {
    return
  }

  showModal.value = false

  editingSupplierId.value = null

  resetForm()

  errorMessage.value = ''
}


function nullableValue(
  value: string
) {
  const trimmed = value.trim()

  return trimmed || null
}


async function loadSuppliers() {
  loading.value = true
  errorMessage.value = ''

  try {
    suppliers.value =
      await getSuppliers()
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to load suppliers'
  } finally {
    loading.value = false
  }
}


async function submitSupplier() {
  errorMessage.value = ''
  successMessage.value = ''

  if (!form.name.trim()) {
    errorMessage.value =
      'Supplier name is required.'

    return
  }

  submitting.value = true

  const payload = {
    name: form.name.trim(),

    contact_person:
      nullableValue(
        form.contact_person
      ),

    phone:
      nullableValue(
        form.phone
      ),

    email:
      nullableValue(
        form.email
      ),

    address:
      nullableValue(
        form.address
      ),

    notes:
      nullableValue(
        form.notes
      ),
  }

  try {
    if (
      editingSupplierId.value !== null
    ) {
      await updateSupplier(
        editingSupplierId.value,
        payload
      )

      successMessage.value =
        'Supplier updated successfully.'
    } else {
      await createSupplier(
        payload
      )

      successMessage.value =
        'Supplier added successfully.'
    }

    showModal.value = false

    editingSupplierId.value = null

    resetForm()

    await loadSuppliers()
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to save supplier'
  } finally {
    submitting.value = false
  }
}


async function removeSupplier(
  supplier: Supplier
) {
  const confirmed =
    window.confirm(
      `Delete supplier "${supplier.name}"?`
    )

  if (!confirmed) {
    return
  }

  errorMessage.value = ''
  successMessage.value = ''

  try {
    await deleteSupplier(
      supplier.id
    )

    successMessage.value =
      'Supplier deleted successfully.'

    await loadSuppliers()
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to delete supplier'
  }
}


function formatDate(
  value: string
) {
  return new Intl.DateTimeFormat(
    'en-PH',
    {
      dateStyle: 'medium',
    }
  ).format(new Date(value))
}


onMounted(loadSuppliers)
</script>


<template>
  <div class="suppliers-page">

    <div class="page-header">

      <div>
      <span class="eyebrow">PRODUCT DIRECTORY</span>
        <h1>Suppliers</h1>

        <p>
          Manage suppliers and business
          contacts for LVL UP inventory.
        </p>
      </div>

      <button
        class="primary-button"
        @click="openAddModal"
      >
        <Plus :size="17" />

        Add Supplier
      </button>

    </div>


    <div
      v-if="successMessage"
      class="alert success-alert"
    >
      {{ successMessage }}
    </div>


    <div
      v-if="
        errorMessage &&
        !showModal
      "
      class="alert error-alert"
    >
      <AlertCircle :size="17" />

      {{ errorMessage }}
    </div>


    <section class="panel">

      <div class="products-toolbar">

        <div class="products-search">

          <Search :size="17" />

          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search suppliers..."
          />

        </div>

        <div class="product-count">
          {{ filteredSuppliers.length }}
          suppliers
        </div>

      </div>


      <div class="table-wrapper">

        <table class="suppliers-table">

          <thead>
            <tr>
              <th>Supplier</th>
              <th>Contact Person</th>
              <th>Phone</th>
              <th>Email</th>
              <th>Address</th>
              <th>Added</th>
              <th>Actions</th>
            </tr>
          </thead>


          <tbody>

            <tr v-if="loading">

              <td
                colspan="7"
                class="table-message"
              >
                Loading suppliers...
              </td>

            </tr>


            <tr
              v-else-if="
                filteredSuppliers.length === 0
              "
            >

              <td
                colspan="7"
                class="table-message"
              >

                <div class="empty-products">

                  <Truck :size="30" />

                  <strong>
                    No suppliers found
                  </strong>

                  <span>
                    Add your first supplier.
                  </span>

                </div>

              </td>

            </tr>


            <tr
              v-for="
                supplier in
                filteredSuppliers
              "
              v-else
              :key="supplier.id"
            >

              <td>
                <strong
                  class="supplier-name"
                >
                  {{ supplier.name }}
                </strong>
              </td>


              <td>
                {{
                  supplier.contact_person
                    || '—'
                }}
              </td>


              <td>
                {{
                  supplier.phone
                    || '—'
                }}
              </td>


              <td>
                {{
                  supplier.email
                    || '—'
                }}
              </td>


              <td>
                <span
                  class="supplier-address"
                >
                  {{
                    supplier.address
                      || '—'
                  }}
                </span>
              </td>


              <td>
                {{
                  formatDate(
                    supplier.created_at
                  )
                }}
              </td>


              <td>

                <div
                  class="table-actions"
                >

                  <button
                    class="table-action-button"
                    title="Edit supplier"
                    @click="
                      openEditModal(
                        supplier
                      )
                    "
                  >
                    <Pencil :size="16" />
                  </button>


                  <button
                    class="
                      table-action-button
                      danger-action
                    "
                    title="Delete supplier"
                    @click="
                      removeSupplier(
                        supplier
                      )
                    "
                  >
                    <Trash2 :size="16" />
                  </button>

                </div>

              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </section>


    <!-- SUPPLIER MODAL -->

    <div
      v-if="showModal"
      class="modal-backdrop"
      @click.self="closeModal"
    >

      <div class="modal-card">

        <div class="modal-header">

          <div>

            <h2>
              {{
                editingSupplierId !== null
                  ? 'Edit Supplier'
                  : 'Add Supplier'
              }}
            </h2>

            <p>
              {{
                editingSupplierId !== null
                  ? 'Update supplier information.'
                  : 'Register a new inventory supplier.'
              }}
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
          @submit.prevent="
            submitSupplier
          "
        >

          <div
            v-if="errorMessage"
            class="alert error-alert"
          >

            <AlertCircle
              :size="17"
            />

            {{ errorMessage }}

          </div>


          <div class="form-grid">

            <div class="form-field">

              <label
                for="supplier-name"
              >
                Supplier Name
              </label>

              <input
                id="supplier-name"
                v-model="form.name"
                type="text"
                placeholder="Supplier name"
                required
              />

            </div>


            <div class="form-field">

              <label
                for="contact-person"
              >
                Contact Person
              </label>

              <input
                id="contact-person"
                v-model="
                  form.contact_person
                "
                type="text"
                placeholder="Contact person"
              />

            </div>


            <div class="form-field">

              <label
                for="supplier-phone"
              >
                Phone
              </label>

              <input
                id="supplier-phone"
                v-model="form.phone"
                type="text"
                placeholder="09XXXXXXXXX"
              />

            </div>


            <div class="form-field">

              <label
                for="supplier-email"
              >
                Email
              </label>

              <input
                id="supplier-email"
                v-model="form.email"
                type="email"
                placeholder="supplier@example.com"
              />

            </div>


            <div
              class="
                form-field
                full-width-field
              "
            >

              <label
                for="supplier-address"
              >
                Address
              </label>

              <textarea
                id="supplier-address"
                v-model="form.address"
                rows="3"
                placeholder="Supplier address"
              />

            </div>


            <div
              class="
                form-field
                full-width-field
              "
            >

              <label
                for="supplier-notes"
              >
                Notes
              </label>

              <textarea
                id="supplier-notes"
                v-model="form.notes"
                rows="3"
                placeholder="Optional notes"
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
                  ? 'Saving...'
                  : editingSupplierId !== null
                    ? 'Save Changes'
                    : 'Add Supplier'
              }}

            </button>

          </div>

        </form>

      </div>

    </div>

  </div>
</template>

<style
  scoped
  src="../styles/suppliers-executive.css"
></style>