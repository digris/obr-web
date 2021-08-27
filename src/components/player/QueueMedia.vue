<script lang="ts">
import { computed, defineComponent } from 'vue';
import { useStore } from 'vuex';
import { getContrastColor, getMediaColor } from '@/utils/color';
import eventBus from '@/eventBus';
import queue from '@/player/queue';
import CircleButton from '@/components/ui/button/CircleButton.vue';
import IconClose from '@/components/ui/icon/IconClose.vue';
import ButtonPlay from '@/components/player/button/ButtonPlay.vue';
import MediaArtists from '@/components/catalog/media/MediaArtists.vue';
import MediaReleases from '@/components/catalog/media/MediaReleases.vue';
import UserRating from '@/components/rating/UserRating.vue';

export default defineComponent({
  components: {
    CircleButton,
    ButtonPlay,
    MediaArtists,
    MediaReleases,
    UserRating,
    IconClose,
  },
  props: {
    media: {
      type: Object,
    },
    index: {
      type: Number,
      required: true,
    },
    isCurrent: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const store = useStore();
    const objKey = computed(() => {
      return `${props.media?.ct}:${props.media?.uid}`;
    });
    // TODO: this is quite a lot duplicate logic as in catalog/media/Row.vue
    // it eventually would be better to combine it in a central place.
    const playerState = computed(() => {
      return props.isCurrent ? store.getters['player/playerState'] : null;
    });
    const isLive = computed(() => playerState.value && playerState.value.isLive);
    const isPlaying = computed(() => {
      return playerState.value && playerState.value.isPlaying && !isLive.value;
    });
    const isBuffering = computed(() => {
      return playerState.value && playerState.value.isBuffering && !isLive.value;
    });
    const color = computed(() => {
      // @ts-ignore
      return getMediaColor(props.media);
    });
    const contrastColor = computed(() => {
      if (color.value && props.isCurrent && !isLive.value) {
        return getContrastColor(color.value);
      }
      return [255, 255, 255];
    });
    const buttonCssVars = computed(() => {
      if (color.value && props.isCurrent) {
        return {
          '--c-fg': color.value.join(','),
        };
      }
      return {
        '--c-fg': '0,0,0',
      };
    });
    const play = async () => {
      await queue.playFromIndex(props.index);
    };
    const pause = () => {
      eventBus.emit('player:controls', { do: 'pause' });
    };
    const remove = async () => {
      await queue.removeAtIndex(props.index);
    };
    return {
      objKey,
      playerState,
      isPlaying,
      isBuffering,
      buttonCssVars,
      contrastColor,
      play,
      pause,
      remove,
    };
  },
});
</script>

<template>
  <div
    class="media-row"
    :style="{
      '--c-fg': 'var(--c-white)',
      '--c-bg': 'var(--c-black)',
    }"
    :class="{
      'is-current': isCurrent,
    }"
  >
    <div
      class="play"
    >
      <ButtonPlay
        @click="play"
        @pause="pause"
        :is-active="(isCurrent)"
        :is-playing="isPlaying"
        :is-buffering="isBuffering"
        :style="buttonCssVars"
        :color="`rgb(${contrastColor.join(',')})`"
      />
    </div>
    <div
      class="name"
    >
      <span>{{ media.name }}</span>
    </div>
    <div
      class="artist"
    >
      <MediaArtists
        :link="(false)"
        :artists="media.artists"
      />
    </div>
    <div
      class="release"
    >
      <MediaReleases
        :link="(false)"
        :releases="media.releases"
      />
    </div>
    <div
      class="actions"
    >
      <CircleButton
        color-var="--c-white"
        :size="(48)"
        :outlined="(false)"
      >
        <UserRating
          color-var="--c-fg"
          :obj-key="objKey"
          :icon-size="24"
        />
      </CircleButton>
      <CircleButton
        color-var="--c-fg"
        @click="remove"
        :disabled="isCurrent"
        :size="(48)"
        :outlined="(true)"
      >
        <IconClose
          color="rgb(var(--c-fg))"
          :size="36"
        />
      </CircleButton>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/abstracts/responsive";
.media-row {
  display: grid;
  grid-row-gap: 0;
  grid-column-gap: 1rem;
  grid-template-areas:
    "play name artist  actions"
    "play name release actions";
  grid-template-columns: 1fr 8fr 5fr 4fr;
  padding: 0.75rem 0;

  > div {
    display: flex;
    align-items: center;
  }

  .play {
    grid-area: play;
    padding-left: 0.5rem;

    .state {
      display: grid;
      grid-template-columns: 12px 12px;
      margin-left: 0.5rem;
      font-size: 90%;
      opacity: 0.5;
    }
  }

  .name {
    grid-area: name;
    @include typo.large;
    min-width: 0;
    > span {
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
    > span {
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }
  }

  .actions {
    grid-area: actions;
    justify-self: flex-end;
  }
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
    //TODO: just a quick fix
    .play,
    .actions {
      transform: scale(calc(40 / 48));
    }
    .release,
    .airplays,
    .duration {
      display: none;
    }
  }
}
</style>
