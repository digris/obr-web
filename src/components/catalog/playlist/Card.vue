<script>
import { computed } from 'vue';
import { DateTime } from 'luxon';

import LazyImage from '@/components/ui/LazyImage.vue';
import PlayIcon from '@/components/catalog/actions/PlayIcon.vue';

export default {
  components: {
    LazyImage,
    PlayIcon,
  },
  props: {
    playlist: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const objKey = computed(() => `${props.playlist.ct}:${props.playlist.uid}`);
    const link = `/discover/playlists/${props.playlist.uid}/`;
    const latestEmission = computed(() => {
      const dt = DateTime.fromISO(props.playlist.latestEmission);
      return dt.toFormat('HH:mm yyyy-LL-dd');
    });
    return {
      objKey,
      link,
      latestEmission,
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
          :image="playlist.image"
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
          {{ playlist.name }}
        </router-link>
      </div>
      <div
        class="subtitle"
      >
        <small>{{ latestEmission }}</small>
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
