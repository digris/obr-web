<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import { useStore } from 'vuex';
import { DateTime } from 'luxon';
import eventBus from '@/eventBus';
import { getContrastColor } from '@/utils/color';
import { requireSubscription } from '@/utils/account';

import Debug from '@/components/dev/Debug.vue';
import CircleButton from '@/components/ui/button/CircleButton.vue';
import ContextMenu from '@/components/context-menu/ContextMenu.vue';
import ButtonPlay from '@/components/player/button/ButtonPlay.vue';
import MediaArtists from '@/components/catalog/media/MediaArtists.vue';
import MediaReleases from '@/components/catalog/media/MediaReleases.vue';
import UserRating from '@/components/rating/UserRating.vue';
import RelativeDateTime from '@/components/ui/date/RelativeDateTime.vue';
import Duration from '@/components/ui/time/Duration.vue';

export default defineComponent({
  props: {
    media: {
      type: Object,
      required: true,
    },
  },
  components: {
    Debug,
    CircleButton,
    ContextMenu,
    ButtonPlay,
    MediaArtists,
    MediaReleases,
    UserRating,
    RelativeDateTime,
    Duration,
  },
  setup(props) {
    const store = useStore();
    const objKey = computed(() => {
      return `${props.media.ct}:${props.media.uid}`;
    });
    const isHover = ref(false);
    const release = computed(() => {
      return (props.media.releases && props.media.releases.length) ? props.media.releases[0] : null;
    });
    const currentMedia = computed(() => {
      return store.getters['queue/currentMedia'];
    });
    const isCurrent = computed(() => {
      return currentMedia.value && (props.media.uid === currentMedia.value.uid);
    });
    const queuedMedia = computed(() => {
      return store.getters['queue/media'];
    });
    const isQueued = computed(() => {
      // @ts-ignore
      return queuedMedia.value.findIndex((i: object) => i.uid === props.media.uid) > -1;
    });
    const queuedIndex = computed(() => {
      return store.getters['queue/currentIndex'];
    });
    const queuePosition = computed(() => {
      if (queuedIndex.value < 0) {
        return null;
      }
      // @ts-ignore
      const index = queuedMedia.value.findIndex((i: object) => i.uid === props.media.uid);
      if (index < 0) {
        return null;
      }
      return index - queuedIndex.value;
    });
    const playerState = computed(() => {
      return isCurrent.value ? store.getters['player/playerState'] : null;
    });
    const isLive = computed(() => playerState.value && playerState.value.isLive);
    const isPlaying = computed(() => {
      return playerState.value && playerState.value.isPlaying && !isLive.value;
    });
    const isBuffering = computed(() => {
      return playerState.value && playerState.value.isBuffering && !isLive.value;
    });
    const latestAirplay = computed(() => {
      if (!props.media.latestAirplay) {
        return null;
      }
      return DateTime.fromISO(props.media.latestAirplay);
    });
    const currentOnairMedia = computed(() => {
      return store.getters['schedule/currentMedia'];
    });
    const isOnair = computed(() => {
      return currentOnairMedia.value && (props.media.uid === currentOnairMedia.value.uid);
    });
    const color = computed(() => {
      return (release.value && release.value.image) ? release.value.image.rgb : null;
    });
    const contrastColor = computed(() => {
      if (color.value && isCurrent.value && !isLive.value) {
        return getContrastColor(color.value);
      }
      return [0, 0, 0];
    });
    const cssVars = computed(() => {
      if (!color.value) {
        return {};
      }
      const rgb = color.value.join(',');
      const rgbContrast = contrastColor.value.join(',');
      return {
        '--c-color': rgb,
        '--c-contrast-color': rgbContrast,
      };
    });
    const buttonCssVars = computed(() => {
      if (color.value && isCurrent.value) {
        return {
          '--c-fg': color.value.join(','),
        };
      }
      return {
        '--c-fg': '0,0,0',
      };
    });
    const play = requireSubscription((media: object) => {
      const payload = {
        media: [media],
      };
      eventBus.emit('queue:controls:enqueue', payload);
    }, 'A plan is required.');
    const pause = () => {
      eventBus.emit('player:controls', { do: 'pause' });
    };
    return {
      objKey,
      isHover,
      release,
      color,
      contrastColor,
      cssVars,
      buttonCssVars,
      // playerState,
      isPlaying,
      isBuffering,
      isCurrent,
      isLive,
      isQueued,
      queuePosition,
      isOnair,
      latestAirplay,
      play,
      pause,
    };
  },
});
</script>

