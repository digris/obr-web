<script>
export default {
  props: {
    artists: {
      type: Array,
      default: () => [],
    },
  },
  setup() {
    const link = `/discover/artists/${123}/`;
    return { link };
  },
};
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
      <router-link
        :to="`/discover/artists/${artist.uid}/`"
        class="artist__name"
      >
        {{ artist.name }}
      </router-link>
    </span>
  </div>
</template>

<style lang="scss" scoped>
.media-artists {
  display: inline-flex;
}
.artist {
  &__join {
    margin-right: 0.25rem;
    margin-left: 0.25rem;
    opacity: 0.5;
  }
  &__name {
    white-space: nowrap;
    &:hover {
      text-decoration: underline;
    }
  }
}
</style>
