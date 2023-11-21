<script lang="ts">
import { computed, defineComponent, onActivated } from "vue";
import { useI18n } from "vue-i18n";

import PlaylistList from "@/components/catalog/playlist/List.vue";
import Searchbar from "@/components/filter/Searchbar.vue";
import ObjectIdentifiers from "@/components/identifier/ObjectIdentifiers.vue";
import ObjectTags from "@/components/tagging/ObjectTags.vue";
import LazyImage from "@/components/ui/LazyImage.vue";
import DetailHeader from "@/layouts/DetailHeader.vue";
import DetailPage from "@/layouts/DetailPage.vue";
import { useBroadcastStore } from "@/stores/broadcast";

export default defineComponent({
  components: {
    DetailPage,
    DetailHeader,
    LazyImage,
    ObjectTags,
    ObjectIdentifiers,
    Searchbar,
    PlaylistList,
  },
  props: {
    uid: {
      type: String,
      required: true,
    },
    query: {
      type: Object,
      default: () => ({}),
    },
  },
  setup(props) {
    const { t } = useI18n();
    const { loadEditor, editorByUid } = useBroadcastStore();
    const editor = computed(() => editorByUid(props.uid));
    const objKey = computed(() => `${editor.value?.ct}:${editor.value?.uid}`);
    const initialFilter = computed(() => {
      return {
        obj_key: objKey.value,
        tags: [],
      };
    });
    const userFilter = computed(() => {
      return props.query;
    });
    const combinedFilter = computed(() => {
      // @ts-ignore
      const tags = [...(initialFilter.value?.tags ?? []), ...(userFilter.value?.tags ?? [])];
      const merged = { ...initialFilter.value, ...userFilter.value };
      // @ts-ignore
      merged.tags = tags;
      return merged;
    });
    onActivated(() => {
      if (!editor.value) {
        loadEditor(props.uid);
      }
    });
    return {
      t,
      objKey,
      editor,
      initialFilter,
      userFilter,
      combinedFilter,
    };
  },
});
</script>

<template>
  <DetailPage v-if="editor">
    <template #header>
      <DetailHeader
        :obj="editor"
        layout="square"
        :show-context-menu="false"
        :show-obj-rating="true"
        :title="editor.name"
        :title-scope="t('broadcast.ct.editor', 1)"
      >
        <template #visual>
          <LazyImage class="image" :image="editor.image" />
        </template>
        <template #info-panel>
          <!--
          <div class="role" v-text="editor.role" />
          -->
          <div v-if="editor.location" class="location" v-text="editor.location" />
          <ObjectTags class="tags" :obj="editor" :limit="4" />
          <div v-if="editor.description" class="description" v-text="editor.description" />
          <ObjectIdentifiers class="identifiers" :obj="editor" :limit="4" />
        </template>
        <template #meta-panel>
          <span>
            {{ editor.numPlaylists }}
            Shows
          </span>
        </template>
        <template #searchbar>
          <Searchbar :filter="combinedFilter" :hide-form-for-mobile="true" />
        </template>
      </DetailHeader>
    </template>
    <PlaylistList :initial-filter="initialFilter" :query="query" layout="table" />
  </DetailPage>
</template>

<style lang="scss" scoped>
.location {
  margin-top: 0.5rem;
}

.tags {
  margin: 0 0 1rem;
}

.description {
  margin: 1rem 0;
  line-height: 1.25;
  max-width: 480px;
}

.identifiers {
  margin: 1rem 0;
}
</style>
