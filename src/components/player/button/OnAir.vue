<script lang="ts">
import { defineComponent } from "vue";

import eventBus from "@/eventBus";
import { usePlayerControls, usePlayerState } from "@/proto/composables/player";

export default defineComponent({
  setup() {
    const { isLive } = usePlayerState();
    const { playLive } = usePlayerControls();
    const click = () => {
      if (isLive.value) {
        // NOTE: this should be implemented in a nicer way
        eventBus.emit("radio:flow", "releaseFocus");
        return;
      }
      playLive();
    };
    return {
      isLive,
      click,
    };
  },
});
</script>

<template>
  <div @click.prevent="click" class="on-air" :class="{ 'is-live': isLive }">
    <div class="on-air__text" v-text="`Live`" />
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";

.on-air {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 1.5rem;
  border-radius: 0.75rem;
  padding: 0 0.75rem;
  border: 1px solid rgb(var(--c-fg) / 25%);
  transition: border 100ms, background 100ms;

  &__text {
    @include typo.small;

    color: rgb(var(--c-fg));
  }

  &:not(.is-live) {
    cursor: pointer;
  }

  &.is-live,
  &:hover {
    background: rgb(var(--c-red));
    border-color: transparent;
  }
}
</style>
