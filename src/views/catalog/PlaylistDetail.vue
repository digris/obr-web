<script>
import {
  computed,
  ref,
  onActivated,
} from 'vue';
import { useStore } from 'vuex';

import DetailHeader from '@/components/layout/DetailHeader.vue';
import LazyImage from '@/components/ui/LazyImage.vue';
import PlayIcon from '@/components/catalog/actions/PlayIcon.vue';
import MediaRow from '@/components/catalog/media/Row.vue';

export default {
  components: {
    DetailHeader,
    LazyImage,
    PlayIcon,
    MediaRow,
  },
  props: {
    uid: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const store = useStore();
    const isLoaded = ref(false);
    const playlist = computed(() => store.getters['catalog/playlistByUid'](props.uid));
    const objKey = computed(() => `${playlist.value.ct}:${playlist.value.uid}`);
    const mediaList = computed(() => {
      return playlist.value.mediaSet.reduce((a, b) => a.concat({ ...b.media, ...b }), []);
    });
    onActivated(() => {
      if (!playlist.value) {
        store.dispatch('catalog/loadPlaylist', props.uid);
      }
    });
    const query = {
      filter: {
        playlist: '39E730FC',
      },
      search: [],
      options: {},
    };
    return {
      objKey,
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
    <DetailHeader
      scope="playlist"
      :title="playlist.name"
    >
      <template #visual>
        <div
          class="visual"
        >
          <div
            class="image"
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
      </template>
      <template #info-panel>
        <div
          class="tags"
        >
          <span class="tag">#Electronic</span>
          <span class="tag">#Rock</span>
          <span class="tag">#Techno</span>
        </div>
      </template>
      <template #meta-panel>
        <span>1h 25m</span>
      </template>
    </DetailHeader>
    <section
      class="section section--light"
    >
      <div
        class="media-list"
      >
        <MediaRow
          v-for="(media, index) in mediaList"
          :key="`media-row-${index}-${media.uid}-${media.position}`"
          :media="media"
        />
      </div>
    </section>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";
.section {
  @include container.section;
}
.playlist-detail {
  margin-bottom: 12rem;
}
.header {
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
.media-list {
  background: rgb(var(--c-white));
}
</style>
