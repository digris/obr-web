<script>
import { ref, onMounted, watch } from 'vue';
import { useStore } from 'vuex';

import LoadingMore from '@/components/ui/LoadingMore.vue';
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
    const store = useStore();
    const isLoaded = ref(false);
    const numResults = ref(0);
    const limit = 16;
    const lastOffset = ref(0);
    const mediaList = ref([]);
    const hasNext = ref(false);
    // eslint-disable-next-line @typescript-eslint/no-shadow
    const fetchMedia = async (limit = 16, offset = 0) => {
      const { count, next, results } = await getMedia(limit, offset, props.filter);
      hasNext.value = !!next;
      numResults.value = count;
      mediaList.value.push(...results);
      // TODO: this kind of smells...
      await store.dispatch('rating/updateObjectRatings', results);
    };
    const fetchNextPage = async () => {
      const offset = lastOffset.value + limit;
      await fetchMedia(limit, offset);
      lastOffset.value = offset;
    };
    onMounted(() => {
      fetchMedia();
    });
    watch(
      () => props.filter,
      async (nv) => {
        console.debug('filter updated', nv);
        lastOffset.value = 0;
        mediaList.value = [];
        await fetchMedia(limit, 0);
      },
    );
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
