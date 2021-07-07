<script>
import eventBus from '@/eventBus';
import Progress from './PlayheadProgress.vue';
import PlayerButton from './PlayerButton.vue';

const dt2hhmmss = (dt) => dt.toISOString().substr(11, 8);
const s2hhmmss = (s) => dt2hhmmss(new Date(s * 1000));

export default {
  components: {
    PlayerButton,
    Progress,
  },
  computed: {
    playerState() {
      return this.$store.getters['player/playerState'];
    },
    isLive() {
      return this.playerState && this.playerState.isLive;
    },
    isPlaying() {
      return this.playerState && this.playerState.isPlaying;
    },
    isBuffering() {
      return this.playerState && this.playerState.isBuffering;
    },
    currentTime() {
      return this.playerState && this.playerState.currentTime;
    },
    duration() {
      return this.playerState && this.playerState.duration;
    },
    relPosition() {
      return this.playerState && this.playerState.relPosition;
    },
    // mapped output
    strCurrentTime() {
      if (!this.currentTime) {
        return '00:00:00';
      }
      if (this.isLive) {
        return dt2hhmmss(this.currentTime);
      }
      return s2hhmmss(this.currentTime);
    },
    strTotalTime() {
      if (this.isLive) {
        return '--:--:--';
      }
      if (!this.duration) {
        return '00:00:00';
      }
      return s2hhmmss(this.duration);
    },
    // strBandwidth() {
    //   if (this.playerState) {
    //     const kbps = Math.round(this.playerState.bandwidth / 1000);
    //     return `${kbps} kbps`;
    //   }
    //   return '-';
    // },
  },
  methods: {
    seek(relPosition) {
      this.$emit('seek', relPosition);
    },
    playNext() {
      eventBus.emit('queue:controls:playNext');
    },
    playPrevious() {
      eventBus.emit('queue:controls:playPrevious');
    },
    stop() {
      eventBus.emit('player:controls', { do: 'stop' });
    },
    pause() {
      eventBus.emit('player:controls', { do: 'pause' });
    },
    resume() {
      eventBus.emit('player:controls', { do: 'resume' });
    },
  },
};
</script>

<template>
  <div class="playhead">
    <div class="actions">
      <button
        @click="stop"
        class="action"
      >S</button>
      <button
        @click="pause"
        class="action"
      >P</button>
      <button
        @click="resume"
        class="action"
      >R</button>
    </div>
    <div class="time time--current">
      <span>{{ strCurrentTime }}</span>
    </div>
    <div class="progress">
      <Progress
        :is-live="isLive"
        :is-playing="isPlaying"
        :is-buffering="isBuffering"
        :rel-position="relPosition"
        @seek="seek"
      />
    </div>
    <div class="time time--total">
      <span>{{ strTotalTime }}</span>
    </div>
    <div class="actions">
      <button
        @click="playPrevious"
        class="action"
      >&lt;</button>
      <button
        @click="playNext"
        class="action"
      >&gt;</button>
    </div>
    <!--
    <div
      class="info"
    >
      <span
        class="bandwidth"
      >{{ strBandwidth }}</span>
    </div>
    -->
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";
@use "@/style/base/typo";

@mixin time {
  padding: 0 0.5rem;
  color: rgba(var(--c-fg), 0.5);
  font-size: 0.9rem;
}

@mixin actions {
  //display: grid;
  //grid-gap: 0.5rem;
  display: flex;
  .action {
    display: inline-block;
    width: 1.5rem;
    height: 1.5rem;
    margin: 0 0.25rem;
    color: rgb(var(--c-bg));
    background: rgba(var(--c-fg), 0.5);
    border: none;
    border-radius: 0.75rem;
    cursor: pointer;
    transition: background 100ms;
    &:hover {
      background: rgba(var(--c-fg), 0.9);
    }
  }
}

.playhead {
  display: grid;
  grid-template-columns: auto auto 1fr auto auto;
  width: 100%;
  .actions,
  .progress,
  .time {
    display: flex;
    align-items: center;
  }
  .actions {
    @include actions;
  }
  .time {
    @include time;
    min-width: 84px;
    max-width: 84px;
  }
  .progress {
    margin: 0 0.5rem;
  }
  .info {
    display: flex;
    align-items: center;
    padding-left: 0.5rem;
    .bandwidth {
      @include typo.small;
    }
  }
}
</style>
