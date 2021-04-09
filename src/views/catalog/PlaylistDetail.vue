<script>
import {
  computed, ref, onMounted, watch,
} from 'vue';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';

import { getImageSrc } from '@/utils/image';
import LazyImage from '@/components/UI/LazyImage.vue';
import MediaList from '@/components/catalog/media/List.vue';
import CircleButton from '@/components/UI/button/CircleButton.vue';
import IconPlay from '@/components/UI/icon/IconPlay.vue';

export default {
  components: {
    LazyImage,
    MediaList,
    CircleButton,
    IconPlay,
  },
  setup() {
    const store = useStore();
    const route = useRoute();
    const uid = ref(route.params.uid);
    const isLoaded = ref(false);
    const playlists = computed(() => store.getters['catalog/playlistByUid'](uid.value));
    const mediaList = ref([]);
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
    const dummyQuery = {
      filter: [],
      search: [],
      options: {},
    };
    return {
      uid,
      isLoaded,
      playlists,
      mediaList,
      dummyQuery,
    };
  },
  computed: {
    imageSrc() {
      return getImageSrc(this.playlists, 480);
    },
  },
};
</script>

<template>
  <div
    v-if="playlists"
    class="playlists-detail"
  >
    <div
      class="header detail-header"
    >
      <div
        class="visual"
      >
        <LazyImage
          :src="imageSrc"
        />
      </div>
      <div
        class="body"
      >
        <div
          class="kind"
        >
          Playlist
          <CircleButton>
            <IconPlay
              :size="24"
            />
          </CircleButton>
        </div>
        <div
          class="title"
        >
          <h1>{{ playlists.name }}</h1>
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
          <span>125 Tracks</span>
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
      <MediaList />
    </div>
  </div>
</template>

<style lang="scss" scoped>
/* stylelint-disable-next-line at-rule-no-unknown */
@use "@/style/elements/container";
/* stylelint-disable-next-line at-rule-no-unknown */
@use "@/style/elements/detail-header";
.playlists-detail {
  @include container.default;
  margin-bottom: 12rem;
}
.detail-header {
  @include detail-header.default;
  display: grid;
  //grid-template-columns: 220px 1fr auto;
  grid-template-columns: 2fr 4fr 2fr;
  grid-gap: 2rem;
}
.header {
  .visual {
    img {
      background: rgba(255, 255, 255, 0.1);
      min-width: 100%;
      max-width: 100%;
      border-radius: 50%;
    }
  }
  .body {
    padding-top: 1rem;
    display: flex;
    flex-direction: column;
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
    justify-content: flex-end;
    align-items: flex-end;
  }
}
</style>
