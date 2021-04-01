<script>
import PlayheadProgress from './PlayheadProgress.vue';

const dt2hhmmss = (dt) => dt.toISOString().substr(11, 8);
const s2hhmmss = (s) => dt2hhmmss(new Date(s * 1000));

export default {
  components: {
    PlayheadProgress,
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
  },
  methods: {
    seek(relPosition) {
      this.$emit('seek', relPosition);
    },
  },
};
</script>

<template>
  <div class="playhead">
    <div class="actions">
      <button class="action">+</button>
      <button class="action">+</button>
    </div>
    <div class="time time--current">
      <span>{{ strCurrentTime }}</span>
    </div>
    <div class="progress">
      <PlayheadProgress
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
      <button class="action">+</button>
      <button class="action">+</button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
/* stylelint-disable-next-line at-rule-no-unknown */
@use "@/style/elements/container";

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
  .time {
    font-size: 0.9rem;
    color: rgb(var(--c-gray-500));
    min-width: 84px;
    max-width: 84px;
  }
  .progress {
    margin: 0 0.5rem;
  }
}
.time {
  padding: 0 0.5rem;
}
.actions {
  display: grid;
  grid-gap: 0.5rem;
  .action {
    border: none;
    display: inline-block;
    width: 1.5rem;
    height: 1.5rem;
    border-radius: 0.75rem;
    background: rgb(var(--c-gray-500));
    cursor: pointer;
    transition: background 100ms;
    &:hover {
      background: rgb(var(--c-gray-100));
    }
  }
}

</style>
