<script lang="ts">
import { defineComponent, watch } from "vue";
import { useEventListener } from "@vueuse/core";

import QueueMedia from "@/components/player/QueueMedia.vue";
import IconCaret from "@/components/ui/icon/IconCaret.vue";
import { useDevice } from "@/composables/device";
import { useQueueControls, useQueueState } from "@/composables/queue";

import Circle from "./button/Circle.vue";
import ShuffleControl from "./ShuffleControl.vue";

export default defineComponent({
  components: {
    QueueMedia,
    ShuffleControl,
    IconCaret,
    Circle,
  },
  props: {
    isVisible: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["close"],
  setup(props, { emit }) {
    const { isMobile } = useDevice();
    const { currentMedia, queuedMedia, queueLength } = useQueueState();
    const { clearQueue } = useQueueControls();
    const close = () => emit("close");
    watch(
      () => queueLength.value,
      (newValue) => {
        if (newValue < 1) {
          close();
        }
      }
    );
    useEventListener(document, "keydown", (e) => {
      if (e.code === "KeyX") {
        close();
      }
    });
    return {
      isMobile,
      close,
      queuedMedia,
      currentMedia,
      clearQueue,
    };
  },
});
</script>
<template>
  <transition name="fade">
    <div v-if="isVisible" @click="close" class="mask" />
  </transition>
  <transition name="slide">
    <div
      v-if="isVisible"
      class="queue"
      :style="{
        '--c-bg': 'var(--c-black)',
        '--c-fg': 'var(--c-white)',
      }"
    >
      <div v-if="isMobile" @click.prevent="close" class="header" />
      <div class="container">
        <QueueMedia
          v-for="(media, index) in queuedMedia"
          :key="`media-row-${media.uid}`"
          :obj-key="`${media.ct}:${media.uid}`"
          :title="media.name"
          :artist-display="media.artistDisplay"
          :releases="media.releases"
          :index="index"
          :is-current="media === currentMedia"
        />
      </div>
    </div>
  </transition>
  <transition name="slide-actions">
    <div
      v-if="isVisible"
      class="actions"
      :style="{
        '--c-bg': 'var(--c-black)',
        '--c-fg': 'var(--c-white)',
      }"
    >
      <div class="container">
        <ShuffleControl />
        <div class="clear-queue">
          <div class="button" v-text="'Clear queue'" @click="clearQueue" />
        </div>
        <Circle
          @click="close"
          background-color="rgb(var(--c-black))"
          hover-background-color="rgb(var(--c-white) / 10%)"
        >
          <IconCaret direction="down" color-var="--c-white" />
        </Circle>
      </div>
    </div>
  </transition>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/responsive";
@use "@/style/elements/container";

/*
 NOTE: `--player-height` is set in parent component
 */

.mask {
  top: 0;
  position: fixed;
  height: 100%;
  width: 100%;
  z-index: 20;
  left: 0;
  background: rgb(var(--c-black) / 80%);

  @include responsive.bp-medium {
    background: unset;
  }
}

.queue {
  z-index: 20;
  position: fixed;
  width: 100%;
  min-height: 100px;
  bottom: 72px; // player height (desktop)
  max-height: calc(100% - 80px);
  overflow-y: auto;
  color: rgb(var(--c-white));
  background: rgb(var(--c-black));
  overscroll-behavior: contain;

  &::-webkit-scrollbar {
    display: none;
  }

  @include responsive.bp-medium {
    max-width: unset;
    box-shadow: 0 -4px 8px 4px rgb(0 0 0 / 10%);
    border-top-left-radius: 28px;
    border-top-right-radius: 28px;

    .header {
      top: 0;
      position: sticky;
      height: 28px;
      background: rgb(var(--c-black));
      z-index: 2;
    }
  }

  .container {
    @include container.default;

    padding-top: 2rem;
    padding-bottom: 92px;
  }

  @include responsive.bp-medium {
    /* sizing based on player height & 60px action bar */
    max-height: calc(100% - calc(var(--player-height) + 60px + var(--sa-t)));
    bottom: calc(var(--player-height) + 60px);
    box-shadow: 0 -4px 8px 4px rgb(0 0 0 / 10%);
  }
}

.actions {
  position: fixed;
  height: 76px;
  width: 100%;
  z-index: 21;
  border-top: 1px solid rgb(var(--c-white) / 25%);
  bottom: 72px; // player height
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
  background: rgb(var(--c-black));

  .container {
    @include container.default;

    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: flex-end;

    > div {
      margin-left: 0.5rem;
    }
  }

  @include responsive.bp-medium {
    height: 60px;
    bottom: var(--player-height);

    .container {
      > div {
        margin-left: unset;
      }

      .clear-queue {
        flex-grow: 1;
        align-items: center;
        justify-content: center;
        display: flex;
      }
    }
  }
}

// NOTE: generalise button styling if also used at other place(s)
.button {
  cursor: pointer;
  height: 48px;
  border-radius: 24px;
  display: flex;
  align-items: center;
  padding: 0 1.5rem;
  color: rgb(var(--c-white));
  border: 1px solid rgb(var(--c-white) / 20%);
  transition: background-color 200ms;

  @include responsive.on-hover {
    border-color: transparent;
    background: rgb(var(--c-white) / 10%);
  }

  @include responsive.bp-medium {
    height: 40px;
    font-size: 16px;

    @include typo.light;
  }
}

// mask transition
.fade-enter-active,
.fade-leave-active {
  transition: opacity 200ms;
}

.fade-enter-from {
  opacity: 0;
}

.fade-leave-to {
  opacity: 0;
}

// queue panel transition
.slide-enter-active,
.slide-leave-active {
  transition: transform 200ms, opacity 200ms;
}

.slide-enter-from {
  transform: translate(0, 100%);
  opacity: 0;
}

.slide-leave-to {
  transform: translate(0, 200%);
}

// queue item list transition
.queue-enter-active,
.queue-leave-active {
  transition: opacity 300ms, transform 100ms;
}

.queue-leave-to {
  opacity: 0;
}
</style>
