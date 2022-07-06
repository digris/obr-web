<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import { useStore } from "vuex";
import { getContrastColor } from "@/utils/color";
import UserRating from "@/components/rating/UserRating.vue";
import CurrentMedia from "./CurrentMedia.vue";
import Playhead from "./Playhead.vue";
import Queue from "./Queue.vue";
import OnAir from "./button/OnAir.vue";
import Circle from "./button/Circle.vue";
import PlayerControl from "./PlayerControl.vue";
import VolumeControl from "./VolumeControl.vue";
import QueueControl from "./QueueControl.vue";
import { usePlayerControls, usePlayerState } from "@/composables/player";

export default defineComponent({
  components: {
    CurrentMedia,
    Playhead,
    OnAir,
    Circle,
    Queue,
    UserRating,
    PlayerControl,
    VolumeControl,
    QueueControl,
  },
  setup() {
    const store = useStore();
    const { seek } = usePlayerControls();
    const { relPosition } = usePlayerState();
    const liveTimeOffset = ref(-10);
    const playerState = computed(() => store.getters["player/playerState"]);
    const isLive = computed(() => store.getters["player/isLive"]);
    const currentMedia = computed(() => store.getters["player/media"]);
    const currentScope = computed(() => store.getters["player/scope"]);
    const isVisible = computed(() => store.getters["player/isVisible"]);
    const objKey = computed(() => {
      if (!currentMedia.value) {
        return null;
      }
      return `${currentMedia.value?.ct}:${currentMedia.value?.uid}`;
    });
    const cssVars = computed(() => {
      try {
        const bg = currentMedia.value.releases[0].image.rgb;
        const fg = getContrastColor(bg);
        const fgInverse = getContrastColor(fg);
        const colors = {
          "--c-bg": bg.join(","),
          "--c-fg": fg.join(","),
          "--c-fg-inverse": fgInverse.join(","),
        };
        return colors;
      } catch (e) {
        // console.debug(e);
      }
      return {
        "--c-bg": isLive.value ? "255, 255, 255" : "0, 0, 0",
        "--c-fg": isLive.value ? "0, 0, 0" : "255, 255, 255",
        "--c-fg-inverse": isLive.value ? "255, 255, 255" : "0, 0, 0",
      };
    });
    const queueVisible = ref(false);
    const queueNumMedia = computed(() => store.getters["queue/numMedia"]);
    const hideQueue = () => {
      queueVisible.value = false;
    };
    const toggleQueue = () => {
      queueVisible.value = !queueVisible.value;
    };
    return {
      isVisible,
      liveTimeOffset,
      playerState,
      currentMedia,
      currentScope,
      objKey,
      cssVars,
      queueVisible,
      queueNumMedia,
      hideQueue,
      toggleQueue,
      //
      seek,
      relPosition,
    };
  },
});
</script>

<template>
  <Queue :is-visible="queueVisible && queueNumMedia > 0" @close="hideQueue" />
  <transition name="slide">
    <div v-if="isVisible" class="player" :style="cssVars">
      <Playhead class="playhead" @seek="seek" />
      <div class="container">
        <div class="left">
          <CurrentMedia :media="currentMedia" />
        </div>
        <div class="center">
          <PlayerControl />
        </div>
        <div class="right">
          <OnAir />
          <VolumeControl />
          <Circle :size="48" :outlined="false">
            <UserRating color-var="--c-fg" v-if="currentMedia" :obj-key="objKey" />
          </Circle>
          <QueueControl
            :queue-visible="queueVisible"
            :num-queued="queueNumMedia"
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
  bottom: 0;
  z-index: 110;
  width: 100%;
  height: $player-height;
  color: rgba(var(--c-fg));
  background: rgba(var(--c-bg));
  transition: background 1000ms;
}

.playhead {
  position: absolute;
  //background: rgba(255,0,255,0.2);
  bottom: 52px;
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
