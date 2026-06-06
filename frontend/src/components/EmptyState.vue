<template>
  <div class="flex flex-col items-center justify-center py-16 text-gray-400">
    <p class="text-4xl mb-4">📊</p>
    <p class="text-sm font-medium">{{ title }}</p>
    <p v-if="description" class="text-xs mt-1">{{ description }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string;
  description?: string;
}>();
</script>
