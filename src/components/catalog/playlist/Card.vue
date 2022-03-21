<script lang="ts">
import { computed, defineComponent } from "vue";
import { DateTime } from "luxon";

import LazyImage from "@/components/ui/LazyImage.vue";
import PlayAction from "@/components/catalog/actions/PlayAction.vue";
import ContextMenu from "@/components/context-menu/ContextMenu.vue";
import RelativeDateTime from "@/components/ui/date/RelativeDateTime.vue";
import PlaylistName from "@/components/catalog/playlist/Name.vue";

export default defineComponent({
  components: {
    LazyImage,
    PlayAction,
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
    const objKey = computed(() => `${props.playlist.ct}:${props.playlist.uid}`);
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
            :size="64"
            :outlined="false"
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
        <!--
        <RelativeDateTime
          v-if="timeRated"
          class="secondary"
          :date-time="timeRated"
        />
        -->
      </div>
      <div class="actions">
        <ContextMenu :obj="playlist" :icon-size="36" :icon-by-rating="true" />
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
    }
  }
}
</style>
