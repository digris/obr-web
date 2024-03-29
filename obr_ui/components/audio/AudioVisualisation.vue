<script lang="ts">
import { computed, defineComponent, onMounted, ref } from "vue";

import type { AudioAnalyser } from "@/player/analyser";

const drawCanvas = async (
  ctx: CanvasRenderingContext2D,
  width: number,
  height: number,
  color: string,
  bins: Uint8Array
) => {
  ctx.canvas.width = width;
  ctx.canvas.height = height;
  // bar width: 6px for canvas of 48px
  const barWidth = 6;
  const heightFactor = 1 / (240 / height);
  const numBins = bins.length;
  const y = 0;
  const w = barWidth;
  for (let i = 0; i < numBins; i++) {
    const value = bins[i] * heightFactor;
    const x = i * (barWidth * 1.5) + barWidth / 3;
    const h = value;
    // ctx.fillStyle = "rgb(255 255 255 / 100%)";
    ctx.fillStyle = color;
    ctx.fillRect(x, y, w, h);
  }
};

export default defineComponent({
  props: {
    width: {
      type: Number,
      default: 48,
    },
    height: {
      type: Number,
      default: 48,
    },
    color: {
      type: String,
      default: "rgb(0 0 0 / 100%)",
    },
  },
  setup(props) {
    const canvas = ref<HTMLCanvasElement | null>(null);
    const style = computed(() => {
      return {
        height: `${props.height}px`,
        width: `${props.width}px`,
        transform: "scaleY(-1)",
      };
    });
    const numBins = computed(() => {
      return Math.floor(props.width / 9); // 6px bar, 3px space;
    });
    onMounted(() => {
      if (!canvas.value) {
        return;
      }
      const player = window.hlsPlayer;
      if (!player) {
        return;
      }

      // const analyser = player.analyser;
      // if (!analyser) {
      //   return;
      // }

      const ctx = canvas.value?.getContext("2d");

      const getDrawData = (analyser: AudioAnalyser) => {
        if (!analyser) {
          return new Uint8Array(300);
        }
        // we just need one channel here
        const a = analyser.a1024;
        const spectrumData = new Uint8Array(300);
        if (a && ctx) {
          a.getByteFrequencyData(spectrumData);
        }
        return spectrumData.slice(0, numBins.value);
      };

      const drawLoop = () => {
        if (player.analyser && ctx) {
          const drawData = getDrawData(player.analyser);
          drawCanvas(ctx, props.width, props.height, props.color, drawData);
        }
        requestAnimationFrame(drawLoop);
      };
      requestAnimationFrame(drawLoop);
    });
    return {
      canvas,
      style,
      numBins,
    };
  },
});
</script>

<template>
  <div class="spectrum" :style="style">
    <canvas ref="canvas" />
  </div>
</template>
