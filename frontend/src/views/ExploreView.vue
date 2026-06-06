<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-800 mb-4">Explore</h1>
    <p class="text-sm text-gray-500 mb-6">
      Interactive Metabase dashboard. Requires Metabase running on
      <code>VITE_METABASE_URL</code>.
    </p>

    <div v-if="iframeUrl" class="rounded-lg overflow-hidden border border-gray-200 shadow-sm">
      <iframe
        :src="iframeUrl"
        frameborder="0"
        width="100%"
        height="720"
        allowtransparency
      />
    </div>
    <div v-else class="p-6 bg-yellow-50 border border-yellow-200 rounded-lg text-yellow-800 text-sm">
      Metabase is not configured. Set <code>VITE_METABASE_URL</code> and
      <code>VITE_METABASE_DASHBOARD_ID</code> environment variables.
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";

const metabaseUrl = import.meta.env.VITE_METABASE_URL ?? "";
const dashboardId = import.meta.env.VITE_METABASE_DASHBOARD_ID ?? "";

const iframeUrl = computed<string | null>(() => {
  if (!metabaseUrl || !dashboardId) return null;
  return `${metabaseUrl}/embed/dashboard/${dashboardId}#bordered=true&titled=true`;
});
</script>
