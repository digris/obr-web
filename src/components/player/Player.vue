<script lang="ts" setup>
import {computed, defineComponent, ref} from "vue";

import UserRating from "@/components/rating/UserRating.vue";
import {usePlayerControls, usePlayerState} from "@/composables/player";
import {useQueueState} from "@/composables/queue";
import {getContrastColor} from "@/utils/color";

import Bandwidth from "./button/Bandwidth.vue";
import Circle from "./button/Circle.vue";
import OnAir from "./button/OnAir.vue";
import CurrentMedia from "./CurrentMedia.vue";
import PlayerControl from "./PlayerControl.vue";
import Playhead from "./Playhead.vue";
import Queue from "./Queue.vue";
import QueueControl from "./QueueControl.vue";
import VolumeControl from "./VolumeControl.vue";
import {useObjKey} from "@/composables/obj";


const { queueLength } = useQueueState();
const { seek } = usePlayerControls();
const { isVisible, media, color: bgColor, isLive } = usePlayerState();
const {objKey} = useObjKey(media);
const fgColor = computed(() => getContrastColor(bgColor.value));
const fgColorInverse = computed(() => getContrastColor(fgColor.value));
const queueVisible = ref(false);
const hideQueue = () => { queueVisible.value = false };
const toggleQueue = () => { queueVisible.value = !queueVisible.value };
</script>

<template>
  <Queue :is-visible="queueVisible && queueLength > 0" @close="hideQueue" />
  <pre style="position: fixed; z-index: 999;" class="debug" v-text="{objKey}" />
  <transition name="slide">
    <div
      v-if="isVisible"
      class="player"
      :style="{
        '--c-bg': bgColor.join(' '),
        '--c-fg': fgColor.join(' '),
        '--c-fg-inverse': fgColorInverse.join(' '),
      }"
    >
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
          <Circle v-if="objKey">
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
  color: rgb(var(--c-fg));
  background: rgb(var(--c-bg));
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
