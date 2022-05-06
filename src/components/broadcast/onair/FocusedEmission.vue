<script lang="ts">
import { computed, defineComponent } from "vue";

import EditorInline from "@/components/broadcast/editor/Inline.vue";

export default defineComponent({
  props: {
    emission: {
      type: Object,
      required: true,
      default: () => null,
    },
    playlist: {
      type: Object,
      required: true,
      default: () => null,
    },
  },
  components: {
    EditorInline,
  },
  setup(props) {
    const title = computed(() => {
      return props.playlist.name;
    });
    const link = computed(() => {
      return {
        name: "playlistDetail",
        params: {
          uid: props.playlist.uid,
        },
      };
    });
    const editor = computed(() => {
      return props.playlist?.editor;
    });
    return {
      title,
      link,
      editor,
    };
  },
});
</script>

<template>
  <div class="metadata metadata--emission">
    <div class="context">Show:</div>
    <router-link :to="link" v-text="title" class="title" />
    <div>
      <EditorInline v-if="editor" :editor="editor" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/live-color";
@use "@/style/abstracts/responsive";
.context {
  @include typo.default;
  // @include typo.underlined;
}
.title {
  @include typo.large;
}
a {
  transition: color, background-color 200ms;
  @include responsive.on-hover {
    @include live-color.bg-inverse(0.1);
  }
}
</style>
