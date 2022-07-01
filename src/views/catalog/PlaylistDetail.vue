<script lang="ts">
import { computed, ref, onActivated, defineComponent } from "vue";
import { useI18n } from "vue-i18n";
import { useStore } from "vuex";

import { playlistTitle } from "@/utils/catalog";

import DetailPage from "@/layouts/DetailPage.vue";
import DetailHeader from "@/layouts/DetailHeader.vue";
import LazyImage from "@/components/ui/LazyImage.vue";
import PlayAllSmall from "@/components/catalog/media/PlayAllSmall.vue";
import Duration from "@/components/ui/time/Duration.vue";
import PlayAction from "@/components/catalog/actions/PlayAction.vue";
import ObjectTags from "@/components/tagging/ObjectTags.vue";
import MediaList from "@/components/catalog/media/List.vue";
import EditorInline from "@/components/broadcast/editor/Inline.vue";
import Visual from "@/components/catalog/playlist/Visual.vue";
// import AudioMeter from "@/components/ui/audio/AudioMeter.vue";
// import AudioSpectrum from "@/components/ui/audio/AudioSpectrum.vue";

export default defineComponent({
  components: {
    DetailPage,
    DetailHeader,
    LazyImage,
    PlayAllSmall,
    Duration,
    PlayAction,
    ObjectTags,
    MediaList,
    EditorInline,
    Visual,
    // AudioMeter,
    // AudioSpectrum,
  },
  props: {
    uid: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const { t } = useI18n();
    const store = useStore();
    const isLoaded = ref(false);
    const playlist = computed(() => store.getters["catalog/playlistByUid"](props.uid));
    const title = computed(() => playlistTitle(playlist.value));
    const objKey = computed(() => `${playlist.value?.ct}:${playlist.value?.uid}`);
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
        store.dispatch("catalog/loadPlaylist", props.uid);
      }
    });
    return {
      t,
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
    <!---->
    <template #background="slotProps">
      <Visual :height="slotProps.height" :width="slotProps.width" />
    </template>
    <template #header>
      <DetailHeader v-if="playlist" :obj="playlist" :title="title" title-scope="Show">
        <template #visual>
          <LazyImage class="image" :image="playlist.image">
            <PlayAction
              :obj-key="objKey"
              :size="96"
              :outlined="false"
              :shadowed="true"
              background-color="rgb(var(--c-white))"
            />
          </LazyImage>
        </template>
        <template #info-panel>
          <ObjectTags class="tags" :obj="playlist" :limit="4" />
          <EditorInline v-if="playlist && playlist.editor" :editor="playlist.editor" />
        </template>
        <template #meta-panel>
          <PlayAllSmall v-if="playlist && playlist.numMedia" :obj-key="objKey">
            <span v-text="t('catalog.list.playAllTracks', playlist.numMedia)" />
            &nbsp; (<Duration :seconds="playlist.duration" :round-seconds="60 * 5" />)
          </PlayAllSmall>
        </template>
      </DetailHeader>
    </template>
    <!--
    <div>
      <div
        :style="{
          // width: '80px',
          // height: '80px',
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
        }"
      >
        <AudioSpectrum />
        <span>&nbsp;</span>
        <AudioSpectrum
          :width="32"
          :height="32"
        />
      </div>
    </div>
    -->
    <MediaList
      v-if="playlist"
      :initial-filter="query.filter"
      :disable-user-filter="true"
      :disable-play-all="true"
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
