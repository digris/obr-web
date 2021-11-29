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
        stroke: props.color,
        strokeWidth: (3 * BASE_SIZE) / props.size,
        strokeMiterlimit: 10,
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
    <line
      x1="15"
      y1="15"
      x2="33"
      y2="33"
    />
    <line
      x1="15"
      y1="33"
      x2="33"
      y2="15"
    />
  </svg>
</template>
