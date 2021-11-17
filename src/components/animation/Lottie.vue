<script lang="ts">
import lottie from 'lottie-web';

import {
  ref,
  computed,
  defineComponent,
  onMounted,
} from 'vue';

export default defineComponent({
  props: {
    src: {
      type: String,
      default: '',
    },
    color: {
      type: Array,
      required: false,
      default: () => [0, 0, 7],
    },
  },
  setup(props) {
    const player = ref();
    const playerEl = ref();
    const cssVars = computed(() => ({
      '--c-star-rgb': props.color.join(','),
    }));
    onMounted(() => {
      console.debug('Lottie.vue mounted', playerEl.value);
      player.value = lottie.loadAnimation({
        container: playerEl.value,
        // @ts-ignore https://github.com/airbnb/lottie-web/pull/2619
        renderer: 'canvas',
        loop: true,
        autoplay: true,
        path: props.src,
        rendererSettings: {
          preserveAspectRatio: 'xMidYMid slice',
        },
      });
      console.debug('p', player);
      player.value.play();
    });
    return {
      playerEl,
      cssVars,
    };
  },
});
</script>

<template>
  <div
    class="lottie"
    :style="cssVars"
  >
    <div
      ref="playerEl"
      class="player"
    />
  </div>
</template>

<style lang="scss" scoped>
.lottie {
  position: relative;
  width: 100%;
  height: 100%;
  filter: grayscale(100%);
  .player {
    width: 100%;
    height: 100%;
  }
}
</style>
