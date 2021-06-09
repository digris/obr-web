<script lang="ts">
import { defineComponent, computed } from 'vue';
import { useStore } from 'vuex';
import { DateTime } from 'luxon';
import eventBus from '@/eventBus';
import { getContrastColor } from '@/utils/color';
import { requireSubscription } from '@/utils/account';

import PlayerControlIcon from '@/components/player/PlayerControlIcon.vue';
import MediaArtists from '@/components/catalog/media/MediaArtists.vue';
import UserRating from '@/components/rating/UserRating.vue';

export default defineComponent({
  props: {
    media: {
      type: Object,
      required: true,
    },
  },
  components: {
    PlayerControlIcon,
    MediaArtists,
    UserRating,
  },
  setup(props) {
    const store = useStore();
    const objKey = computed(() => {
      return `${props.media.ct}:${props.media.uid}`;
    });
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
    const playerState = computed(() => {
      return isCurrent.value ? store.getters['player/playerState'] : null;
    });
    const duration = computed(() => {
      return new Date(props.media.duration * 1000).toISOString().substr(11, 8);
    });
    const latestAirplay = computed(() => {
      if (!props.media.latestAirplay) {
        return null;
      }
      const dt = DateTime.fromISO(props.media.latestAirplay);
      return dt.toFormat('HH:mm yyyy-LL-dd');
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
    const cssVars = computed(() => {
      if (!color.value) {
        return {};
      }
      const rgb = color.value.join(',');
      const rgbContrast = getContrastColor(color.value).join(',');
      return {
        '--c-color': rgb,
        '--c-contrast-color': rgbContrast,
      };
    });
    const controls = requireSubscription((media: object) => {
      const payload = {
        mode: 'replace',
        media: [media],
      };
      // NOTE: hm - this is not very nice...
      store.dispatch('queue/updateQueue', payload);
      eventBus.emit('queue:controls:startPlayCurrent');
    }, 'A subscription is required...');
    return {
      objKey,
      release,
      color,
      cssVars,
      duration,
      playerState,
      isCurrent,
      isQueued,
      isOnair,
      latestAirplay,
      controls,
    };
  },
});
</script>

<template>
  <div
    class="media-row"
    :style="cssVars"
    :class="{'is-current': isCurrent, 'is-onair': isOnair}"
  >
    <div class="play">
      <PlayerControlIcon
        @click="controls(media)"
        :player-state="playerState"
      />
      <div
        class="state"
      >
        <div>
          <span
            v-if="isOnair"
          >A</span>
        </div>
        <div>
          <span
            v-if="isQueued"
          >Q</span>
        </div>
      </div>
    </div>
    <div
      class="name"
    >
      {{ media.name }}
    </div>
    <div class="artist">
      <MediaArtists
        :artists="media.artists"
      />
    </div>
    <div class="airplays">
      <span
        v-if="latestAirplay"
        :title="`Total: ${media.numAirplays}`"
      >{{ latestAirplay }}</span>
    </div>
    <div class="duration">
      {{ duration }}
    </div>
    <div class="rating">
      <UserRating
        :obj-key="objKey"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
.media-row {
  display: grid;
  grid-row-gap: 0.25rem;
  grid-column-gap: 1rem;
  grid-template-areas:
    "play name   duration rating"
    "play artist airplays rating";
  grid-template-columns: 1fr 9fr 3fr 1fr;
  padding: 0.5rem 0;
  border-bottom: 2px solid rgb(var(--c-live-fg));
  //TODO: find a modular way to handle color / ui transitions
  transition: border-bottom 200ms 1400ms, color 200ms, background 200ms;
  &:hover {
    color: rgb(var(--c-contrast-color));
    background: rgb(var(--c-color));
  }
  > div {
    display: flex;
    align-items: center;
  }
  .play {
    grid-area: play;
    padding-left: 0.5rem;
  }
  .name {
    grid-area: name;
    @include typo.large;
  }
  .artist {
    grid-area: artist;
    @include typo.dim(0.5);
  }
  .airplays {
    grid-area: airplays;
    @include typo.small;
  }
  .duration {
    grid-area: duration;
    @include typo.small;
    @include typo.dim;
  }
  .rating {
    grid-area: rating;
  }
  &.is-current {
    background: rgba(var(--c-live-fg), 0.1);
  }
}
.play {
  .state {
    display: grid;
    grid-template-columns: 12px 12px;
    margin-left: 0.5rem;
    font-size: 90%;
    opacity: 0.5;
  }
}
</style>
