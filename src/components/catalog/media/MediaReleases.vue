<script>
export default {
  props: {
    releases: {
      type: Array,
      default: () => [],
    },
  },
};
</script>

<template>
  <div
    v-if="(releases.length)"
    class="media-releases"
  >
    <span
      v-for="(release, index) in releases"
      :key="`media-release-${index}`"
      class="release"
    >
      <span
        class="releaset__name"
      >
        {{ release.name }}
      </span>
    </span>
  </div>
</template>

<style lang="scss" scoped>
.media-releases {
  display: inline-flex;
}
.release {
  &__name {
    white-space: nowrap;
  }
}
</style>
