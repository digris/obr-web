<script lang="ts">
import { computed, ref, onActivated, defineComponent } from "vue";
import { useI18n } from "vue-i18n";
import { useStore } from "vuex";
import type { Tag } from "@/typings/api/models/Tag";

import DetailPage from "@/layouts/DetailPage.vue";
import DetailHeader from "@/layouts/DetailHeader.vue";
import DetailHeaderLoading from "@/layouts/DetailHeaderLoading.vue";
import PlayAction from "@/components/catalog/actions/PlayAction.vue";
import PlayAllAction from "@/components/catalog/actions/PlayAllAction.vue";
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
    PlayAllAction,
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
    const { t } = useI18n();
    const store = useStore();
    const mood = computed(() => store.getters["catalog/moodByUid"](props.uid));
    // const objKey = computed(() => `${mood.value.ct}:${mood.value.uid}`);
    const objKey = computed(() => {
      return `catalog.mood:${props.uid}`;
    });
    const initialFilter = computed(() => {
      if (!mood.value) {
        return {};
      }
      return {
        tags: mood.value.tags.map((tag: Tag) => tag.uid),
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
    onActivated(() => {
      if (!mood.value) {
        store.dispatch("catalog/loadMood", props.uid);
      }
    });
    const allMediaLoaded = ref(false);
    return {
      t,
      objKey,
      mood,
      initialFilter,
      userFilter,
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
        v-if="mood"
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
              :filled="true"
              :color="[0, 0, 0]"
            />
          </div>
        </template>
        <template #info-panel>
          <ObjectTags class="tags" :obj="mood" :limit="4" />
        </template>
        <template #meta-panel>
          <PlayAllAction :obj-key="objKey">
            <span v-text="t('catalog.list.playAllTracks', 1)" />
          </PlayAllAction>
        </template>
        <template #searchbar>
          <Searchbar :filter="combinedFilter" :hide-form-for-mobile="true" />
        </template>
      </DetailHeader>
      <DetailHeaderLoading v-else title-scope="Mood" />
    </template>
    <template #default>
      <MediaList
        v-if="objKey"
        :initial-filter="initialFilter"
        :query="query"
        :disable-user-filter="false"
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
:deep(.visual) {
  height: 25vh;
}
</style>
