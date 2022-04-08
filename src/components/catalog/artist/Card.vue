<script lang="ts">
import { computed, defineComponent } from "vue";

import LazyImage from "@/components/ui/LazyImage.vue";
import PlayAction from "@/components/catalog/actions/PlayAction.vue";
import ContextMenu from "@/components/context-menu/ContextMenu.vue";

export default defineComponent({
  components: {
    LazyImage,
    PlayAction,
    ContextMenu,
  },
  props: {
    artist: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const objKey = computed(() => `${props.artist.ct}:${props.artist.uid}`);
    const link = `/discover/artists/${props.artist.uid}/`;
    return {
      objKey,
      link,
    };
  },
});
</script>
<template>
  <div class="card card--artist">
    <router-link :to="link" class="visual">
      <div class="visual__image">
        <LazyImage :image="artist.image">
          <PlayAction
            :obj-key="objKey"
            :size="64"
            :outlined="false"
            background-color="rgb(var(--c-white))"
          />
        </LazyImage>
      </div>
    </router-link>
    <div class="meta">
      <div class="title">
        <router-link class="primary" :to="link" v-text="artist.name" />
        <div class="secondary">
          <span v-if="artist.numMedia === 1"> {{ artist.numMedia }} Track </span>
          <span v-else> {{ artist.numMedia }} Tracks </span>
        </div>
      </div>
      <div class="actions">
        <ContextMenu :obj="artist" :icon-size="36" :icon-by-rating="true" />
      </div>
    </div>
    <!--
    <div
      class="meta"
    >
      <div
        class="title"
      >
        <router-link
          :to="link"
        >
          {{ artist.name }}
        </router-link>
      </div>
      <div
        class="subtitle"
      >
        {{ artist.numMedia }} Tracks
      </div>
    </div>
    -->
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
.card {
  .visual {
    position: relative;
    background: rgba(var(--c-white), 0.25);
    cursor: pointer;
    &__image {
      position: relative;
      width: 100%;
      padding-bottom: 100%;
      //filter: grayscale(100%);
      transition: opacity 200ms;
      .lazy-image {
        position: absolute;
        width: 100%;
      }
    }
  }

  .meta {
    display: flex;
    line-height: 1.25rem;
    .title {
      display: flex;
      flex-direction: column;
      flex-grow: 1;
      padding: 4px 1rem 0 0;
      .primary {
        font-weight: 500;
      }
      .secondary {
        @include typo.dim;
        @include typo.light;
        text-transform: capitalize;
      }
    }
    .actions {
      height: 36px;
    }
  }
  &:hover {
    .visual {
      background: rgba(var(--c-black), 0.2);
      :deep(img) {
        opacity: 0.5;
      }
    }
  }
}
</style>
