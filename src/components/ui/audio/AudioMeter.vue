<script lang="ts">
import { computed, defineComponent, onMounted, ref, watch } from "vue";

import type { AudioAnalyser } from "@/player/analyser";

function maxVolume(data: Uint8Array) {
  const max = Math.max.apply(
    null,
    Array.from(data).map((x) => Math.abs((x - 128) / 128))
  );
  // return Math.sin((max * Math.PI) / 2);
  return max;
}

const drawCanvas = async (
  ctx: CanvasRenderingContext2D,
  width: number,
  height: number,
  offsetY: number,
  volL: number,
  volR: number
) => {
  ctx.canvas.width = width;
  ctx.canvas.height = height;

  // const center = {
  //   x: width / 2,
  //   y: height / 2 + offsetY / 2,
  // };

  // ctx.globalCompositeOperation = "darker";
  // ctx.globalCompositeOperation = "lighter";
  // ctx.fillStyle = "rgba(0, 0, 0, 1)";

  const space = width / 12;
  const w = width / 3;
  const yL = volL * height;
  const yR = volR * height;

  ctx.beginPath();
  ctx.rect(space, 0, w, yL);
  ctx.fill();

  ctx.beginPath();
  ctx.rect(width / 2 + space, 0, w, yR);
  ctx.fill();

  // ctx.beginPath();
  // ctx.rect(0, 0, width, height);
  // ctx.fillStyle = "rgba(0, 0, 0, 0.3)";
  // ctx.fill();

  // ctx.beginPath();
  // ctx.rect(812, yR, 10, vR);
  // ctx.fill();

  // ctx.beginPath();
  // ctx.rect(0, 0, 24, 24);
  // ctx.fill();

  ctx.closePath();
};

export default defineComponent({
  props: {
    width: {
      type: Number,
      default: 24,
    },
    height: {
      type: Number,
      default: 24,
    },
  },
  setup(props) {
    const canvas = ref<HTMLCanvasElement | null>(null);
    const size = computed(() => {
      return {
        height: props.height,
        width: props.width,
      };
    });
    const style = computed(() => {
      return {
        height: `${props.height}px`,
        width: `${props.width}px`,
        transform: "scaleY(-1)",
      };
    });
    const updateCanvas = async () => {
      const ctx = canvas.value?.getContext("2d");
      if (ctx) {
        // TODO: implement offset calculation
        // await drawCanvas(ctx, props.width, props.height, 92, rays.value);
      }
    };
    onMounted(() => {
      if (!canvas.value) {
        return;
      }
      const ctx = canvas.value?.getContext("2d");
      const fftL = new Uint8Array(2048);
      const fftR = new Uint8Array(2048);
      const freqL = new Uint8Array(2048);

      const getDrawData = (analyser: AudioAnalyser) => {
        let volL = 0;
        let volR = 0;
        const aL = analyser.left;
        const aR = analyser.right;
        if (aL && aR && ctx) {
          aL.getByteTimeDomainData(fftL);
          aR.getByteTimeDomainData(fftR);
          aL.getByteFrequencyData(freqL);
          volL = maxVolume(fftL);
          volR = maxVolume(fftR);
        }
        return {
          volL,
          volR,
        };
      };

      const drawLoop = () => {
        if (window.audioPlayer.analyser) {
          const { volL, volR } = getDrawData(window.audioPlayer.analyser);
          drawCanvas(ctx, props.width, props.height, 92, volL, volR);
        }
        requestAnimationFrame(drawLoop);
      };
      requestAnimationFrame(drawLoop);
    });
    watch(
      () => size.value,
      async () => {
        await updateCanvas();
      }
    );
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
