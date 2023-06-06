<script lang="ts">
import { computed, defineComponent, onActivated } from "vue";

import PlayAction from "@/components/catalog/actions/PlayAction.vue";
import MediaArtists from "@/components/catalog/media/MediaArtists.vue";
import MediaReleases from "@/components/catalog/media/MediaReleases.vue";
import PlaylistList from "@/components/catalog/playlist/List.vue";
import ObjectIdentifiers from "@/components/identifier/ObjectIdentifiers.vue";
import ObjectTags from "@/components/tagging/ObjectTags.vue";
import LazyImage from "@/components/ui/LazyImage.vue";
import Duration from "@/components/ui/time/Duration.vue";
import DetailHeader from "@/layouts/DetailHeader.vue";
import DetailHeaderLoading from "@/layouts/DetailHeaderLoading.vue";
import DetailPage from "@/layouts/DetailPage.vue";
import { useCatalogStore } from "@/stores/catalog";
import Spectrogram from "@/components/audio/Spectrogram.vue";

export default defineComponent({
  components: {
    Spectrogram,
    DetailPage,
    DetailHeader,
    DetailHeaderLoading,
    LazyImage,
    Duration,
    PlayAction,
    ObjectTags,
    ObjectIdentifiers,
    MediaArtists,
    MediaReleases,
    PlaylistList,
  },
  props: {
    uid: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const { mediaByUid, loadMedia } = useCatalogStore();
    const media = computed(() => mediaByUid(props.uid));
    const objKey = computed(() => `catalog.media:${props.uid}`);
    const query = computed(() => ({
      filter: {
        obj_key: objKey.value,
      },
      search: [],
      options: {},
    }));
    const release = computed(() => {
      if (!(media.value && media.value.releases && media.value.releases.length)) {
        return null;
      }
      return media.value.releases[0];
    });
    const image = computed(() => {
      return release.value && release.value.image ? release.value.image : null;
    });
    onActivated(() => loadMedia(props.uid));
    return {
      media,
      objKey,
      query,
      release,
      image,
    };
  },
});
</script>
<template>
  <DetailPage>
    <template #header>
      <DetailHeader v-if="media" :obj="media" title-scope="Track" :title="media.name">
        <template #visual>
          <LazyImage class="image" :image="image">
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
          <div class="artists">
            <MediaArtists :artists="media.artists" />
          </div>
          <div class="releases">
            <MediaReleases :releases="media.releases" />
          </div>
          <ObjectTags class="tags" :obj="media" :limit="4" />
          <ObjectIdentifiers class="identifiers" :obj="media" :limit="4" />
        </template>
        <template #meta-panel>
          <Duration :seconds="media.duration" />
        </template>
      </DetailHeader>
      <DetailHeaderLoading v-else />
    </template>
    <PlaylistList :initial-filter="query.filter" :disable-user-filter="true" layout="table" />
  </DetailPage>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";

.artists {
  margin-bottom: 1rem;

  :deep(span) {
    @include typo.large;
  }

  :deep(a) {
    @include typo.large;

    text-decoration: underline;
  }
}

.tags,
.identifiers {
  margin: 0.5rem 0;
}
</style>
