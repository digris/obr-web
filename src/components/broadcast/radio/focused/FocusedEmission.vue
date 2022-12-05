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
    const displayName = computed(() => {
      const name = props.playlist?.series?.name || props.playlist.name;
      const appendix = props.playlist?.series?.episode;
      return name && appendix ? `${name} #${appendix}` : name;
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
      displayName,
      link,
      editor,
    };
  },
});
</script>

<template>
  <div class="metadata metadata--emission">
    <i18n-t keypath="catalog.ct.playlist" tag="div" class="context" />
    <router-link :to="link" v-text="displayName" class="title" />
    <div>
      <EditorInline v-if="editor" :editor="editor" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/live-color";
@use "@/style/base/responsive";

.context {
  @include typo.default;

  text-transform: capitalize;

  &::after {
    content: ":";
  }
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
