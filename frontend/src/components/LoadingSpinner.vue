<template>
  <div class="flex items-center justify-center py-12">
    <div class="animate-spin rounded-full h-10 w-10 border-4 border-blue-600 border-t-transparent" />
    <span class="ml-3 text-gray-500 text-sm">{{ label }}</span>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{ label?: string }>(), { label: "Loading…" });
</script>
