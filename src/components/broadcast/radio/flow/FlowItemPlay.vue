<script lang="ts">
import type { AnnotatedSchedule } from "@/stores/schedule";
import type { PropType } from "vue";
import { computed, defineComponent, ref } from "vue";
import CircleButton from "@/components/ui/button/CircleButton.vue";
import IconLogo from "@/components/ui/icon/IconLogo.vue";
import { storeToRefs } from "pinia";
import { useScheduleStore } from "@/stores/schedule";
import { useStreamControls } from "@/composables/stream";
import { requireSubscription } from "@/utils/account";
import { useQueueControls } from "@/composables/queue";
import { usePlayerControls, usePlayerState } from "@/composables/player";

export default defineComponent({
  components: {
    CircleButton,
    IconLogo,
  },
  props: {
    item: {
      type: Object as PropType<AnnotatedSchedule>,
      required: true,
    },
  },
  setup(props) {
    // state & controls
    // queue states
    const { current: currentScheduleItem } = storeToRefs(useScheduleStore());
    const isCurrentScheduleItem = computed(() => currentScheduleItem.value?.key === props.item.key);
    // player states
    const { playerState, media: currentPlayerMedia } = usePlayerState();
    const isCurrentPlayerMedia = computed(
      () => currentPlayerMedia.value?.uid === props.item.media.uid
    );
    const isPlaying = computed(() => {
      return isCurrentPlayerMedia.value && playerState.value.isPlaying;
    });
    const isBuffering = computed(() => {
      return isCurrentPlayerMedia.value && playerState.value.isBuffering;
    });
    const isPaused = computed(() => {
      return isCurrentPlayerMedia.value && playerState.value.isPaused;
    });
    // controls
    const { startPlayStream } = useStreamControls();
    const { pause: pausePlayer, resume: resumePlayer } = usePlayerControls();
    const { enqueueObj, startPlayCurrent } = useQueueControls();
    const startPlayMedia = requireSubscription(async (media: any) => {
      await enqueueObj(media, "replace");
      await startPlayCurrent(true);
    });
    // appearance / ui
    const isHover = ref(false);
    const iconMode = computed(() => {
      if (isBuffering.value || isPlaying.value) {
        return "pause";
      }
      return "play";
    });
    const handleClick = async () => {
      if (isBuffering.value || isPlaying.value) {
        pausePlayer();
        return;
      }
      if (isCurrentScheduleItem.value) {
        const startTime = -10;
        startPlayStream(startTime);
      } else if (isPaused.value) {
        resumePlayer();
      } else {
        startPlayMedia(props.item.media);
      }
    };
    return {
      isHover,
      iconMode,
      handleClick,
    };
  },
});
</script>

<template>
  <CircleButton
    :scale="3.35"
    :outline-opacity="1"
    :outline-width="6"
    :filled="true"
    :outlined="true"
    :outline-on-hover="true"
    color-var="--c-fg"
    @mouseover="isHover = true"
    @mouseleave="isHover = false"
    @click="handleClick"
  >
    <IconLogo :mode="iconMode" :scale="3.35" :outline-width="1.8" color-var="--c-fg" />
  </CircleButton>
</template>
