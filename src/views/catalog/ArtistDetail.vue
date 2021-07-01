<script>
import {
  computed,
  ref,
  onMounted,
  watch,
} from 'vue';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';

import LazyImage from '@/components/ui/LazyImage.vue';
import PlayIcon from '@/components/catalog/actions/PlayIcon.vue';
import MediaList from '@/components/catalog/media/List.vue';

export default {
  components: {
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
    <section
      class="section section--dark"
    >
      <div
        class="header detail-header"
      >
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
        <div
          class="body"
        >
          <div
            class="kind"
          >
            Artist {{ uid }}
          </div>
          <div
            class="title"
          >
            <h1>{{ artist.name }}</h1>
          </div>
          <div
            class="tags"
          >
            <span class="tag">#Electronic</span>
            <span class="tag">#Rock</span>
            <router-link
              :to="{
                name: 'artistDetail',
                params: {
                  uid: uid,
                },
                query:{
                  'filter.duration': 'long',
                  'filter.tags': 'techno+hiphop',
                },
                // query: {
                //   filter: JSON.stringify(dummyQuery),
                // },
              }"
            >
              #Techno
            </router-link>
          </div>
          <div
            class="summary"
          >
            <span
              v-if="artist"
            >{{ artist.numMedia }} Tracks</span>
            <span>1h 25m</span>
          </div>
        </div>
        <div
          class="actions">
          <span>+</span>
          <span>-</span>
        </div>
      </div>
    </section>
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
@use "@/style/elements/detail-header";
.section {
  @include container.section;
}
.artist-detail {
  //@include container.default;
  margin-bottom: 12rem;
  //background: rgb(var(--c-gray-900));
}
.detail-header {
  @include detail-header.default;
  @include container.default;
  display: grid;
  grid-gap: 2rem;
  //grid-template-columns: 220px 1fr auto;
  grid-template-columns: 2fr 4fr 2fr;
  padding-top: 2rem;
  padding-bottom: 2rem;
}
.header {
  .visual {
    /*
    img {
      min-width: 100%;
      max-width: 100%;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 50%;
    }
    */
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
