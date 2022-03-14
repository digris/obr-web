<script lang="ts">
import { defineComponent, computed } from 'vue';

const BASE_SIZE = 48;

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
        fill: 'none',
        stroke: props.color,
        strokeWidth: (2 * BASE_SIZE) / props.size,
        strokeMiterlimit: 10,
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
    height="48px"
    width="48px"
    viewBox="0 0 48 48"
    :style="style"
  >
    <polyline
      points="34,19.1 20.2,33 14,34 15.1,27.8 28.9,14 "
    />
    <path
      d="M25.3,16.6"
    />
    <line
      x1="28.9"
      y1="14"
      x2="34"
      y2="19.1"
    />
    <line
      x1="24.8"
      y1="18.1"
      x2="29.9"
      y2="23.2"
    />
  </svg>
</template>
