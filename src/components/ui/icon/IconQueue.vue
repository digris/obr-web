<script lang="ts">
import { defineComponent, computed } from "vue";

const BASE_SIZE = 48;

export default defineComponent({
  props: {
    size: {
      type: Number,
      default: 24,
    },
    color: {
      type: String,
      default: "rgb(var(--c-page-fg))",
    },
  },
  setup(props) {
    const size = computed(() => {
      return props.size || BASE_SIZE;
    });
    const style = computed(() => {
      return {
        fill: props.color,
        stroke: "none",
        width: `${size.value}px`,
        height: `${size.value}px`,
      };
    });
    return {
      style,
    };
  },
});
</script>
<template>
  <!-- eslint-disable max-len -->
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" :style="style">
    <rect x="16" y="14.5" width="20" height="3" />
    <rect x="16" y="22.5" width="20" height="3" />
    <rect x="16" y="30.5" width="20" height="3" />

    <circle cx="12" cy="24" r="2" />
    <circle cx="12" cy="16" r="2" />
    <circle cx="12" cy="32" r="2" />
  </svg>
  <!-- eslint-enable max-len -->
</template>
