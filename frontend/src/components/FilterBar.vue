<template>
  <div class="flex flex-wrap gap-4 mb-6 p-4 bg-white rounded-lg border border-gray-200">
    <!-- Period type -->
    <div class="flex flex-col gap-1">
      <label class="text-xs font-medium text-gray-500 uppercase tracking-wide">Period</label>
      <div class="flex gap-2">
        <button
          v-for="pt in ['month', 'quarter']"
          :key="pt"
          :class="[
            'px-3 py-1 rounded text-sm font-medium transition-colors',
            store.selectedPeriodType === pt
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200',
          ]"
          @click="store.selectedPeriodType = pt as 'month' | 'quarter'; store.fetchTrends()"
        >
          {{ pt === "month" ? "Monthly" : "Quarterly" }}
        </button>
      </div>
    </div>

    <!-- Region filter -->
    <div class="flex flex-col gap-1">
      <label class="text-xs font-medium text-gray-500 uppercase tracking-wide">County</label>
      <select
        :value="store.selectedRegion ?? ''"
        class="border border-gray-300 rounded px-3 py-1 text-sm"
        @change="store.selectRegion(($event.target as HTMLSelectElement).value || null)"
      >
        <option value="">All counties</option>
        <option v-for="r in store.regions" :key="r.county" :value="r.county">
          {{ r.county }}
        </option>
      </select>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { useHousingStore } from "../stores/housing";

const store = useHousingStore();
onMounted(() => { if (!store.regions.length) store.fetchRegions(); });
</script>
