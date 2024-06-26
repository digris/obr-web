<script lang="ts">
import { defineComponent } from "vue";
import { useI18n } from "vue-i18n";

import PlayAction from "@/components/catalog/actions/PlayAction.vue";
import ContextMenu from "@/components/context-menu/ContextMenu.vue";
import UserRating from "@/components/rating/UserRating.vue";
import ObjectTags from "@/components/tagging/ObjectTags.vue";
import CircleButton from "@/components/ui/button/CircleButton.vue";
import LazyImage from "@/components/ui/LazyImage.vue";
import { useDevice } from "@/composables/device";
import { useObjKey } from "@/composables/obj";

export default defineComponent({
  components: {
    LazyImage,
    PlayAction,
    CircleButton,
    UserRating,
    ContextMenu,
    ObjectTags,
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
    const { isDesktop } = useDevice();
    const link = `/discover/artists/${props.artist.uid}/`;
    return {
      t,
      objKey,
      isDesktop,
      link,
    };
  },
});
</script>
<template>
  <div class="card card--artist">
    <router-link :to="link" class="visual">
      <LazyImage :image="artist.image">
        <PlayAction
          :obj-key="objKey"
          :icon-scale="1.5"
          :outlined="true"
          :filled="true"
          :color="[0, 0, 0]"
        />
      </LazyImage>
      <UserRating
        v-if="!isDesktop"
        :obj-key="objKey"
        :readonly="true"
        :hide-if-unset="true"
        class="rating"
      />
    </router-link>
    <div class="meta">
      <router-link class="title" :to="link">
        {{ artist.name }}
        <span v-if="artist.countryCode">({{ artist.countryCode }})</span>
      </router-link>
      <ObjectTags v-if="isDesktop" class="tags" :obj="artist" :limit="4" :types="['genre']" />
      <div class="subtitle" v-text="t('catalog.ct.numMedia', artist.numMedia)" />
      <div v-if="isDesktop" class="actions">
        <CircleButton :scale="0.75">
          <UserRating :obj-key="objKey" :icon-scale="0.75" />
        </CircleButton>
        <ContextMenu :obj="artist" :icon-scale="0.75" />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/card";

.card {
  @include card.default;
  @include card.actions-on-hover;
}
</style>
