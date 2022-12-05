<script lang="ts">
import { computed, defineComponent, onActivated, onBeforeUpdate } from "vue";
import { useI18n } from "vue-i18n";
import { useTitle } from "@vueuse/core";

import PlayAction from "@/components/catalog/actions/PlayAction.vue";
import PlayAllAction from "@/components/catalog/actions/PlayAllAction.vue";
import MediaList from "@/components/catalog/media/List.vue";
import ObjectIdentifiers from "@/components/identifier/ObjectIdentifiers.vue";
import ObjectTags from "@/components/tagging/ObjectTags.vue";
import LazyImage from "@/components/ui/LazyImage.vue";
import Duration from "@/components/ui/time/Duration.vue";
import DetailHeader from "@/layouts/DetailHeader.vue";
import DetailPage from "@/layouts/DetailPage.vue";
import { useCatalogStore } from "@/stores/catalog";

export default defineComponent({
  components: {
    DetailPage,
    DetailHeader,
    LazyImage,
    PlayAllAction,
    Duration,
    PlayAction,
    ObjectTags,
    ObjectIdentifiers,
    MediaList,
  },
  props: {
    uid: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const { t } = useI18n();
    const { artistByUid, loadArtist } = useCatalogStore();
    const artist = computed(() => artistByUid(props.uid));
    const objKey = computed(() => `catalog.artist:${props.uid}`);
    const query = computed(() => ({
      filter: {
        obj_key: objKey.value,
      },
      search: [],
      options: {},
    }));
    const title = computed(() => {
      return artist.value?.name;
    });
    useTitle(title);
    // this is kind of bad. don't know yet how to improve...
    // onActivated is called when component is already in keep-alive router,
    // onBeforeUpdate is needed to switch between different objects in the already active component.
    // it also needs some ugly bits in the store (see catalog/loadArtist):
    // when the component is in keep-alive, and routing to here from another place both
    // onActivated and onBeforeUpdate will fire ;(
    onActivated(() => loadArtist(props.uid));
    onBeforeUpdate(() => loadArtist(props.uid));
    return {
      t,
      objKey,
      artist,
      query,
    };
  },
});
</script>

<template>
  <DetailPage>
    <template #header>
      <DetailHeader v-if="artist" :obj="artist" title-scope="Künstler*in" :title="artist.name">
        <template #visual>
          <LazyImage class="image" :image="artist.image">
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
          <ObjectTags class="tags" :obj="artist" :limit="4" />
          <div v-if="artist.countryCode">
            <span v-text="artist.countryCode" />
            <span v-if="artist.dateStart"> ({{ artist.dateStart.substr(0, 4) }}) </span>
          </div>
          <ObjectIdentifiers class="identifiers" :obj="artist" :limit="4" />
        </template>
        <template #meta-panel>
          <PlayAllAction v-if="artist && artist.numMedia > 1" :obj-key="objKey">
            <span v-text="t('catalog.list.playAllTracks', artist.numMedia)" />
            &nbsp; (<Duration :seconds="artist.mediaTotalDuration" />)
          </PlayAllAction>
        </template>
      </DetailHeader>
      <MediaList v-if="artist" :initial-filter="query.filter" :disable-user-filter="true" />
    </template>
  </DetailPage>
</template>

<style lang="scss" scoped>
.tags,
.identifiers {
  margin: 0.5rem 0;
}
</style>
