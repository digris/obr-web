<script>
import { DateTime } from 'luxon';
import eventBus from '@/eventBus';
import { getDashUrl } from '@/player/media';

import PlayerControlIcon from '@/components/player/PlayerControlIcon.vue';
import MediaArtists from '@/components/catalog/media/MediaArtists.vue';

export default {
  props: {
    media: {
      type: Object,
    },
  },
  components: {
    PlayerControlIcon,
    MediaArtists,
  },
  computed: {
    duration() {
      return new Date(this.media.duration * 1000).toISOString().substr(11, 8);
    },
    currentMedia() {
      return this.$store.getters['player/currentMedia'];
    },
    playerState() {
      return this.isCurrent ? this.$store.getters['player/playerState'] : null;
    },
    isCurrent() {
      return this.media.uid === this.currentMedia.uid;
    },
    latestAirplay() {
      if (!this.media.latestAirplay) {
        return null;
      }
      const dt = DateTime.fromISO(this.media.latestAirplay);
      return dt.toFormat('HH:mm yyyy-LL-dd');
    },
  },
  methods: {
    controls(media) {
      const url = getDashUrl(media);
      const event = {
        do: 'play',
        url,
        startTime: 0,
      };
      eventBus.emit('player:controls', event);
      this.$store.dispatch('player/updateCurrentMedia', media);
    },
  },
};
</script>

<template>
  <div
    class="media-row"
    :class="{'is-current': isCurrent}"
  >
    <div class="play">
      <PlayerControlIcon
        @click="controls(media)"
        :player-state="playerState"
      />
    </div>
    <div class="name">
      {{ media.name }}
    </div>
    <div class="artist">
      <MediaArtists
        :artists="media.artists"
      />
    </div>
    <div class="airplays">
      <span
        v-if="latestAirplay"
        :title="`Total: ${media.numAirplays}`"
      >{{ latestAirplay }}</span>
    </div>
    <div class="duration">
      {{ duration }}
    </div>
  </div>
</template>

<style lang="scss" scoped>
.media-row {
  display: grid;
  grid-gap: 1rem;
  grid-template-columns: 1fr 6fr 7fr 3fr 2fr;
  padding: 0.5rem 0;
  border-bottom: 2px solid rgb(var(--c-live-fg));
  //TODO: find a modular way to handle color / ui transitions
  transition: border-bottom 200ms 1400ms;
  > div {
    display: flex;
    align-items: center;
  }
  .play {
    padding-left: 0.5rem;
  }
  &.is-current {
    background: rgba(var(--c-live-fg), 0.1);
  }
}
</style>
