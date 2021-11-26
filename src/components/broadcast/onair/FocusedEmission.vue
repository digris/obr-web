<script lang="ts">
import { computed, defineComponent } from 'vue';

import LazyImage from '@/components/ui/LazyImage.vue';

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
    LazyImage,
  },
  setup(props) {
    const title = computed(() => {
      return props.playlist.name;
    });
    const link = computed(() => {
      return {
        name: 'playlistDetail',
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
  <div
    class="metadata metadata--emission"
  >
    <div
      class="context"
    >
      Show
    </div>
    <router-link
      :to="link"
      v-text="title"
      class="title"
    />
    <div>
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
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/live-color";
@use "@/style/abstracts/responsive";
.context {
  @include typo.default;
  @include typo.light;
  // @include typo.underlined;
}
.title {
  @include typo.large;
}
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
}
a {
  @include responsive.hover-supported {
    &:hover {
      @include live-color.bg-inverse(0.1);
      transition: color, background-color 200ms;
    }
  }
}
</style>
