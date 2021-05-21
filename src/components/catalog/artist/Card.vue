<script>
import { computed } from 'vue';

import { getImageSrc } from '@/utils/image';
import LazyImage from '@/components/ui/LazyImage.vue';
import UserRating from '@/components/rating/UserRating.vue';

export default {
  components: {
    LazyImage,
    UserRating,
  },
  props: {
    artist: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const objKey = computed(() => `${props.artist.ct}:${props.artist.uid}`);
    const link = `/discover/artists/${props.artist.uid}/`;
    // const imageSrc = `https://picsum.photos/seed/${props.artist.uid}/200`;
    const imageSrc = getImageSrc(props.artist);
    return {
      objKey,
      link,
      imageSrc,
    };
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
          {{ artist.name }}
        </router-link>
        <div class="rating">
          <UserRating
            :obj-key="objKey"
          />
        </div>
      </div>
      <div
        class="subtitle"
      >
        <small>{{ artist.numMedia }} tracks</small>
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
      display: flex;
      font-weight: 600;
      a {
        flex-grow: 1;
      }
    }
  }
}
</style>
