<script lang="ts">
import { defineComponent } from 'vue';

import LazyImage from '@/components/ui/LazyImage.vue';

export default defineComponent({
  props: {
    editor: {
      type: Object,
      required: true,
      default: () => null,
    },
  },
  components: {
    LazyImage,
  },
});
</script>

<template>
  <router-link
    v-if="editor"
    class="editor"
    :to="`/discover/editors/${editor.uid}/`"
  >
    <div
      class="visual"
    >
      <LazyImage
        v-if="editor.image"
        class="image"
        :image="editor.image"
        :size="(128)"
      />
    </div>
    <div
      class="name"
    >
      {{ editor.name }}
    </div>
  </router-link>
</template>

<style lang="scss" scoped>
@use "@/style/base/live-color";
@use "@/style/abstracts/responsive";
.editor {
  display: inline-flex;
  align-items: center;
  height: 3rem;
  margin-top: 0.75rem;
  border-radius: 1.5rem;
  .visual {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 3rem;
    height: 3rem;
    .image {
      width: 3rem;
      min-width: unset;
      max-width: 3rem;
      height: 3rem;
      border-radius: 50%;
      filter: grayscale(1);
      transition: width 100ms, height 100ms;
      :deep(> img) {
        border-radius: 50%;
      }
    }
  }
  .name {
    display: flex;
    align-items: center;
    height: 3rem;
    padding: 0 1rem;
  }
  &:hover {
    .image {
      width: 2.5rem;
      height: 2.5rem;

    }
  }
  @include responsive.hover-supported {
    &:hover {
      @include live-color.bg-inverse(0.1);
      transition: color, background-color 200ms;
    }
  }
}
</style>
