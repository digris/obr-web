<script lang="ts">
import { defineComponent } from "vue";
import { useI18n } from "vue-i18n";
import { useObjKey } from "@/composables/obj";

import LazyImage from "@/components/ui/LazyImage.vue";
import PlayAction from "@/components/catalog/actions/PlayAction.vue";
import CircleButton from "@/components/ui/button/CircleButton.vue";
import UserRating from "@/components/rating/UserRating.vue";
import ContextMenu from "@/components/context-menu/ContextMenu.vue";

export default defineComponent({
  components: {
    LazyImage,
    PlayAction,
    CircleButton,
    UserRating,
    ContextMenu,
  },
  props: {
    artist: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const { t } = useI18n();
    const { objKey } = useObjKey(props.artist);
    const link = `/discover/artists/${props.artist.uid}/`;
    return {
      t,
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
            :size="86"
            :outlined="true"
            background-color="rgb(var(--c-white))"
          />
        </LazyImage>
      </div>
    </router-link>
    <div class="meta">
      <div class="title">
        <router-link class="primary" :to="link" v-text="artist.name" />
        <div class="secondary" v-text="t('catalog.ct.numMedia', artist.numMedia)" />
      </div>
      <div class="actions">
        <CircleButton :scale="0.75">
          <UserRating :obj-key="objKey" :icon-size="40" />
        </CircleButton>
        <ContextMenu :obj="artist" :icon-size="36" />
      </div>
    </div>
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
      width: 72px;
      display: flex;
      margin-top: 0.5rem;
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
