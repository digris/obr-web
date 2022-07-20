<script lang="ts">
import { computed, ref, onActivated, defineComponent } from "vue";
import { useStore } from "vuex";
import type { Tag } from "@/typings/api/models/Tag";

import DetailPage from "@/layouts/DetailPage.vue";
import DetailHeader from "@/layouts/DetailHeader.vue";
import DetailHeaderLoading from "@/layouts/DetailHeaderLoading.vue";
import PlayAction from "@/components/catalog/actions/PlayAction.vue";
import ObjectTags from "@/components/tagging/ObjectTags.vue";
import Searchbar from "@/components/filter/Searchbar.vue";
import MediaList from "@/components/catalog/media/List.vue";
import Visual from "@/components/catalog/mood/Visual.vue";

export default defineComponent({
  components: {
    DetailPage,
    DetailHeader,
    DetailHeaderLoading,
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
    const mood = computed(() => store.getters["catalog/moodByUid"](props.uid));
    // const objKey = computed(() => `${mood.value.ct}:${mood.value.uid}`);
    const objKey = computed(() => {
      return `catalog.mood:${props.uid}`;
    });
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
    });
    onActivated(() => {
      if (!mood.value) {
        store.dispatch("catalog/loadMood", props.uid);
      }
    });
    const allMediaLoaded = ref(false);
    return {
      objKey,
      mood,
      initialFilter,
      userFilter,
      showPlayAll,
      combinedFilter,
      allMediaLoaded,
    };
  },
});
</script>

<template>
  <DetailPage :appendix-visible="allMediaLoaded">
    <template #background="slotProps">
      <Visual
        :color="mood.rgb"
        :ray-config="mood.rays"
        :height="slotProps.height"
        :width="slotProps.width"
      />
    </template>
    <template #header>
      <DetailHeader
        v-if="mood"
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
              :icon-scale="2"
              :outlined="true"
              :shadowed="true"
              background-color="rgb(var(--c-white))"
              hover-background-color="rgba(var(--c-white), 0.8)"
            />
          </div>
        </template>
        <template #info-panel>
          <ObjectTags class="tags" :obj="mood" :limit="4" />
        </template>
        <template #meta-panel>
          (( Play All - T.B.D. ))
          <!--
          <PlayAllSmall :obj-key="objKey">
            <span
              v-text="t('catalog.list.playAllTracks', 1)"
            />
          </PlayAllSmall>
          -->
        </template>
        <template #searchbar>
          <Searchbar :filter="combinedFilter" />
        </template>
      </DetailHeader>
      <DetailHeaderLoading v-else title-scope="Mood" />
    </template>
    <template #default>
      <MediaList
        v-if="objKey"
        class="media-list"
        :initial-filter="initialFilter"
        :query="query"
        :disable-user-filter="false"
        :disable-play-all="true"
        @allLoaded="allMediaLoaded = true"
        @hasMore="allMediaLoaded = false"
      />
    </template>
  </DetailPage>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";
.section {
  @include container.section;
}
</style>
