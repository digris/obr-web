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
      default: 'rgb(var(--c-live-fg))',
    },
  },
  setup(props) {
    const style = computed(() => {
      return {
        fill: props.color,
        stroke: props.color,
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
    <line
      x1="12"
      y1="7.5"
      x2="12"
      y2="12"
    />
    <line
      x1="15.5"
      y1="12"
      x2="11.5"
      y2="12"
    />
    <path
      d="M12,18 C8.7,18 6,15.3 6,12 C6,8.7 8.7,6 12,6 C15.3,6 18,8.7 18,12"
      fill="none"
    />
    <polyline
      fill-rule="nonzero"
      points="11.45 15.9 13.55 18 11.45 20.1"
    />
  </svg>
</template>
