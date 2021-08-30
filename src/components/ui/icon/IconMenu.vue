<script lang="ts">
import { defineComponent, computed } from 'vue';

const BASE_SIZE = 24;

export default defineComponent({
  props: {
    size: {
      type: Number,
      default: 24,
    },
    color: {
      type: String,
      default: 'rgb(var(--c-page-fg))',
    },
  },
  setup(props) {
    const style = computed(() => {
      return {
        fill: props.color,
        transform: `scale(${props.size / BASE_SIZE})`,
      };
    });
    return {
      style,
    };
  },
});
</script>
<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    height="24px"
    width="24px"
    viewBox="0 0 24 24"
    :style="style"
  >
    <rect
      x="4"
      y="6"
      width="16"
      height="1.5"
    />
    <rect
      x="4"
      y="11"
      width="16"
      height="1.5"
    />
    <rect
      x="4"
      y="16"
      width="16"
      height="1.5"
    />
  </svg>
</template>
