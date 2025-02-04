<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import { invoke, until } from "@vueuse/core";
import { storeToRefs } from "pinia";

import MediaArtists from "@/components/catalog/media/MediaArtists.vue";
import { useDevice } from "@/composables/device";
import { usePlayerState } from "@/composables/player";
import { useQueueState } from "@/composables/queue";
import { useUiStore } from "@/stores/ui";
import { getContrastColor } from "@/utils/color";

import NewsSurvey from "../button/NewsSurvey.vue";
import OnAir from "../button/OnAir.vue";
// NOTE: shared components for desktop & mobile
import Queue from "../Queue.vue";
import QueueControl from "../QueueControl.vue";
// NOTE: adapted / extra components for mobile
import Panel from "./Panel.vue";
import PlayerPlayButton from "./PlayerPlayButton.vue";

export default defineComponent({
  components: {
    Panel,
    Queue,
    QueueControl,
    MediaArtists,
    NewsSurvey,
    OnAir,
    PlayerPlayButton,
  },
  setup() {
    const { isApp } = useDevice();
    const { playerVisible } = storeToRefs(useUiStore());
    const { mode, playState, media, color } = usePlayerState();
    invoke(async () => {
      // permanently show player as soon as playing or buffering starts
      await until(playState).toMatch((s) => ["buffering", "playing"].includes(s));
      playerVisible.value = true;
    });
    const { queueLength } = useQueueState();
    const queueVisible = ref(false);
    const hideQueue = () => (queueVisible.value = false);
    const toggleQueue = () => (queueVisible.value = !queueVisible.value);
    const panelVisible = ref(false);
    const hidePanel = () => (panelVisible.value = false);
    const togglePanel = () => {
      // when both panel & queue are visible: close the queue (but keep the panel)
      if (queueVisible.value && panelVisible.value) {
        hideQueue();
      } else {
        panelVisible.value = !panelVisible.value;
        // hide queue in case panel becomes visible
        if (panelVisible.value) {
          hideQueue();
        }
      }
    };
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
        return {
          "--c-bg": bg.join(" "),
          "--c-fg": fg.join(" "),
          "--c-fg-inverse": fgInverse.join(" "),
        };
      } catch (e) {
        console.warn(e);
      }
      return {};
    });

    return {
      isApp,
      playerVisible,
      mode,
      media,
      fgColor,
      cssVars,
      //
      panelVisible,
      hidePanel,
      togglePanel,
      //
      queueVisible,
      queueLength,
      hideQueue,
      toggleQueue,
    };
  },
});
</script>

<template>
  <div
    :style="{
      '--player-height': isApp ? '82px' : '60px',
    }"
  >
    <Panel :is-visible="panelVisible" :style="cssVars" @close="hidePanel" />
    <Queue :is-visible="queueVisible && queueLength > 0" @close="hideQueue" />
    <transition name="slide">
      <div
        v-if="playerVisible"
        class="player-container"
        :style="cssVars"
        :class="{ 'has-panel': panelVisible }"
      >
        <div class="player-bg" />
        <div class="player">
          <PlayerPlayButton class="player-control" :fg-color="fgColor" />
          <div @click="togglePanel" class="current-media">
            <div v-if="media" class="media">
              <div class="name" v-text="media.name" />
              <MediaArtists class="artists" :artists="media.artists" :link="false" />
            </div>
          </div>
          <div class="right">
            <OnAir class="on-air" />
            <NewsSurvey class="news" />
            <QueueControl
              class="queue-control"
              :queue-visible="queueVisible"
              :num-queued="queueLength"
              @toggle-visibility="toggleQueue"
            />
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";

.player-container {
  position: fixed;
  bottom: 0;
  z-index: 110;
  height: var(--player-height);
  width: 100%;
  background: rgb(var(--c-bg));
  box-shadow: 0 0 1px 1px rgb(var(--c-fg) / 20%);
  transition: background 200ms;
  transition-delay: 1ms;

  .player-bg {
    inset: 0;
    position: absolute;
    pointer-events: none;
  }

  &.has-panel {
    transition-delay: 100ms;

    .player-bg {
      background: rgb(var(--c-fg) / 10%);
    }
  }
}

.player {
  color: rgb(var(--c-fg));
  transition: background 1000ms;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;

  .player-control {
    margin: auto 0.625rem;
    display: flex;
  }

  .current-media {
    flex-grow: 1;
    display: flex;
    height: 100%;
    overflow: hidden;

    .media {
      flex-grow: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }

    .name {
      @include typo.small;

      width: 100%;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }

    .artists {
      @include typo.small;
      @include typo.dim;
      @include typo.light;
    }
  }

  .right {
    margin: auto 0.625rem;
    display: flex;
    align-items: center;
    justify-content: center;

    .on-air {
      margin-right: 0.25rem;
    }

    .queue-control {
      :deep(.number) {
        right: 0.625rem;
        top: 8px;
        font-size: 10px;
        min-height: 16px;
        min-width: 16px;
      }
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
