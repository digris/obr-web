<script lang="ts">
import {
  computed,
  defineComponent,
  ref,
  onActivated,
} from 'vue';
import { useStore } from 'vuex';

import DetailHeader from '@/components/layout/DetailHeader.vue';
import LazyImage from '@/components/ui/LazyImage.vue';
import PlayIcon from '@/components/catalog/actions/PlayIcon.vue';
import MediaList from '@/components/catalog/media/List.vue';

export default defineComponent({
  components: {
    DetailHeader,
    LazyImage,
    PlayIcon,
    MediaList,
  },
  props: {
    uid: {
      type: String,
      required: true,
    },
    primaryColor: {
      type: Array,
      default: null,
    },
  },
  setup(props) {
    const store = useStore();
    const isLoaded = ref(false);
    const artist = computed(() => store.getters['catalog/artistByUid'](props.uid));
    const objKey = computed(() => `${artist.value.ct}:${artist.value.uid}`);
    const query = computed(() => ({
      filter: {
        obj_key: objKey.value,
      },
      search: [],
      options: {},
    }));
    onActivated(() => {
      if (!artist.value) {
        store.dispatch('catalog/loadArtist', props.uid);
      }
      if (props.primaryColor) {
        store.dispatch('ui/setPrimaryColor', props.primaryColor);
      }
    });
    return {
      objKey,
      isLoaded,
      artist,
      query,
    };
  },
});
</script>

<template>
  <div
    v-if="artist"
    class="artist-detail"
  >
    <DetailHeader
      scope="artist"
      :title="artist.name"
    >
      <template #visual>
        <div
          class="visual"
        >
          <div
            class="image"
          >
            <LazyImage
              :image="artist.image"
            />
          </div>
          <PlayIcon
            class="visual__play"
            :obj-key="objKey"
          />
        </div>
      </template>
      <template #info-panel>
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
          v-if="artist"
        >{{ artist.numMedia }} Tracks</span>
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
.artist-detail {
  margin-bottom: 12rem;
}
.header {
  .body {
    display: flex;
    flex-direction: column;
    padding-top: 1rem;
    .title {
      margin-top: 2rem;
    }
    .tags,
    .summary {
      margin-top: 1rem;
    }
    .summary {
      display: flex;
      flex-grow: 1;
      align-items: flex-end;
    }
  }
  .actions {
    display: flex;
    align-items: flex-end;
    justify-content: flex-end;
  }
}
</style>
