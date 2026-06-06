<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-800 mb-6">Price per sqm Distribution</h1>
    <LoadingSpinner v-if="store.loading" />
    <ErrorAlert v-else-if="store.error" :message="store.error" :on-retry="store.fetchRegions" />
    <EChart v-else :option="chartOption" height="440px" />
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

const chartOption = computed<EChartsOption>(() => {
  const bucketSize = 5000;
  const buckets: Record<number, number> = {};

  for (const r of store.regions) {
    if (r.avg_price_per_sqm == null) continue;
    const bucket = Math.floor(r.avg_price_per_sqm / bucketSize) * bucketSize;
    buckets[bucket] = (buckets[bucket] ?? 0) + 1;
  }

  const sorted = Object.entries(buckets)
    .map(([k, v]) => ({ label: `${(+k / 1000).toFixed(0)}k`, count: v }))
    .sort((a, b) => parseFloat(a.label) - parseFloat(b.label));

  return {
    tooltip: { trigger: "axis" },
    xAxis: { type: "category", data: sorted.map((b) => b.label), name: "SEK/sqm" },
    yAxis: { type: "value", name: "Counties" },
    series: [{ type: "bar", data: sorted.map((b) => b.count) }],
  };
});
</script>
