<script lang="ts">
import { computed, defineComponent, onActivated } from "vue";
import { useI18n } from "vue-i18n";

import Spectrogram from "@/components/audio/Spectrogram.vue";
import EditorInline from "@/components/broadcast/editor/Inline.vue";
import PlayAction from "@/components/catalog/actions/PlayAction.vue";
import PlayAllAction from "@/components/catalog/actions/PlayAllAction.vue";
import MediaList from "@/components/catalog/media/List.vue";
import ObjectTags from "@/components/tagging/ObjectTags.vue";
import LazyImage from "@/components/ui/LazyImage.vue";
import Duration from "@/components/ui/time/Duration.vue";
import { usePageTitle } from "@/composables/title";
import DetailHeader from "@/layouts/DetailHeader.vue";
import DetailHeaderLoading from "@/layouts/DetailHeaderLoading.vue";
import DetailPage from "@/layouts/DetailPage.vue";
import { useCatalogStore } from "@/stores/catalog";
import { playlistTitle } from "@/utils/catalog";

export default defineComponent({
  components: {
    DetailPage,
    DetailHeader,
    DetailHeaderLoading,
    LazyImage,
    PlayAllAction,
    Duration,
    PlayAction,
    ObjectTags,
    MediaList,
    EditorInline,
    Spectrogram,
  },
  props: {
    uid: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const { t } = useI18n();
    const { playlistByUid, loadPlaylist } = useCatalogStore();
    const playlist = computed(() => playlistByUid(props.uid));
    const objKey = computed(() => `catalog.playlist:${props.uid}`);
    const title = computed(() => playlistTitle(playlist.value));
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
    usePageTitle(computed(() => playlist.value?.name));
    onActivated(() => loadPlaylist(props.uid));
    return {
      t,
      objKey,
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
    <template #background="slotProps">
      <Spectrogram
        :height="slotProps.height / 3"
        :width="slotProps.width"
        color="rgb(0 0 0 / 10%)"
      />
    </template>
    <template #header>
      <DetailHeader v-if="playlist" :obj="playlist" :title="title" title-scope="Show">
        <template #visual>
          <LazyImage class="image" :image="playlist.image">
            <PlayAction
              :obj-key="objKey"
              :icon-scale="2"
              :outlined="true"
              :filled="true"
              :color="[0, 0, 0]"
            />
          </LazyImage>
        </template>
        <template #info-panel>
          <ObjectTags class="tags" :obj="playlist" :limit="4" />
          <EditorInline v-if="playlist && playlist.editor" :editor="playlist.editor" />
        </template>
        <template #meta-panel>
          <PlayAllAction v-if="playlist && playlist.numMedia" :obj-key="objKey">
            <span v-text="t('catalog.list.playAllTracks', playlist.numMedia)" />
            &nbsp; (<Duration :seconds="playlist.duration" :round-seconds="60 * 5" />)
          </PlayAllAction>
        </template>
      </DetailHeader>
      <DetailHeaderLoading v-else title-scope="Show" />
    </template>
    <MediaList
      v-if="objKey"
      :initial-filter="query.filter"
      :disable-user-filter="true"
      :hide-upcoming="true"
    />
  </DetailPage>
</template>

<style lang="scss" scoped>
.tags,
.identifiers {
  margin: 0.5rem 0;
}
</style>
