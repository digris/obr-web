<script lang="ts">
import { defineComponent } from 'vue';

import LazyImage from '@/components/ui/LazyImage.vue';

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
  <router-link
    class="card card--editor"
    :to="link"
  >
    <div
      class="visual"
    >
      <div
        class="visual__image"
      >
        <LazyImage
          :image="editor.image"
        />
      </div>
    </div>
    <div
      class="meta"
    >
      <div
        class="title"
      >
        {{ editor.name }}
      </div>
      <div
        class="subtitle"
      >
        <!-- {{ editor.role }} -->
        Musikredaktor
      </div>
    </div>
  </router-link>
</template>
<style lang="scss" scoped>
@use "@/style/base/typo";
.card {
  .visual {
    position: relative;
    background: rgba(var(--c-white), .25);
    cursor: pointer;
    &__image {
      position: relative;
      width: 100%;
      padding-bottom: 100%;
      transition: opacity 200ms;
      img {
        position: absolute;
        width: 100%;
      }
    }
  }
  .meta {
    padding: 0.5rem 0 0 0;
    line-height: 1.25rem;
    .title {
      display: flex;
      font-weight: 600;
      a {
        flex-grow: 1;
      }
    }
    .subtitle {
      @include typo.dim;
      @include typo.light;
    }
  }
  &:hover {
    .visual {
      background: rgba(var(--c-black), 0.2);
      &__image {
        opacity: 0.5;
      }
    }
  }
}
</style>
