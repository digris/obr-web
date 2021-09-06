<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import { useStore } from 'vuex';
import { getContrastColor } from '@/utils/color';
import CurrentMedia from './CurrentMedia.vue';
import Playhead from './Playhead.vue';
import Radio from './Radio.vue';
import Queue from './Queue.vue';
import Circle from './button/Circle.vue';
import UserRating from '@/components/rating/UserRating.vue';
import Debug from '@/components/dev/Debug.vue';

export default defineComponent({
  components: {
    CurrentMedia,
    Playhead,
    Radio,
    Circle,
    Queue,
    UserRating,
    Debug,
  },
  setup() {
    const store = useStore();
    const liveTimeOffset = ref(-10);
    const playerState = computed(() => store.getters['player/playerState']);
    const isLive = computed(() => store.getters['player/isLive']);
    const currentMedia = computed(() => store.getters['player/currentMedia']);
    const currentScope = computed(() => store.getters['player/currentScope']);
    const isVisible = computed(() => !!currentMedia.value);
    const objKey = computed(() => {
      if (!currentMedia.value) {
        return null;
      }
      return `${currentMedia.value?.ct}:${currentMedia.value?.uid}`;
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
      isVisible,
      isLive,
      liveTimeOffset,
      playerState,
      currentMedia,
      currentScope,
      objKey,
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
  <Debug
    :visible="(false)"
    :value="{
      isLive,
      currentScope,
      playerState,
    }"
  />
  <Queue
    :is-visible="(queueVisible && queueNumMedia > 0)"
    @close="hideQueue"
  />
  <transition
    name="slide"
  >
    <div
      v-if="isVisible"
      class="player"
      :style="cssVars"
    >
      <div
        class="container"
      >
        <div
          class="left"
        >
          <CurrentMedia
            :media="currentMedia"
          />
        </div>
        <div
          class="center"
        >
          <Radio
            v-if="isLive"
          />
          <Playhead
            v-else
          />
        </div>
        <div
          class="right"
        >
          <Circle
            :size="(48)"
            :outlined="(false)"
          >
            <UserRating
              color-var="--c-fg"
              v-if="currentMedia"
              :obj-key="objKey"
            />
          </Circle>
          <Circle
            :size="(48)"
            :active="queueVisible"
            :disabled="(queueNumMedia < 1)"
            @click.prevent="toggleQueue"
            :style="{
              color: queueVisible ? 'rgb(var(--c-bg))' : 'rgb(var(--c-fg))',
            }"
          >
            <span
              v-text="queueNumMedia"
            />
          </Circle>
        </div>
      </div>
    </div>
  </transition>
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
  z-index: 110;
  width: 100%;
  height: $player-height;
  color: rgba(var(--c-fg));
  background: rgba(var(--c-bg));
  border-top: 1px solid rgba(var(--c-page-fg), .2);
  transition: background 1000ms;
}

.container {
  @include container.default;
  display: grid;
  grid-template-columns: 4fr 6fr 4fr;
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
    .on-air {
      padding: 12px 24px;
      color: rgb(var(--c-white));
      background: rgb(var(--c-red));
    }
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

.slide-enter-active,
.slide-leave-active {
  transition: transform 200ms, opacity 200ms;
}
.slide-enter-from {
  transform: translate(0, 100%);
  opacity: 0;
}
.slide-leave-to {
  transform: translate(0, 100%);
}
</style>
