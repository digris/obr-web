<script lang="ts">
import { defineComponent } from 'vue';

import CircleButton from '@/components/ui/button/CircleButton.vue';
import IconContext from '@/components/ui/icon/IconContext.vue';
import ButtonPlay from '@/components/player/button/ButtonPlay.vue';

export default defineComponent({
  components: {
    CircleButton,
    IconContext,
    ButtonPlay,
  },
  props: {
    isLoading: {
      type: Boolean,
      default: false,
    },
    numTotal: {
      type: Number,
      default: 0,
    },
  },
});
</script>

<template>
  <div
    class="play-all"
    :style="{
      '--c-fg': '255,255,255',
      '--c-bg': '0,0,0',
    }"
    :class="{
      'is-loading': isLoading,
    }"
  >
    <div
      class="container"
    >
      <div class="play">
        <ButtonPlay
          :is-buffering="isLoading"
        />
      </div>
      <div
        class="info"
      >
        <div
          class="text"
        >
          Alle {{ numTotal }} Tracks spielen
        </div>
      </div>
      <div class="actions">
        <CircleButton
          :size="(48)"
          :outlined="(false)"
        >
          <IconContext
            :color="'rgb(var(--c-white))'"
            :size="36"
          />
        </CircleButton>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/button";
@use "@/style/elements/container";
.play-all {
  color: rgb(var(--c-white));
  background: rgb(var(--c-black));
  &.is-loading {
    cursor: wait;
  }
}
.container {
  @include container.default;
  display: grid;
  grid-row-gap: 0;
  grid-column-gap: 1rem;
  grid-template-columns: 1fr 16fr 1fr;
  padding: 0.75rem 0;
  > div {
    display: flex;
    align-items: center;
  }
  .play {
    padding-left: 0.5rem;
  }
  .info {
    justify-self: center;
    .text {
      cursor: pointer;
    }
  }
  .actions {
    justify-self: flex-end;
  }

}
</style>
