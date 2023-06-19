<script lang="ts">
import type { PropType } from "vue";
import { computed, defineComponent } from "vue";

import type { Media } from "@/typings/api";

export default defineComponent({
  props: {
    media: {
      type: Object as PropType<Media>,
      required: true,
    },
  },
  setup(props) {
    const link = computed(() => {
      return {
        name: "mediaDetail",
        params: {
          uid: props.media.uid,
        },
      };
    });
    return {
      link,
    };
  },
});
</script>

<template>
  <router-link :to="link" class="focused-media">
    <div class="name">
      <span class="label">Track: </span>
      {{ media.name }}
    </div>
    <div class="artist">
      <span class="label">by </span>
      {{ media.artistDisplay }}
    </div>
  </router-link>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";

.focused-media {
  max-width: 100%;
  line-height: 20px;

  .name,
  .artist {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}
</style>
