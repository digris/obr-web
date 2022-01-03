<script lang="ts">
import {
  computed,
  ref,
  onActivated,
  defineComponent,
} from 'vue';
import { useStore } from 'vuex';

import { playlistTitle } from '@/utils/catalog';

import DetailPage from '@/layouts/DetailPage.vue';
// eslint-disable-next-line import/no-unresolved
import DetailHeader from '@/layouts/DetailHeader.vue';
import LazyImage from '@/components/ui/LazyImage.vue';
import Duration from '@/components/ui/time/Duration.vue';
import PlayAction from '@/components/catalog/actions/PlayAction.vue';
import ObjectTags from '@/components/tagging/ObjectTags.vue';
import MediaList from '@/components/catalog/media/List.vue';
import EditorInline from '@/components/broadcast/editor/Inline.vue';
// import PlaylistName from '@/components/catalog/playlist/Name.vue';

export default defineComponent({
  components: {
    DetailPage,
    DetailHeader,
    LazyImage,
    Duration,
    PlayAction,
    ObjectTags,
    MediaList,
    EditorInline,
    // PlaylistName,
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
    const title = computed(() => playlistTitle(playlist.value));
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
      title,
      mediaList,
      query,
    };
  },
});
</script>

<template>
  <DetailPage>
    <template
      #header
    >
      <DetailHeader
        :obj-key="objKey"
        :enable-rating="(true)"
        title-scope="Show"
        :title="title"
      >
        <template
          #visual
        >
          <LazyImage
            class="image"
            :image="playlist.image"
          >
            <PlayAction
              :obj-key="objKey"
              :size="(64)"
              :outlined="(false)"
              background-color="rgb(var(--c-white))"
            />
          </LazyImage>
        </template>
        <template
          #info-panel
        >
          <ObjectTags
            class="tags"
            :obj="playlist"
            :limit="(4)"
          />
          <EditorInline
            v-if="(playlist && playlist.editor)"
            :editor="playlist.editor"
          />
        </template>
        <template
          #meta-panel
        >
          <span
            v-if="(playlist && playlist.numMedia)"
          >
            {{ playlist.numMedia }} Tracks
          </span>
          <span>
            •
          </span>
          <Duration
            v-if="(playlist && playlist.duration)"
            :seconds="playlist.duration"
          />
        </template>
      </DetailHeader>
      <pre
        class="debug"
        v-text="playlist.latestEmission"
      />
    </template>
    <MediaList
      :initial-filter="query.filter"
      :disable-user-filter="(true)"
      :disable-play-all="(true)"
      :hide-upcoming="true"
    />
  </DetailPage>
</template>

<style lang="scss" scoped>
.tags,
.identifiers {
  margin: .5rem 0;
}
</style>
