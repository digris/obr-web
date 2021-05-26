<script>
import MediaArtists from '@/components/catalog/media/MediaArtists.vue';

export default {
  props: {
    media: {
      type: Object,
    },
  },
  components: {
    MediaArtists,
  },
  computed: {
    objKey() {
      return `${this.media.ct}:${this.media.uid}`;
    },
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
      return this.currentMedia && (this.media.uid === this.currentMedia.uid);
    },
  },
};
</script>

<template>
  <div
    class="media-row"
    :class="{'is-current': isCurrent}"
  >
    <div class="name">
      {{ media.name }}
    </div>
    <div class="artist">
      <MediaArtists
        :artists="media.artists"
      />
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
  grid-template-columns: 2fr 2fr 1fr;
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
