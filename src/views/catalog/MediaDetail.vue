<script lang="ts">
import { computed, defineComponent, onActivated } from "vue";
import { useStore } from "vuex";

import DetailPage from "@/layouts/DetailPage.vue";
import DetailHeader from "@/layouts/DetailHeader.vue";
import LazyImage from "@/components/ui/LazyImage.vue";
import Duration from "@/components/ui/time/Duration.vue";
import PlayAction from "@/components/catalog/actions/PlayAction.vue";
import ObjectTags from "@/components/tagging/ObjectTags.vue";
import MediaArtists from "@/components/catalog/media/MediaArtists.vue";
import MediaReleases from "@/components/catalog/media/MediaReleases.vue";
import PlaylistList from "@/components/catalog/playlist/List.vue";

export default defineComponent({
  components: {
    DetailPage,
    DetailHeader,
    LazyImage,
    Duration,
    PlayAction,
    ObjectTags,
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
    const store = useStore();
    const media = computed(() => store.getters["catalog/mediaByUid"](props.uid));
    const objKey = computed(() => {
      return media.value ? `${media.value.ct}:${media.value.uid}` : null;
    });
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
    onActivated(() => {
      if (!media.value) {
        store.dispatch("catalog/loadMedia", props.uid);
      }
    });
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
      <DetailHeader :obj="media" title-scope="Track" :title="media.name">
        <template #visual>
          <LazyImage class="image" :image="image">
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
          <div class="artists">
            <MediaArtists :artists="media.artists" />
          </div>
          <div class="releases">
            <MediaReleases :releases="media.releases" />
          </div>
          <ObjectTags class="tags" :obj="media" :limit="4" />
        </template>
        <template #meta-panel>
          <!--
          <span
            v-if="media"
          >
            {{ media.numAirplays }} Airplays
          </span>
          <span>
            •
          </span>
          -->
          <Duration :seconds="media.duration" />
        </template>
      </DetailHeader>
    </template>
    <PlaylistList
      :initial-filter="query.filter"
      :disable-user-filter="true"
      :disable-play-all="true"
      layout="table"
    />
  </DetailPage>
</template>

<style lang="scss" scoped>
.tags,
.identifiers {
  margin: 0.5rem 0;
}
</style>
