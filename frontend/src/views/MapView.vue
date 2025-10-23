<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-800 mb-6">Price Heatmap</h1>
    <p class="text-sm text-gray-500 mb-4">Average price per sqm — click a county to filter.</p>
    <div v-if="store.loading" class="text-gray-500">Loading...</div>
    <div v-else-if="store.error" class="text-red-500">{{ store.error }}</div>
    <EChart v-else :option="mapOption" height="640px" @click="onMapClick" />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from "vue";
import type { EChartsOption } from "echarts";
import EChart from "../components/EChart.vue";
import { useHousingStore } from "../stores/housing";
import { useSwedenmMap } from "../composables/useSwedenmMap";

useSwedenmMap();
const store = useHousingStore();
onMounted(() => store.fetchRegions());

const values = computed(() => store.regions.map((r) => r.avg_price_per_sqm ?? 0).filter(Boolean));
const minVal = computed(() => Math.floor((Math.min(...values.value) - 5000) / 5000) * 5000);
const maxVal = computed(() => Math.ceil((Math.max(...values.value) + 5000) / 5000) * 5000);

const mapOption = computed<EChartsOption>(() => ({
  visualMap: {
    min: minVal.value || 20000,
    max: maxVal.value || 100000,
    text: ["High", "Low"],
    calculable: true,
    inRange: { color: ["#d4e6f1", "#1a5276"] },
    orient: "vertical",
    left: "right",
    top: "center",
  },
  tooltip: {
    trigger: "item",
    formatter: (params: { name: string; value: number }) => {
      const region = store.regions.find((r) => r.county === params.name);
      const sales = region ? ` (${region.total_sales.toLocaleString("sv-SE")} sales)` : "";
      return `<b>${params.name}</b>${sales}<br/>Avg SEK/sqm: ${params.value?.toLocaleString("sv-SE") ?? "N/A"}`;
    },
  },
  series: [
    {
      name: "Avg price / sqm",
      type: "map",
      map: "sweden",
      roam: true,
      emphasis: { label: { show: true } },
      data: store.regions.map((r) => ({
        name: r.county,
        value: r.avg_price_per_sqm ?? 0,
      })),
    },
  ],
}));

function onMapClick(params: { name: string }) {
  store.selectRegion(params.name);
}
</script>
