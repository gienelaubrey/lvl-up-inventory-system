<script setup lang="ts">
import {
  computed,
} from 'vue'

import {
  FileText,
  Truck,
} from 'lucide-vue-next'

import {
  useRoute,
  useRouter,
} from 'vue-router'

import SupplierView
  from './SupplierView.vue'

import ReportsView
  from './ReportsView.vue'

const route = useRoute()
const router = useRouter()

const activeTab = computed(
  () =>
    route.query.tab === 'reports'
      ? 'reports'
      : 'suppliers'
)

function setTab(
  tab: 'suppliers' | 'reports'
) {
  router.replace({
    path: '/suppliers-reports',
    query: {
      tab:
        tab === 'reports'
          ? 'reports'
          : undefined,
    },
  })
}
</script>

<template>
  <div class="supplier-report-hub">
    <div class="hub-switch">
      <button
        type="button"
        :class="{ active: activeTab === 'suppliers' }"
        @click="setTab('suppliers')"
      >
        <Truck :size="16" />
        Suppliers
      </button>

      <button
        type="button"
        :class="{ active: activeTab === 'reports' }"
        @click="setTab('reports')"
      >
        <FileText :size="16" />
        Supplier Reports
      </button>
    </div>

    <SupplierView
      v-if="activeTab === 'suppliers'"
    />

    <ReportsView
      v-else
    />
  </div>
</template>

<style scoped src="../styles/supplier-report-hub.css"></style>
