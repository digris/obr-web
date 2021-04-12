<script>
import { ref, onMounted } from 'vue';

import LoadingMore from '@/components/UI/LoadingMore.vue';
import MediaRow from '@/components/catalog/media/Row.vue';
import { getMedia } from '@/api/catalog';

export default {
  components: {
    LoadingMore,
    MediaRow,
  },
  props: {
    filter: {
      type: Object,
      default: () => {},
    },
  },
  setup(props) {
    // const store = useStore();
    const isLoaded = ref(false);
    const numResults = ref(0);
    const limit = 16;
    const lastOffset = ref(0);
    const mediaList = ref([]);
    const hasNext = ref(false);
    // eslint-disable-next-line no-shadow
    const fetchMedia = async (limit = 16, offset = 0) => {
      const { count, next, results } = await getMedia(limit, offset, props.filter);
      hasNext.value = !!next;
      numResults.value = count;
      mediaList.value.push(...results);
    };
    const fetchNextPage = async () => {
      const offset = lastOffset.value + limit;
      await fetchMedia(limit, offset);
      lastOffset.value = offset;
    };
    onMounted(() => {
      fetchMedia();
    });
    return {
      isLoaded,
      mediaList,
      hasNext,
      numResults,
      fetchNextPage,
    };
  },
};
</script>

<template>
  <pre
    class="_debug"
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
    <LoadingMore
      v-if="hasNext"
      :has-next="hasNext"
      @on-enter="fetchNextPage"
    />
  </div>
</template>
