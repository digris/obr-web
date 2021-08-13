<script lang="ts">
import { defineComponent, computed } from 'vue';

const BASE_SIZE = 24;

export default defineComponent({
  props: {
    color: {
      type: String,
      default: 'rgb(var(--c-page-bg))',
    },
    size: {
      type: Number,
      default: 24,
    },
    outlined: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const style = computed(() => {
      if (props.outlined) {
        return {
          stroke: props.color,
          fill: 'transparent',
          transform: `scale(${props.size / BASE_SIZE})`,
          strokeWidth: (2 * BASE_SIZE) / props.size,
        };
      }
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
  <!-- eslint-disable max-len -->
  <svg
    xmlns="http://www.w3.org/2000/svg"
    height="24px"
    width="24px"
    viewBox="0 0 24 24"
    :style="style"
  >
    <polyline
      points="13.45,6 7.6,12 16.4,12 10.55,18"
    />
  </svg>
  <!-- eslint-enable max-len -->
</template>

<style lang="scss" scoped>
svg {
  path {
    shape-rendering: geometricprecision;
  }
}
</style>
