<script lang="ts">
import {
  computed,
  onMounted,
  ref,
  watch,
} from 'vue';
import { useStore } from 'vuex';
import { useRoute, useRouter } from 'vue-router';

import LoadingMore from '@/components/ui/LoadingMore.vue';
import ListFilter from '@/components/filter/ListFilter.vue';
import PlayAction from '@/components/catalog/actions/PlayAction.vue';
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
    showUserFilter: {
      type: Boolean,
      default: true,
    },
    primaryColor: {
      type: Array,
      default: () => null,
    },
  },
  setup(props:any) {
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
      userFilter,
      updateUserFilter,
    };
  },
};
</script>

<template>
  <pre
    class="_debug"
    v-text="combinedFilter"
  />
  <pre
    class="_debug"
    v-text="tagList"
  />
  <ListFilter
    v-if="showUserFilter"
    :filter="userFilter"
    :tag-list="tagList"
    :is-loading="tagListLoading"
    @change="updateUserFilter"
  />
  <div>
    <div
      class="play-all"
    >
      <PlayAction
        :filter="combinedFilter"
      >
        Play all
      </PlayAction>
    </div>
  </div>
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
.media-list {
  margin: 1rem 0 8rem;
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
