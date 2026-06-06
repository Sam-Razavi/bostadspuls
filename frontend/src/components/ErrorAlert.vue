<template>
  <div class="flex items-start gap-3 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
    <span class="text-lg">!</span>
    <div>
      <p class="font-medium text-sm">Something went wrong</p>
      <p class="text-sm mt-1">{{ message }}</p>
      <button
        v-if="onRetry"
        class="mt-2 text-sm underline hover:no-underline"
        @click="onRetry"
      >
        Try again
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  message: string;
  onRetry?: () => void;
}>();
</script>
