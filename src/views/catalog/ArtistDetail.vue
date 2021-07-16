<script>
import {
  computed,
  ref,
  onMounted,
  onActivated,
  watch,
} from 'vue';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';

import DetailHeader from '@/components/layout/DetailHeader.vue';
import LazyImage from '@/components/ui/LazyImage.vue';
import PlayIcon from '@/components/catalog/actions/PlayIcon.vue';
import MediaList from '@/components/catalog/media/List.vue';

export default {
  components: {
    DetailHeader,
    LazyImage,
    PlayIcon,
    MediaList,
  },
  props: {
    primaryColor: {
      type: Array,
      default: null,
    },
  },
  setup(props) {
    const store = useStore();
    const route = useRoute();
    const uid = ref(route.params.uid);
    const isLoaded = ref(false);
    const artist = computed(() => store.getters['catalog/artistByUid'](uid.value));
    const objKey = computed(() => `${artist.value.ct}:${artist.value.uid}`);
    const query = computed(() => ({
      filter: {
        obj_key: objKey.value,
      },
      search: [],
      options: {},
    }));
    onMounted(() => {
      console.debug('onMounted');
      // store.dispatch('catalog/loadArtist', uid.value);
    });
    onActivated(() => {
      // console.debug('activated', route.params.uid);
      store.dispatch('catalog/loadArtist', route.params.uid);
      if (props.primaryColor) {
        store.dispatch('ui/setPrimaryColor', props.primaryColor);
      }
    });
    watch(
      () => route.params,
      async (newParams) => {
        uid.value = newParams.uid;
        if (!artist.value && uid.value) {
          await store.dispatch('catalog/loadArtist', uid.value);
        }
      },
    );
    return {
      uid,
      objKey,
      isLoaded,
      artist,
      query,
    };
  },
};
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
            class="visual__image"
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
  //@include container.default;
  margin-bottom: 12rem;
  //background: rgb(var(--c-gray-900));
}
.visual {
  height: 50vh;
  min-height: 240px;
  max-height: 500px;
  &__image {
    height: 100%;
  }
  img {
    border-radius: 50%;
  }
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
/*
.media-list {
  background: rgb(var(--c-white));
}
*/
</style>
