<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-800 mb-2">Dashboard</h1>
    <p class="text-gray-500 mb-8">Overview of the Swedish housing market.</p>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <RouterLink
        v-for="card in cards"
        :key="card.to"
        :to="card.to"
        class="block p-5 bg-white rounded-lg border border-gray-200 shadow-sm hover:border-blue-400 hover:shadow transition-all"
      >
        <p class="text-lg font-semibold text-gray-800">{{ card.title }}</p>
        <p class="text-sm text-gray-500 mt-1">{{ card.description }}</p>
      </RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
const cards = [
  { to: "/trends",      title: "Price Trends",     description: "Monthly and quarterly price-per-sqm over time by county." },
  { to: "/regions",     title: "Regions",           description: "Cross-county ranking by average price per sqm." },
  { to: "/map",         title: "Map",               description: "Interactive choropleth heatmap of Sweden." },
  { to: "/distribution",title: "Distribution",      description: "Price-per-sqm histogram across counties." },
  { to: "/by-type",    title: "By Type",           description: "Avg price per sqm broken down by property type (villa, lägenhet, etc.)." },
  { to: "/compare",    title: "Compare",           description: "Year-over-year price change by county and period." },
  { to: "/explore",    title: "Explore",           description: "Metabase dashboard with interactive saved questions." },
];
</script>
