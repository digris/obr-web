<script lang="ts">
import { defineComponent, ref, computed, watch, onMounted } from "vue";
import type { AudioAnalyser } from "@/player/analyser";

const drawCanvas = async (
  ctx: CanvasRenderingContext2D,
  width: number,
  height: number,
  bins: Uint8Array,
) => {
  ctx.canvas.width = width;
  ctx.canvas.height = height;
  // bar width: 6px for canvas of 48px
  const barWidth = width / 8;
  const heightFactor = 1 / (240 / height);
  const numBins = bins.length;
  const y = 0;
  const w = barWidth;
  for (let i = 0; i < numBins; i++) {
    const value = bins[i] * heightFactor;
    const x = i * (barWidth * 2) + (barWidth / 3);
    const h = value;
    ctx.fillStyle = "rgb(0,0,0)";
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
  },
  setup(props) {
    const canvas = ref<HTMLCanvasElement | null>(null);
    const style = computed(() => {
      return {
        height: `${props.height}px`,
        width: `${props.width}px`,
        transform: "scaleY(-1)",
        // background: 'rgba(0,0,0,0.2)',
      };
    });
    onMounted(() => {
      if (!canvas.value) {
        return;
      }
      const ctx = canvas.value?.getContext("2d");

      let max = 0;

      const getDrawData = (analyser: AudioAnalyser) => {
        // we just need one channel here
        const a = analyser.a64;
        const spectrumData = new Uint8Array(a.frequencyBinCount);
        if (a && ctx) {
          a.getByteFrequencyData(spectrumData);
        }
        // spectrum fft is 64 - so buffer length is 32
        // we discard the highest 1/2 of frequencise
        const avg = (arr) => arr.reduce( ( p, c ) => p + c, 0 ) / arr.length;
        const s = spectrumData.slice(0,16);
        const bins = [
          avg(s.slice(0,4)) * 0.8,
          avg(s.slice(4,8)),
          avg(s.slice(8,12)),
          avg(s.slice(12,16)) * 1.1,
        ];

        const newMax = Math.max(...bins);
        if (newMax > max) {
          console.debug('newMax', newMax);
          max = newMax;
        }

        // console.debug(spectrumData[18]);
        return bins;
      };

      const drawLoop = () => {
        if (window.audioPlayer.analyser && ctx) {
          const spectrumData = getDrawData(window.audioPlayer.analyser);
          drawCanvas(ctx, props.width, props.height, spectrumData);
        }
        requestAnimationFrame(drawLoop);
      };
      requestAnimationFrame(drawLoop);
    });
    return {
      canvas,
      style,
    };
  },
});
</script>

<template>
  <div class="level" :style="style">
    <canvas ref="canvas" />
  </div>
</template>
