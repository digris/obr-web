<script lang="ts">
import { computed, defineComponent } from "vue";
import AudioMeter from "@/components/ui/audio/AudioMeter.vue";

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
    pause: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    AudioMeter,
  },
  setup(props) {
    const style = computed(() => {
      return {
        "--color": props.color,
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
  <div
    :style="style"
    class="playing"
    :class="{
      pause: pause,
    }"
  >
    <AudioMeter />
  </div>
</template>
<style lang="scss" scoped>
.playing__ {
  display: grid;
  grid-column-gap: 2px;
  grid-template-columns: 4px 4px 4px;
  align-items: flex-end;
  width: 16px;
  height: 14px;
}
</style>
