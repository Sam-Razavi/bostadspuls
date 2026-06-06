import { defineStore } from "pinia";
import { ref } from "vue";
import { api, type RegionSummary, type TrendPoint } from "../api/client";

export const useHousingStore = defineStore("housing", () => {
  const trends = ref<TrendPoint[]>([]);
  const regions = ref<RegionSummary[]>([]);
  const selectedRegion = ref<string | null>(null);
  const selectedPeriodType = ref<"month" | "quarter">("month");
  const loading = ref(false);
  const error = ref<string | null>(null);

  async function fetchTrends() {
    loading.value = true;
    error.value = null;
    try {
      trends.value = await api.trends({
        period_type: selectedPeriodType.value,
        county: selectedRegion.value ?? undefined,
        limit: "120",
      });
    } catch (e) {
      error.value = (e as Error).message;
    } finally {
      loading.value = false;
    }
  }

  async function fetchRegions() {
    loading.value = true;
    error.value = null;
    try {
      regions.value = await api.regions();
    } catch (e) {
      error.value = (e as Error).message;
    } finally {
      loading.value = false;
    }
  }

  function selectRegion(county: string | null) {
    selectedRegion.value = county;
    fetchTrends();
  }

  return {
    trends,
    regions,
    selectedRegion,
    selectedPeriodType,
    loading,
    error,
    fetchTrends,
    fetchRegions,
    selectRegion,
  };
});
