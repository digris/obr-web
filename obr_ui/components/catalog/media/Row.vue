<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import { DateTime } from "luxon";

import PlayAction from "@/components/catalog/actions/PlayAction.vue";
import MediaArtists from "@/components/catalog/media/MediaArtists.vue";
import MediaReleases from "@/components/catalog/media/MediaReleases.vue";
import ContextMenu from "@/components/context-menu/ContextMenu.vue";
import UserRating from "@/components/rating/UserRating.vue";
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
    MediaArtists,
    MediaReleases,
    UserRating,
    RelativeDateTime,
    Duration,
  },
  props: {
    media: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const { objKey } = useObjKey(props.media);
    const { isMobile } = useDevice();
    const { darkMode, userSettings } = useSettings();
    const testingEnabled = computed(() => userSettings.value?.testingEnabled);
    const isHover = ref(isMobile);
    const release = computed(() => {
      return props.media.releases && props.media.releases.length ? props.media.releases[0] : null;
    });
    const latestAirplay = computed(() => {
      if (!props.media.latestAirplay) {
        return null;
      }
      return DateTime.fromISO(props.media.latestAirplay);
    });
    const color = computed(() => {
      return release.value && release.value.image ? release.value.image.rgb : null;
    });
    return {
      objKey,
      testingEnabled,
      isMobile,
      darkMode,
      isHover,
      release,
      color,
      latestAirplay,
    };
  },
});
</script>

<template>
  <div
    class="media-row"
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
        <div
          v-if="testingEnabled"
          class="license"
          :class="`license--${media.license}`"
          v-text="media.license.charAt(0)"
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
        <div v-if="media.lyricsExplicit === 'explicit'" class="lyrics-explicit">
          <span title="Explicit lyrics">E</span>
        </div>
      </div>
      <div class="artist">
        <MediaArtists :artists="media.artists" />
      </div>
      <div class="release">
        <MediaReleases :releases="media.releases" />
      </div>
      <div class="airplays">
        <RelativeDateTime v-if="latestAirplay" :date-time="latestAirplay" />
      </div>
      <Duration class="duration" :seconds="media.duration" />
      <div class="actions">
        <CircleButton>
          <UserRating :obj-key="objKey" :hide-if-unset="!isHover" />
        </CircleButton>
        <ContextMenu :obj="media" />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/responsive";
@use "@/style/elements/container";
@use "@/style/elements/list-row";

.media-row {
  @include list-row.default;
}

.container {
  @include container.default;

  display: grid;
  grid-row-gap: 0;
  grid-column-gap: 1rem;
  grid-template-areas:
    "play name artist  duration actions"
    "play name release airplays actions";
  grid-template-columns: 96px 16fr 10fr 6fr 96px;
  height: 71px;
  color: rgb(var(--c-dark));
  transition: border-bottom 200ms 1400ms, color 200ms, background 200ms;

  > div {
    display: flex;
    align-items: center;
  }

  .play {
    position: relative;
    grid-area: play;

    & > .license {
      top: 6px;
      position: absolute;
      font-size: 8px;
      font-family: monospace;
      font-weight: 600;
      left: 0;
      color: currentcolor;
      text-transform: uppercase;
      display: none;

      &--major,
      &--major_root {
        display: block;
        color: rgb(var(--c-red));
      }

      &--independent {
        display: block;
        color: rgb(var(--c-green));
      }
    }
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

    .lyrics-explicit {
      position: relative;
      display: flex;

      > span {
        @include typo.light;

        top: -10px;
        position: absolute;
        display: inline-flex;
        padding-left: 0.25em;
        font-size: 10px;

        @include responsive.bp-medium-up {
          font-size: 12px;
          padding-left: 0.5em;
          top: -16px;
        }
      }
    }
  }

  .artist {
    grid-area: artist;
    align-self: end;
    overflow: hidden;

    > div {
      overflow: hidden;
    }
  }

  .release {
    grid-area: release;
    align-self: start;
    min-width: 0;

    > div {
      overflow: hidden;
    }
  }

  .duration {
    grid-area: duration;
    align-self: end;
  }

  .airplays {
    grid-area: airplays;
    align-self: start;
    overflow: hidden;
  }

  .actions {
    grid-area: actions;
    justify-self: flex-end;
  }

  @include responsive.bp-medium {
    grid-template-areas:
      "play name   actions"
      "play artist actions";
    grid-template-columns: 80px 1fr 80px;
    height: 60px;

    .release,
    .airplays,
    .duration {
      display: none;
    }

    .name {
      align-self: end;
      margin-left: -40px;
    }

    .artist {
      align-self: start;
      margin-left: -40px;

      @include typo.light;
      @include typo.dim;
    }
  }
}
</style>
