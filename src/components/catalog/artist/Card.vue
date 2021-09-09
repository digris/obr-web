<script lang="ts">
import {
  computed,
  defineComponent,
} from 'vue';

import LazyImage from '@/components/ui/LazyImage.vue';
import PlayAction from '@/components/catalog/actions/PlayAction.vue';

export default defineComponent({
  components: {
    LazyImage,
    PlayAction,
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
});
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
        >
          <PlayAction
            :obj-key="objKey"
            :size="(64)"
            :outlined="(false)"
            background-color="rgb(var(--c-white))"
          />
        </LazyImage>
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
      </div>
      <div
        class="subtitle"
      >
        {{ artist.numMedia }} Tracks
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
.card {
  .visual {
    position: relative;
    background: rgba(var(--c-white), .25);
    cursor: pointer;
    &__image {
      position: relative;
      width: 100%;
      padding-bottom: 100%;
      //filter: grayscale(100%);
      transition: opacity 200ms;
      .lazy-image {
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
    .subtitle {
      @include typo.dim;
      @include typo.light;
    }
  }
  &:hover {
    .visual {
      background: rgba(var(--c-black), 0.2);
      :deep(img) {
        opacity: 0.5;
      }
      /*
      &__image {
        opacity: 0.5;
      }
      */
    }
  }
}
</style>
