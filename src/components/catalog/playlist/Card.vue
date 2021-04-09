<script>

import LazyImage from '@/components/UI/LazyImage.vue';
import { getImageSrc } from '@/utils/image';

export default {
  components: { LazyImage },
  props: {
    playlist: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const link = `/discover/playlists/${props.playlist.uid}/`;
    const imageSrc = getImageSrc(props.playlist);
    return { link, imageSrc };
  },
};
</script>
<template>
  <div
    class="card card--artist"
  >
    <div
      class="visual"
    >
      <div
        class="visual__image"
      >
        <LazyImage
          :src="imageSrc"
        />
      </div>
    </div>
    <div
      class="meta"
    >
      <div
        class="title"
      >
        <router-link
          :to="link"
        >
          {{ playlist.name }}
        </router-link>
      </div>
      <div
        class="subtitle"
      >
        ( Sub Title )
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.card {
  .visual {
    background: rgba(var(--c-white), .25);
    &__image {
      position: relative;
      width: 100%;
      padding-bottom: 100%;
      img {
        position: absolute;
        width: 100%;
      }
    }
  }
  .meta {
    padding: 0.5rem 0 0 0;
    line-height: 1.25rem;
    .title {
      font-weight: 600;
      overflow-wrap: anywhere;
    }
  }
}
</style>
