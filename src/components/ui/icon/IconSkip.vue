<script lang="ts">
import { computed, defineComponent } from 'vue';

const BASE_SIZE = 24;

export default defineComponent({
  props: {
    size: {
      type: Number,
      default: 24,
    },
    color: {
      type: String,
      default: 'rgb(var(--c-live-bg))',
    },
    rotate: {
      type: Number,
      default: 0,
    },
  },
  setup(props) {
    const style = computed(() => {
      return {
        fill: props.color,
        transform: `scale(${props.size / BASE_SIZE}) rotate(${props.rotate}deg)`,
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
    <path
      d="M15 18h2V6h-2M6 18l8.5-6L6 6v12z"
    />
  </svg>
</template>
