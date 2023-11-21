<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  props: {
    releases: {
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
  <div v-if="releases.length" class="media-releases">
    <span v-for="(release, index) in releases" :key="`media-release-${index}`" class="release">
      <span class="release__name" v-text="release.name" />
    </span>
  </div>
</template>

<style lang="scss" scoped>
.media-releases {
  display: inline-flex;
}

.release {
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;

  &__name {
    white-space: nowrap;
  }
}
</style>
