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
      default: "rgb(var(--c-page-bg))",
    },
    // marked: {
    //   type: Boolean,
    //   default: false,
    // },
  },
  setup(props) {
    const style = computed(() => {
      return {
        fill: "transparent",
        stroke: props.color,
        strokeWidth: (2.5 * BASE_SIZE) / props.size,
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
    viewBox="0 0 48 48"
    :style="style"
  >
    <polygon points="34.7,24 17.3,32.7 17.3,15.3 " />
    <!--
    <circle v-if="marked" cx="23" cy="24" r="0.5" />
    -->
  </svg>
</template>
