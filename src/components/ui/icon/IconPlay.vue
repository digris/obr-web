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
    <path
      d="M0 0h24v24H0z"
      fill="none"
    />
    <path
      d="M8 5v14l11-7z"
    />
  </svg>
</template>
