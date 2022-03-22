<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import { DateTime } from "luxon";

import CircleButton from "@/components/ui/button/CircleButton.vue";
import ContextMenu from "@/components/context-menu/ContextMenu.vue";
import PlayAction from "@/components/catalog/actions/PlayAction.vue";
import ObjectTags from "@/components/tagging/ObjectTags.vue";
import UserRating from "@/components/rating/UserRating.vue";
import RelativeDateTime from "@/components/ui/date/RelativeDateTime.vue";
import Duration from "@/components/ui/time/Duration.vue";
import PlaylistName from "@/components/catalog/playlist/Name.vue";

export default defineComponent({
  components: {
    CircleButton,
    ContextMenu,
    PlayAction,
    ObjectTags,
    UserRating,
    RelativeDateTime,
    Duration,
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
    const isHover = ref(false);
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
    return {
      objKey,
      isHover,
      title,
      subtitle,
      link,
      latestEmission,
    };
  },
});
</script>

<template>
  <div class="playlist-row" @mouseenter="isHover = true" @mouseleave="isHover = false">
    <div class="container">
      <div class="play">
        <PlayAction
          :obj-key="objKey"
          :size="48"
          :outlined="false"
          background-color="rgb(var(--c-white))"
        />
      </div>
      <div class="name">
        <router-link
          :to="{
            name: 'playlistDetail',
            params: {
              uid: playlist.uid,
            },
          }"
        >
          <PlaylistName :playlist="playlist" />
        </router-link>
      </div>
      <div class="editor" v-if="playlist.editor">
        <router-link
          :to="{
            name: 'editorDetail',
            params: {
              uid: playlist.editor.uid,
            },
          }"
          v-text="playlist.editor.name"
        />
      </div>
      <ObjectTags class="tags" :obj="playlist" :limit="4" />
      <RelativeDateTime class="airplays" v-if="latestEmission" :date-time="latestEmission" />
      <Duration class="duration" :seconds="playlist.duration" :round-seconds="60 * 5" />
      <!--
      <div
        class="emissions"
      >
        {{ playlist.numEmissions }} Emissions
      </div>
      -->
      <div class="actions">
        <CircleButton :size="48" :outlined="false">
          <UserRating :obj-key="objKey" :icon-size="48" :hide-if-unset="!isHover" />
        </CircleButton>
        <ContextMenu :obj="playlist" />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/abstracts/responsive";
@use "@/style/elements/container";

.playlist-row {
  border-bottom: 1px solid rgb(var(--c-gray-200));
  transition: background 200ms;

  &:first-child {
    border-top: 1px solid rgb(var(--c-gray-200));
  }

  &:hover {
    background: rgb(var(--c-gray-100));
  }
}

.container {
  @include container.default;
  display: grid;
  grid-row-gap: 0;
  grid-column-gap: 1rem;
  grid-template-areas:
    "play name editor airplays actions"
    "play name tags   duration actions";
  grid-template-columns: 48px 8fr 5fr 3fr 48px;
  padding-top: 0.75rem;
  padding-bottom: 0.75rem;
  color: rgb(var(--c-black));

  > div {
    display: flex;
    align-items: center;
  }

  .play {
    grid-area: play;
  }

  .name {
    grid-area: name;
    @include typo.large;
    min-width: 0;
    > a {
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }
  }

  .editor {
    grid-area: editor;
    min-width: 0;
    > a {
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }
  }

  .tags {
    grid-area: tags;
    overflow: hidden;
  }

  .airplays {
    grid-area: airplays;
  }

  .emissions {
    grid-area: emissions;
  }

  .duration {
    grid-area: duration;
  }

  .actions {
    grid-area: actions;
    justify-self: flex-end;
  }
}
</style>
