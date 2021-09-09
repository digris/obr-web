<script lang="ts">
import {
  defineComponent,
  ref,
  onMounted,
  onActivated,
  onDeactivated,
  // nextTick,
} from 'vue';

import { Starfield } from './playground';

export default defineComponent({
  setup() {
    const root = ref(null);
    // const canvas = ref(false);
    const canvas = ref(null);
    // const ctx = ref(null);
    // const canvasWidth = ref(0);
    // const canvasHeight = ref(0);
    const created = ref(false);
    const gl = ref(null);
    const initializeCanvas = () => {
      // @ts-ignore
      const { clientWidth, clientHeight } = root.value;
      console.debug('w / h', clientWidth, clientHeight);
      // @ts-ignore
      canvas.value.width = clientWidth;
      // @ts-ignore
      canvas.value.height = clientHeight;
      // @ts-ignore
      // ctx.value = canvas.value.getContext('2d');
      // console.debug('c', canvas.value);
      // window.r = root.value;
      // window.c = canvas.value;
      // window.ctx = ctx.value;
      // @ts-ignore
      gl.value = new Starfield(canvas.value);
      // @ts-ignore
      window.g = gl.value;
    };
    const cleanCanvas = () => {
      console.debug('destroyCanvas: destroyed');
      created.value = false;
    };
    onMounted(() => {
      initializeCanvas();
    });
    onActivated(() => {
      cleanCanvas();
    });
    onDeactivated(() => {
      cleanCanvas();
    });
    return {
      root,
      canvas,
    };
  },
});
</script>

<template>
  <div
    ref="root"
    class="animation"
  >
    <canvas
      ref="canvas"
    />
  </div>
</template>

<style lang="scss" scoped>
.animation {
  width: 100%;
  height: 100%;
  //background: linear-gradient(0.25turn, #3f87a6, #ebf8e1, #f69d3c);
}
</style>
