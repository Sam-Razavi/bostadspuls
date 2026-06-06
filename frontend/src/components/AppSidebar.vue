<template>
  <nav class="w-52 min-h-screen bg-white border-r border-gray-200 pt-4">
    <ul class="space-y-1 px-3">
      <li v-for="item in navItems" :key="item.to">
        <RouterLink
          :to="item.to"
          class="flex items-center gap-2 px-3 py-2 rounded-lg text-gray-700 hover:bg-blue-50 hover:text-blue-700 transition-colors"
          active-class="bg-blue-50 text-blue-700 font-medium"
        >
          {{ item.label }}
        </RouterLink>
      </li>
    </ul>
  </nav>
</template>

<script setup lang="ts">
const navItems = [
  { to: "/", label: "Dashboard" },
  { to: "/trends", label: "Price Trends" },
  { to: "/regions", label: "Regions" },
  { to: "/map", label: "Map" },
  { to: "/distribution", label: "Distribution" },
  { to: "/by-type", label: "By Type" },
  { to: "/compare", label: "Compare" },
  { to: "/explore", label: "Explore" },
];
</script>
