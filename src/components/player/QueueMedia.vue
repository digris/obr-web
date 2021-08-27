<script lang="ts">
import { computed, defineComponent } from 'vue';
import eventBus from '@/eventBus';
import MediaArtists from '@/components/catalog/media/MediaArtists.vue';

export default defineComponent({
  components: {
    MediaArtists,
  },
  props: {
    media: {
      type: Object,
    },
    index: {
      type: Number,
    },
    isCurrent: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const objKey = computed(() => {
      return `${props.media.ct}:${props.media.uid}`;
    });
    const duration = computed(() => {
      return new Date(props.media.duration * 1000).toISOString().substr(11, 8);
    });
    const play = () => {
      eventBus.emit('queue:controls:playFromIndex', props.index);
    };
    return {
      objKey,
      duration,
      play,
    };
  },
});
</script>

<template>
  <div
    class="media-row"
    :class="{'is-current': isCurrent}"
  >
    <div class="play" @click="play">
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
