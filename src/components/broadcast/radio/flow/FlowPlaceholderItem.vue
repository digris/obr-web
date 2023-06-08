<script lang="ts">
import { computed, defineComponent } from "vue";

import CircleButton from "@/components/ui/button/CircleButton.vue";
import IconDAB from "@/components/ui/icon/brand/IconDAB.vue";
import IconLogo from "@/components/ui/icon/IconLogo.vue";
import { usePlayerControls, usePlayerState } from "@/proto/composables/player";

export default defineComponent({
  components: {
    CircleButton,
    IconLogo,
    IconDAB,
  },
  setup() {
    const { isPlaying, isBuffering } = usePlayerState();
    const { playLive, pause: pausePlayer } = usePlayerControls();
    const iconMode = computed(() => (isBuffering.value || isPlaying.value ? "pause" : "play"));
    const handleClick = async () => {
      if (isBuffering.value || isPlaying.value) {
        pausePlayer();
        return;
      }
      const startTime = -10;
      await playLive(startTime);
    };
    return {
      iconMode,
      handleClick,
    };
  },
});
</script>

<template>
  <div class="placeholder-item">
    <CircleButton
      :scale="3.35"
      outline-opacity="100%"
      :outline-width="6"
      :filled="true"
      :outlined="true"
      :outline-on-hover="true"
      color-var="--c-page-fg"
      @click="handleClick"
    >
      <IconLogo :mode="iconMode" :scale="3.35" :outline-width="1.8" color-var="--c-page-fg" />
    </CircleButton>
    <div class="icon-dab">
      <IconDAB :mode="iconMode" :scale="1" color-var="--c-page-bg" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.placeholder-item {
  position: relative;
  height: var(--item-size);
  width: var(--item-size);
  background: rgb(var(--c-page-fg));
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 20px rgb(0 0 0 / 50%);

  .circle-button {
    background: rgb(var(--c-page-bg));
  }

  .icon-dab {
    position: absolute;
    bottom: 6px;
    right: 8px;
    pointer-events: none;
  }
}
</style>
