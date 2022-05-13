<script lang="ts">
import { computed, onMounted, onActivated, ref, watch, onUnmounted } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { isEqual } from "lodash-es";
import { DateTime } from "luxon";

import LoadingMore from "@/components/ui/loading/Loading.vue";
import ListFilter from "@/components/filter/ListFilter.vue";
import PlayAll from "@/components/catalog/media/PlayAll.vue";
import MediaRowHeader from "@/components/catalog/media/RowHeader.vue";
import MediaRow from "@/components/catalog/media/Row.vue";
import { getMedia, getMediaTags } from "@/api/catalog";

export default {
  components: {
    ListFilter,
    PlayAll,
    MediaRowHeader,
    MediaRow,
    LoadingMore,
  },
  props: {
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
    disablePlayAll: {
      type: Boolean,
      default: false,
    },
    disableUserFilter: {
      type: Boolean,
      default: false,
    },
    hideUpcoming: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["allLoaded", "hasMore"],
  setup(props: any, { emit }) {
    const store = useStore();
    const route = useRoute();
    const router = useRouter();
    const now = ref(DateTime.now());
    const timer = ref(null);
    const numResults = ref(0);
    const limit = 16;
    const lastOffset = ref(0);
    const mediaList = ref([]);
    const mediaListLoading = ref(false);
    const tagList = ref([]);
    const tagListLoading = ref(false);
    const hasNext = ref(false);
    // const lastFilter = ref({});
    // const userFilter = ref({});
    const userFilter = computed(() => {
      return props.query;
    });
    const visibleMediaList = computed(() => {
      if (!props.hideUpcoming) {
        return mediaList.value;
      }
      return mediaList.value.filter((m: any) => DateTime.fromISO(m.latestAirplay) < now.value);
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
    const fetchMedia = async (limit = 16, offset = 0) => {
      mediaListLoading.value = true;
      const { count, next, results } = await getMedia(
        limit,
        offset,
        combinedFilter.value,
        ordering.value
      );
      hasNext.value = !!next;
      numResults.value = count;
      // @ts-ignore
      mediaList.value.push(...results);
      // TODO: this kind of smells...
      await store.dispatch("rating/updateObjectRatings", results);
      mediaListLoading.value = false;
      if (!hasNext.value) {
        emit("allLoaded");
      } else {
        emit("hasMore");
      }
    };
    const fetchNextPage = async () => {
      const offset = lastOffset.value + limit;
      await fetchMedia(limit, offset);
      lastOffset.value = offset;
    };
    // eslint-disable-next-line @typescript-eslint/no-shadow
    const fetchTags = async () => {
      tagListLoading.value = true;
      tagList.value = await getMediaTags(combinedFilter.value);
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
      const routeName = route.name || "discoverMedia";
      router.push({ name: routeName, query });
    };
    onMounted(() => {
      fetchMedia(limit, 0).then(() => {});
      fetchTags().then(() => {});
      if (props.hideUpcoming) {
        // @ts-ignore
        timer.value = setInterval(() => {
          now.value = DateTime.now();
        }, 2000);
      }
    });
    onUnmounted(() => {
      // @ts-ignore
      clearInterval(timer.value);
    });
    onActivated(() => {
      /*
      if (props.primaryColor) {
        store.dispatch('ui/setPrimaryColor', props.primaryColor);
      }
      */
    });
    watch(
      () => combinedFilter.value,
      async (oldFilter, newFilter) => {
        if (isEqual(oldFilter, newFilter)) {
          return;
        }
        lastOffset.value = 0;
        mediaList.value = [];
        fetchMedia(limit, 0).then(() => {});
        fetchTags().then(() => {});
      }
    );
    return {
      combinedFilter,
      tagList,
      ordering,
      tagListLoading,
      visibleMediaList,
      mediaListLoading,
      hasNext,
      numResults,
      fetchNextPage,
      showSearchBar,
      showUserFilter,
      userFilter,
      updateUserFilter,
      now,
    };
  },
};
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
  <div v-if="!disablePlayAll && numResults > 0">
    <PlayAll :num-total="numResults" :filter="combinedFilter" :ordering="ordering" />
  </div>
  <div class="media-list">
    <div class="table-header">
      <MediaRowHeader />
    </div>
    <div class="table">
      <MediaRow
        v-for="(media, index) in visibleMediaList"
        :key="`media-row-${index}`"
        :media="media"
      />
    </div>
    <LoadingMore v-if="hasNext" :has-next="hasNext" layout="table" @on-enter="fetchNextPage" />
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/abstracts/responsive";
@use "@/style/elements/container";
.list-filter-container {
  @include container.default;
  margin-bottom: 1rem;
  //padding-left: 5rem;
}
.media-list {
  //margin: 0 0 8rem;
  background: rgb(var(--c-white));
}
</style>
