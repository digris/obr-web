<script lang="ts">
import { computed, defineComponent } from "vue";
import { DateTime } from "luxon";

import MediaArtists from "@/components/catalog/media/MediaArtists.vue";
import MediaReleases from "@/components/catalog/media/MediaReleases.vue";

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
    MediaReleases,
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
    const timeDisplay = computed(() => {
      if (!props.item) {
        return null;
      }
      return `${props.item.timeStart.toLocaleString(
        DateTime.TIME_24_WITH_SECONDS
      )} - ${props.item.timeEnd.toLocaleString(DateTime.TIME_24_WITH_SECONDS)}`;
    });
    return {
      title,
      link,
      timeDisplay,
    };
  },
});
</script>

<template>
  <div class="metadata metadata--media">
    <div class="context">Track:</div>
    <div class="title">
      <router-link :to="`/discover/tracks/${media.uid}/`" v-text="title" />
    </div>
    <div class="subtitle subtitle--artists">
      <span class="subtitle--label" v-text="media.artists.length === 1 ? 'Artist' : 'Artists'" />
      <MediaArtists :artists="media.artists" />
    </div>
    <div class="subtitle subtitle--releases">
      <span class="subtitle--label" v-text="`Album`" />
      <MediaReleases :releases="media.releases" />
    </div>
    <br />
    <div v-if="timeDisplay" v-text="timeDisplay" />
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/live-color";
@use "@/style/abstracts/responsive";
.context {
  @include typo.default;
}
.title {
  @include typo.large;
}
.subtitle {
  margin-top: 0;
  &--artists {
    margin-top: 0.75rem;
  }
  &--label {
    &:after {
      content: ": ";
    }
  }
  .media-releases {
    display: inline;
  }
  :deep {
    a,
    span {
      white-space: initial;
    }
  }
}
a {
  transition: color, background-color 200ms;
  @include responsive.on-hover {
    @include live-color.bg-inverse(0.1);
  }
}
</style>
