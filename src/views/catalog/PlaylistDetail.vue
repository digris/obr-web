<script lang="ts">
import { computed, onActivated, defineComponent } from "vue";
import { useI18n } from "vue-i18n";
import { useCatalogStore } from "@/stores/catalog";

import { playlistTitle } from "@/utils/catalog";

import DetailPage from "@/layouts/DetailPage.vue";
import DetailHeader from "@/layouts/DetailHeader.vue";
import DetailHeaderLoading from "@/layouts/DetailHeaderLoading.vue";
import LazyImage from "@/components/ui/LazyImage.vue";
import PlayAllAction from "@/components/catalog/actions/PlayAllAction.vue";
import Duration from "@/components/ui/time/Duration.vue";
import PlayAction from "@/components/catalog/actions/PlayAction.vue";
import ObjectTags from "@/components/tagging/ObjectTags.vue";
import MediaList from "@/components/catalog/media/List.vue";
import EditorInline from "@/components/broadcast/editor/Inline.vue";
import Visual from "@/components/catalog/playlist/Visual.vue";

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
    Visual,
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
      <Visual :height="slotProps.height" :width="slotProps.width" />
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
