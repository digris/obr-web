<script lang="ts">
import { computed, defineComponent } from 'vue';

import MediaArtists from '@/components/catalog/media/MediaArtists.vue';
import MediaReleases from '@/components/catalog/media/MediaReleases.vue';

export default defineComponent({
  props: {
    media: {
      type: Object,
      true: false,
      default: () => null,
    },
  },
  components: {
    MediaArtists,
    MediaReleases,
  },
  setup(props) {
    const title = computed(() => {
      return props.media.name;
    });
    const link = computed(() => {
      return {
        name: 'mediaDetail',
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
  <div
    class="metadata metadata--media"
  >
    <div
      class="context"
    >
      Track
    </div>
    <div
      class="title"
    >
      <a href="#">
        {{ title }}
      </a>
    </div>
    <div
      class="subtitle"
    >
      <MediaArtists
        :artists="media.artists"
      />
    </div>
    <div
      class="subtitle"
    >
      <MediaReleases
        :releases="media.releases"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/live-color";
@use "@/style/abstracts/responsive";
.context {
  @include typo.large;
  @include typo.dim;
}
.title {
  @include typo.large;
}
.subtitle {
  margin-top: 0.75rem;
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
