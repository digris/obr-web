<script>
import MediaArtists from '@/components/catalog/media/MediaArtists.vue';

export default {
  props: {
    media: {
      type: Object,
    },
    isCurrent: {
      type: Boolean,
      default: false,
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
    // currentMedia() {
    //   return this.$store.getters['player/currentMedia'];
    // },
    // playerState() {
    //   return this.isCurrent ? this.$store.getters['player/playerState'] : null;
    // },
    // isCurrent() {
    //   return this.currentMedia && (this.media.uid === this.currentMedia.uid);
    // },
  },
};
</script>

<template>
  <div
    class="media-row"
    :class="{'is-current': isCurrent}"
  >
    <div class="play">
      (P)
    </div>
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
    <div class="rating">
      (R)
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
.media-row {
  display: grid;
  grid-row-gap: 0.25rem;
  grid-column-gap: 1rem;
  grid-template-areas:
    "play name   duration rating"
    "play artist .        rating";
  grid-template-columns: 1fr 9fr 3fr 1fr;
  padding: 0.25rem 0;
  border-bottom: 2px solid rgb(var(--c-black));
  //TODO: find a modular way to handle color / ui transitions
  transition: border-bottom 200ms 1400ms;
  > div {
    display: flex;
    align-items: center;
  }
  .play {
    grid-area: play;
    padding-left: 0.5rem;
  }
  .name {
    grid-area: name;
    //@include typo.large;
  }
  .artist {
    grid-area: artist;
  }
  .airplays {
    grid-area: airplays;
    @include typo.small;
  }
  .duration {
    grid-area: duration;
    @include typo.small;
    @include typo.dim;
  }
  .rating {
    grid-area: rating;
  }
  &.is-current {
    background: rgba(var(--c-page-bg), 0.1);
  }
}
</style>
