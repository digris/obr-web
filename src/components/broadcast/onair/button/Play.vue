<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import { usePlayerState } from "@/composables/player";
import CircleButton from "@/components/ui/button/CircleButton.vue";
import IconLogo from "@/components/ui/icon/IconLogo.vue";

export default defineComponent({
  components: {
    CircleButton,
    IconLogo,
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
  emits: ["play", "pause"],
  setup(props, { emit }) {
    const isHover = ref(false);
    const { playerState, currentMedia } = usePlayerState();
    // const isCurrent = computed(() => currentMedia.value?.uid === props.media?.uid);
    const isCurrent = computed(() => {
      // eslint-disable-next-line max-len
      return currentMedia.value && props.media ? currentMedia.value.uid === props.media.uid : false;
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
    const iconMode = computed(() => {
      if (isBuffering.value) {
        return "pause";
      }
      if (isPlaying.value && isHover.value) {
        return "pause";
      }
      if (isPlaying.value) {
        return "playing";
      }
      return "play";
    });
    const isFilled = computed(() => {
      return isPlaying.value || isBuffering.value;
    });
    const handleClick = () => {
      if (isBuffering.value || isPlaying.value) {
        emit("pause");
      } else {
        emit("play");
      }
    };
    return {
      isHover,
      handleClick,
      isPlaying,
      isFilled,
      progress,
      iconMode,
    };
  },
});
</script>

<template>
  <CircleButton
    :scale="3.35"
    :outline-opacity="1"
    :outline-width="6"
    :filled="isFilled"
    :outlined="true"
    :outline-on-hover="true"
    color-var="--c-page-fg"
    @mouseover="isHover = true"
    @mouseleave="isHover = false"
    @click="handleClick"
  >
    <IconLogo :mode="iconMode" :scale="3.35" :outline-width="1.8" color-var="--c-page-fg" />
  </CircleButton>
</template>
