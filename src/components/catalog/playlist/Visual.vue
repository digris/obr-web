<script lang="ts">
import { defineComponent, computed } from "vue";
import AudioSpectrum from "@/components/ui/audio/AudioSpectrumB.vue";

export default defineComponent({
  components: {
    AudioSpectrum,
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
  },
  setup(props) {
    const containerStyle = computed(() => {
      return {};
    });
    const visualStyle = computed(() => {
      return {
        height: `${props.height}px`,
        width: `${props.width}px`,
      };
    });
    return {
      containerStyle,
      visualStyle,
    };
  },
});
</script>

<template>
  <div class="visual-container" :style="containerStyle">
    <div class="visual" :style="visualStyle">
      <AudioSpectrum
        :width="width"
        :height="256"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.visual {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
}
</style>
