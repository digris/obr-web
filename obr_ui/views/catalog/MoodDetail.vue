<script lang="ts">
import { computed, defineComponent, onActivated, ref } from "vue";
import { useI18n } from "vue-i18n";

import PlayAction from "@/components/catalog/actions/PlayAction.vue";
import PlayAllAction from "@/components/catalog/actions/PlayAllAction.vue";
import MediaList from "@/components/catalog/media/List.vue";
import Visual from "@/components/catalog/mood/Visual.vue";
import Searchbar from "@/components/filter/Searchbar.vue";
import { usePageTitle } from "@/composables/title";
import DetailHeader from "@/layouts/DetailHeader.vue";
import DetailHeaderLoading from "@/layouts/DetailHeaderLoading.vue";
import DetailPage from "@/layouts/DetailPage.vue";
import { useCatalogStore } from "@/stores/catalog";
import type { Tag } from "@/typings";

export default defineComponent({
  components: {
    DetailPage,
    DetailHeader,
    DetailHeaderLoading,
    PlayAction,
    PlayAllAction,
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
    const { moodByUid, loadMood } = useCatalogStore();
    const mood = computed(() => moodByUid(props.uid));
    const objKey = computed(() => `catalog.mood:${props.uid}`);
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
    usePageTitle(computed(() => mood.value?.name));
    onActivated(() => loadMood(props.uid));
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
        :title-scope="t('catalog.ct.mood', 1)"
        :title="mood.name"
        mobile-body-position="top"
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
        <!--
        <template #info-panel>
          <ObjectTags class="tags" :obj="mood" :limit="4" />
        </template>
        -->
        <template #meta-panel>
          <PlayAllAction :obj-key="objKey">
            <span v-text="t('catalog.list.playAllTracks', 1)" />
          </PlayAllAction>
        </template>
        <template #searchbar>
          <Searchbar :filter="userFilter" :hide-form-for-mobile="true" />
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
