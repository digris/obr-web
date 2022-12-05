<script lang="ts">
import type { PropType } from "vue";
import { computed, defineComponent, onMounted, ref, watch } from "vue";

type RGBAColor = Array<[number, number, number, number]>;

interface Colors {
  inner: RGBAColor;
  outer: RGBAColor;
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
  blend: string;
  blur: number;
  colors: Colors;
}

const colorToRGBA = (color: RGBAColor) => {
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
  const center = {
    x: width / 2,
    y: height / 2 + offsetY / 2,
  };
  rays.forEach((ray: Ray) => {
    const { length, colors, start, blend, blur } = ray;
    const gradient = ctx.createRadialGradient(center.x, center.y, 0, center.x, center.y, length);
    ctx.beginPath();
    gradient.addColorStop(0, colorToRGBA(colors.inner));
    gradient.addColorStop(1, colorToRGBA(colors.outer));
    ctx.fillStyle = gradient;
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
};

export default defineComponent({
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
      type: Array,
      default: () => [255, 0, 255],
    },
    rayConfig: {
      type: Array as PropType<Array<RayConfig>>,
      default: () => [],
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
    const containerStyle = computed(() => {
      const bg = props.color.join(",");
      return {
        // TODO: implement calculation taking into account screen size
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
    const rays = computed(() => {
      const r: Ray[] = [];
      props.rayConfig.forEach((conf: RayConfig) => {
        const { count, colors, spread, width, length } = conf;
        for (let i = 0; i < count; i++) {
          r.push({
            blur: 0,
            blend: "multiply",
            start: Math.PI * Math.random() * spread,
            width: Math.PI * Math.random() * width,
            length,
            colors,
          });
        }
      });
      return r;
    });
    const updateCanvas = async () => {
      const ctx = canvas.value?.getContext("2d");
      if (ctx) {
        // TODO: implement offset calculation
        await drawCanvas(ctx, props.width, props.height, 92, rays.value);
      }
    };
    onMounted(async () => {
      await updateCanvas();
    });
    watch(
      () => size.value,
      async () => {
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
      <canvas ref="canvas" />
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
