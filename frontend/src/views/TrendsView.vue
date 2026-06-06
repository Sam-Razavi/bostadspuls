<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-800 mb-6">Price Trends</h1>
    <div v-if="store.loading" class="text-gray-500">Loading...</div>
    <div v-else-if="store.error" class="text-red-500">{{ store.error }}</div>
    <EChart v-else :option="chartOption" height="440px" />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from "vue";
import type { EChartsOption } from "echarts";
import EChart from "../components/EChart.vue";
import { useHousingStore } from "../stores/housing";

const store = useHousingStore();

onMounted(() => store.fetchTrends());

const chartOption = computed<EChartsOption>(() => {
  const byCounty = new Map<string, { dates: string[]; prices: (number | null)[] }>();

  for (const pt of store.trends) {
    if (!byCounty.has(pt.county)) byCounty.set(pt.county, { dates: [], prices: [] });
    const entry = byCounty.get(pt.county)!;
    entry.dates.push(pt.period_start);
    entry.prices.push(pt.avg_price_per_sqm);
  }

  const firstCounty = byCounty.values().next().value;

  return {
    tooltip: { trigger: "axis" },
    legend: { top: "bottom" },
    xAxis: {
      type: "category",
      data: firstCounty?.dates ?? [],
    },
    yAxis: {
      type: "value",
      name: "SEK / sqm",
      axisLabel: { formatter: (v: number) => `${(v / 1000).toFixed(0)}k` },
    },
    series: [...byCounty.entries()].map(([county, { prices }]) => ({
      name: county,
      type: "line",
      data: prices,
      smooth: true,
    })),
  };
});
</script>
