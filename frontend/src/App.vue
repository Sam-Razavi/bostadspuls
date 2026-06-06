<template>
  <div class="min-h-screen bg-gray-50">
    <AppHeader />
    <div class="flex">
      <AppSidebar />
      <main class="flex-1 p-6">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import AppHeader from "./components/AppHeader.vue";
import AppSidebar from "./components/AppSidebar.vue";
</script>
