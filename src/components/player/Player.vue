<script>
import settings from '@/settings';
import eventBus from '@/eventBus';
import CurrentMedia from './CurrentMedia.vue';
import Playhead from './Playhead.vue';

export default {
  components: {
    CurrentMedia,
    Playhead,
  },
  computed: {
    playerState() {
      return this.$store.getters['player/playerState'];
    },
    streamUrl() {
      // e.g. https://stream-abr.next.openbroadcast.ch/stream.mpd
      return settings.STREAM_ENDPOINTS.dash;
    },
    mediaBaseUrl() {
      return settings.MEDIA_ENDPOINTS.dash;
    },
    isLive() {
      return this.playerState && this.playerState.isLive;
    },
    cssVars() {
      return {
        '--c-black': this.isLive ? '100, 100, 100' : '0, 0, 0',
      };
    },
  },
  methods: {
    play(key) {
      let url;
      let startTime;
      if (key === 'stream') {
        url = `${this.streamUrl}?${Date.now()}`;
        startTime = -10;
      } else {
        // e.g. https://media.next.openbroadcast.ch/encoded/F002/manifest.mpd
        url = `${this.mediaBaseUrl}${key}/dash/manifest.mpd`;
      }

      const event = {
        do: 'play',
        url,
        startTime,
      };
      eventBus.emit('player:controls', event);
    },
    seek(relPosition) {
      const event = {
        do: 'seek',
        relPosition,
      };
      eventBus.emit('player:controls', event);
    },
    pause() {
      eventBus.emit('player:controls', { do: 'pause' });
    },
    resume() {
      eventBus.emit('player:controls', { do: 'resume' });
    },
    stop() {
      eventBus.emit('player:controls', { do: 'stop' });
    },
  },
};
</script>

<template>
  <div
    class="player"
    :style="cssVars"
  >
    <div class="container">
      <div class="left">
        <CurrentMedia />
      </div>
      <div class="center">
        <Playhead
          @seek="seek"
        />
      </div>
      <div class="right">
        ( actions )
      </div>
    </div>
  </div>
  <div class="player-dummy-controls">
    <div>
      <button @click="play('stream')">LIVE</button>
      <button @click="play('F001')">F001</button>
      <button @click="play('F002')">F002</button>
      <button @click="play('F003')">F003</button>
      <button @click="pause">PAUSE</button>
      <button @click="resume">RESUME</button>
      <button @click="stop">STOP</button>
    </div>
  </div>
  <div class="player-debug">
    <pre
      v-text="playerState"
      class="debug"
    />
  </div>
</template>

<style lang="scss" scoped>
/* stylelint-disable-next-line at-rule-no-unknown */
@use "@/style/elements/container";

$player-height: 60px;

.player {
  position: fixed;
  bottom: 0;
  height: $player-height;
  width: 100%;
  //@include container.default;
  color: rgba(var(--c-white));
  background: rgba(var(--c-black));
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
  bottom: 70px;
  right: 10px;
  max-width: 600px;
  width: 100%;
  background: #000;
}
</style>
