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
    rotate: {
      type: Number,
      default: 0,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
});
</script>

<template>
  <Circle :disabled="disabled">
    <IconSkip :rotate="rotate" />
  </Circle>
</template>
