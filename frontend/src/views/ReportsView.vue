<script setup lang="ts">
import {
  computed,
  onMounted,
  ref,
} from 'vue'

import {
  CalendarDays,
  Download,
  FileText,
} from 'lucide-vue-next'

import {
  downloadSupplierReport,
  getSuppliers,
  type Supplier,
} from '../services/api'


const suppliers =
  ref<Supplier[]>([])

const supplierId =
  ref<number | ''>('')

const startDate =
  ref('')

const endDate =
  ref('')

const generating =
  ref(false)

const errorMessage =
  ref('')


const selectedSupplier =
  computed(() => {
    return suppliers.value.find(
      (supplier) =>
        supplier.id ===
        supplierId.value
    )
  })


function localDateString(
  date: Date
) {
  const year =
    date.getFullYear()

  const month =
    String(
      date.getMonth() + 1
    ).padStart(2, '0')

  const day =
    String(
      date.getDate()
    ).padStart(2, '0')

  return (
    `${year}-` +
    `${month}-` +
    `${day}`
  )
}


function applyPreset(
  preset:
    | 'today'
    | '3days'
    | 'week'
    | 'month'
    | 'year'
) {
  const end =
    new Date()

  let start =
    new Date(end)


  if (preset === '3days') {
    start.setDate(
      start.getDate() - 2
    )
  }


  if (preset === 'week') {
    start.setDate(
      start.getDate() - 6
    )
  }


  if (preset === 'month') {
    start =
      new Date(
        end.getFullYear(),
        end.getMonth(),
        1
      )
  }


  if (preset === 'year') {
    start =
      new Date(
        end.getFullYear(),
        0,
        1
      )
  }


  startDate.value =
    localDateString(start)

  endDate.value =
    localDateString(end)
}


async function generateReport() {
  errorMessage.value = ''

  if (!supplierId.value) {
    errorMessage.value =
      'Please select a supplier.'

    return
  }


  if (
    !startDate.value ||
    !endDate.value
  ) {
    errorMessage.value =
      'Please select a date range.'

    return
  }


  if (
    endDate.value <
    startDate.value
  ) {
    errorMessage.value =
      'End date cannot be before start date.'

    return
  }


  generating.value = true


  try {
    const blob =
      await downloadSupplierReport(
        Number(
          supplierId.value
        ),
        startDate.value,
        endDate.value
      )


    const url =
      URL.createObjectURL(
        blob
      )


    const link =
      document.createElement(
        'a'
      )


    const safeName =
      (
        selectedSupplier.value
          ?.name ||
        'supplier'
      )
        .replace(
          /[^a-z0-9]+/gi,
          '-'
        )
        .toLowerCase()


    link.href = url

    link.download =
      `${safeName}-report-` +
      `${startDate.value}-` +
      `${endDate.value}.pdf`


    document.body.appendChild(
      link
    )

    link.click()

    link.remove()

    URL.revokeObjectURL(
      url
    )
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to generate report'
  } finally {
    generating.value = false
  }
}


onMounted(
  async () => {
    suppliers.value =
      await getSuppliers()

    applyPreset(
      'week'
    )
  }
)
</script>


<template>
  <div class="reports-page">

    <div class="page-header">

      <div>

        <h1>
          Supplier Reports
        </h1>

        <p>
          Generate supplier performance
          and inventory reports.
        </p>

      </div>

    </div>


    <section class="report-card">

      <div class="report-card-header">

        <div
          class="report-heading-icon"
        >
          <FileText
            :size="21"
          />
        </div>


        <div>

          <h2>
            Generate Report
          </h2>

          <p>
            Select a supplier and
            reporting period.
          </p>

        </div>

      </div>


      <div class="report-form">

        <div class="form-field">

          <label>
            Supplier
          </label>

          <select
            v-model="supplierId"
          >

            <option value="">
              Select supplier
            </option>

            <option
              v-for="
                supplier in suppliers
              "
              :key="supplier.id"
              :value="supplier.id"
            >
              {{ supplier.name }}
            </option>

          </select>

        </div>


        <div class="preset-section">

          <label>
            Quick Range
          </label>


          <div
            class="preset-buttons"
          >

            <button
              type="button"
              @click="
                applyPreset(
                  'today'
                )
              "
            >
              Today
            </button>


            <button
              type="button"
              @click="
                applyPreset(
                  '3days'
                )
              "
            >
              3 Days
            </button>


            <button
              type="button"
              @click="
                applyPreset(
                  'week'
                )
              "
            >
              7 Days
            </button>


            <button
              type="button"
              @click="
                applyPreset(
                  'month'
                )
              "
            >
              This Month
            </button>


            <button
              type="button"
              @click="
                applyPreset(
                  'year'
                )
              "
            >
              This Year
            </button>

          </div>

        </div>


        <div class="date-grid">

          <div class="form-field">

            <label>
              Start Date
            </label>

            <div
              class="date-input"
            >
              <CalendarDays
                :size="16"
              />

              <input
                v-model="startDate"
                type="date"
              />
            </div>

          </div>


          <div class="form-field">

            <label>
              End Date
            </label>

            <div
              class="date-input"
            >
              <CalendarDays
                :size="16"
              />

              <input
                v-model="endDate"
                type="date"
              />
            </div>

          </div>

        </div>


        <div
          v-if="errorMessage"
          class="report-error"
        >
          {{ errorMessage }}
        </div>


        <button
          type="button"
          class="report-generate-button"
          :disabled="generating"
          @click="generateReport"
        >

          <Download
            :size="17"
          />

          {{
            generating
              ? 'Generating...'
              : 'Generate PDF'
          }}

        </button>

      </div>

    </section>

  </div>
</template>


<style
  scoped
  src="../styles/reports.css"
></style>