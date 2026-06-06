<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-800 mb-2">Year-over-Year Comparison</h1>
    <p class="text-sm text-gray-500 mb-4">
      Price change vs. the same period one year ago, by county (%).
    </p>

    <div class="flex gap-4 mb-4 items-center flex-wrap">
      <div>
        <label class="text-sm text-gray-600 mr-2">Period:</label>
        <select
          v-model="store.selectedPeriodType"
          class="text-sm border border-gray-300 rounded px-2 py-1"
          @change="reload"
        >
          <option value="month">Monthly</option>
          <option value="quarter">Quarterly</option>
        </select>
      </div>
      <div>
        <label class="text-sm text-gray-600 mr-2">County:</label>
        <select
          v-model="selectedCounty"
          class="text-sm border border-gray-300 rounded px-2 py-1"
          @change="reload"
        >
          <option value="">All counties</option>
          <option v-for="county in counties" :key="county" :value="county">{{ county }}</option>
        </select>
      </div>
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

onMounted(() => store.fetchCompare());

const counties = computed(() => {
  const set = new Set(store.yoyData.map((r) => r.county));
  return Array.from(set).sort();
});

function reload() {
  store.fetchCompare(selectedCounty.value || undefined);
}

const chartOption = computed<EChartsOption>(() => {
  const countyList = selectedCounty.value
    ? [selectedCounty.value]
    : Array.from(new Set(store.yoyData.map((r) => r.county))).sort().slice(0, 8);

  const periods = Array.from(new Set(store.yoyData.map((r) => r.period_start)))
    .sort()
    .slice(-24);

  const series = countyList.map((county) => ({
    name: county,
    type: "line" as const,
    smooth: true,
    data: periods.map((period) => {
      const row = store.yoyData.find(
        (r) => r.county === county && r.period_start === period
      );
      return row?.yoy_pct_change ?? null;
    }),
  }));

  return {
    tooltip: {
      trigger: "axis",
      valueFormatter: (v: number | null) =>
        v !== null ? `${v.toFixed(1)}%` : "N/A",
    },
    legend: { top: 0, type: "scroll" },
    grid: { left: "5%", right: "5%", bottom: "10%", containLabel: true },
    xAxis: {
      type: "category",
      data: periods,
      axisLabel: { rotate: 45, fontSize: 10 },
    },
    yAxis: {
      type: "value",
      name: "YoY %",
      axisLabel: { formatter: (v: number) => `${v}%` },
      markLine: {
        data: [{ yAxis: 0, lineStyle: { color: "#999", type: "dashed" } }],
      },
    },
    series,
  };
});
</script>
