<script lang="ts">
import { computed, defineComponent } from 'vue';
import { useStore } from 'vuex';
import eventBus from '@/eventBus';
import ButtonPlay from './button/ButtonPlay.vue';

export default defineComponent({
  components: {
    ButtonPlay,
  },
  setup() {
    const store = useStore();
    const playerState = computed(() => store.getters['player/playerState']);
    const isLive = computed(() => playerState.value && playerState.value.isLive);
    const isPlaying = computed(() => playerState.value && playerState.value.isPlaying);
    const isBuffering = computed(() => playerState.value && playerState.value.isBuffering);

    const pause = () => {
      eventBus.emit('player:controls', { do: 'pause' });
    };

    const play = () => {
      eventBus.emit('player:controls', { do: 'resume' });
    };

    return {
      isLive,
      isPlaying,
      isBuffering,
      pause,
      play,
    };
  },
});
</script>

<template>
  <div class="radio">
    <div class="actions">
      <ButtonPlay
        :is-playing="isPlaying"
        :is-buffering="isBuffering"
        @pause="pause"
        @play="play"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";
@use "@/style/base/typo";

@mixin time {
  padding: 0 0.5rem;
  color: rgba(var(--c-fg), 0.5);
  font-size: 0.9rem;
}

@mixin actions {
  //display: grid;
  //grid-gap: 0.5rem;
  display: flex;
  .action {
    display: inline-block;
    width: 1.5rem;
    height: 1.5rem;
    margin: 0 0.25rem;
    color: rgb(var(--c-bg));
    background: rgba(var(--c-fg), 0.5);
    border: none;
    border-radius: 0.75rem;
    cursor: pointer;
    transition: background 100ms;
    &:hover {
      background: rgba(var(--c-fg), 0.9);
    }
  }
}

.playhead {
  display: grid;
  grid-template-columns: auto 1fr auto;
  width: 100%;
  min-height: 48px;
  .actions,
  .progress,
  .time {
    display: flex;
    align-items: center;
  }
  .actions {
    @include actions;
  }
  .progress {
    position: relative;
    margin: 0 1rem;
    .time {
      @include time;
      position: absolute;
      top: -4px;
      display: flex;
      justify-content: center;
      width: 100%;
      //min-width: 84px;
      //max-width: 84px;
    }
  }
  .info {
    display: flex;
    align-items: center;
    padding-left: 0.5rem;
    .bandwidth {
      @include typo.small;
    }
  }
}
</style>
