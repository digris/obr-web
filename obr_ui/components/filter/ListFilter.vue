<script lang="js">
import { computed, defineComponent } from 'vue';

import { useAnalytics } from "@/composables/analytics";

import Query from './Query.vue';
import Tag from './Tag.vue';

const addOrRemove = (arr, item) => {
  if (!arr) {
    return [item];
  }
  return arr.includes(item) ? arr.filter((i) => i !== item) : [...arr, item];
};

export default defineComponent({
  components: {
    Query,
    Tag,
  },
  props: {
    isLoading: {
      type: Boolean,
      default: false,
    },
    filter: {
      type: Object,
      required: true,
      default: () => {},
    },
    tagList: {
      type: Array,
      required: true,
      default: () => [],
    },
  },
  emits: [
    'change',
  ],
  setup(props, { emit }) {
    const { logRawEvent } = useAnalytics();
    const selectedTags = computed(() => {
      return props.filter.tags || [];
    });
    const searchQuery = computed(() => {
      return props.filter.q;
    });
    const moodTags = computed(() => {
      return props.tagList.filter((t) => {
        return t.type === 'mood';
      }).sort((t) => {
        return (selectedTags.value.includes(t.uid) ? -1 : 1);
      });
    });
    const otherTags = computed(() => {
      return props.tagList.filter((t) => {
        return t.type !== 'mood';
      }).sort((t) => {
        return (selectedTags.value.includes(t.uid) ? -1 : 1);
      });
    });
    const clearSearchQuery = () => {
      const filter = { ...props.filter };
      filter.q = '';
      emit('change', filter);
    };
    const toggleTag = (tag) => {
      const { tags, ...other } = { ...props.filter };
      const filter = {
        tags: addOrRemove(tags, tag.uid),
        ...other,
      };
      emit('change', filter);
      if (filter.tags.length) {
        const tagNames = filter.tags.map((t) => {
          const tagObj = props.tagList.find((el) => el.uid === t);
          return tagObj ? tagObj.name : t;
        }).sort((a, b) => a.localeCompare(b));
        console.debug("filter", filter, tagNames);
        logRawEvent("view_search_results", {
          search_term: tagNames.join(','),
          filter_type: "tags",
        });
      }
    };
    return {
      selectedTags,
      searchQuery,
      moodTags,
      otherTags,
      toggleTag,
      clearSearchQuery,
    };
  },
});
</script>

<template>
  <div class="list-filter">
    <div class="tag-list" :class="{ 'is-loading': isLoading }">
      <div>
        <Query v-if="searchQuery" :q="searchQuery" @click="clearSearchQuery" />
        <Tag
          v-for="tag in moodTags"
          :key="`tag-list-tag-${tag.uid}`"
          :tag="tag"
          :selected="selectedTags.includes(tag.uid)"
          @click="toggleTag"
        />
      </div>
      <div>
        <Tag
          v-for="tag in otherTags"
          :key="`tag-list-tag-${tag.uid}`"
          :tag="tag"
          :selected="selectedTags.includes(tag.uid)"
          @click="toggleTag"
        />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.tag-list {
  .query {
    margin-right: 0.5rem;
    margin-bottom: 0.5rem;
  }

  .tag {
    margin-bottom: 0.25rem;

    &:not(:last-child) {
      margin-right: 0.25rem;
    }
  }

  &.is-loading {
    cursor: wait;
    opacity: 0.7;

    > * {
      pointer-events: none;
    }
  }
}
</style>
