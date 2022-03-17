<script lang="ts">
import { computed, defineComponent } from 'vue';

export default defineComponent({
  props: {
    seconds: {
      type: Number,
      default: 0,
      required: true,
      validator: (value: number) => {
        return (value >= 0 && value < 86400);
      },
    },
  },
  setup(props) {
    const durationDisplay = computed(() => {
      if (props.seconds < 60) {
        return `${Math.round(props.seconds)}s`;
      }
      const dateStr = new Date(props.seconds * 1000).toISOString();
      if (props.seconds < 60 * 60) {
        return dateStr.substr(14, 5);
      }
      return dateStr.substr(11, 8);
    });
    return {
      durationDisplay,
    };
  },
});

</script>
<template>
  <div
    class="duration"
    v-text="durationDisplay"
  />
</template>

<style lang="scss" scoped>
.duration {
  display: inline-flex;
  white-space: nowrap;
}
</style>
