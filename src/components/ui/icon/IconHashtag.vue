<script lang="ts">
import { computed, defineComponent } from 'vue';

const BASE_SIZE = 48;

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
        strokeWidth: 3,
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
    height="48px"
    width="48px"
    viewBox="0 0 48 48"
    :style="style"
  >
    <line
      x1="15"
      y1="21"
      x2="33"
      y2="21"
    />
    <line
      x1="15"
      y1="27"
      x2="33"
      y2="27"
    />
    <line
      x1="21"
      y1="33"
      x2="21"
      y2="15"
    />
    <line
      x1="27"
      y1="33"
      x2="27"
      y2="15"
    />
  </svg>
</template>