<template>
  <div
    class="media-row"
    :style="cssVars"
    :class="{
      'is-current': isCurrent,
      'is-onair': isOnair,
    }"
    @mouseenter="isHover=true"
    @mouseleave="isHover=false"
  >
    <Debug
      :visible="(false)"
      :value="media"
    />
    <div
      class="container"
    >
      <div
        class="play"
      >
        <ButtonPlay
          @play="play(media)"
          @pause="pause"
          :is-active="(isCurrent && !isLive)"
          :is-playing="isPlaying"
          :is-buffering="isBuffering"
          :style="buttonCssVars"
          :color="`rgb(${contrastColor.join(',')})`"
        />
        <div
          class="state"
        >
          <div
            class="state__on-air"
            v-if="isOnair"
          >R</div>
          <div
            class="state__queued"
            v-if="isQueued"
          >{{ queuePosition }}</div>
        </div>
      </div>
      <div
        class="name"
      >
        <router-link
          :to="{
            name: 'mediaDetail',
            params: {
              uid: media.uid,
            },
          }"
        >
          {{ media.name }}
        </router-link>
      </div>
      <div
        class="artist"
      >
        <MediaArtists
          :artists="media.artists"
        />
      </div>
      <div
        class="release"
      >
        <MediaReleases
          :releases="media.releases"
        />
      </div>
      <div
        class="airplays"
      >
        <RelativeDateTime
          v-if="latestAirplay"
          :date-time="latestAirplay"
        />
      </div>
      <Duration
        class="duration"
        :seconds="media.duration"
      />
      <div
        class="actions"
      >
        <CircleButton
          :size="(48)"
          :outlined="(false)"
        >
          <UserRating
            :obj-key="objKey"
            :icon-size="48"
            :hide-if-unset="(!isHover)"
          />
        </CircleButton>
        <!--
        <CircleButton
          :size="(48)"
          :outlined="(false)"
        >
          <IconContext
            :size="48"
          />
        </CircleButton>
        -->
        <ContextMenu
          :obj="media"
        />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/abstracts/responsive";
@use "@/style/elements/container";

.media-row {
  border-bottom: 1px solid rgb(var(--c-gray-200));
  transition: background 200ms;

  &:first-child {
    border-top: 1px solid rgb(var(--c-gray-200));
  }

  @include responsive.hover-supported {
    &:hover {
      background: rgb(var(--c-gray-100));
    }
  }
}

.container {
  @include container.default;
  display: grid;
  grid-row-gap: 0;
  grid-column-gap: 1rem;
  grid-template-areas:
    "play name artist  duration actions"
    "play name release airplays actions";
  grid-template-columns: 1fr 8fr 5fr 2fr 2fr;
  padding-top: 0.75rem;
  padding-bottom: 0.75rem;
  color: rgb(var(--c-black));
  //TODO: find a modular way to handle color / ui transitions
  transition: border-bottom 200ms 1400ms, color 200ms, background 200ms;

  > div {
    display: flex;
    align-items: center;
  }

  .play {
    position: relative;
    grid-area: play;
    //padding-left: 0.5rem;

    .state {
      position: absolute;
      top: 1px;
      right: 0;
      font-size: 8px;
      font-family: monospace;
      -webkit-font-smoothing: none;
      &__onair {
        color: red;
      }
      &__queued {
        color: black;
      }
    }
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

  .artist {
    grid-area: artist;
    overflow: hidden;
  }

  .release {
    grid-area: release;
    min-width: 0;
    > a {
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }
  }

  .airplays {
    grid-area: airplays;
  }

  .duration {
    grid-area: duration;
  }

  .actions {
    grid-area: actions;
    justify-self: flex-end;
  }
  // TODO: responsive styles have to be cleaned up
  @include responsive.bp-small {
    grid-template-areas:
      "play name   actions"
      "play artist actions";
    grid-template-columns: 48px 1fr 96px;
    padding: 0.375rem 0;
    .name {
      @include typo.default;
    }
    .artist {
      @include typo.default;
      @include typo.dim;
      @include typo.light;
      min-width: 0;
      margin-top: -4px; //TODO: just a quick fix
      overflow: hidden;
      > div {
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
      }
    }
    .release,
    .airplays,
    .duration {
      display: none;
    }
  }
}
</style>
