<script lang="ts">
import { defineComponent } from 'vue';
import IconSkip from '@/components/ui/icon/IconSkip.vue';
import Circle from './Circle.vue';

export default defineComponent({
  components: {
    Circle,
    IconSkip,
  },
  props: {
    size: {
      type: Number,
      default: 48,
    },
    color: {
      type: String,
      default: 'rgb(var(--c-fg))',
    },
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
  <Circle
    :size="size"
    :disabled="disabled"
  >
    <IconSkip
      :size="size"
      :rotate="rotate"
      :color="color"
    />
  </Circle>
</template>
