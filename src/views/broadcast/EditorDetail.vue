<script lang="ts">
import { computed, defineComponent, ref, onActivated, onBeforeUpdate } from "vue";
import { useStore } from "vuex";

import DetailPage from "@/layouts/DetailPage.vue";
import DetailHeader from "@/layouts/DetailHeader.vue";
import LazyImage from "@/components/ui/LazyImage.vue";
import ObjectTags from "@/components/tagging/ObjectTags.vue";
import ObjectIdentifiers from "@/components/identifier/ObjectIdentifiers.vue";
import PlaylistList from "@/components/catalog/playlist/List.vue";

export default defineComponent({
  components: {
    DetailPage,
    DetailHeader,
    LazyImage,
    ObjectTags,
    ObjectIdentifiers,
    PlaylistList,
  },
  props: {
    uid: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const store = useStore();
    const isLoaded = ref(false);
    const editor = computed(() => store.getters["broadcast/editorByUid"](props.uid));
    const objKey = computed(() => `${editor.value.ct}:${editor.value.uid}`);
    const query = computed(() => ({
      filter: {
        obj_key: objKey.value,
      },
      search: [],
      options: {},
    }));
    // this is kind of bad. don't know yet how to improve..
    // onActivated is called when component is already in keep-alive router,
    // onBefore is needed to switch between different objects in the already active component.
    // it also needs some ugly bits in the store (see broadcast/loadEditor):
    // when the component is in keep-alive, and routing to here from another place both
    // onActivated and onBeforeUpdate will fire ;(
    onActivated(() => {
      if (!editor.value) {
        store.dispatch("broadcast/loadEditor", props.uid);
      }
    });
    onBeforeUpdate(() => {
      if (!editor.value) {
        store.dispatch("broadcast/loadEditor", props.uid);
      }
    });
    return {
      objKey,
      isLoaded,
      editor,
      query,
    };
  },
});
</script>

<template>
  <DetailPage>
    <template #header>
      <DetailHeader
        :obj="editor"
        :show-context-menu="false"
        :title="editor.name"
        title-scope="Editor*in"
      >
        <template #visual>
          <LazyImage class="image" :image="editor.image" />
        </template>
        <template #info-panel>
          <div class="role" v-text="editor.role" />
          <ObjectTags class="tags" :obj="editor" :limit="4" />
          <ObjectIdentifiers class="identifiers" :obj="editor" :limit="4" />
        </template>
        <template #meta-panel>
          <span>
            {{ editor.numPlaylists }}
            Shows
          </span>
        </template>
      </DetailHeader>
    </template>
    <PlaylistList :initial-filter="query.filter" :disable-user-filter="false" layout="table" />
  </DetailPage>
</template>

<style lang="scss" scoped>
.tags,
.identifiers {
  margin: 0.5rem 0;
}
</style>
