<script lang="ts">
import { computed, defineComponent, ref, watch } from "vue";
import { useEventListener } from "@vueuse/core";
import { useSwipe } from "@vueuse/core";
import { getContrastColor } from "@/utils/color";
import { usePlayerControls, usePlayerState } from "@/composables/player";
import LazyImage from "@/components/ui/LazyImage.vue";
import CircleButton from "@/components/ui/button/CircleButton.vue";
import IconClose from "@/components/ui/icon/IconClose.vue";
import UserRating from "@/components/rating/UserRating.vue";
import CurrentMedia from "./CurrentMedia.vue";
import Playhead from "./Playhead.vue";
import PlayerControl from "./PlayerControl.vue";
import { useRoute } from "vue-router";

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
    const { media, color, image } = usePlayerState();
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
    return {
      el,
      top,
      close,
      //
      objKey,
      media,
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
    <div
      v-if="isVisible"
      :style="{ top: `${top}px` }"
      class="player-panel"
      :class="{ 'is-swiping': isSwiping }"
    >
      <nav>
        <CircleButton @click="close" :outlined="true">
          <IconClose />
        </CircleButton>
      </nav>
      <main>
        <div class="visual">
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
          <UserRating color-var="--c-fg" :obj-key="objKey" :icon-scale="1.25" />
        </div>
      </main>
    </div>
  </transition>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/abstracts/responsive";
@use "@/style/elements/container";
// NOTE: color variables are set in parent Player component
.player-panel {
  z-index: 20;
  position: fixed;
  width: 100%;
  min-height: calc(100% + 60px);
  //top: 0;
  left: 0;
  bottom: 0;
  background: rgb(var(--c-bg));
  display: flex;
  flex-direction: column;
  transition: top 200ms, background 500ms;
  &.is-swiping {
    transition-duration: 1ms;
    background: rgba(var(--c-bg), 0.95);
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
      width: 70vw;
      aspect-ratio: 1;
      box-shadow: 0 0 20px rgba(0, 0, 0, 0.4);
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
      min-height: 32px;
    }
    .controls {
      width: 100%;
      padding: 0 0.625rem;
      display: grid;
      grid-template-columns: 40px 1fr 40px;
      align-items: center;
      justify-content: center;
      .player-control {
        grid-column: 2/3;
        justify-self: center;
      }
      .user-rating {
      }
    }
  }
}

// panel transition
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
