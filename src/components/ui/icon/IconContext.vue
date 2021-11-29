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
    const size = computed(() => {
      return props.size || BASE_SIZE;
    });
    const style = computed(() => {
      return {
        fill: props.color,
        // transform: `scale(${props.size / BASE_SIZE})`,
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
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 48 48"
    :style="style"
  >
    <circle
      cx="24"
      cy="17"
      r="2"
    />
    <circle
      cx="24"
      cy="24"
      r="2"
    />
    <circle
      cx="24"
      cy="31"
      r="2"
    />
  </svg>
</template>
