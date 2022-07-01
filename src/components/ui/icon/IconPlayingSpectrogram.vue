<script lang="ts">
import { computed, defineComponent } from "vue";
import AudioSpectrum from "@/components/ui/audio/AudioSpectrum.vue";

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
  },
  components: {
    AudioSpectrum,
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
  <div :style="style" class="playing">
    <AudioSpectrum :width="24" :height="24" :color="color" />
  </div>
</template>
