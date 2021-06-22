<script>
import { ref, onMounted } from 'vue';

import LoadingMore from '@/components/ui/LoadingMore.vue';
import PlaylistCard from '@/components/catalog/playlist/Card.vue';
import { getWTFPlaylists } from '@/api/catalog';

export default {
  components: {
    LoadingMore,
    PlaylistCard,
  },
  props: {
    filter: {
      type: Array,
      default: () => [],
    },
  },
  setup() {
    const isLoaded = ref(false);
    const numResults = ref(0);
    const limit = 16;
    const lastOffset = ref(0);
    const playlists = ref([]);
    const hasNext = ref(false);
    // eslint-disable-next-line @typescript-eslint/no-shadow
    const fetchMedia = async (limit = 16, offset = 0) => {
      const { count, next, results } = await getWTFPlaylists(limit, offset);
      hasNext.value = !!next;
      numResults.value = count;
      playlists.value.push(...results);
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
      playlists,
      hasNext,
      numResults,
      fetchNextPage,
    };
  },
};
</script>

<template>
  <div class="playlist-list">
    <div class="grid">
      <PlaylistCard
        v-for="playlist in playlists"
        :key="playlist.uid"
        :playlist="playlist"
      />
    </div>
    <LoadingMore
      v-if="hasNext"
      :has-next="hasNext"
      @on-enter="fetchNextPage"
    />
  </div>
</template>

<style lang="scss" scoped>
.playlist-list {
  margin: 0 0 8rem;
}
.grid {
  display: grid;
  grid-gap: 2rem;
  grid-template-columns: repeat(4, 1fr);
}
</style>
