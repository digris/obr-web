<script>
import {
  computed, ref, onMounted, watch,
} from 'vue';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';

import { getImageSrc } from '@/utils/image';
import LazyImage from '@/components/UI/LazyImage.vue';
import MediaRow from '@/components/catalog/media/Row.vue';
import CircleButton from '@/components/UI/button/CircleButton.vue';
import IconPlay from '@/components/UI/icon/IconPlay.vue';

export default {
  components: {
    LazyImage,
    MediaRow,
    CircleButton,
    IconPlay,
  },
  setup() {
    const store = useStore();
    const route = useRoute();
    const uid = ref(route.params.uid);
    const isLoaded = ref(false);
    const playlist = computed(() => store.getters['catalog/playlistByUid'](uid.value));
    const mediaList = computed(() => {
      const media = playlist.value.mediaSet.reduce((a, b) => a.concat({ ...b.media, ...b }), []);
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
  computed: {
    imageSrc() {
      return getImageSrc(this.playlist, 480);
    },
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
/* stylelint-disable-next-line at-rule-no-unknown */
@use "@/style/elements/container";
/* stylelint-disable-next-line at-rule-no-unknown */
@use "@/style/elements/detail-header";
.playlist-detail {
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
