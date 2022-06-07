<script lang="ts">
import { computed, defineComponent, ref, watchEffect, onActivated, onBeforeUpdate } from "vue";
import { useI18n } from "vue-i18n";
import { useStore } from "vuex";
import { setPageTitle } from "@/utils/page";

import DetailPage from "@/layouts/DetailPage.vue";
import DetailHeader from "@/layouts/DetailHeader.vue";
import LazyImage from "@/components/ui/LazyImage.vue";
import PlayAllSmall from "@/components/catalog/media/PlayAllSmall.vue";
import Duration from "@/components/ui/time/Duration.vue";
import PlayAction from "@/components/catalog/actions/PlayAction.vue";
import ObjectTags from "@/components/tagging/ObjectTags.vue";
import ObjectIdentifiers from "@/components/identifier/ObjectIdentifiers.vue";
import MediaList from "@/components/catalog/media/List.vue";

export default defineComponent({
  components: {
    DetailPage,
    DetailHeader,
    LazyImage,
    PlayAllSmall,
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
    const store = useStore();
    const isLoaded = ref(false);
    const artist = computed(() => store.getters["catalog/artistByUid"](props.uid));
    const objKey = computed(() => `${artist.value.ct}:${artist.value.uid}`);
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
    // this is kind of bad. don't know yet how to improve...
    // onActivated is called when component is already in keep-alive router,
    // onBefore is needed to switch between different objects in the already active component.
    // it also needs some ugly bits in the store (see catalog/loadArtist):
    // when the component is in keep-alive, and routing to here from another place both
    // onActivated and onBeforeUpdate will fire ;(
    onActivated(() => {
      if (!artist.value) {
        store.dispatch("catalog/loadArtist", props.uid);
      } else {
        setPageTitle(title.value);
      }
    });
    onBeforeUpdate(() => {
      if (!artist.value) {
        store.dispatch("catalog/loadArtist", props.uid);
      }
    });
    watchEffect(() => {
      setPageTitle(title.value);
    });
    return {
      t,
      objKey,
      isLoaded,
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
              :size="96"
              :outlined="false"
              :shadowed="true"
              background-color="rgb(var(--c-white))"
              hover-background-color="rgb(var(--c-gray-200))"
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
          <PlayAllSmall :obj-key="objKey">
            <span
              v-if="artist && artist.numMedia"
              v-text="t('catalog.ct.numMedia', artist.numMedia)"
            />
            <span>&nbsp;•&nbsp;</span>
            <Duration
              v-if="artist && artist.mediaTotalDuration"
              :seconds="artist.mediaTotalDuration"
            />
          </PlayAllSmall>
        </template>
      </DetailHeader>
      <MediaList
        v-if="artist"
        :initial-filter="query.filter"
        :disable-user-filter="true"
        :disable-play-all="true"
      />
    </template>
  </DetailPage>
</template>

<style lang="scss" scoped>
.tags,
.identifiers {
  margin: 0.5rem 0;
}
</style>
