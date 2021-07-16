<script lang="ts">
import { defineComponent, computed } from 'vue';

const BASE_SIZE = 24;

export default defineComponent({
  props: {
    color: {
      type: String,
      default: 'rgb(var(--c-live-bg))',
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
    // const style = ref({
    //   fill: props.color,
    //   transform: `scale(${props.size / BASE_SIZE})`,
    // });
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
    <path
      d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
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
