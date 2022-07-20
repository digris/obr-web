<script lang="ts">
import { computed, defineComponent } from "vue";
import { DateTime } from "luxon";
import { useObjKey } from "@/composables/obj";

import LazyImage from "@/components/ui/LazyImage.vue";
import PlayAction from "@/components/catalog/actions/PlayAction.vue";
import CircleButton from "@/components/ui/button/CircleButton.vue";
import UserRating from "@/components/rating/UserRating.vue";
import ContextMenu from "@/components/context-menu/ContextMenu.vue";
import RelativeDateTime from "@/components/ui/date/RelativeDateTime.vue";
import PlaylistName from "@/components/catalog/playlist/Name.vue";

export default defineComponent({
  components: {
    LazyImage,
    PlayAction,
    CircleButton,
    UserRating,
    ContextMenu,
    RelativeDateTime,
    PlaylistName,
  },
  props: {
    playlist: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const { objKey } = useObjKey(props.playlist);
    const link = `/discover/playlists/${props.playlist.uid}/`;
    const title = computed(() => {
      return {
        name: props.playlist.series ? props.playlist.series.name : props.playlist.name,
        appendix: props.playlist.series ? props.playlist.series.episode : null,
      };
    });
    const subtitle = computed(() => {
      if (props.playlist.series) {
        return props.playlist.name;
      }
      return "-";
    });
    const latestEmission = computed(() => {
      return DateTime.fromISO(props.playlist.latestEmissionTimeStart);
    });
    const timeRated = computed(() => {
      const userRatingTimeRated = props.playlist?.userRatingTimeRated;
      return userRatingTimeRated ? DateTime.fromISO(userRatingTimeRated) : null;
    });
    return {
      objKey,
      title,
      subtitle,
      link,
      latestEmission,
      timeRated,
    };
  },
});
</script>

<template>
  <div class="card card--artist">
    <router-link :to="link" class="visual">
      <div class="visual__image">
        <LazyImage :image="playlist.image">
          <PlayAction
            :obj-key="objKey"
            :icon-scale="2"
            :outlined="true"
            background-color="rgb(var(--c-white))"
          />
        </LazyImage>
      </div>
    </router-link>
    <div class="meta">
      <div class="title">
        <router-link class="primary" :to="link">
          <PlaylistName :playlist="playlist" />
          <!--
          <div
            v-text="playlist.name"
          />
          -->
        </router-link>
        <RelativeDateTime class="secondary" :date-time="latestEmission" />
      </div>
      <div class="actions">
        <CircleButton :scale="0.75">
          <UserRating :obj-key="objKey" :icon-scale="0.75" />
        </CircleButton>
        <ContextMenu :obj="playlist" :icon-scale="0.75" />
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
    &__image {
      position: relative;
      width: 100%;
      padding-bottom: 100%;
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
