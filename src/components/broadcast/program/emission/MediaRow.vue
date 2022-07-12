<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import { DateTime } from "luxon";

import PlayAction from "@/components/catalog/actions/PlayAction.vue";
import ContextMenu from "@/components/context-menu/ContextMenu.vue";
import MediaArtists from "@/components/catalog/media/MediaArtists.vue";
import MediaReleases from "@/components/catalog/media/MediaReleases.vue";
import UserRating from "@/components/rating/UserRating.vue";
import CircleButton from "@/components/ui/button/CircleButton.vue";

export default defineComponent({
  components: {
    PlayAction,
    ContextMenu,
    MediaArtists,
    MediaReleases,
    UserRating,
    CircleButton,
  },
  props: {
    emissionMedia: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const isHover = ref(false);
    const media = computed(() => {
      return props.emissionMedia?.media;
    });
    const objKey = computed(() => {
      return `catalog.media:${media.value.uid}`;
    });
    const timeStart = computed(() => {
      return DateTime.fromISO(props.emissionMedia.timeStart);
    });
    const timeStartDisplay = computed(() => {
      return timeStart.value.setLocale("de-ch").toLocaleString(DateTime.TIME_24_SIMPLE);
    });
    return {
      media,
      objKey,
      isHover,
      timeStartDisplay,
    };
  },
});
</script>

<template>
  <div class="media-row" @mouseenter="isHover = true" @mouseleave="isHover = false">
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
          name: 'mediaDetail',
          params: {
            uid: media.uid,
          },
        }"
        v-text="media.name"
      />
      <!--
      <span>{{ media.name }}</span>
      -->
    </div>
    <div class="artist">
      <MediaArtists :artists="media.artists" :link="false" />
    </div>
    <div class="release">
      <MediaReleases :releases="media.releases" />
    </div>
    <div class="time-start">
      {{ timeStartDisplay }}
    </div>
    <div class="actions">
      <CircleButton :size="48" :outlined="false">
        <UserRating :obj-key="objKey" :icon-size="48" :autoload="true" :hide-if-unset="!isHover" />
      </CircleButton>
      <ContextMenu :obj="media" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/abstracts/responsive";
@use "@/style/elements/container";

.media-row {
  @include container.default;
  display: grid;
  grid-row-gap: 0;
  grid-column-gap: 1rem;
  grid-template-areas:
    "play name editor  time-start actions"
    "play name tags    time-start actions";
  grid-template-columns: 48px 9fr 8fr 2fr 96px;
  padding: 0.75rem 1.5rem 0.75rem 1rem;
  color: rgb(var(--c-black));
  //background-color: rgb(var(--c-white));

  > div {
    display: flex;
    align-items: center;
  }

  .play {
    position: relative;
    grid-area: play;
    max-height: 48px;
  }

  .name {
    grid-area: name;
    @include typo.large;
    min-width: 0;
    > a,
    > span {
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }
  }

  .editor {
    grid-area: editor;
    overflow: hidden;
  }

  .tags {
    grid-area: tags;
  }

  .time-start {
    grid-area: time-start;
    @include typo.large;
    justify-content: flex-end;
  }

  .actions {
    grid-area: actions;
  }
}
</style>
