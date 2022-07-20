<script lang="ts">
import { defineComponent } from "vue";

import CircleButton from "@/components/ui/button/CircleButton.vue";
import IconPaginate from "@/components/ui/icon/IconPaginate.vue";

export default defineComponent({
  components: {
    CircleButton,
    IconPaginate,
  },
  props: {
    disabled: {
      type: Boolean,
      default: false,
    },
    rotate: {
      type: Number,
      default: 0,
    },
  },
  setup() {
    return {};
  },
});
</script>

<template>
  <CircleButton :scale="2.5" :disabled="disabled">
    <IconPaginate :size="120" :rotate="rotate" color="rgb(var(--c-page-fg))" />
  </CircleButton>
</template>
