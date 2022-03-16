<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import { usePlayerState } from '@/composables/player';
import CircleButton from '@/components/ui/button/CircleButton.vue';
import IconPlay from '@/components/ui/icon/IconPlay.vue';
import IconBuffering from '@/components/ui/icon/IconBuffering.vue';
import IconPlaying from '@/components/ui/icon/IconPlaying.vue';

export default defineComponent({
  components: {
    CircleButton,
    IconPlay,
  },
  props: {
    media: {
      type: Object,
      required: false,
      default: () => ({}),
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  emits: [
    'play',
    'pause',
  ],
  setup(props, { emit }) {
    const isHover = ref(false);
    const {
      playerState,
      currentMedia,
    } = usePlayerState();
    // const isCurrent = computed(() => currentMedia.value?.uid === props.media?.uid);
    const isCurrent = computed(() => {
      // eslint-disable-next-line max-len
      return (currentMedia.value && props.media) ? currentMedia.value.uid === props.media.uid : false;
    });
    const isPlaying = computed(() => {
      if (!isCurrent.value) {
        return false;
      }
      return playerState.value.isPlaying;
    });
    const isBuffering = computed(() => {
      if (!isCurrent.value) {
        return false;
      }
      return playerState.value.isBuffering;
    });
    const progress = computed(() => {
      if (!isCurrent.value) {
        return null;
      }
      return playerState.value && playerState.value.relPosition;
    });
    const icon = computed(() => {
      if (isBuffering.value) {
        return IconBuffering;
      }
      if (isPlaying.value && isHover.value) {
        // return IconPause;
        return IconPlaying;
      }
      if (isPlaying.value) {
        return IconPlaying;
      }
      return IconPlay;
    });
    const isFilled = computed(() => {
      return (isPlaying.value || isBuffering.value);
    });
    const handleClick = () => {
      if (isBuffering.value || isPlaying.value) {
        emit('pause');
      } else {
        emit('play');
      }
    };
    return {
      isHover,
      handleClick,
      isPlaying,
      isFilled,
      progress,
      icon,
    };
  },
});
</script>

<template>
  <CircleButton
    :size="120"
    :outline-opacity="(1)"
    :outline-width="(6)"
    :filled="isFilled"
    @mouseover="isHover = true"
    @mouseleave="isHover = false"
    @click="handleClick"
  >
    <component
      :is="icon"
      :size="96"
      :color="(isFilled) ? 'rgb(var(--c-page-fg-inverse))' : 'rgb(var(--c-page-fg))'"
      :pause="(isPlaying && isHover)"
    />
  </CircleButton>
</template>
