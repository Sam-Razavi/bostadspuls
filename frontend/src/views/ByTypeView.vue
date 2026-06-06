<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-800 mb-2">By Property Type</h1>
    <p class="text-sm text-gray-500 mb-4">Average price per sqm broken down by property type per county.</p>

    <div class="mb-4">
      <label class="text-sm text-gray-600 mr-2">Filter by county:</label>
      <select
        v-model="selectedCounty"
        class="text-sm border border-gray-300 rounded px-2 py-1"
        @change="onCountyChange"
      >
        <option value="">All counties</option>
        <option v-for="county in counties" :key="county" :value="county">{{ county }}</option>
      </select>
    </div>

    <div v-if="store.loading" class="text-gray-500">Loading...</div>
    <div v-else-if="store.error" class="text-red-500">{{ store.error }}</div>
    <EChart v-else :option="chartOption" height="520px" />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import type { EChartsOption } from "echarts";
import EChart from "../components/EChart.vue";
import { useHousingStore } from "../stores/housing";

const store = useHousingStore();
const selectedCounty = ref("");

onMounted(() => store.fetchPropertyTypes());

const counties = computed(() => {
  const set = new Set(store.propertyTypes.map((r) => r.county));
  return Array.from(set).sort();
});

function onCountyChange() {
  store.fetchPropertyTypes(selectedCounty.value || undefined);
}

const chartOption = computed<EChartsOption>(() => {
  const types = Array.from(new Set(store.propertyTypes.map((r) => r.object_type_en))).sort();
  const countyList = Array.from(new Set(store.propertyTypes.map((r) => r.county))).sort();

  const series = types.map((typeEn) => ({
    name: typeEn,
    type: "bar" as const,
    data: countyList.map((county) => {
      const row = store.propertyTypes.find(
        (r) => r.county === county && r.object_type_en === typeEn
      );
      return row?.avg_price_per_sqm ?? 0;
    }),
  }));

  return {
    tooltip: {
      trigger: "axis",
      axisPointer: { type: "shadow" },
      valueFormatter: (v: number) => `${v.toLocaleString("sv-SE")} SEK/sqm`,
    },
    legend: { top: 0 },
    grid: { left: "20%", right: "5%", bottom: "5%", containLabel: false },
    xAxis: {
      type: "value",
      name: "SEK / sqm",
      axisLabel: { formatter: (v: number) => `${(v / 1000).toFixed(0)}k` },
    },
    yAxis: {
      type: "category",
      data: countyList,
      axisLabel: { fontSize: 11 },
    },
    series,
  };
});
</script>
