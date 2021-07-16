<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import { useStore } from 'vuex';
import { getContrastColor } from '@/utils/color';
import CurrentMedia from './CurrentMedia.vue';
import Playhead from './Playhead.vue';
import Queue from './Queue.vue';
import Circle from './button/Circle.vue';

export default defineComponent({
  components: {
    CurrentMedia,
    Playhead,
    Circle,
    Queue,
  },
  setup() {
    const store = useStore();
    const liveTimeOffset = ref(-10);
    const playerState = computed(() => store.getters['player/playerState']);
    const isLive = computed(() => playerState.value && playerState.value.isLive);
    const currentMedia = computed(() => {
      if (isLive.value) {
        return store.getters['schedule/currentMedia'];
      }
      return store.getters['queue/currentMedia'];
    });
    const cssVars = computed(() => {
      try {
        const bg = currentMedia.value.releases[0].image.rgb;
        const fg = getContrastColor(bg);
        const fgInverse = getContrastColor(fg);
        const colors = {
          '--c-bg': bg.join(','),
          '--c-fg': fg.join(','),
          '--c-fg-inverse': fgInverse.join(','),
        };
        return colors;
      } catch (e) {
        // console.debug(e);
      }
      return {
        '--c-bg': isLive.value ? '255, 255, 255' : '0, 0, 0',
        '--c-fg': isLive.value ? '0, 0, 0' : '255, 255, 255',
        '--c-fg-inverse': isLive.value ? '255, 255, 255' : '0, 0, 0',
      };
    });

    const queueVisible = ref(false);
    const queueNumMedia = computed(() => store.getters['queue/numMedia']);
    const hideQueue = () => {
      queueVisible.value = false;
    };
    const toggleQueue = () => {
      queueVisible.value = !queueVisible.value;
    };
    return {
      isLive,
      liveTimeOffset,
      playerState,
      currentMedia,
      cssVars,
      queueVisible,
      queueNumMedia,
      hideQueue,
      toggleQueue,
    };
  },
});
</script>

<template>
  <Queue
    :is-visible="queueVisible"
    @close="hideQueue"
  />
  <div
    class="player"
    :style="cssVars"
  >
    <div class="container">
      <div class="left">
        <CurrentMedia
          :media="currentMedia"
        />
      </div>
      <div class="center">
        <Playhead />
      </div>
      <div class="right">
        <Circle
          :size="(48)"
          :active="queueVisible"
          @click.prevent="toggleQueue"
          v-text="queueNumMedia"
          :style="{
            color: queueVisible ? 'rgb(var(--c-bg))' : 'rgb(var(--c-fg))',
          }"
        />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";

$player-height: 72px;

.queue {
  z-index: 30;
}

.player {
  position: fixed;
  bottom: 0;
  z-index: 31;
  width: 100%;
  height: $player-height;
  color: rgba(var(--c-fg));
  background: rgba(var(--c-bg));
  border-top: 1px solid rgba(var(--c-live-fg), .2);
  transition: background 1000ms;
}

.container {
  @include container.default;
  display: grid;
  grid-template-columns: 3fr 6fr 3fr;
  .left,
  .center,
  .right {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    height: $player-height;
  }
  .left {
    justify-content: flex-start;
  }
  .center {
    justify-content: center;
  }
  .right {
    justify-content: flex-end;
  }
}

.player-dummy-controls {
  position: fixed;
  bottom: 70px;
  left: 10px;
  max-width: 600px;
  background: #000;
}

.player-debug {
  position: fixed;
  right: 10px;
  bottom: 70px;
  width: 100%;
  max-width: 600px;
  background: #000;
}
</style>
