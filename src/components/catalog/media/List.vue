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
import { isEqual } from 'lodash-es';

import LoadingMore from '@/components/ui/LoadingMore.vue';
import ListFilter from '@/components/filter/ListFilter.vue';
import PlayAction from '@/components/catalog/actions/PlayAction.vue';
import PlayAll from '@/components/catalog/media/PlayAll.vue';
import MediaRow from '@/components/catalog/media/Row.vue';
import { getMedia, getMediaTags } from '@/api/catalog';
// import { parseFilterQuery } from '@/utils/filter';

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
  },
  setup(props:any) {
    const store = useStore();
    const route = useRoute();
    const router = useRouter();
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
      /*
      const filter = parseFilterQuery(route.query);
      userFilter.value = filter;
      if (props.primaryColor) {
        store.dispatch('ui/setPrimaryColor', props.primaryColor);
      }
      */
      fetchMedia(limit, 0).then(() => {});
      fetchTags().then(() => {});
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
      async () => {
        // console.debug('watched combinedFilter', newValue, oldValue, isEqual(newValue, oldValue));
        lastOffset.value = 0;
        mediaList.value = [];
        fetchMedia(limit, 0).then(() => {});
        fetchTags().then(() => {});
      },
    );
    watch(
      () => props.query,
      async (newValue, oldValue) => {
        if (isEqual(newValue, oldValue)) {
          console.debug('unchanged');
        }
        // userFilter.value = newValue;
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
  <!--
  <pre
    class="debug"
    v-text="{
      initialFilter: initialFilter,
      userFilter: userFilter,
      combinedFilter: combinedFilter,
    }"
  ></pre>
  -->
  <PlayAction
    v-if="(!disablePlayAll && numResults > 0)"
    :filter="combinedFilter"
  >
    <template
      #default="{
        isLoading,
      }"
    >
      <PlayAll
        :is-loading="isLoading"
        :num-total="numResults"
      />
    </template>
  </PlayAction>
  <div
    class="media-list"
  >
    <div
      class="table"
    >
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
@use "@/style/elements/container";
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
