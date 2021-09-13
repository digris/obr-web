<script lang="ts">
import {
  computed,
  ref,
  onActivated,
  defineComponent,
} from 'vue';
import { useStore } from 'vuex';
import { Tag } from '@/typings/api/models/Tag';

import DetailHeader from '@/components/layout/DetailHeader.vue';
import Filterbar from '@/components/filter/Filterbar.vue';
import PlayAction from '@/components/catalog/actions/PlayAction.vue';
import ObjectTags from '@/components/tagging/ObjectTags.vue';
import MediaList from '@/components/catalog/media/List.vue';
import Animation from '@/components/animation/Animation.vue';
import Space from '@/components/animation/Space.vue';

export default defineComponent({
  components: {
    DetailHeader,
    Filterbar,
    PlayAction,
    ObjectTags,
    MediaList,
    Animation,
    Space,
  },
  props: {
    uid: {
      type: String,
      required: true,
    },
    query: {
      type: Object,
      default: () => {},
    },
  },
  setup(props) {
    const store = useStore();
    const isLoaded = ref(false);
    const mood = computed(() => store.getters['catalog/moodByUid'](props.uid));
    const mediaColor = computed(() => store.getters['player/color']);
    const objKey = computed(() => `${mood.value.ct}:${mood.value.uid}`);
    const initialFilter = computed(() => {
      return {
        tags: mood.value.tags.map((t: Tag) => t.uid),
      };
    });
    const userFilter = computed(() => {
      return props.query;
    });
    // combinedQuery is needed for the 'play action'
    const combinedFilter = computed(() => {
      // @ts-ignore
      const tags = [...initialFilter.value?.tags ?? [], ...userFilter.value?.tags ?? []];
      const merged = { ...initialFilter.value, ...userFilter.value };
      // @ts-ignore
      merged.tags = tags;
      return merged;
    });
    onActivated(() => {
      if (!mood.value) {
        store.dispatch('catalog/loadMood', props.uid);
      }
    });
    return {
      objKey,
      isLoaded,
      mood,
      initialFilter,
      userFilter,
      combinedFilter,
      mediaColor,
    };
  },
});
</script>

<template>
  <div
    v-if="mood"
    class="mood-detail"
  >
    <DetailHeader
      title-scope="Stimmung"
      :title="mood.name"
    >
      <template
        #visual
      >
        <PlayAction
          :obj-key="objKey"
          :filter="combinedFilter"
          :size="(96)"
          :outlined="(false)"
          background-color="rgb(var(--c-white))"
        />
        <!--
        <pre
          class="debug"
          v-text="{
            initialFilter: initialFilter,
            query: query,
            userFilter: userFilter,
            combinedFilter: combinedFilter,
          }"
        ></pre>
        -->
      </template>
      <template
        #info-panel
      >
        <ObjectTags
          class="tags"
          :obj="mood"
          :limit="(4)"
        />
      </template>
      <template
        #meta-panel
      >
        ...
      </template>
      <template
        #appendix
      >
        <Filterbar />
      </template>
      <template
        #background
      >
        <Animation
          v-if="mood.name === 'Focus'"
        />
        <Space
          v-if="mood.name === 'Cocktail'"
          :color="mediaColor"
        />
      </template>
    </DetailHeader>
    <section
      class="section section--light"
    >
      <div
        class="media-list"
      >
        <MediaList
          :initial-filter="initialFilter"
          :query="query"
          :disable-user-filter="(false)"
          :disable-play-all="(false)"
        />
      </div>
    </section>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";
.section {
  @include container.section;
}
.mood-detail {
  margin-bottom: 12rem;
  .detail-header {
    // TODO: find / define appropriate value...
    min-height: 60vh;
  }
  .filterbar {
    flex-grow: 1;
    justify-content: flex-end;
    margin-bottom: 1rem;
  }
}
.media-list {
  background: rgb(var(--c-white));
}
</style>
