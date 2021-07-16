<script lang="ts">
import {
  computed,
  onMounted,
  onActivated,
  ref,
  watch,
} from 'vue';
import { useStore } from 'vuex';
import { useRoute, useRouter } from 'vue-router';

import LoadingMore from '@/components/ui/LoadingMore.vue';
import ListFilter from '@/components/filter/ListFilter.vue';
import PlayAction from '@/components/catalog/actions/PlayAction.vue';
import PlayAll from '@/components/catalog/media/PlayAll.vue';
import MediaRow from '@/components/catalog/media/Row.vue';
import { getMedia, getMediaTags } from '@/api/catalog';

const parseFilterQuery = (query:any) => {
  let tags = query.tags || [];
  if (typeof (tags) === 'string') {
    tags = [tags];
  }
  const filter = {
    tags,
  };
  // console.debug('query', query);
  // console.debug('parsed', filter);
  return filter;
};

export default {
  components: {
    ListFilter,
    PlayAction,
    PlayAll,
    MediaRow,
    LoadingMore,
  },
  props: {
    scope: {
      type: String,
      default: null,
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
    primaryColor: {
      type: Array,
      default: () => null,
    },
  },
  setup(props:any) {
    console.debug('MediaList', props);
    const store = useStore();
    const route = useRoute();
    const router = useRouter();
    // const currentUser = computed(() => store.getters['account/currentUser']);
    const numResults = ref(0);
    const limit = 16;
    const lastOffset = ref(0);
    const mediaList = ref([]);
    const mediaListLoading = ref(false);
    const tagList = ref([]);
    const tagListLoading = ref(false);
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
      mediaListLoading.value = true;
      const { count, next, results } = await getMedia(limit, offset, combinedFilter.value);
      hasNext.value = !!next;
      numResults.value = count;
      // @ts-ignore
      mediaList.value.push(...results);
      // TODO: this kind of smells...
      await store.dispatch('rating/updateObjectRatings', results);
      mediaListLoading.value = false;
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
    const showUserFilter = computed(() => {
      if (props.disableUserFilter) {
        return false;
      }
      return store.getters['ui/filterExpanded'];
    });
    const updateUserFilter = (filter: any) => {
      const query = filter;
      const routeName = route.name || 'discoverMedia';
      router.push({ name: routeName, query });
    };
    onMounted(() => {
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const filter = parseFilterQuery(route.query);
      userFilter.value = filter;
      // fetchMedia();
      // fetchTags();
      if (props.primaryColor) {
        store.dispatch('ui/setPrimaryColor', props.primaryColor);
      }
    });
    onActivated(() => {
      if (props.primaryColor) {
        store.dispatch('ui/setPrimaryColor', props.primaryColor);
      }
    });
    watch(
      // () => props.filter,
      () => combinedFilter.value,
      async () => {
        lastOffset.value = 0;
        mediaList.value = [];
        fetchMedia(limit, 0).then(() => {});
        fetchTags().then(() => {});
      },
    );
    watch(
      () => route.query,
      async (newQuery) => {
        const filter = parseFilterQuery(newQuery);
        userFilter.value = filter;
      },
    );
    return {
      combinedFilter,
      tagList,
      tagListLoading,
      mediaList,
      mediaListLoading,
      hasNext,
      numResults,
      fetchNextPage,
      showUserFilter,
      userFilter,
      updateUserFilter,
    };
  },
};
</script>

<template>
  <div
    class="list-filter-container"
  >
    <ListFilter
      v-if="showUserFilter"
      :filter="userFilter"
      :tag-list="tagList"
      :is-loading="tagListLoading"
      @change="updateUserFilter"
    />
  </div>
  <PlayAction
    v-if="(!disablePlayAll && numResults > 0)"
    :filter="combinedFilter"
  >
    <template #default="{
      isLoading,
    }">
      <PlayAll
        :is-loading="isLoading"
        :num-total="numResults"
      />
    </template>
  </PlayAction>
  <div class="media-list">
    <div class="table">
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

<style lang="scss" scoped>
@use "@/style/abstracts/responsive";
@use "@/style/elements/button";
@use "@/style/elements/container";
/*
.play-all {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 1rem 0;
  .play-action {
    @include button.default;
    //padding: 0.5rem 1rem;
  }
}
*/
.list-filter-container {
  @include container.default;
}
.media-list {
  margin: 0 0 8rem;
  background: rgb(var(--c-white));
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
