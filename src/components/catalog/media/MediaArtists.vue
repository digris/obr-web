<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  props: {
    artists: {
      type: Array,
      default: () => [],
    },
    link: {
      type: Boolean,
      default: true,
    },
  },
});
</script>

<template>
  <div
    class="media-artists"
  >
    <span
      v-for="(artist, index) in artists"
      :key="`media-artist-${index}`"
      class="artist"
    >
      <span
        v-if="(index > 0 && artist.joinPhrase)"
        class="artist__join"
      >
        {{ artist.joinPhrase }}
      </span>
      <span
        v-else-if="(index > 0)"
        class="artist__join artist__join--spaceless"
      >, </span>
      <router-link
        v-if="link"
        :to="`/discover/artists/${artist.uid}/`"
        class="artist__name"
        v-text="artist.name"
      />
      <span
        v-else
        v-text="artist.name"
      />
    </span>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/live-color";
@use "@/style/abstracts/responsive";
.media-artists {
  display: inline-flex;
}
.artist {
  &__join {
    margin-right: 0.25rem;
    margin-left: 0.25rem;
    opacity: 0.5;
    &--spaceless {
      margin-right: 0;
      margin-left: 0;
    }
  }
  &__name {
    white-space: nowrap;
    transition: color, background-color 200ms;
    @include responsive.on-hover {
      @include live-color.bg-inverse($alpha: 0.1, $transition: false);
    }
  }
}
</style>
