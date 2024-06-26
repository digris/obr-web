<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import { DateTime } from "luxon";

import PlayAction from "@/components/catalog/actions/PlayAction.vue";
import PlaylistName from "@/components/catalog/playlist/Name.vue";
import ContextMenu from "@/components/context-menu/ContextMenu.vue";
import UserRating from "@/components/rating/UserRating.vue";
import ObjectTags from "@/components/tagging/ObjectTags.vue";
import CircleButton from "@/components/ui/button/CircleButton.vue";
import RelativeDateTime from "@/components/ui/date/RelativeDateTime.vue";
import Duration from "@/components/ui/time/Duration.vue";
import { useDevice } from "@/composables/device";
import { useObjKey } from "@/composables/obj";
import { useSettings } from "@/composables/settings";

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
    const { objKey } = useObjKey(props.playlist);
    const { isMobile } = useDevice();
    const { darkMode } = useSettings();
    const isHover = ref(isMobile);
    const link = `/discover/playlists/${props.playlist.uid}/`;
    const latestEmission = computed(() => {
      return DateTime.fromISO(props.playlist.latestEmissionTimeStart);
    });
    const title = computed(() => {
      return {
        name: props.playlist.series ? props.playlist.series.name : props.playlist.name,
        // appendix: props.playlist.series ? props.playlist.series.episode : null,
        appendix: latestEmission.value,
      };
    });
    return {
      objKey,
      isHover,
      isMobile,
      darkMode,
      title,
      link,
      latestEmission,
    };
  },
});
</script>

<template>
  <div
    class="playlist-row"
    @mouseenter="isMobile ? null : (isHover = true)"
    @mouseleave="isMobile ? null : (isHover = false)"
  >
    <div class="container">
      <div class="play">
        <PlayAction
          :obj-key="objKey"
          :outlined="true"
          :color="darkMode ? [255, 255, 255] : [0, 0, 0]"
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
          <!--<PlaylistName :playlist="playlist" :airtime="latestEmission" />-->
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
      <Duration class="duration" :seconds="playlist.duration" :round-seconds="60 * 5" />
      <RelativeDateTime class="airplays" v-if="latestEmission" :date-time="latestEmission" />
      <div class="actions">
        <CircleButton>
          <UserRating :obj-key="objKey" :hide-if-unset="!isHover" />
        </CircleButton>
        <ContextMenu :obj="playlist" />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/responsive";
@use "@/style/elements/container";
@use "@/style/elements/list-row";

.playlist-row {
  @include list-row.default;
}

.container {
  @include container.default;

  display: grid;
  grid-row-gap: 0;
  grid-column-gap: 1rem;
  grid-template-areas:
    "play name editor duration actions"
    "play name tags   airplays actions";
  grid-template-columns: 96px 16fr 10fr 6fr 96px;
  padding-top: 0.7rem;
  padding-bottom: 0.7rem;
  color: rgb(var(--c-dark));

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
    margin-left: -48px;

    > a {
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }
  }

  .editor {
    grid-area: editor;
    align-self: end;
    min-width: 0;

    > a {
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }
  }

  .tags {
    grid-area: tags;
    align-self: start;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }

  .airplays {
    grid-area: airplays;
    align-self: end;
    overflow: hidden;
  }

  .duration {
    grid-area: duration;
  }

  .actions {
    grid-area: actions;
    justify-self: flex-end;
  }

  @include responsive.bp-medium {
    grid-template-areas:
      "play name   actions"
      "play tags actions";
    grid-template-columns: 80px 1fr 80px;
    height: 60px;

    .editor,
    .airplays,
    .duration {
      display: none;
    }

    .name {
      align-self: end;
      margin-left: -40px;
    }

    .tags {
      align-self: start;
      margin-left: -40px;

      @include typo.light;
      @include typo.dim;
    }
  }
}
</style>
