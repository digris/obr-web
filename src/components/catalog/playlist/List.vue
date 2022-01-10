<script lang="ts">
import {
  ref,
  onMounted, computed, watch,
} from 'vue';
import { useStore } from 'vuex';
import { useRoute, useRouter } from 'vue-router';

import LoadingMore from '@/components/ui/loading/Loading.vue';
import ListFilter from '@/components/filter/ListFilter.vue';
import PlaylistCard from '@/components/catalog/playlist/Card.vue';
import PlaylistRow from '@/components/catalog/playlist/Row.vue';
import { getPlaylists, getPlaylistsTags } from '@/api/catalog';

export default {
  components: {
    ListFilter,
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
    query: {
      type: Object,
      default: () => {},
    },
    initialFilter: {
      type: Object,
      default: () => null,
    },
    disableUserFilter: {
      type: Boolean,
      default: false,
    },
    layout: {
      type: String,
      default: 'grid',
    },
  },
  setup(props:any) {
    const store = useStore();
    const route = useRoute();
    const router = useRouter();
    const numResults = ref(0);
    const limit = 16;
    const lastOffset = ref(0);
    const playlists = ref([]);
    const tagList = ref([]);
    const tagListLoading = ref(false);
    const hasNext = ref(false);
    const userFilter = computed(() => {
      return props.query;
    });
    const combinedFilter = computed(() => {
      // @ts-ignore
      const tags = [...props.initialFilter?.tags ?? [], ...userFilter.value?.tags ?? []];
      const merged = { ...props.initialFilter, ...userFilter.value };
      // @ts-ignore
      merged.tags = tags;
      if (props.scope === 'collection') {
        // @ts-ignore
        merged.user_rating = 1;
      }
      return merged;
    });
    const playlistComponent = computed(() => {
      return (props.layout === 'grid') ? PlaylistCard : PlaylistRow;
    });
    /*
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
    */
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
    const fetchTags = async () => {
      tagListLoading.value = true;
      tagList.value = await getPlaylistsTags(combinedFilter.value);
      tagListLoading.value = false;
    };
    const showSearchBar = computed(() => {
      return !props.disableUserFilter;
    });
    const showUserFilter = computed(() => {
      if (props.disableUserFilter) {
        return false;
      }
      return store.getters['ui/filterExpanded'];
    });
    const updateUserFilter = (filter: any) => {
      const query = filter;
      const routeName = route.name || 'discoverPlaylists';
      router.push({ name: routeName, query });
    };
    onMounted(() => {
      fetchPlaylists();
      fetchTags().then(() => {});
    });
    watch(
      () => combinedFilter.value,
      async () => {
        lastOffset.value = 0;
        playlists.value = [];
        fetchPlaylists(limit, 0).then(() => {});
        fetchTags().then(() => {});
      },
    );
    return {
      combinedFilter,
      tagList,
      tagListLoading,
      playlists,
      playlistComponent,
      hasNext,
      numResults,
      fetchNextPage,
      showSearchBar,
      showUserFilter,
      userFilter,
      updateUserFilter,
    };
  },
};
</script>

<template>
  <div
    v-if="showUserFilter"
    class="list-filter-container"
  >
    <ListFilter
      :filter="userFilter"
      :tag-list="tagList"
      :is-loading="tagListLoading"
      @change="updateUserFilter"
    />
  </div>
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
      class="loading-more-container"
      v-if="hasNext"
      :has-next="hasNext"
      @on-enter="fetchNextPage"
    />
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/abstracts/responsive";
@use "@/style/elements/container";
.list-filter-container {
  @include container.default;
  margin-bottom: 1rem;
}

.loading-more-container {
  @include container.default;
}

@mixin grid {
  display: grid;
  grid-row-gap: 2rem;
  grid-column-gap: 0.5rem;
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
