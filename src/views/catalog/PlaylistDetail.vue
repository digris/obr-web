<script>
import {
  computed, ref, onMounted, watch,
} from 'vue';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';

import LazyImage from '@/components/ui/LazyImage.vue';
import MediaRow from '@/components/catalog/media/Row.vue';

export default {
  components: {
    LazyImage,
    MediaRow,
  },
  setup() {
    const store = useStore();
    const route = useRoute();
    const uid = ref(route.params.uid);
    const isLoaded = ref(false);
    const playlist = computed(() => store.getters['catalog/playlistByUid'](uid.value));
    const mediaList = computed(() => {
      const media = playlist.value.mediaSet.reduce((a, b) => a.concat({ ...b.media, ...b }), []);
      // const sortedMedia = media.sort((a, b) => b.position - a.position);
      // return sortedMedia;
      return media;
    });
    onMounted(() => {
      store.dispatch('catalog/loadPlaylist', uid.value);
    });
    watch(
      () => route.params,
      async (newParams) => {
        uid.value = newParams.uid;
        if (uid.value) {
          await store.dispatch('catalog/loadPlaylist', uid.value);
        }
      },
    );
    const query = {
      filter: {
        playlist: '39E730FC',
      },
      search: [],
      options: {},
    };
    return {
      uid,
      isLoaded,
      playlist,
      mediaList,
      query,
    };
  },
};
</script>

<template>
  <div
    v-if="playlist"
    class="playlist-detail"
  >
    <div
      class="header detail-header"
    >
      <div
        class="visual"
      >
        <LazyImage
          :image="playlist.image"
        />
      </div>
      <div
        class="body"
      >
        <div
          class="kind"
        >
          Playlist
        </div>
        <div
          class="title"
        >
          <h1>{{ playlist.name }}</h1>
        </div>
        <div
          class="tags"
        >
          <span class="tag">#Electronic</span>
          <span class="tag">#Rock</span>
        </div>
        <div
          class="summary"
        >
          <span>{{ mediaList.length }} Tracks</span>
          <span>1h 25m</span>
        </div>
      </div>
      <div
        class="actions">
        <span>+</span>
        <span>-</span>
      </div>
    </div>
    <div
      class="body"
    >
      <div class="media-list">
        <div class="grid">
          <MediaRow
            v-for="(media, index) in mediaList"
            :key="`media-row-${index}-${media.uid}-${media.position}`"
            :media="media"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";
@use "@/style/elements/detail-header";
.playlist-detail {
  @include container.default;
  margin-bottom: 12rem;
}
.detail-header {
  @include detail-header.default;
  display: grid;
  grid-gap: 2rem;
  //grid-template-columns: 220px 1fr auto;
  grid-template-columns: 2fr 4fr 2fr;
}
.header {
  .visual {
    img {
      min-width: 100%;
      max-width: 100%;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 50%;
    }
  }
  .body {
    display: flex;
    flex-direction: column;
    padding-top: 1rem;
    .title {
      margin-top: 2rem;
    }
    .tags,
    .summary {
      margin-top: 1rem;
    }
    .summary {
      display: flex;
      flex-grow: 1;
      align-items: flex-end;
    }
  }
  .actions {
    display: flex;
    align-items: flex-end;
    justify-content: flex-end;
  }
}
</style>
