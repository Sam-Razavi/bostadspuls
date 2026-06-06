<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-800 mb-6">Regional Comparison</h1>
    <LoadingSpinner v-if="store.loading" />
    <ErrorAlert v-else-if="store.error" :message="store.error" :on-retry="store.fetchRegions" />
    <EChart v-else :option="chartOption" height="520px" />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from "vue";
import type { EChartsOption } from "echarts";
import EChart from "../components/EChart.vue";
import ErrorAlert from "../components/ErrorAlert.vue";
import LoadingSpinner from "../components/LoadingSpinner.vue";
import { useHousingStore } from "../stores/housing";

const store = useHousingStore();
onMounted(() => store.fetchRegions());

const chartOption = computed<EChartsOption>(() => ({
  tooltip: { trigger: "axis", axisPointer: { type: "shadow" } },
  grid: { left: "20%" },
  xAxis: {
    type: "value",
    name: "SEK / sqm",
    axisLabel: { formatter: (v: number) => `${(v / 1000).toFixed(0)}k` },
  },
  yAxis: {
    type: "category",
    data: store.regions.map((r) => r.county).reverse(),
  },
  series: [
    {
      name: "Avg price / sqm",
      type: "bar",
      data: store.regions.map((r) => r.avg_price_per_sqm).reverse(),
    },
  ],
}));
</script>
