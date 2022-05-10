<script lang="ts">
import { computed, ref, onActivated, defineComponent } from "vue";
import { useStore } from "vuex";
import { Tag } from "@/typings/api/models/Tag";

import DetailPage from "@/layouts/DetailPage.vue";
import DetailHeader from "@/layouts/DetailHeader.vue";
import PlayAction from "@/components/catalog/actions/PlayAction.vue";
import ObjectTags from "@/components/tagging/ObjectTags.vue";
import Searchbar from "@/components/filter/SearchbarAlt.vue";
import MediaList from "@/components/catalog/media/List.vue";
import Visual from "@/components/catalog/mood/Visual.vue";

export default defineComponent({
  components: {
    DetailPage,
    DetailHeader,
    PlayAction,
    ObjectTags,
    Searchbar,
    MediaList,
    Visual,
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
    const mood = computed(() => store.getters["catalog/moodByUid"](props.uid));
    const mediaColor = computed(() => store.getters["player/color"]);
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
      const tags = [...(initialFilter.value?.tags ?? []), ...(userFilter.value?.tags ?? [])];
      const merged = { ...initialFilter.value, ...userFilter.value };
      // @ts-ignore
      merged.tags = tags;
      return merged;
    });
    const showPlayAll = computed(() => {
      return (userFilter.value?.tags || []).length || userFilter.value?.q;
      // return true;
    });
    onActivated(() => {
      if (!mood.value) {
        store.dispatch("catalog/loadMood", props.uid);
      }
    });
    return {
      objKey,
      isLoaded,
      mood,
      initialFilter,
      userFilter,
      showPlayAll,
      combinedFilter,
      mediaColor,
    };
  },
});
</script>

<template>
  <DetailPage>
    <template #background>
      <Visual :color="mood.rgb" />
    </template>
    <template #header>
      <DetailHeader
        :obj="mood"
        :show-context-menu="false"
        title-scope="Stimmung"
        :title="mood.name"
      >
        <template #visual>
          <div
            class="image"
            :style="{
              display: 'flex',
              alignItems: 'center',
            }"
          >
            <PlayAction
              :obj-key="objKey"
              :filter="combinedFilter"
              :size="96"
              :outlined="false"
              :shadowed="true"
              background-color="rgb(var(--c-white))"
            />
          </div>
        </template>
        <template #info-panel>
          <ObjectTags class="tags" :obj="mood" :limit="4" />
        </template>
        <template #meta-panel>
          <span>1h 25m</span>
        </template>
        <template #searchbar>
          <Searchbar :filter="combinedFilter" />
        </template>
      </DetailHeader>
    </template>
    <template #default>
      <MediaList
        :initial-filter="initialFilter"
        :query="query"
        :disable-user-filter="false"
        :disable-play-all="!showPlayAll"
      />
    </template>
  </DetailPage>
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
  .--disabled--searchbar {
    flex-grow: 1;
    justify-content: flex-end;
    margin-bottom: 1rem;
  }
}
.media-list {
  background: rgb(var(--c-white));
}
</style>
