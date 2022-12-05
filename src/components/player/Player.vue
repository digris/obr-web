<script lang="ts">
import { computed, defineComponent, ref } from "vue";

import UserRating from "@/components/rating/UserRating.vue";
import { usePlayerControls, usePlayerState } from "@/composables/player";
import { useQueueState } from "@/composables/queue";
import { getContrastColor } from "@/utils/color";

import Bandwidth from "./button/Bandwidth.vue";
import Circle from "./button/Circle.vue";
import OnAir from "./button/OnAir.vue";
import CurrentMedia from "./CurrentMedia.vue";
import PlayerControl from "./PlayerControl.vue";
import Playhead from "./Playhead.vue";
import Queue from "./Queue.vue";
import QueueControl from "./QueueControl.vue";
import VolumeControl from "./VolumeControl.vue";

export default defineComponent({
  components: {
    CurrentMedia,
    Playhead,
    OnAir,
    Bandwidth,
    Circle,
    Queue,
    UserRating,
    PlayerControl,
    VolumeControl,
    QueueControl,
  },
  setup() {
    const { queueLength } = useQueueState();
    const { seek } = usePlayerControls();
    const { media, color, isLive } = usePlayerState();
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
    const cssVars = computed(() => {
      try {
        const bg = color.value;
        const fg = getContrastColor(bg);
        const fgInverse = getContrastColor(fg);
        const colors = {
          "--c-bg": bg.join(" "),
          "--c-fg": fg.join(" "),
          "--c-fg-inverse": fgInverse.join(" "),
        };
        return colors;
      } catch (e) {
        console.warn(e);
      }
      return {
        "--c-bg": isLive.value ? "255 255 255" : "0 0 0",
        "--c-fg": isLive.value ? "0 0 0" : "255 255 255",
        "--c-fg-inverse": isLive.value ? "255 255 255" : "0 0 0",
      };
    });
    const queueVisible = ref(false);
    const hideQueue = () => {
      queueVisible.value = false;
    };
    const toggleQueue = () => {
      queueVisible.value = !queueVisible.value;
    };
    return {
      media,
      objKey,
      fgColor,
      cssVars,
      queueVisible,
      queueLength,
      hideQueue,
      toggleQueue,
      //
      seek,
    };
  },
});
</script>

<template>
  <Queue :is-visible="queueVisible && queueLength > 0" @close="hideQueue" />
  <transition name="slide">
    <div v-if="media" class="player" :style="cssVars">
      <Playhead class="playhead" @seek="seek" />
      <div class="container">
        <div class="left">
          <CurrentMedia :media="media" />
        </div>
        <div class="center">
          <PlayerControl :fg-color="fgColor" />
        </div>
        <div class="right">
          <OnAir />
          <Bandwidth />
          <VolumeControl />
          <Circle>
            <UserRating color-var="--c-fg" :obj-key="objKey" />
          </Circle>
          <QueueControl
            :queue-visible="queueVisible"
            :num-queued="queueLength"
            @toggle-visibility="toggleQueue"
          />
        </div>
      </div>
    </div>
  </transition>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";

$player-height: 72px;

.queue {
  z-index: 30;
}

.player {
  position: fixed;
  height: $player-height;
  width: 100%;
  bottom: 0;
  z-index: 110;
  color: rgba(var(--c-fg));
  background: rgba(var(--c-bg));
  transition: background 1000ms;
}

.playhead {
  position: absolute;
  bottom: 54px;
}

.container {
  @include container.default;

  padding-top: 0.25rem;
  display: grid;
  grid-template-columns: 4fr 6fr 4fr;

  .left,
  .center,
  .right {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    height: $player-height;
  }

  .left {
    justify-content: flex-start;
  }

  .center {
    justify-content: center;
  }

  .right {
    justify-content: flex-end;

    .bandwidth {
      margin-left: 1rem;
      margin-right: 1rem;
    }

    .circle-button {
      position: relative;
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
