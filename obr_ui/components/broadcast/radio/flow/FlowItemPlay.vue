<script lang="ts">
import type { PropType } from "vue";
import { computed, defineComponent, ref } from "vue";
import { storeToRefs } from "pinia";

import CircleButton from "@/components/ui/button/CircleButton.vue";
import IconLogo from "@/components/ui/icon/IconLogo.vue";
import { useAnalytics } from "@/composables/analytics";
import { useDevice } from "@/composables/device";
import { usePlayerControls, usePlayerState } from "@/composables/player";
import { useQueueControls } from "@/composables/queue";
import type { AnnotatedSchedule } from "@/stores/schedule";
import { useScheduleStore } from "@/stores/schedule";
import { requireSubscription } from "@/utils/account";

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
    const { isMobile } = useDevice();
    // state & controls
    // queue states
    const { current: currentScheduleItem } = storeToRefs(useScheduleStore());
    const isCurrentScheduleItem = computed(() => currentScheduleItem.value?.key === props.item.key);
    // mapped player states
    const {
      media: currentPlayerMedia,
      isPlaying: playerIsPlaying,
      isBuffering: playerIsBuffering,
      isPaused: playerIsPaused,
    } = usePlayerState();
    const { logUIEvent } = useAnalytics();
    const isCurrentPlayerMedia = computed(
      () => currentPlayerMedia.value?.uid === props.item.media.uid
    );
    const isPlaying = computed(() => isCurrentPlayerMedia.value && playerIsPlaying.value);
    const isBuffering = computed(() => isCurrentPlayerMedia.value && playerIsBuffering.value);
    const isPaused = computed(() => isCurrentPlayerMedia.value && playerIsPaused.value);
    // controls
    const { playLive } = usePlayerControls();
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
        await pausePlayer();
        logUIEvent("player:pause");
        return;
      }
      if (isCurrentScheduleItem.value) {
        await playLive();
        logUIEvent("player:play", "live");
      } else if (isPaused.value) {
        await resumePlayer();
        logUIEvent("player:resume", "on-demand");
      } else {
        startPlayMedia(props.item.media);
        logUIEvent("player:play", "on-demand");
      }
    };
    return {
      isMobile,
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
    outline-opacity="100%"
    :outline-width="6"
    :filled="true"
    :outlined="true"
    :outline-on-hover="true"
    color-var="--c-fg"
    @mouseover="isMobile ? null : (isHover = true)"
    @mouseleave="isMobile ? null : (isHover = false)"
    @click="handleClick"
  >
    <IconLogo :mode="iconMode" :scale="3.35" :outline-width="1.8" color-var="--c-fg" />
  </CircleButton>
</template>
