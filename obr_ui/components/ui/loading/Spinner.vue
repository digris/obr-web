<script lang="ts" setup>
import IconBuffering from "@/components/ui/icon/IconBuffering.vue";

withDefaults(
  defineProps<{
    scale?: number;
    colorVar?: string;
  }>(),
  {
    scale: 1,
    colorVar: "--c-fg",
  }
);
</script>

<template>
  <div>
    <IconBuffering :scale="scale" :color-var="colorVar" />
  </div>
</template>
