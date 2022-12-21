<script lang="ts">
import { computed, defineComponent, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { useEventListener, useSwipe } from "@vueuse/core";

import UserRating from "@/components/rating/UserRating.vue";
import CircleButton from "@/components/ui/button/CircleButton.vue";
import IconClose from "@/components/ui/icon/IconClose.vue";
import LazyImage from "@/components/ui/LazyImage.vue";
import { usePlayerControls, usePlayerState } from "@/composables/player";
import { getContrastColor } from "@/utils/color";
import { preloadImage } from "@/utils/image";

import CurrentMedia from "./CurrentMedia.vue";
import PlayerControl from "./PlayerControl.vue";
import Playhead from "./Playhead.vue";

export default defineComponent({
  components: {
    LazyImage,
    CircleButton,
    IconClose,
    UserRating,
    CurrentMedia,
    Playhead,
    PlayerControl,
  },
  props: {
    isVisible: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["close"],
  setup(props, { emit }) {
    const el = ref<HTMLElement | null>(null);
    const { media, nextMedia, color, image } = usePlayerState();
    const { seek } = usePlayerControls();
    const route = useRoute();
    const close = () => emit("close");
    watch(() => route.path, close);
    useEventListener(document, "keydown", (e) => {
      if (e.code === "KeyX") {
        close();
      }
    });
    const top = ref(0);
    const objKey = computed(() => {
      if (!media.value) {
        return null;
      }
      return `${media.value?.ct}:${media.value?.uid}`;
    });
    const fgColor = computed(() => {
      try {
        const bg = color.value;
        return getContrastColor(bg);
      } catch (e) {
        console.warn(e);
      }
      return [128, 128, 128];
    });
    const { isSwiping, direction, lengthY } = useSwipe(el, {
      passive: false,
      onSwipe() {
        top.value = Math.max(lengthY.value * -1, 0);
      },
      onSwipeEnd() {
        if (lengthY.value < -150) {
          top.value = 700;
          setTimeout(() => {
            top.value = 0;
            close();
          }, 200);
        } else {
          top.value = 0;
        }
      },
    });
    // NOTE: preload upcoming images
    const nextImage = computed(() => {
      return nextMedia.value?.releases?.length ? nextMedia.value.releases[0].image : null;
    });
    watch(
      () => nextImage.value,
      (imageObj) => preloadImage(imageObj)
    );
    return {
      el,
      top,
      close,
      //
      objKey,
      media,
      nextImage,
      image,
      fgColor,
      //
      isSwiping,
      direction,
      lengthY,
      //
      seek,
    };
  },
});
</script>

<template>
  <transition name="slide" :duration="200">
    <div v-if="isVisible" class="player-panel" :class="{ 'is-swiping': isSwiping }">
      <nav>
        <CircleButton @click="close" :outlined="true">
          <IconClose />
        </CircleButton>
      </nav>
      <main>
        <div class="visual">
          <!--
          <LazyImage class="next" v-if="nextImage" :image="nextImage" />
          -->
          <LazyImage :image="image" />
        </div>
        <div class="meta">
          <CurrentMedia :media="media" />
        </div>
        <div class="playhead-container">
          <Playhead @seek="seek" />
        </div>
        <div class="controls">
          <PlayerControl :fg-color="fgColor" />
          <UserRating color-var="--c-fg" :obj-key="objKey" />
        </div>
      </main>
    </div>
  </transition>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/responsive";
@use "@/style/elements/container";

// NOTE: color variables are set in parent Player component
.player-panel {
  z-index: 20;
  top: var(--sa-t);
  position: fixed;
  width: 100%;
  min-height: calc(100% + 60px);
  left: 0;
  bottom: 0;
  background: rgb(var(--c-bg));
  display: flex;
  flex-direction: column;
  transition: top 200ms, background 500ms;
  box-shadow: 0 -4px 8px 4px rgb(0 0 0 / 10%);
  border-top-left-radius: 28px;
  border-top-right-radius: 28px;

  &.is-swiping {
    transition-duration: 1ms;
    background: rgb(var(--c-bg) / 95%);
  }

  > nav {
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: end;
    padding: 0.625rem;
  }

  > main {
    display: flex;
    row-gap: 1rem;
    flex-direction: column;
    align-items: center;
    padding: 0.625rem;
    color: rgb(var(--c-fg));

    .visual {
      position: relative;
      width: 70vw;
      aspect-ratio: 1;
      box-shadow: 0 0 20px rgb(0 0 0 / 40%);

      .next {
        top: 0;
        position: absolute;
        opacity: 0;
      }
    }

    .meta {
      display: flex;
      align-items: center;
      justify-content: center;

      :deep(.metadata) {
        align-items: center;
      }

      height: 32px;
    }

    .playhead-container {
      width: 100%;
      min-height: 42px;
    }

    .controls {
      width: 100%;
      display: grid;
      grid-template-columns: 40px 1fr 40px;
      align-items: center;
      justify-content: center;

      .player-control {
        grid-column: 2/3;
        justify-self: center;
      }
    }
  }
}

// transitions
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
