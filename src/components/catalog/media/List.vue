<script lang="ts">
import {
  computed,
  defineComponent,
  onActivated,
  onDeactivated,
  onMounted,
  onUnmounted,
  ref,
  watch,
} from "vue";
import { useI18n } from "vue-i18n";
import { useRoute, useRouter } from "vue-router";
import { DateTime } from "luxon";
import PullToRefresh from "pulltorefreshjs";
import { storeToRefs } from "pinia";
import { isEqual } from "lodash-es";

import { getMedia, getMediaTags } from "@/api/catalog";
import PlayAllAction from "@/components/catalog/actions/PlayAllAction.vue";
import MediaRow from "@/components/catalog/media/Row.vue";
import MediaRowHeader from "@/components/catalog/media/RowHeader.vue";
import ContextMenu from "@/components/context-menu/ContextMenu.vue";
import ListFilter from "@/components/filter/ListFilter.vue";
import LoadingMore from "@/components/ui/loading/Loading.vue";
import { useDevice } from "@/composables/device";
import { useRatingStore } from "@/stores/rating";
import { useUiStore } from "@/stores/ui";

export default defineComponent({
  components: {
    ListFilter,
    PlayAllAction,
    ContextMenu,
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
    showListActions: {
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
  setup(props, { emit }) {
    const { t } = useI18n();
    const route = useRoute();
    const router = useRouter();
    const { isDesktop } = useDevice();
    const { filterExpanded } = storeToRefs(useUiStore());
    const { injectRatings } = useRatingStore();
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
      await injectRatings(results);
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
      try {
        tagList.value = await getMediaTags(combinedFilter.value);
      } catch (e) {
        console.warn("unable to load tag list", e);
      }
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
    const listEl = ref(null);
    onActivated(() => {
      PullToRefresh.init({
        mainElement: listEl.value,
        onRefresh() {
          mediaList.value = [];
          fetchMedia(limit, 0).then(() => {});
          fetchTags().then(() => {});
        },
      });
    });
    onDeactivated(() => {
      PullToRefresh.destroyAll();
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
      t,
      isDesktop,
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
      listEl,
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
  <div v-if="showListActions && numResults > 0" class="list-actions">
    <div class="container">
      <PlayAllAction color-var="--c-white" :filter="combinedFilter" :ordering="ordering">
        <span v-text="t('catalog.list.playAllTracks', numResults)" />
      </PlayAllAction>
      <ContextMenu
        :list="{
          filter: combinedFilter,
          ordering,
        }"
      />
    </div>
  </div>
  <div ref="listEl" class="media-list">
    <div v-if="isDesktop" class="table-header">
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
@use "@/style/base/responsive";
@use "@/style/elements/container";

.list-filter-container {
  background: rgb(0 0 0);
  padding-top: 0.75rem;
  padding-bottom: 0.5rem;

  .list-filter {
    @include container.default;
  }
}

.list-actions {
  // background: rgb(var(--c-gray-500));

  background: rgb(var(--c-black));

  [data-theme="dark"] & {
    background: rgb(var(--c-black));
  }

  // NOTE: for sticky we need a solid background
  @include responsive.bp-medium-up {
    top: 75px;
    position: sticky;
    z-index: 2;
  }

  > .container {
    @include container.default;

    display: grid;
    grid-row-gap: 0;
    grid-column-gap: 1rem;
    grid-template-columns: auto 48px;
    color: rgb(var(--c-white));
    padding-top: 0.75rem;
    padding-bottom: 0.75rem;
    @include responsive.bp-medium {
      height: 60px;
      grid-template-columns: auto 40px;
      align-items: center;
    }
  }
}

.media-list {
  background: rgb(var(--c-light));
}
</style>
