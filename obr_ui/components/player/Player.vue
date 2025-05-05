<script lang="ts" setup>
import { computed, ref } from "vue";
import { useToggle } from "@vueuse/core";

import UserRating from "@/components/rating/UserRating.vue";
import { useObjKey } from "@/composables/obj";
import { usePlayerControls, usePlayerState } from "@/composables/player";
import { useQueueState } from "@/composables/queue";
import { useSettings } from "@/composables/settings";
import { getContrastColor } from "@/utils/color";

import Bandwidth from "./button/Bandwidth.vue";
import Circle from "./button/Circle.vue";
import Donate from "./button/Donate.vue";
import News from "./button/News.vue";
import NewsSurvey from "./button/NewsSurvey.vue";
import OnAir from "./button/OnAir.vue";
import CurrentMedia from "./CurrentMedia.vue";
import PlayerControl from "./PlayerControl.vue";
import Playhead from "./Playhead.vue";
import Queue from "./Queue.vue";
import QueueControl from "./QueueControl.vue";
import VolumeControl from "./VolumeControl.vue";

const { queueLength } = useQueueState();
const { seek } = usePlayerControls();
const { isVisible, isNews, media, color: bgColor } = usePlayerState();
const { objKey } = useObjKey(media);
const fgColor = computed(() => getContrastColor(bgColor.value));
const fgColorInverse = computed(() => getContrastColor(fgColor.value));
const queueVisible = ref(false);
const toggleQueue = useToggle(queueVisible);

const { userSettings } = useSettings();
const testingEnabled = computed(() => userSettings.value?.testingEnabled);
</script>

<template>
  <Queue :is-visible="queueVisible && queueLength > 0" @close="toggleQueue(false)" />
  <!--<pre style="position: fixed; z-index: 999" class="debug" v-text="{ objKey }" />-->
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
          <div v-if="isNews">(( CurrentNews ))</div>
          <CurrentMedia v-else :media="media" />
        </div>
        <div class="center">
          <PlayerControl :fg-color="fgColor" />
        </div>
        <div class="right">
          <OnAir />
          <!--
          news controls for test-users. survey for the others.
          -->
          <News v-if="testingEnabled" />
          <NewsSurvey v-else />
          <!--
          donate disabled for the moment
          -->
          <Donate />
          <Bandwidth />
          <VolumeControl />
          <Circle v-if="objKey">
            <UserRating color-var="--c-fg" :obj-key="objKey" />
          </Circle>
          <QueueControl
            :queue-visible="queueVisible"
            :num-queued="queueLength"
            @toggle-visibility="toggleQueue()"
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

    .news {
      margin-left: 1rem;
    }

    .donate {
      margin-left: 1rem;
    }

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
