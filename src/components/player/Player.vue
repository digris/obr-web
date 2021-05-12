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
  data() {
    return {
      startTime: -10,
    };
  },
  computed: {
    playerState() {
      return this.$store.getters['player/playerState'];
    },
    encodingFormat() {
      return this.$store.getters['player/encodingFormat'];
    },
    currentMedia() {
      return this.$store.getters['player/currentMedia'];
    },
    streamUrl() {
      // e.g. https://stream-abr.next.openbroadcast.ch/stream.mpd
      // return 'http://local.stream-dash.openbroadcast.ch:7779/alt.m3u8';
      // return 'http://local.stream-dash.openbroadcast.ch:7779/manifest.m3u8';
      // return 'http://local.stream-dash.openbroadcast.ch:7779/stream.mpd';
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
        '--c-bg': this.isLive ? '255, 255, 255' : '0, 0, 0',
        '--c-fg': this.isLive ? '0, 0, 0' : '255, 255, 255',
      };
    },
  },
  methods: {
    play(key) {
      let url;
      let startTime;
      if (key === 'stream') {
        url = `${this.streamUrl}?${Date.now()}`;
        startTime = parseInt(this.startTime, 10);
      } else {
        // e.g. https://media.next.openbroadcast.ch/encoded/F002/manifest.mpd
        url = `${this.mediaBaseUrl}${key}/dash/manifest.mpd`;
        // url = `${this.mediaBaseUrl}${key}/hls/manifest.m3u8`;
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
    setEncodingFormat(encodingFormat) {
      this.$store.dispatch('player/updateEncodingFormat', encodingFormat);
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
        ({{ encodingFormat }})
        <a @click.prevent="setEncodingFormat('dash')">DASH</a>
        <span> - </span>
        <a @click.prevent="setEncodingFormat('hls')">HLS</a>
      </div>
    </div>
  </div>
  <div class="player-dummy-controls">
    <div>
      <button @click="play('stream')">LIVE</button>
      <input v-model="startTime" type="number">
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
      class="_debug"
    />
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";

$player-height: 60px;

.player {
  position: fixed;
  bottom: 0;
  width: 100%;
  height: $player-height;
  //@include container.default;
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
