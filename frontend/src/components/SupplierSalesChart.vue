<script setup lang="ts">
import {
  computed,
  nextTick,
  onBeforeUnmount,
  onMounted,
  ref,
  watch,
} from 'vue'

import Chart from 'chart.js/auto'

import {
  getSalesBySupplier,
  type SupplierSalesAnalytics,
} from '../services/api'


const analytics =
  ref<SupplierSalesAnalytics[]>([])

const loading = ref(true)
const errorMessage = ref('')

const selectedSupplierId =
  ref<number | null>(null)

const metric =
  ref<'units' | 'value'>('units')

const canvas =
  ref<HTMLCanvasElement | null>(null)

let chart: Chart | null = null


const selectedSupplier = computed(() => {
  return analytics.value.find(
    (supplier) =>
      supplier.supplier_id ===
      selectedSupplierId.value
  )
})

async function loadAnalytics() {
  loading.value = true
  errorMessage.value = ''

  try {
    analytics.value =
      await getSalesBySupplier()

    if (analytics.value.length > 0) {
      selectedSupplierId.value =
        analytics.value[0].supplier_id
    }
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to load analytics'
  } finally {
    loading.value = false
  }

  await nextTick()

  if (
    !errorMessage.value &&
    analytics.value.length > 0
  ) {
    renderChart()
  }
}


function renderChart() {
  if (!canvas.value) {
    return
  }

  chart?.destroy()

  const supplier =
    selectedSupplier.value

  if (!supplier) {
    return
  }

  const products = [
    ...supplier.products,
  ].sort((a, b) => {
    if (metric.value === 'units') {
      return (
        b.units_sold -
        a.units_sold
      )
    }

    return (
      Number(b.sales_value) -
      Number(a.sales_value)
    )
  })


  chart = new Chart(
    canvas.value,
    {
      type: 'bar',

      data: {
        labels: products.map(
          (product) => product.sku
        ),

        datasets: [
          {
            label:
              metric.value === 'units'
                ? 'Units Sold'
                : 'Sales Value',

            data: products.map(
              (product) =>
                metric.value === 'units'
                  ? product.units_sold
                  : Number(
                      product.sales_value
                    )
            ),

            backgroundColor:
              '#7b1e23',

            borderColor:
              '#4f1115',

            borderWidth: 1,

            borderRadius: 6,
          },
        ],
      },

      options: {
        responsive: true,

        maintainAspectRatio: false,

        indexAxis: 'y',

        plugins: {
          legend: {
            display: false,
          },

          tooltip: {
            callbacks: {
              label(context) {
                if (
                  metric.value ===
                  'value'
                ) {
                  return new Intl.NumberFormat(
                    'en-PH',
                    {
                      style: 'currency',
                      currency: 'PHP',
                    }
                  ).format(
                    Number(context.raw)
                  )
                }

                return (
                  `${context.raw} units`
                )
              },
            },
          },
        },

        scales: {
          x: {
            beginAtZero: true,

            grid: {
              color:
                'rgba(80, 60, 55, 0.08)',
            },

            ticks: {
              color: '#7c706d',
            },
          },

          y: {
            grid: {
              display: false,
            },

            ticks: {
              color: '#514846',
            },
          },
        },
      },
    }
  )
}


watch(
  [
    selectedSupplierId,
    metric,
  ],

  async () => {
    await nextTick()

    renderChart()
  }
)


onMounted(loadAnalytics)


onBeforeUnmount(() => {
  chart?.destroy()
})
</script>


<template>
  <section class="analytics-card">

    <div class="analytics-header">

      <div>
        <h2>SKU Sales Ranking</h2>

        <p>
          Highest to lowest selling products
          by supplier.
        </p>
      </div>


      <div class="analytics-controls">

        <select
          v-model="selectedSupplierId"
        >
          <option
            v-for="supplier in analytics"
            :key="supplier.supplier_id"
            :value="supplier.supplier_id"
          >
            {{ supplier.supplier_name }}
          </option>
        </select>


        <select v-model="metric">

          <option value="units">
            Units Sold
          </option>

          <option value="value">
            Sales Value
          </option>

        </select>

      </div>

    </div>


    <div
      v-if="loading"
      class="analytics-empty"
    >
      Loading analytics...
    </div>


    <div
      v-else-if="errorMessage"
      class="analytics-empty"
    >
      {{ errorMessage }}
    </div>


    <div
      v-else-if="analytics.length"
      class="analytics-canvas"
    >
      <canvas ref="canvas"></canvas>
    </div>


    <div
      v-else
      class="analytics-empty"
    >
      No supplier sales data available yet.
    </div>

  </section>
</template>


<style
  scoped
  src="../styles/supplier-sales-chart.css"
></style>