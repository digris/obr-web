<script lang="ts">
import { defineComponent, ref, onMounted, computed, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { storeToRefs } from "pinia";
import { isEqual } from "lodash-es";
import { useUiStore } from "@/stores/ui";
import { useRatingStore } from "@/stores/rating";
import { getArtists, getArtistsTags } from "@/api/catalog";

import LoadingMore from "@/components/ui/loading/Loading.vue";
import NoResults from "@/components/ui/loading/NoResults.vue";
import ListFilter from "@/components/filter/ListFilter.vue";
import ArtistCard from "@/components/catalog/artist/Card.vue";

export default defineComponent({
  components: {
    ListFilter,
    LoadingMore,
    NoResults,
    ArtistCard,
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
  },
  setup(props) {
    const route = useRoute();
    const router = useRouter();
    const { filterExpanded } = storeToRefs(useUiStore());
    const { injectRatings } = useRatingStore();
    const numResults = ref(-1);
    const limit = 16;
    const lastOffset = ref(0);
    const artists = ref([]);
    const tagList = ref([]);
    const tagListLoading = ref(false);
    const hasNext = ref(false);
    const userFilter = computed(() => {
      return props.query;
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
    // eslint-disable-next-line @typescript-eslint/no-shadow
    const fetchArtists = async (limit = 16, offset = 0) => {
      // NOTE: depending on the layout we need different data / expands
      const { count, next, results } = await getArtists(
        limit,
        offset,
        combinedFilter.value,
        ordering.value
      );
      hasNext.value = !!next;
      numResults.value = count;
      // @ts-ignore
      artists.value.push(...results);
      await injectRatings(results);
    };
    const fetchNextPage = async () => {
      const offset = lastOffset.value + limit;
      await fetchArtists(limit, offset);
      lastOffset.value = offset;
    };
    const fetchTags = async () => {
      tagListLoading.value = true;
      tagList.value = await getArtistsTags(combinedFilter.value);
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
      const routeName = route.name || "discoverArtists";
      router.push({ name: routeName, query });
    };
    onMounted(() => {
      fetchArtists();
      fetchTags().then(() => {});
    });
    watch(
      () => combinedFilter.value,
      async (oldFilter, newFilter) => {
        if (isEqual(oldFilter, newFilter)) {
          return;
        }
        lastOffset.value = 0;
        artists.value = [];
        numResults.value = -1;
        fetchArtists(limit, 0).then(() => {});
        fetchTags().then(() => {});
      }
    );
    return {
      combinedFilter,
      tagList,
      tagListLoading,
      artists,
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
  <div class="artist-list">
    <LoadingMore v-if="numResults === -1" />
    <NoResults v-if="numResults === 0" />
    <div class="list-container">
      <ArtistCard v-for="artist in artists" :key="artist.uid" :artist="artist" />
    </div>
    <LoadingMore v-if="artists.length && hasNext" :has-next="hasNext" @on-enter="fetchNextPage" />
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";
@use "@/style/elements/grid";
.list-filter-container {
  background: rgb(var(--c-black));
  padding-top: 0.75rem;
  padding-bottom: 0.75rem;
  margin-bottom: 1rem;
  .list-filter {
    @include container.default;
  }
}

.artist-list {
  margin-bottom: 0;
  .list-container {
    @include container.default;
    @include grid.default;
  }
  .loading-more {
    @include container.default;
  }
}
</style>
