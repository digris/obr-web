<script lang="ts">
import {
  computed,
  ref,
  onActivated,
  defineComponent,
} from 'vue';
import { useStore } from 'vuex';

import DetailHeader from '@/components/layout/DetailHeader.vue';
import LazyImage from '@/components/ui/LazyImage.vue';
import PlayAction from '@/components/catalog/actions/PlayAction.vue';
import MediaList from '@/components/catalog/media/List.vue';

export default defineComponent({
  components: {
    DetailHeader,
    LazyImage,
    PlayAction,
    MediaList,
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
      return playlist.value.mediaSet.reduce((a: any, b: any) => a.concat({ ...b.media, ...b }), []);
    });
    const query = computed(() => ({
      filter: {
        obj_key: objKey.value,
      },
      search: [],
      options: {},
    }));
    onActivated(() => {
      if (!playlist.value) {
        store.dispatch('catalog/loadPlaylist', props.uid);
      }
    });
    return {
      objKey,
      isLoaded,
      playlist,
      mediaList,
      query,
    };
  },
});
</script>

<template>
  <div
    v-if="playlist"
    class="playlist-detail"
  >
    <DetailHeader
      :obj-key="objKey"
      :enable-rating="(true)"
      title-scope="Show"
      :title="playlist.name"
    >
      <template
        #visual
      >
        <div
          class="visual"
        >
          <div
            class="image"
          >
            <LazyImage
              :image="playlist.image"
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
      </template>
      <template
        #info-panel
      >
        <div
          class="tags"
        >
          <span
            class="tag"
          >#Electronic</span>
          <span
            class="tag"
          >#Rock</span>
          <span
            class="tag"
          >#Techno</span>
        </div>
      </template>
      <template
        #meta-panel
      >
        <span>1h 25m</span>
      </template>
    </DetailHeader>
    <section
      class="section section--light"
    >
      <div
        class="media-list"
      >
        <MediaList
          :initial-filter="query.filter"
          :disable-user-filter="(true)"
          :disable-play-all="(true)"
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
.media-list {
  background: rgb(var(--c-white));
}
</style>
