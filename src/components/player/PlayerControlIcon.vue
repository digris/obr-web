<script lang="ts">
import { defineComponent, computed } from 'vue';
import CircleButton from '@/components/ui/button/CircleButton.vue';
import IconPlay from '@/components/ui/icon/IconPlay.vue';

export default defineComponent({
  components: {
    CircleButton,
    IconPlay,
  },
  props: {
    playerState: {
      type: Object,
      required: false,
      default: () => null,
    },
  },
  setup(props) {
    // const state = ref('stopped');
    const state = computed(() => {
      if (!props.playerState) {
        return 'stopped';
      }
      if (props.playerState.isLive) {
        return 'stopped';
      }
      if (props.playerState.isBuffering) {
        return 'buffering';
      }
      if (props.playerState.isPlaying) {
        return 'playing';
      }
      if (props.playerState.isPaused) {
        return 'paused';
      }
      return 'stopped';
    });
    return {
      state,
    };
  },
});
</script>

<template>
  <div
    class="player-control-icon"
    :class="`is-${state}`"
  >
    <CircleButton
      :size="24"
    >
      <IconPlay
        v-if="(state === 'playing')"
        :size="20"
        color="#0ff"
      />
      <IconPlay
        v-else
        :size="20"
      />
    </CircleButton>
  </div>
</template>

<style lang="scss" scoped>
.player-control-icon {
  display: flex;
  align-items: center;
}
</style>
