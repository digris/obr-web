<script lang="ts">
import {
  defineComponent,
  computed,
} from 'vue';

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
        stroke: 'none',
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
  <!-- eslint-disable max-len -->
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 48 48"
    :style="style"
  >
    <rect
      x="8"
      y="22.5"
      width="32"
      height="3"
    />
    <rect
      x="8"
      y="13.5"
      width="32"
      height="3"
    />
    <rect
      x="8"
      y="31.5"
      width="32"
      height="3"
    />
  </svg>
  <!-- eslint-enable max-len -->
</template>
