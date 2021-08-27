<script lang="ts">
import { computed, defineComponent } from 'vue';

import LazyImage from '@/components/ui/LazyImage.vue';
import MediaArtists from '@/components/catalog/media/MediaArtists.vue';

export default defineComponent({
  props: {
    media: {
      type: Object,
      required: false,
      default: () => null,
    },
  },
  components: {
    LazyImage,
    MediaArtists,
  },
  setup(props) {
    const release = computed(() => {
      if (props.media && props.media.releases.length) {
        return props.media.releases[0];
      }
      return null;
    });
    const image = computed(() => {
      return (release.value && release.value.image) ? release.value.image : null;
    });
    return {
      release,
      image,
    };
  },
});
</script>

<template>
  <div
    class="current-media"
  >
    <router-link
      v-if="media"
      class="visual"
      :to="{
        name: 'mediaDetail',
        params: {
          uid: media.uid,
        },
      }"
    >
      <LazyImage
        :image="image"
      />
    </router-link>
    <div
      v-if="media"
      class="metadata"
    >
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
      <div
        class="metadata--secondary"
      >
        <MediaArtists
          :artists="media.artists"
        />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.current-media {
  display: grid;
  grid-template-columns: 64px 1fr;
  .visual {
    //padding: 0.75rem;
    width: 3rem;
    height: 3rem;
  }
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
      max-width: 100%;
      overflow: inherit;
      white-space: inherit;
      text-overflow: inherit;
    }
    /*
    &--secondary {
      color: rgba(var(--c-fg), 0.5);
    }
    */
  }
}
</style>
