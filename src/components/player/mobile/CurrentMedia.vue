<script lang="ts">
import { defineComponent } from "vue";

import MediaArtists from "@/components/catalog/media/MediaArtists.vue";

export default defineComponent({
  props: {
    media: {
      type: Object,
      required: false,
      default: () => null,
    },
  },
  components: {
    MediaArtists,
  },
  setup() {
    return {};
  },
});
</script>

<template>
  <div class="current-media">
    <div v-if="media" class="metadata">
      <router-link
        class="metadata--primary"
        :to="{
          name: 'mediaDetail',
          params: {
            uid: media.uid,
          },
        }"
        v-text="media.name"
      />
      <div class="metadata--secondary">
        <MediaArtists :artists="media.artists" :link="false" />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
.current-media {
  display: grid;
  .metadata {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    &--primary,
    &--secondary {
      @include typo.small;
      max-width: 100%;
      overflow: inherit;
      white-space: inherit;
      text-overflow: inherit;
    }
    &--secondary {
      @include typo.dim;
    }
  }
}
</style>
