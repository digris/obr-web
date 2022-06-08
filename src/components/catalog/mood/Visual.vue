<script lang="ts">
import type { PropType } from "vue";
import { defineComponent, ref, computed, onMounted, watch } from "vue";

interface Colors {
  inner: Array<[number, number, number, number]>;
  outer: Array<[number, number, number, number]>;
}

interface RayConfig {
  count: number;
  spread: number;
  width: number;
  length: number;
  colors: Colors;
}

interface Ray {
  start: number;
  width: number;
  length: number;
  colors: Colors;
  blend: string;
  blur: number;
}

const colorToRGBA = (color: Array<[number, number, number, number]>) => {
  return `rgba(${color.join(",")})`;
};

const drawCanvas = async (
  ctx: CanvasRenderingContext2D,
  width: number,
  height: number,
  offsetY: number,
  rays: Array<Ray>
) => {
  ctx.canvas.width = width;
  ctx.canvas.height = height;
  console.debug("CTX", ctx.canvas.width, ctx.canvas.height, offsetY, rays);

  const center = {
    x: width / 2,
    y: height / 2 + offsetY / 2,
  };

  rays.forEach((ray: Ray) => {
    const { length, colors, start, blend, blur } = ray;
    const g = ctx.createRadialGradient(center.x, center.y, 0, center.x, center.y, length);
    ctx.beginPath();
    g.addColorStop(0, colorToRGBA(colors.inner));
    g.addColorStop(1, colorToRGBA(colors.outer));
    ctx.fillStyle = g;
    ctx.arc(center.x, center.y, length, start, start + ray.width);
    ctx.lineTo(center.x, center.y);
    ctx.globalCompositeOperation = blend;
    if (blur === 0) {
      ctx.filter = "";
    } else {
      ctx.filter = `blur(${blur}px)`;
    }
    ctx.fill();
  });
  // ctx.beginPath();
  // ctx.arc(center.x, center.y, 60, 0, 2 * Math.PI);
  // ctx.stroke();
};

export default defineComponent({
  props: {
    color: {
      type: Array,
      default: () => [255, 0, 255],
    },
    rayConfig: {
      type: Array as PropType<Array<RayConfig>>,
      required: true,
    },
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
    const canvas = ref<HTMLCanvasElement | null>(null);
    const containerStyle = computed(() => {
      const bg = props.color.join(",");
      return {
        height: `${props.height + 300}px`,
        background: `rgb(${bg})`,
      };
    });
    const visualStyle = computed(() => {
      return {
        height: `${props.height}px`,
        width: `${props.width}px`,
      };
    });
    const initCanvas = async () => {
      console.debug("initCanvas");
    };

    const rays = computed(() => {
      const r: Ray[] = [];
      props.rayConfig.forEach((conf: RayConfig) => {
        const { count, colors, spread, width, length } = conf;
        for (let i = 0; i < count; i++) {
          r.push({
            start: Math.PI * Math.random() * spread,
            width: Math.PI * Math.random() * width,
            length,
            colors,
            blur: 0,
            blend: "multiply",
          });
        }
      });
      return r;
    });

    const updateCanvas = async () => {
      const ctx = canvas.value?.getContext("2d");
      if (ctx) {
        await drawCanvas(ctx, props.width, props.height, 92, rays.value);
      }
    };
    onMounted(() => {
      initCanvas();
    });
    const size = computed(() => {
      return {
        height: props.height,
        width: props.width,
      };
    });
    watch(
      () => size.value,
      async () => {
        // await initCanvas();
        await updateCanvas();
      }
    );
    return {
      canvas,
      containerStyle,
      visualStyle,
    };
  },
});
</script>

<template>
  <div class="visual-container" :style="containerStyle">
    <div class="visual" :style="visualStyle">
      <canvas ref="canvas"></canvas>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.visual {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
