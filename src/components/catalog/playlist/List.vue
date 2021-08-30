<script lang="ts">
import {
  ref,
  onMounted, computed,
} from 'vue';
import { useStore } from 'vuex';

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
    scope: {
      type: String,
      default: null,
    },
    initialFilter: {
      type: Object,
      default: () => null,
    },
  },
  setup(props:any) {
    const store = useStore();
    const isLoaded = ref(false);
    const numResults = ref(0);
    const limit = 16;
    const lastOffset = ref(0);
    const playlists = ref([]);
    const hasNext = ref(false);
    const userFilter = ref({});
    const combinedFilter = computed(() => {
      if (props.scope === 'collection') {
        return {
          ...props.initialFilter,
          ...userFilter.value,
          user_rating: 1,
        };
      }
      return {
        ...props.initialFilter,
        ...userFilter.value,
      };
    });
    // eslint-disable-next-line @typescript-eslint/no-shadow
    const fetchMedia = async (limit = 16, offset = 0) => {
      const { count, next, results } = await getWTFPlaylists(limit, offset, combinedFilter.value);
      hasNext.value = !!next;
      numResults.value = count;
      // @ts-ignore
      playlists.value.push(...results);
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
  <div
    class="playlist-list"
  >
    <div
      class="grid"
    >
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
@use "@/style/abstracts/responsive";
@use "@/style/elements/container";
.playlist-list {
  @include container.default;
  margin-bottom: 8rem;
}
.grid {
  display: grid;
  grid-gap: 2rem;
  grid-template-columns: repeat(4, 1fr);
  @include responsive.bp-small {
    grid-gap: 1rem;
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
