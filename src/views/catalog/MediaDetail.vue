<script lang="ts">
import {
  computed,
  defineComponent,
  onActivated,
} from 'vue';
import { useStore } from 'vuex';

import DetailHeader from '@/components/layout/DetailHeader.vue';
import LazyImage from '@/components/ui/LazyImage.vue';
import PlayIcon from '@/components/catalog/actions/PlayIcon.vue';
import MediaArtists from '@/components/catalog/media/MediaArtists.vue';
import MediaReleases from '@/components/catalog/media/MediaReleases.vue';
import PlaylistList from '@/components/catalog/playlist/List.vue';

export default defineComponent({
  components: {
    DetailHeader,
    LazyImage,
    PlayIcon,
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
    const media = computed(() => store.getters['catalog/mediaByUid'](props.uid));
    const objKey = computed(() => {
      return `${media.value.ct}:${media.value.uid}`;
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
      return (release.value && release.value.image) ? release.value.image : null;
    });
    onActivated(() => {
      if (!media.value) {
        store.dispatch('catalog/loadMedia', props.uid);
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
  <div
    v-if="media"
    class="media-detail"
  >
    <DetailHeader
      scope="media"
      :title="media.name"
    >
      <template #visual>
        <div
          class="visual"
        >
          <div
            class="image"
          >
            <LazyImage
              :image="image"
            />
          </div>
          <PlayIcon
            class="visual__play"
            :obj-key="objKey"
          />
        </div>
      </template>
      <template #info-panel>
        <div class="artists">
          <MediaArtists
            :artists="media.artists"
          />
        </div>
        <div class="releases">
          <MediaReleases
            :releases="media.releases"
          />
        </div>
        <div
          class="tags"
        >
          <span class="tag">#Electronic</span>
          <span class="tag">#Rock</span>
          <span class="tag">#Techno</span>
        </div>
      </template>
      <template #meta-panel>
        <span
          v-if="media"
        >
          {{ media.numAirplays }} Airplays
        </span>
        <span>
          •
        </span>
        <span>{{ media.duration }}s</span>
      </template>
    </DetailHeader>
    <section
      class="section section--light"
    >
      <div
        class="playlist-list"
      >
        <PlaylistList
          :initial-filter="query.filter"
          :disable-user-filter="(true)"
          :disable-play-all="(true)"
        />
      </div>
    </section>
  </div>
</template>
