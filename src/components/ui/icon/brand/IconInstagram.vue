<script lang="ts">
import { computed, defineComponent } from "vue";

const BASE_SIZE = 48;

export default defineComponent({
  props: {
    size: {
      type: Number,
      default: 24,
    },
    color: {
      type: String,
      default: "rgb(var(--c-page-fg))",
    },
  },
  setup(props) {
    const style = computed(() => {
      return {
        fill: props.color,
        stroke: "none",
        strokeWidth: (2 * BASE_SIZE) / props.size,
        strokeMiterlimit: 10,
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
    viewBox="0 0 60 60"
    :style="style"
  >
    <path
      d="M30.1,25.2c-2.6-0.1-4.8,2-4.9,4.6s2,4.8,4.6,4.9c2.6,0.1,4.8-2,4.9-4.6C34.8,27.5,32.7,25.3,30.1,25.2z"
    />
    <path
      d="M38.4,15H21.6C18,15,15,18,15,21.6v16.8c0,3.6,3,6.6,6.6,6.6h16.8c3.6,0,6.6-3,6.6-6.6V21.6
	C45,18,42,15,38.4,15z M29.8,37.7c-4.3-0.1-7.6-3.7-7.5-8c0.1-4.3,3.7-7.6,8-7.5c4.3,0.1,7.6,3.7,7.5,8
	C37.6,34.5,34.1,37.9,29.8,37.7z M38.8,23.1c-1,0-1.9-0.8-1.9-1.9c0-1,0.8-1.9,1.9-1.9s1.9,0.8,1.9,1.9c0,0,0,0,0,0
	C40.7,22.3,39.8,23.1,38.8,23.1C38.8,23.1,38.8,23.1,38.8,23.1L38.8,23.1z"
    />
  </svg>
</template>
