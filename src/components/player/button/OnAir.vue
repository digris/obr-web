<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import { useStore } from 'vuex';
import eventBus from '@/eventBus';
import IconBuffering from '@/components/ui/icon/IconBuffering.vue';
import IconPause from '@/components/ui/icon/IconPause.vue';
import IconPlaying from '@/components/ui/icon/IconPlaying.vue';
import IconPlay from '@/components/ui/icon/IconPlay.vue';

export default defineComponent({
  setup() {
    const store = useStore();
    const playerState = computed(() => store.getters['player/playerState']);
    const isLive = computed(() => playerState.value && playerState.value.isLive);
    const isPlaying = computed(() => playerState.value && playerState.value.isPlaying);
    const isBuffering = computed(() => playerState.value && playerState.value.isBuffering);
    const isHover = ref(false);
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

    // const pause = () => {
    //   eventBus.emit('player:controls', { do: 'pause' });
    // };
    //
    // const play = () => {
    //   eventBus.emit('player:controls', { do: 'resume' });
    // };

    const click = () => {
      if (isBuffering.value || isPlaying.value) {
        eventBus.emit('player:controls', { do: 'pause' });
      } else {
        eventBus.emit('player:controls', { do: 'resume' });
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
  <div
    class="on-air"
  >
    <div
      class="button"
      @click.prevent="click"
      @mouseover="isHover = true"
      @mouseleave="isHover = false"
    >
      <div
        class="button__icon"
      >
        <component
          :is="icon"
          :size="(48)"
          color="rgb(var(--c-fg))"
        />
      </div>
      <div
        class="button__text"
      >
        Live On-Air
      </div>
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
    background: whitesmoke;
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
