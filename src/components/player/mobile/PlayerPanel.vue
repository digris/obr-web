<script lang="ts">
import { computed, defineComponent } from "vue";

import { usePlayerState, usePlayerControls } from "@/composables/player";
import { useQueueControls } from "@/composables/queue";
import CircleButton from "@/components/ui/button/CircleButton.vue";
import IconClose from "@/components/ui/icon/IconClose.vue";
import LazyImage from "@/components/ui/LazyImage.vue";
import MediaArtists from "@/components/catalog/media/MediaArtists.vue";
import ButtonPlay from "../button/ButtonPlay.vue";
import ButtonSkip from "../button/ButtonSkip.vue";
import Playhead from "./Playhead.vue";

export default defineComponent({
  components: {
    CircleButton,
    IconClose,
    LazyImage,
    MediaArtists,
    ButtonPlay,
    ButtonSkip,
    Playhead,
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
  emits: ["close"],
  setup(props, { emit }) {
    const { isLive, isPlaying, isBuffering } = usePlayerState();
    const { resume, pause } = usePlayerControls();
    const { hasPrevious, hasNext, playPrevious, playNext } = useQueueControls();
    const release = computed(() => {
      if (props.media && props.media.releases.length) {
        return props.media.releases[0];
      }
      return null;
    });
    const image = computed(() => {
      return release.value && release.value.image ? release.value.image : null;
    });
    const close = () => {
      emit("close");
    };
    return {
      image,
      close,
      pause,
      play: resume,
      isPlaying,
      isBuffering,
      isLive,
      hasPrevious,
      hasNext,
      playPrevious,
      playNext,
    };
  },
});
</script>

<template>
  <transition name="slide">
    <div v-if="isVisible" class="player-panel">
      <div class="header">
        <CircleButton @click="close" color-var="--c-fg">
          <IconClose />
        </CircleButton>
      </div>
      <div class="visual">
        <LazyImage :image="image" :ratio="1" />
      </div>
      <div class="metadata">
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
        <div class="metadata--secondary">
          <MediaArtists :artists="media.artists" :link="false" />
        </div>
      </div>
      <Playhead :disabled="isLive" />
      <div class="controls">
        <ButtonSkip :disabled="!hasPrevious" :rotate="180" @click.prevent="playPrevious" />
        <ButtonPlay
          class="play-button"
          :is-playing="isPlaying"
          :is-buffering="isBuffering"
          :outline-width="2"
          :outline-opacity="1"
          @pause="pause"
          @play="play"
        />
        <ButtonSkip :disabled="!hasNext" @click.prevent="playNext" />
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
