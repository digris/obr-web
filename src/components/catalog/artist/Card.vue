<script>
import settings from '@/settings';
import LazyImage from '@/components/UI/LazyImage.vue';

const { IMAGE_RESIZER_URL } = settings;

const getImageSrc = (obj) => {
  if (obj.image && obj.image.path) {
    return `${IMAGE_RESIZER_URL}crop/256x256/${obj.image.path}`;
  }
  return `https://picsum.photos/seed/${obj.uid}/200`;
};

export default {
  components: { LazyImage },
  props: {
    artist: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const link = `/discover/artists/${props.artist.uid}/`;
    // const imageSrc = `https://picsum.photos/seed/${props.artist.uid}/200`;
    const imageSrc = getImageSrc(props.artist);
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
          {{ artist.name }}
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
    }
  }
}
</style>
