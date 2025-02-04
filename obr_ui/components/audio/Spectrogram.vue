<script lang="ts">
import { computed, defineComponent } from "vue";

import AudioVisualisation from "./AudioVisualisation.vue";

export default defineComponent({
  components: {
    AudioVisualisation,
  },
  props: {
    width: {
      type: Number,
      default: 0,
    },
    height: {
      type: Number,
      default: 0,
    },
    color: {
      type: String,
      default: "rgb(255 255 255 / 100%)",
    },
  },
  setup(props) {
    const containerStyle = computed(() => {
      return {};
    });
    const spectrogramStyle = computed(() => {
      return {
        height: `${props.height}px`,
        width: `${props.width}px`,
      };
    });
    return {
      containerStyle,
      spectrogramStyle,
    };
  },
});
</script>

<template>
  <div class="spectrogram-container" :style="containerStyle">
    <div class="spectrogram" :style="spectrogramStyle">
      <AudioVisualisation :width="width" :height="height + 60" :color="color" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.spectrogram-container {
  padding-top: 0;
  pointer-events: none;
}

.spectrogram {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
}
</style>
