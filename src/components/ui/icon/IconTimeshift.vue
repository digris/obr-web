<script lang="ts">
import { computed, defineComponent } from "vue";

import { useIconSize } from "@/composables/icon";

export default defineComponent({
  props: {
    scale: {
      type: Number,
      default: 1,
    },
    colorVar: {
      type: String,
      default: "--c-fg",
    },
  },
  setup(props) {
    const { iconSize: size } = useIconSize(props.scale);
    const color = computed(() => `rgb(var(${props.colorVar}))`);
    const style = computed(() => {
      return {
        stroke: "none",
        fill: color.value,
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
  <svg xmlns="http://www.w3.org/2000/svg" x="10" y="0" viewBox="0 0 48 48" :style="style">
    <path d="M22.5,13.6v8.9v3v0h8v-3h-5v-8.9c-0.5-0.1-1-0.1-1.5-0.1S23,13.5,22.5,13.6z" />
    <path
      d="M10.5,24c0,7.4,6.1,13.5,13.5,13.5c0.5,0,1,0,1.5-0.1v-3c-0.5,0.1-1,0.1-1.5,0.1c-5.8,0-10.5-4.7-10.5-10.5c0-5.3,3.9-9.6,9-10.4v-3C15.8,11.3,10.5,17.1,10.5,24z"
    />
    <path
      d="M25.5,10.6v3c5.1,0.7,9,5.1,9,10.4c0,0.5,0,1-0.1,1.5h3c0.1-0.5,0.1-1,0.1-1.5C37.5,17.1,32.2,11.3,25.5,10.6z"
    />
    <polygon points="22.5,41 22.5,31 27.5,36 " />
  </svg>
  <!-- eslint-enable max-len -->
</template>
