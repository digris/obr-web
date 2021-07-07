<script lang="ts">
import { computed, defineComponent } from 'vue';

// import LazyImage from '@/components/ui/LazyImage.vue';
// import MediaArtists from '@/components/catalog/media/MediaArtists.vue';

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
    // LazyImage,
    // MediaArtists,
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
    return {
      title,
      link,
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
    >
    </router-link>
    <div
      class="subtitle"
    >
      <a href="#">
        (( Editor ))
      </a>
    </div>
    <div
      class="classification"
    >
      <div
        class="tags"
      >
        <span>
          #flow
        </span>
        <span>
          #mellow
        </span>
      </div>
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
.classification {
  margin-top: 0.325rem;
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
