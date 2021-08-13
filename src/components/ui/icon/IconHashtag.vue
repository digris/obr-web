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
      default: 'rgb(var(--c-page-bg))',
    },
  },
  setup(props) {
    const style = computed(() => {
      return {
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
      x1="7.5"
      y1="10.5"
      x2="16.5"
      y2="10.5"
    />
    <line
      x1="7.5"
      y1="13.5"
      x2="16.5"
      y2="13.5"
    />
    <line
      x1="10.5"
      y1="16.5"
      x2="10.5"
      y2="7.5"
    />
    <line
      x1="13.5"
      y1="16.5"
      x2="13.5"
      y2="7.5"
    />
  </svg>
</template>
