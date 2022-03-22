<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import { usePlayerState, usePlayerControls } from "@/composables/player";

import IconBuffering from "@/components/ui/icon/IconBuffering.vue";
import IconPause from "@/components/ui/icon/IconPause.vue";
import IconPlaying from "@/components/ui/icon/IconPlaying.vue";
import IconPlay from "@/components/ui/icon/IconPlay.vue";

export default defineComponent({
  setup() {
    const isHover = ref(false);
    const { isLive, isPlaying, isBuffering } = usePlayerState();
    const { resume, pause } = usePlayerControls();
    const icon = computed(() => {
      if (isBuffering.value) {
        return IconBuffering;
      }
      if (isPlaying.value && isHover.value) {
        return IconPause;
      }
      if (isPlaying.value) {
        return IconPlaying;
      }
      return IconPlay;
    });
    const click = () => {
      if (isBuffering.value || isPlaying.value) {
        pause();
      } else {
        resume();
      }
    };
    return {
      isHover,
      isLive,
      isPlaying,
      isBuffering,
      icon,
      click,
    };
  },
});
</script>

<template>
  <div class="on-air">
    <div
      class="button"
      @click.prevent="click"
      @mouseover="isHover = true"
      @mouseleave="isHover = false"
    >
      <div class="button__icon">
        <component :is="icon" :size="48" color="rgb(var(--c-fg))" />
      </div>
      <div class="button__text">Live On-Air</div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.on-air {
  display: flex;
  align-items: center;
  justify-content: center;
  .button {
    display: flex;
    align-items: center;
    height: 48px;
    color: rgb(var(--c-fg));
    border: 3px solid rgb(var(--c-fg));
    border-radius: 24px;
    cursor: pointer;
    &__icon {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 48px;
      height: 48px;
    }
    &__text {
      padding-right: 1.25rem;
    }
  }
}
</style>
