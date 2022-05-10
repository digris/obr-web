<script lang="ts">
import { ref, onMounted, computed, watch } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { isEqual } from "lodash-es";

import LoadingMore from "@/components/ui/loading/Loading.vue";
import ListFilter from "@/components/filter/ListFilter.vue";
import ArtistCard from "@/components/catalog/artist/Card.vue";
import { getArtists, getArtistsTags } from "@/api/catalog";

export default {
  components: {
    ListFilter,
    LoadingMore,
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
  setup(props: any) {
    const store = useStore();
    const route = useRoute();
    const router = useRouter();
    const numResults = ref(0);
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

      // TODO: this kind of smells...
      await store.dispatch("rating/updateObjectRatings", results);
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
      return store.getters["ui/filterExpanded"];
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
};
</script>
<template>
  <div class="list-filter-container">
    <ListFilter
      v-if="showUserFilter"
      :filter="userFilter"
      :tag-list="tagList"
      :is-loading="tagListLoading"
      @change="updateUserFilter"
    />
  </div>
  <div class="artist-list">
    <div class="list-container">
      <ArtistCard v-for="artist in artists" :key="artist.uid" :artist="artist" />
    </div>
    <LoadingMore v-if="artists.length && hasNext" :has-next="hasNext" @on-enter="fetchNextPage" />
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/abstracts/responsive";
@use "@/style/elements/container";
.list-filter-container {
  @include container.default;
  margin-bottom: 1rem;
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

.artist-list {
  margin-bottom: 0;
  .list-container {
    @include container.default;
    @include grid;
  }
  .loading-more {
    @include container.default;
  }
}
</style>
