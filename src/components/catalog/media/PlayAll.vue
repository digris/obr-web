<script lang="ts">
import { defineComponent } from "vue";
import { useI18n } from "vue-i18n";

// import CircleButton from '@/components/ui/button/CircleButton.vue';
// import IconContext from '@/components/ui/icon/IconContext.vue';
import ButtonPlay from "@/components/player/button/ButtonPlay.vue";

export default defineComponent({
  components: {
    // CircleButton,
    // IconContext,
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
  setup() {
    const { t } = useI18n();
    return {
      t,
    };
  },
});
</script>

<template>
  <div
    class="play-all"
    :style="{
      '--c-fg': '0,0,0',
      '--c-bg': '128,128,128',
    }"
    :class="{
      'is-loading': isLoading,
    }"
  >
    <div class="container">
      <div class="play">
        <ButtonPlay :is-buffering="isLoading" />
      </div>
      <div class="info">
        <div class="text" v-text="t('catalog.list.playAllTracks', numTotal)" />
      </div>
      <div class="actions">
        <!--
        <CircleButton
          :size="(48)"
          :outlined="(false)"
        >
          <IconContext
            :color="'rgb(var(--c-black))'"
            :size="36"
          />
        </CircleButton>
        -->
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/button";
@use "@/style/elements/container";
.play-all {
  color: rgb(var(--c-black));
  background: rgb(var(--c-gray-500));
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
  padding-top: 0.75rem;
  padding-bottom: 0.75rem;
  > div {
    display: flex;
    align-items: center;
  }
  .play {
    padding-left: 0;
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
