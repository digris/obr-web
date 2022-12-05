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
    <i18n-t keypath="catalog.ct.media" tag="div" class="context" />
    <div class="title">
      <router-link :to="`/discover/tracks/${media.uid}/`" v-text="title" />
    </div>
    <div class="subtitle subtitle--artists">
      <i18n-t
        keypath="catalog.ct.artist"
        tag="span"
        class="subtitle--label"
        :plural="media.artists.length"
      />
      <MediaArtists :artists="media.artists" />
    </div>
    <div class="subtitle subtitle--releases">
      <i18n-t keypath="catalog.ct.release" tag="span" class="subtitle--label" />
      <MediaReleases :releases="media.releases" />
    </div>
    <!--
    <br />
    <div v-if="timeDisplay" v-text="timeDisplay" />
    -->
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/live-color";
@use "@/style/base/responsive";

.context {
  @include typo.default;

  text-transform: capitalize;

  &::after {
    content: ":";
  }
}

.title {
  @include typo.large;
}

.subtitle {
  display: flex;
  margin-top: 0;

  &--artists {
    margin-top: 0.75rem;
  }

  &--label {
    margin-right: 0.25rem;

    &::first-letter {
      text-transform: uppercase;
    }

    &::after {
      content: ": ";
    }
  }

  .media-artists {
    max-width: 100%;
  }

  .media-releases {
    max-width: 100%;

    :deep(a),
    :deep(span) {
      white-space: unset;
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
