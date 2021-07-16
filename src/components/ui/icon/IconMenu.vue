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
          x="6"
          y="7.5"
          width="12"
          height="1"
        />
        <rect
          x="6"
          y="11.5"
          width="12"
          height="1"
        />
        <rect
          x="6"
          y="15.5"
          width="12"
          height="1"
        />
  </svg>
</template>
