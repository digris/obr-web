<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import { useStore } from 'vuex';
import { getContrastColor } from '@/utils/color';
// import CurrentMedia from './CurrentMedia.vue';
// import Playhead from './Playhead.vue';
// import OnAir from './button/OnAir.vue';
import eventBus from '@/eventBus';
import Queue from '@/components/player/Queue.vue';
import Circle from '@/components/player/button/Circle.vue';
import UserRating from '@/components/rating/UserRating.vue';
import IconQueue from '@/components/ui/icon/IconQueue.vue';
import ButtonPlay from '@/components/player/button/ButtonPlay.vue';
import MediaArtists from '@/components/catalog/media/MediaArtists.vue';
import PlayerPanel from './PlayerPanel.vue';

export default defineComponent({
  components: {
    ButtonPlay,
    Circle,
    Queue,
    UserRating,
    MediaArtists,
    IconQueue,
    PlayerPanel,
  },
  setup() {
    const store = useStore();
    const liveTimeOffset = ref(-10);
    const playerState = computed(() => store.getters['player/playerState']);
    const isLive = computed(() => store.getters['player/isLive']);
    const isPlaying = computed(() => playerState.value && playerState.value.isPlaying);
    const isBuffering = computed(() => playerState.value && playerState.value.isBuffering);
    const currentMedia = computed(() => store.getters['player/media']);
    const currentScope = computed(() => store.getters['player/scope']);
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
    const pause = () => {
      eventBus.emit('player:controls', { do: 'pause' });
    };
    const play = () => {
      eventBus.emit('player:controls', { do: 'resume' });
    };
    const queueVisible = ref(false);
    const queueNumMedia = computed(() => store.getters['queue/numMedia']);
    const hideQueue = () => {
      queueVisible.value = false;
    };
    const toggleQueue = () => {
      queueVisible.value = !queueVisible.value;
    };
    const playerPanelVisible = ref(false);
    const hidePlayerPanel = () => {
      playerPanelVisible.value = false;
    };
    const togglePlayerPanel = () => {
      playerPanelVisible.value = !playerPanelVisible.value;
    };
    return {
      isVisible,
      isLive,
      isPlaying,
      isBuffering,
      liveTimeOffset,
      playerState,
      currentMedia,
      currentScope,
      objKey,
      cssVars,
      queueVisible,
      queueNumMedia,
      pause,
      play,
      hideQueue,
      toggleQueue,
      playerPanelVisible,
      hidePlayerPanel,
      togglePlayerPanel,
    };
  },
});
</script>

<template>
  <Queue
    :is-visible="(queueVisible && queueNumMedia > 0)"
    :bottom="(60)"
    @close="hideQueue"
  />
  <PlayerPanel
    :is-visible="playerPanelVisible"
    :current-media="currentMedia"
    :style="cssVars"
    @close="hidePlayerPanel"
  />
  <transition
    name="slide"
  >
    <div
      v-if="isVisible"
      class="mobile-player"
      :style="cssVars"
    >
      <div
        class="container"
      >
        <div
          class="left"
        >
          <ButtonPlay
            :size="40"
            :is-playing="isPlaying"
            :is-buffering="isBuffering"
            @pause="pause"
            @play="play"
          />
        </div>
        <div
          class="center"
        >
          <div
            v-if="currentMedia"
            @click="togglePlayerPanel"
            class="current-media"
          >
            <div
              v-text="currentMedia.name"
              class="title"
            />
            <MediaArtists
              :artists="currentMedia.artists"
              :link="false"
              class="artists"
            />
          </div>
        </div>
        <div
          class="right"
        >
          <Circle
            :size="(40)"
            :outlined="(false)"
          >
            <UserRating
              color-var="--c-fg"
              v-if="currentMedia"
              :obj-key="objKey"
            />
          </Circle>
          <Circle
            :size="(40)"
            :active="queueVisible"
            :disabled="(queueNumMedia < 1)"
            @click.prevent="toggleQueue"
            :style="{
              color: queueVisible ? 'rgb(var(--c-bg))' : 'rgb(var(--c-fg))',
            }"
          >
            <IconQueue
              :size="(40)"
              :color="(queueVisible ? 'rgb(var(--c-bg))' : 'rgb(var(--c-fg))')"
              :num-queued="queueNumMedia"
            />
          </Circle>
        </div>
      </div>
    </div>
  </transition>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
//@use "@/style/elements/container";

$player-height: 60px;

.queue {
  z-index: 30;
}

.player-panel {
  z-index: 29;
}

.mobile-player {
  position: fixed;
  bottom: 0;
  z-index: 110;
  width: 100%;
  height: $player-height;
  padding: 0 0.5rem;
  color: rgba(var(--c-fg));
  background: rgba(var(--c-bg));
  border-top: 1px solid rgba(var(--c-page-fg), .2);
  transition: background 1000ms;
}

.container {
  display: grid;
  grid-column-gap: 1rem;
  grid-template-columns: 40px 6fr 80px;
  .left,
  .center,
  .right {
    display: flex;
    align-items: center;
    justify-content: center;
    height: $player-height;
  }
  .left {
    justify-content: center;
  }
  .center {
    overflow: hidden;
    justify-content: flex-start;
  }
  .right {
    justify-content: flex-end;
  }
}

.current-media {
  white-space: nowrap;
  overflow: hidden;
  .title {
    line-height: 1rem;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .artists {
    @include typo.dim;
    @include typo.light;
    overflow: hidden;
    text-overflow: ellipsis;
  }
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
