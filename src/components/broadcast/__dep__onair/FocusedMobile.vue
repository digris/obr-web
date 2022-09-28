<script lang="ts">
import { computed, defineComponent } from "vue";

import MediaArtists from "@/components/catalog/media/MediaArtists.vue";

export default defineComponent({
  props: {
    media: {
      type: Object,
      true: false,
      default: () => null,
    },
    item: {
      type: Object,
      required: false,
    },
  },
  components: {
    MediaArtists,
  },
  setup(props) {
    const title = computed(() => {
      return props.media.name;
    });
    const link = computed(() => {
      return {
        name: "mediaDetail",
        params: {
          uid: props.media.uid,
        },
      };
    });
    return {
      title,
      link,
    };
  },
});
</script>

<template>
  <div class="metadata metadata--media">
    <div class="title">
      <router-link :to="`/discover/tracks/${media.uid}/`" v-text="title" />
    </div>
    <div class="subtitle subtitle--artists">
      <MediaArtists :artists="media.artists" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
.metadata {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0 0.625rem;
  width: 100%;
}
.title {
  @include typo.large;
}
.subtitle {
  margin-top: 0;
  &--artists {
    margin-top: 0.25rem;
  }
}
</style>
