<script lang="ts">
import { defineComponent } from "vue";
import { useObjKey } from "@/composables/obj";
import LazyImage from "@/components/ui/LazyImage.vue";
import CircleButton from "@/components/ui/button/CircleButton.vue";
import UserRating from "@/components/rating/UserRating.vue";
import { useDevice } from "@/composables/device";

export default defineComponent({
  components: {
    LazyImage,
    CircleButton,
    UserRating,
  },
  props: {
    editor: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const { objKey } = useObjKey(props.editor);
    const { isDesktop } = useDevice();
    const link = `/discover/editors/${props.editor.uid}/`;
    return {
      objKey,
      isDesktop,
      link,
    };
  },
});
</script>

<template>
  <div class="card card--editor">
    <router-link :to="link" class="visual">
      <LazyImage
        :image="editor.image"
        :class="{
          'is-grayscale': !editor.isActive,
        }"
      />
      <UserRating
        v-if="!isDesktop"
        :obj-key="objKey"
        :readonly="true"
        :hide-if-unset="true"
        class="rating"
      />
    </router-link>
    <div class="meta">
      <router-link class="title" v-text="editor.name" :to="link" />
      <div class="subtitle" v-text="editor.role" />
      <div v-if="isDesktop" class="actions">
        <CircleButton :scale="0.75">
          <UserRating :obj-key="objKey" :autoload="false" :icon-scale="0.75" />
        </CircleButton>
      </div>
    </div>
  </div>
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
