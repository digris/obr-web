<script lang="ts">
import {
  computed,
  defineComponent,
} from 'vue';
import { useStore } from 'vuex';

import eventBus from '@/eventBus';
import CircleButton from '@/components/ui/button/CircleButton.vue';
import IconClose from '@/components/ui/icon/IconClose.vue';
import LazyImage from '@/components/ui/LazyImage.vue';
import MediaArtists from '@/components/catalog/media/MediaArtists.vue';
import Playhead from './Playhead.vue';
import ButtonPlay from '../button/ButtonPlay.vue';
import ButtonSkip from '../button/ButtonSkip.vue';

export default defineComponent({
  components: {
    CircleButton,
    IconClose,
    LazyImage,
    MediaArtists,
    Playhead,
    ButtonPlay,
    ButtonSkip,
  },
  props: {
    isVisible: {
      type: Boolean,
      default: false,
    },
    media: {
      type: Object,
    },
  },
  emits: [
    'close',
  ],
  setup(props, { emit }) {
    const store = useStore();
    const playerState = computed(() => store.getters['player/playerState']);
    const isLive = computed(() => playerState.value && playerState.value.isLive);
    const isPlaying = computed(() => playerState.value && playerState.value.isPlaying);
    const isBuffering = computed(() => playerState.value && playerState.value.isBuffering);
    const release = computed(() => {
      if (props.media && props.media.releases.length) {
        return props.media.releases[0];
      }
      return null;
    });
    const image = computed(() => {
      return (release.value && release.value.image) ? release.value.image : null;
    });
    const close = () => {
      emit('close');
    };
    const pause = () => {
      eventBus.emit('player:controls', { do: 'pause' });
    };
    const play = () => {
      eventBus.emit('player:controls', { do: 'resume' });
    };
    return {
      image,
      close,
      pause,
      play,
      isPlaying,
      isBuffering,
      isLive,
    };
  },
});
</script>

<template>
  <transition
    name="slide"
  >
    <div
      v-if="isVisible"
      class="player-panel"
    >
      <div
        class="header"
      >
        <CircleButton
          @click="close"
          :size="(48)"
          color-var="--c-fg"
        >
          <IconClose
            :size="(48)"
            color="rgb(var(--c-fg))"
          />
        </CircleButton>
      </div>
      <div
        class="visual"
      >
        <LazyImage
          :image="image"
          :ratio="1"
        />
      </div>
      <div
        class="metadata"
      >
        <router-link
          class="metadata--primary"
          @click="close"
          :to="{
            name: 'mediaDetail',
            params: {
              uid: media.uid,
            },
          }"
          v-text="media.name"
        />
        <div
          class="metadata--secondary"
        >
          <MediaArtists
            :artists="media.artists"
            :link="false"
          />
        </div>
      </div>
      <Playhead
        :disabled="isLive"
      />
      <div
        class="controls"
      >
        <ButtonSkip
          :rotate="180"
        />
        <ButtonPlay
          class="play-button"
          :is-playing="isPlaying"
          :is-buffering="isBuffering"
          @pause="pause"
          @play="play"
          :size="60"
          :outline-width="2"
          :outline-opacity="1"
        />
        <ButtonSkip
          :disabled="isLive"
        />
      </div>
    </div>
  </transition>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
.player-panel {
  position: fixed;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  height: calc(100% - 60px);
  padding: 0.5rem;
  color: rgb(var(--c-fg));
  background: rgb(var(--c-bg));
  transition: background 1000ms;
  .header {
    display: flex;
    align-items: flex-end;
    justify-content: flex-end;
    width: 100%;
    margin-bottom: 0.75rem;
  }
  .visual {
    width: calc(100% - 6rem);
    box-shadow: rgba(var(--c-fg), 0.05) 0 0 16px 0;

  }
  .metadata {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: 1rem 0;
    padding: 0 1rem;
    text-align: center;
    &--secondary {
      @include typo.dim;
    }
  }
  .controls {
    display: flex;
    align-items: center;
    .play-button {
      margin: 0 0.5rem;
    }
  }
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 200ms, opacity 200ms;
}
.slide-enter-from {
  transform: translate(0, 100%);
  opacity: 0;
}
.slide-leave-to {
  transform: translate(0, 100%);
}
</style>
