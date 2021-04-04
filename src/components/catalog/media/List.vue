<script>
import { ref, onMounted } from 'vue';
import Intersect from '@/components/utils/intersect';
// import { useRoute } from 'vue-router';
// import { useStore } from 'vuex';

import MediaRow from '@/components/catalog/media/Row.vue';
import { getMedia } from '@/graphql/catalog';

export default {
  components: {
    Intersect,
    MediaRow,
  },
  props: {
    filter: {
      type: Array,
      default: () => [],
    },
  },
  setup() {
    // const store = useStore();
    const isLoaded = ref(false);
    // const mediaList = ref([
    //   { name: 'the name 1' },
    //   { name: 'the name 2' },
    // ]);
    const limit = 24;
    const lastOffset = ref(0);
    const mediaList = ref([]);
    const hasNext = ref(false);
    // eslint-disable-next-line no-shadow
    const fetchMedia = async (limit = 8, offset = 0) => {
      const { results } = await getMedia({ limit, offset });
      hasNext.value = true;
      mediaList.value.push(...results);
    };
    const fetchNextPage = async () => {
      const offset = lastOffset.value + limit;
      await fetchMedia(limit, offset);
      lastOffset.value = offset;
    };
    onMounted(() => {
      console.debug('MediaList - mounted');
      fetchMedia();
      // store.dispatch('catalog/loadArtist', uid.value);
    });
    return {
      isLoaded,
      mediaList,
      hasNext,
      fetchNextPage,
    };
  },
};
</script>

<template>
  <pre
    class="debug"
    v-text="filter"
  />
  <div class="media-list">
    <div class="grid">
      <MediaRow
        v-for="(media, index) in mediaList"
        :key="`media-row-${index}`"
        :media="media"
      />
    </div>
    <intersect
      v-if="hasNext"
      @enter="fetchNextPage"
    >
      <span>Load more...</span>
    </Intersect>
  </div>
</template>
