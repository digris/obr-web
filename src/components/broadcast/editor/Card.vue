<script lang="ts">
import { defineComponent } from "vue";

import LazyImage from "@/components/ui/LazyImage.vue";

export default defineComponent({
  components: {
    LazyImage,
  },
  props: {
    editor: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const link = `/discover/editors/${props.editor.uid}/`;
    return {
      link,
    };
  },
});
</script>

<template>
  <router-link class="card card--editor" :to="link">
    <div class="visual">
      <LazyImage
        :image="editor.image"
        :class="{
          'is-grayscale': !editor.isActive,
        }"
      />
    </div>
    <div class="meta">
      <div class="title" v-text="editor.name" />
      <div class="subtitle" v-text="editor.role" />
    </div>
  </router-link>
</template>
<style lang="scss" scoped>
@use "@/style/elements/card";
.card {
  @include card.default;
  .visual {
    .lazy-image {
      &.is-grayscale {
        filter: grayscale(1);
      }
    }
  }
}
</style>
