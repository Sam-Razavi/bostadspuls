<template>
  <div ref="chartEl" :style="{ width: width, height: height }" />
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from "vue";
import * as echarts from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import type { EChartsOption } from "echarts";

echarts.use([CanvasRenderer]);

const props = withDefaults(
  defineProps<{
    option: EChartsOption;
    width?: string;
    height?: string;
  }>(),
  { width: "100%", height: "400px" }
);

const chartEl = ref<HTMLDivElement | null>(null);
let chart: echarts.ECharts | null = null;

onMounted(() => {
  if (chartEl.value) {
    chart = echarts.init(chartEl.value);
    chart.setOption(props.option);
    window.addEventListener("resize", () => chart?.resize());
  }
});

watch(
  () => props.option,
  (newOpt) => chart?.setOption(newOpt, { notMerge: true }),
  { deep: true }
);

onBeforeUnmount(() => {
  chart?.dispose();
  window.removeEventListener("resize", () => chart?.resize());
});
</script>
