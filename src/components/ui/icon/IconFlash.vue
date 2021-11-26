<script lang="ts">
import { defineComponent, computed } from 'vue';

const BASE_SIZE = 48;

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
          strokeMiterlimit: 10,
          transform: `scale(${props.size / BASE_SIZE})`,
          strokeWidth: (3 * BASE_SIZE) / props.size,
        };
      }
      return {
        stroke: props.color,
        fill: props.color,
        strokeMiterlimit: 10,
        transform: `scale(${props.size / BASE_SIZE})`,
        strokeWidth: (3 * BASE_SIZE) / props.size,
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
    height="48px"
    width="48px"
    viewBox="0 0 48 48"
    :style="style"
  >
    <polygon
      points="35,21 24,21 24,13 13,26 24,26 24,35"
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
