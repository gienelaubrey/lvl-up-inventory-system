<script setup lang="ts">
import {
  nextTick,
  onBeforeUnmount,
  onMounted,
  ref,
} from 'vue'

import Chart from 'chart.js/auto'

import {
  getStockMovements,
  type StockMovement,
} from '../services/api'


const movements = ref<StockMovement[]>([])
const loading = ref(true)
const errorMessage = ref('')

const canvas =
  ref<HTMLCanvasElement | null>(null)

let chart: Chart | null = null


function dateKey(date: Date) {
  const year = date.getFullYear()

  const month = String(
    date.getMonth() + 1
  ).padStart(2, '0')

  const day = String(
    date.getDate()
  ).padStart(2, '0')

  return `${year}-${month}-${day}`
}


function dateLabel(date: Date) {
  return new Intl.DateTimeFormat(
    'en-PH',
    {
      month: 'short',
      day: 'numeric',
    }
  ).format(date)
}


function buildLastSevenDays() {
  const days = []

  for (let index = 6; index >= 0; index--) {
    const date = new Date()

    date.setHours(
      0,
      0,
      0,
      0
    )

    date.setDate(
      date.getDate() - index
    )

    days.push({
      key: dateKey(date),
      label: dateLabel(date),
      stockIn: 0,
      stockOut: 0,
    })
  }

  return days
}


function renderChart() {
  if (!canvas.value) {
    return
  }

  chart?.destroy()

  const days =
    buildLastSevenDays()

  const dayMap =
    new Map(
      days.map(
        (day) => [
          day.key,
          day,
        ]
      )
    )


  for (const movement of movements.value) {
    const movementDate =
      new Date(
        movement.created_at
      )

    const key =
      dateKey(movementDate)

    const day =
      dayMap.get(key)

    if (!day) {
      continue
    }

    if (
      movement.movement_type ===
      'IN'
    ) {
      day.stockIn +=
        movement.quantity
    }

    if (
      movement.movement_type ===
      'OUT'
    ) {
      day.stockOut +=
        movement.quantity
    }
  }


  const rootStyles =
    getComputedStyle(
      document.documentElement
    )

  const brand =
    rootStyles
      .getPropertyValue(
        '--brand-700'
      )
      .trim() ||
    '#7b1e23'

  const success =
    rootStyles
      .getPropertyValue(
        '--success'
      )
      .trim() ||
    '#2f6d49'

  const muted =
    rootStyles
      .getPropertyValue(
        '--text-500'
      )
      .trim() ||
    '#7c706d'

  const gridColor =
    'rgba(90, 70, 65, 0.08)'


  chart = new Chart(
    canvas.value,
    {
      type: 'line',

      data: {
        labels:
          days.map(
            (day) =>
              day.label
          ),

        datasets: [
          {
            label:
              'Stock In',

            data:
              days.map(
                (day) =>
                  day.stockIn
              ),

            borderColor:
              success,

            backgroundColor:
              success,

            borderWidth: 2,

            tension: 0.35,

            pointRadius: 3,

            pointHoverRadius: 5,
          },

          {
            label:
              'Stock Out',

            data:
              days.map(
                (day) =>
                  day.stockOut
              ),

            borderColor:
              brand,

            backgroundColor:
              brand,

            borderWidth: 2,

            tension: 0.35,

            pointRadius: 3,

            pointHoverRadius: 5,
          },
        ],
      },


      options: {
        responsive: true,

        maintainAspectRatio: false,

        interaction: {
          mode: 'index',
          intersect: false,
        },

        plugins: {
          legend: {
            position: 'top',

            align: 'end',

            labels: {
              usePointStyle: true,

              boxWidth: 7,

              color: muted,

              font: {
                size: 11,
              },
            },
          },

          tooltip: {
            callbacks: {
              label(context) {
                return (
                  `${context.dataset.label}: ` +
                  `${context.parsed.y} units`
                )
              },
            },
          },
        },


        scales: {
          x: {
            grid: {
              display: false,
            },

            ticks: {
              color: muted,
            },
          },

          y: {
            beginAtZero: true,

            grid: {
              color:
                gridColor,
            },

            ticks: {
              color: muted,

              precision: 0,
            },
          },
        },
      },
    }
  )
}


async function loadChart() {
  loading.value = true
  errorMessage.value = ''

  try {
    movements.value =
      await getStockMovements()
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to load stock activity'
  } finally {
    loading.value = false
  }

  await nextTick()

  if (!errorMessage.value) {
    renderChart()
  }
}


onMounted(loadChart)


onBeforeUnmount(() => {
  chart?.destroy()
})
</script>


<template>
  <section class="trend-card">

    <div class="trend-header">

      <div>
        <h2>Inventory Activity</h2>

        <p>
          Stock movement during the
          last 7 days.
        </p>
      </div>

      <span class="trend-period">
        Last 7 days
      </span>

    </div>


    <div
      v-if="loading"
      class="trend-empty"
    >
      Loading activity...
    </div>


    <div
      v-else-if="errorMessage"
      class="trend-empty"
    >
      {{ errorMessage }}
    </div>


    <div
      v-else
      class="trend-canvas"
    >
      <canvas ref="canvas"></canvas>
    </div>

  </section>
</template>


<style
  scoped
  src="../styles/stock-movement-trend.css"
></style>