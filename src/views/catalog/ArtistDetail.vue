<script>
import {
  computed,
  ref,
  onMounted,
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
      store.dispatch('catalog/loadArtist', uid.value);
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
  img {
    border-radius: 50%;
  }
}
.visual__ {
  position: relative;
  &__image {
    position: relative;
    width: 100%;
    padding-bottom: 100%;
    filter: grayscale(100%);
    transition: filter 100ms;
    img {
      position: absolute;
      width: 100%;
      background: rgba(var(--c-white), .25);
      border-radius: 50%;
    }
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
.media-list {
  background: rgb(var(--c-white));
}
</style>
