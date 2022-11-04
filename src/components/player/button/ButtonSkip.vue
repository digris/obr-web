<script lang="ts">
import { defineComponent } from "vue";
import IconSkip from "@/components/ui/icon/IconSkip.vue";
import Circle from "./Circle.vue";

export default defineComponent({
  components: {
    Circle,
    IconSkip,
  },
  props: {
    scale: {
      type: Number,
      default: 1,
    },
    rotate: {
      type: Number,
      default: 0,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    outlined: {
      type: Boolean,
      default: false,
    },
  },
});
</script>

<template>
  <Circle :disabled="disabled" :scale="scale" :outlined="outlined">
    <IconSkip :rotate="rotate" :scale="scale" />
  </Circle>
</template>
