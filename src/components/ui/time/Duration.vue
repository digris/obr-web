<script lang="ts">
import { computed, defineComponent } from "vue";

export default defineComponent({
  props: {
    seconds: {
      type: Number,
      default: 0,
      required: true,
      validator: (value: number) => {
        return value >= 0 && value < 86400;
      },
    },
    roundSeconds: {
      type: Number,
      default: null,
    },
  },
  setup(props) {
    const roundedSeconds = computed(() => {
      if (props.roundSeconds && props.roundSeconds < props.seconds) {
        return Math.round(props.seconds / props.roundSeconds) * props.roundSeconds;
      }
      return props.seconds;
    });
    const durationDisplay = computed(() => {
      if (roundedSeconds.value < 60) {
        return `${Math.round(roundedSeconds.value)}s`;
      }
      const dateStr = new Date(roundedSeconds.value * 1000).toISOString();
      if (roundedSeconds.value < 60 * 60) {
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
  <div class="duration" v-text="durationDisplay" />
</template>

<style lang="scss" scoped>
.duration {
  display: inline-flex;
  white-space: nowrap;
}
</style>
