<script lang="ts">
import { computed, defineComponent, onMounted, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { storeToRefs } from "pinia";
import { isEqual } from "lodash-es";

import { getPlaylists, getPlaylistsTags } from "@/api/catalog";
import PlaylistCard from "@/components/catalog/playlist/Card.vue";
import PlaylistRow from "@/components/catalog/playlist/Row.vue";
import PlaylistRowHeader from "@/components/catalog/playlist/RowHeader.vue";
import ListFilter from "@/components/filter/ListFilter.vue";
import LoadingMore from "@/components/ui/loading/Loading.vue";
import { useDevice } from "@/composables/device";
import { useRatingStore } from "@/stores/rating";
import { useUiStore } from "@/stores/ui";

export default defineComponent({
  components: {
    ListFilter,
    LoadingMore,
    PlaylistRowHeader,
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
      default: "grid",
    },
  },
  setup(props) {
    const route = useRoute();
    const router = useRouter();
    const { filterExpanded } = storeToRefs(useUiStore());
    const { injectRatings } = useRatingStore();
    const { isDesktop } = useDevice();
    const numResults = ref(-1);
    const limit = 16;
    const lastOffset = ref(0);
    const playlists = ref([]);
    const tagList = ref([]);
    const tagListLoading = ref(false);
    const hasNext = ref(false);
    const userFilter = computed(() => {
      const filter = props.query;
      // if (filter?.tags && (typeof filter.tags === 'string' || filter.tags instanceof String)) {
      //   return {
      //     ...filter,
      //     tags: [filter.tags],
      //   };
      // }
      return filter;
    });
    const combinedFilter = computed(() => {
      // @ts-ignore
      const tags = [...(props.initialFilter?.tags ?? []), ...(userFilter.value?.tags ?? [])];
      const merged = { ...props.initialFilter, ...userFilter.value };
      // @ts-ignore
      merged.tags = tags;
      if (props.scope === "collection") {
        // @ts-ignore
        merged.user_rating = 1;
      }
      return merged;
    });
    const ordering = computed(() => {
      return props.scope === "collection" ? ["time_rated"] : [];
    });
    const playlistComponent = computed(() => {
      return props.layout === "grid" ? PlaylistCard : PlaylistRow;
    });
    // eslint-disable-next-line @typescript-eslint/no-shadow
    const fetchPlaylists = async (limit = 16, offset = 0) => {
      // NOTE: depending on the layout we need different data / expands
      const expand = props.layout === "grid" ? [] : ["tags", "editor", "duration"];
      const { count, next, results } = await getPlaylists(
        limit,
        offset,
        combinedFilter.value,
        ordering.value,
        expand
      );
      hasNext.value = !!next;
      numResults.value = count;
      // @ts-ignore
      playlists.value.push(...results);
      await injectRatings(results);
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
      return filterExpanded.value;
    });
    const updateUserFilter = (filter: any) => {
      const query = filter;
      const routeName = route.name || "discoverPlaylists";
      router.push({ name: routeName, query });
    };
    onMounted(() => {
      fetchPlaylists();
      fetchTags().then(() => {});
    });
    watch(
      () => combinedFilter.value,
      async (oldFilter, newFilter) => {
        if (isEqual(oldFilter, newFilter)) {
          return;
        }
        lastOffset.value = 0;
        playlists.value = [];
        fetchPlaylists(limit, 0).then(() => {});
        fetchTags().then(() => {});
      }
    );
    return {
      isDesktop,
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
});
</script>

<template>
  <div v-if="showUserFilter" class="list-filter-container">
    <ListFilter
      :filter="userFilter"
      :tag-list="tagList"
      :is-loading="tagListLoading"
      @change="updateUserFilter"
    />
  </div>
  <div class="playlist-list">
    <div v-if="layout === 'table' && isDesktop" class="table-header">
      <PlaylistRowHeader />
    </div>
    <LoadingMore v-if="numResults === -1" :layout="layout" :class="`layout--${layout}`" />
    <div class="list-container" :class="`layout--${layout}`">
      <component
        v-for="playlist in playlists"
        :key="playlist.uid"
        :playlist="playlist"
        :is="playlistComponent"
      />
    </div>
    <LoadingMore
      v-if="playlists.length && hasNext"
      :has-next="hasNext"
      :layout="layout"
      :class="`layout--${layout}`"
      @on-enter="fetchNextPage"
    />
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";
@use "@/style/elements/grid";

.list-filter-container {
  background: rgb(0 0 0);
  padding-top: 0.75rem;
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;

  .list-filter {
    @include container.default;
  }
}

.playlist-list {
  margin-bottom: 4rem;

  .list-container {
    &.layout {
      &--grid {
        @include container.default;
        @include grid.default;
      }
    }
  }

  .loading-more {
    &.layout {
      &--grid {
        @include container.default;
      }
    }
  }
}
</style>
