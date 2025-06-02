<script lang="ts" setup>
import LazyImage from "@/components/ui/LazyImage.vue";
import { useDevice } from "@/composables/device";
import type { Editor } from "@/typings";

defineProps<{
  editor: Editor;
}>();

const { isSmallScreen } = useDevice();
</script>

<template>
  <router-link v-if="editor" class="editor" :to="`/discover/editors/${editor.uid}/`">
    <div v-if="!isSmallScreen" class="visual">
      <LazyImage v-if="editor.image" class="image" :image="editor.image" />
    </div>
    <div class="name" v-text="editor.name" />
  </router-link>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";
@use "@/style/base/live-color";

.editor {
  display: inline-flex;
  align-items: center;
  height: 3rem;
  margin-top: 0.75rem;
  border-radius: 1.5rem;
  transition: color, background-color 200ms;

  .visual {
    height: 3rem;
    width: 3rem;
    display: flex;
    align-items: center;
    justify-content: center;

    .image {
      height: 3rem;
      width: 3rem;
      min-width: unset;
      max-width: 3rem;
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
      height: 2.5rem;
      width: 2.5rem;
    }
  }

  @include responsive.on-hover {
    @include live-color.bg-inverse(10%);
  }

  @include responsive.bp-medium {
    height: unset;
    margin-top: unset;
    border-radius: unset;

    .name {
      height: unset;
      padding: unset;
    }
  }
}
</style>
