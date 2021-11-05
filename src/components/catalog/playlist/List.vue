<script lang="ts">
import {
  ref,
  onMounted, computed,
} from 'vue';
import { useStore } from 'vuex';

import LoadingMore from '@/components/ui/LoadingMore.vue';
import PlaylistCard from '@/components/catalog/playlist/Card.vue';
import PlaylistRow from '@/components/catalog/playlist/Row.vue';
import { getPlaylists } from '@/api/catalog';

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
    layout: {
      type: String,
      default: 'grid',
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
    const playlistComponent = computed(() => {
      return (props.layout === 'grid') ? PlaylistCard : PlaylistRow;
    });
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
    const fetchPlaylists = async (limit = 16, offset = 0) => {
      // NOTE: depending on the layout we need different data / expands
      const expand = (props.layout === 'grid') ? [] : ['tags', 'editor'];
      const {
        count,
        next,
        results,
      } = await getPlaylists(limit, offset, combinedFilter.value, expand);
      hasNext.value = !!next;
      numResults.value = count;
      // @ts-ignore
      playlists.value.push(...results);
      // TODO: this kind of smells...
      await store.dispatch('rating/updateObjectRatings', results);
    };
    const fetchNextPage = async () => {
      const offset = lastOffset.value + limit;
      await fetchPlaylists(limit, offset);
      lastOffset.value = offset;
    };
    onMounted(() => {
      fetchPlaylists();
    });
    return {
      isLoaded,
      playlists,
      playlistComponent,
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
      class="list-container"
      :class="`layout--${layout}`"
    >
      <component
        v-for="playlist in playlists"
        :key="playlist.uid"
        :playlist="playlist"
        :is="playlistComponent"
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

@mixin grid {
  display: grid;
  grid-gap: 2rem;
  grid-template-columns: repeat(4, 1fr);
  @include responsive.bp-small {
    grid-gap: 1rem;
    grid-template-columns: repeat(2, 1fr);
  }
}

@mixin table {
  // background: red;
}

.playlist-list {
  // @include container.default;
  .list-container {
    &.layout--grid {
      @include container.default;
      @include grid;
    }
    &.layout--table {
      @include table;
    }
  }
}
</style>
