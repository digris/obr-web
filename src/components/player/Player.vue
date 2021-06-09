<script lang="ts">
import settings from '@/settings';
import eventBus from '@/eventBus';
import { computed, defineComponent, ref } from 'vue';
import { useStore } from 'vuex';
import CurrentMedia from './CurrentMedia.vue';
import Playhead from './Playhead.vue';
import Queue from './Queue.vue';

export default defineComponent({
  components: {
    CurrentMedia,
    Playhead,
    Queue,
  },
  setup() {
    const store = useStore();
    const liveTimeOffset = ref(-10);
    const streamUrl = computed(() => settings.STREAM_ENDPOINTS.dash);
    const playerState = computed(() => store.getters['player/playerState']);
    const isLive = computed(() => playerState.value && playerState.value.isLive);
    // const currentMedia = computed(() => store.getters['player/currentMedia']);
    const currentMedia = computed(() => {
      if (isLive.value) {
        return store.getters['schedule/currentMedia'];
      }
      return store.getters['queue/currentMedia'];
    });
    const cssVars = computed(() => ({
      '--c-bg': isLive.value ? '255, 255, 255' : '0, 0, 0',
      '--c-fg': isLive.value ? '0, 0, 0' : '255, 255, 255',
    }));

    const play = (key:string) => {
      if (key !== 'live') {
        return;
      }
      const startTime = parseInt(`${liveTimeOffset.value}`, 10);
      const event = {
        do: 'play',
        url: `${streamUrl.value}?${Date.now()}`,
        startTime,
      };
      eventBus.emit('player:controls', event);
    };

    const seek = (relPosition:number) => {
      const event = {
        do: 'seek',
        relPosition,
      };
      eventBus.emit('player:controls', event);
    };

    const pause = () => {
      eventBus.emit('player:controls', { do: 'pause' });
    };

    const resume = () => {
      eventBus.emit('player:controls', { do: 'resume' });
    };

    const stop = () => {
      eventBus.emit('player:controls', { do: 'stop' });
    };

    const queueVisible = ref(false);
    const queueNumMedia = computed(() => store.getters['queue/numMedia']);
    const queueTotalDuration = computed(() => store.getters['queue/totalDuration']);

    const showQueue = () => {
      queueVisible.value = true;
    };

    const hideQueue = () => {
      queueVisible.value = false;
    };

    return {
      isLive,
      liveTimeOffset,
      playerState,
      currentMedia,
      cssVars,
      play,
      seek,
      pause,
      resume,
      stop,
      //
      queueVisible,
      queueNumMedia,
      queueTotalDuration,
      showQueue,
      hideQueue,
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
        <Playhead
          @seek="seek"
        />
      </div>
      <div class="right">
        <span
          v-if="(!queueVisible)"
          @click="showQueue"
        >
          Q
          <small>{{ queueNumMedia }} / {{ queueTotalDuration }}</small>
        </span>
        <span
          v-else
          @click="hideQueue"
        >
          Q
          <small>{{ queueNumMedia }} / {{ queueTotalDuration }}</small>
        </span>
      </div>
    </div>
  </div>
  <div class="player-dummy-controls">
    <div>
      <button @click="play('live')">LIVE</button>
      <input v-model="liveTimeOffset" type="number" style="width: 60px;">
      <button @click="pause">PAUSE</button>
      <button @click="resume">RESUME</button>
      <button @click="stop">STOP</button>
    </div>
  </div>
  <div
    v-if="(1 === 2)"
    class="player-debug"
  >
    <!--
    <pre
      v-text="currentMedia"
      class="_debug"
    />
    <pre
      v-text="playerState"
      class="_debug"
    />
    -->
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";

$player-height: 60px;

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
  transition: background 500ms;
}

.container {
  @include container.default;
  display: grid;
  grid-template-columns: 2fr 6fr 2fr;
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
