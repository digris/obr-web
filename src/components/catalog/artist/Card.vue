<script>
import { computed } from 'vue';

import LazyImage from '@/components/ui/LazyImage.vue';
import PlayIcon from '@/components/catalog/actions/PlayIcon.vue';
import UserRating from '@/components/rating/UserRating.vue';

export default {
  components: {
    LazyImage,
    PlayIcon,
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
    return {
      objKey,
      link,
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
          :image="artist.image"
        />
      </div>
      <PlayIcon
        class="visual__play"
        :obj-key="objKey"
      />
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
    position: relative;
    background: rgba(var(--c-white), .25);
    &__image {
      position: relative;
      width: 100%;
      padding-bottom: 100%;
      filter: grayscale(100%);
      transition: filter 100ms;
      img {
        position: absolute;
        width: 100%;
      }
    }
    /*
    &__play {
      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      left: 0;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    */
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
  &:hover {
    .visual {
      &__image {
        filter: grayscale(0);
      }
    }
  }
}
</style>
