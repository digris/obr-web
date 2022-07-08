<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import { useMagicKeys } from "@vueuse/core";
import { usePlayerState, usePlayerControls } from "@/composables/player";
import { useQueueControls, useQueueState } from "@/composables/queue";
import { useObjCtUid } from "@/composables/obj";
import { requireSubscription } from "@/utils/account";
import { getMedia } from "@/api/catalog";
import { getContrastColor } from "@/utils/color";
import ButtonPlay from "@/components/player/button/ButtonPlay.vue";

export default defineComponent({
  components: {
    ButtonPlay,
  },
  props: {
    objKey: {
      type: String,
      required: false,
      default: null,
    },
    filter: {
      type: Object,
      required: false,
      default: () => {},
    },
    ordering: {
      type: Array,
      default: () => [],
    },
    mode: {
      type: String,
      default: "replace",
    },
    restartQueue: {
      type: Boolean,
      default: false,
    },
    size: {
      type: Number,
      default: 48,
    },
    outlined: {
      type: Boolean,
      default: true,
    },
    backgroundColor: {
      type: String,
      default: null,
    },
    hoverBackgroundColor: {
      type: String,
      default: null,
    },
    shadowed: {
      type: Boolean,
      default: false,
    },
  },
  setup(props, { slots }) {
    const { objCt, objUid } = useObjCtUid(props.objKey);
    const { shift: shiftKey } = useMagicKeys();
    const { queuedMedia, currentIndex: currentQueueIndex } = useQueueState();
    const { enqueueMedia, startPlayCurrent, playFromIndex } = useQueueControls();
    const {
      isPlaying,
      isBuffering,
      issPaused,
      //
      currentScope,
      currentColor,
    } = usePlayerState();
    const { pause, resume } = usePlayerControls();
    const inScope = computed(() => {
      return currentScope.value.includes(props.objKey);
    });
    const queueIndex = computed(() => {
      if (currentQueueIndex.value < 0) {
        return null;
      }
      const index = queuedMedia.value.findIndex((obj: object) => {
        return obj.uid === objUid.value && obj.ct === objCt.value;
      });
      if (index < 0) {
        return null;
      }
      return index;
    });
    const queuePosition = computed(() => {
      return queueIndex.value !== null ? queueIndex.value - currentQueueIndex.value : null;
    });
    const inQueue = computed(() => {
      return queuePosition.value !== null;
    });
    const objIsPlaying = computed(() => inScope.value && isPlaying.value);
    const objIsBuffering = computed(() => inScope.value && isBuffering.value);
    const objIsPaused = computed(() => inScope.value && issPaused.value);
    const actionStyle = computed(() => {
      if (slots.default) {
        return {};
      }
      return {
        width: `${props.size}px`,
        height: `${props.size}px`,
      };
    });
    const buttonCssVars = computed(() => {
      if (inScope.value && currentColor.value) {
        return {
          "--c-fg": currentColor.value.join(","),
        };
      }
      return {
        "--c-fg": "0,0,0",
      };
    });
    const buttonColor = computed(() => {
      if (inScope.value && currentColor.value) {
        return getContrastColor(currentColor.value);
      }
      return [0, 0, 0];
    });
    const isLoading = ref(false);
    const play = async () => {
      // play directly if obj is already in the queue
      if (inQueue.value && queueIndex.value !== null) {
        await playFromIndex(queueIndex.value);
        return;
      }

      isLoading.value = true;
      const filter = { ...props.filter };
      const ordering = props.ordering;
      const mode = props.mode;
      const scope = props.objKey ? [props.objKey] : [];
      if (props.objKey) {
        filter.obj_key = props.objKey;
      }
      const { results } = await getMedia(100, 0, filter, ordering);
      // TODO: implement play behaviour in case (single) media is already queued
      // see: player/queue.ts:58
      await enqueueMedia(results, mode, scope);
      await startPlayCurrent(true);
      isLoading.value = false;
    };
    const onClick = requireSubscription(async (e) => {
      if (e.shiftKey || props.restartQueue) {
        await play();
      } else if (objIsPlaying.value || isBuffering.value) {
        await pause();
      } else if (objIsPaused.value) {
        await resume();
      } else {
        await play();
      }
    });
    return {
      actionStyle,
      onClick,
      isPlaying: objIsPlaying,
      isBuffering: objIsBuffering,
      isPaused: objIsPaused,
      isLoading,
      inScope,
      inQueue,
      queuePosition,
      buttonCssVars,
      buttonColor,
      //
      shiftKey,
      objCt,
      objUid,
    };
  },
});
</script>

<template>
  <div class="play-action" :style="actionStyle">
    <div
      @click="onClick"
      class="container"
      :class="{
        'is-loading': isLoading,
        'in-queue': inQueue,
      }"
    >
      <slot name="default">
        <ButtonPlay
          :is-active="inScope"
          :is-playing="isPlaying && !shiftKey"
          :is-buffering="isLoading || isBuffering"
          :size="size"
          :outlined="outlined"
          :shadowed="shadowed"
          :style="buttonCssVars"
          :color="`rgb(${buttonColor.join(',')})`"
          :background-color="backgroundColor"
          :hover-background-color="hoverBackgroundColor"
        />
        <div class="state">
          <div v-if="inQueue && queuePosition" class="in-queue">
            <span v-text="queuePosition" />
          </div>
        </div>
      </slot>
    </div>
    <div v-if="isPaused && size > 86" class="hint"></div>
  </div>
</template>

<style lang="scss" scoped>
.play-action {
  position: relative;
  .is-loading {
    cursor: wait;
  }
  .state {
    pointer-events: none;
    position: absolute;
    display: flex;
    align-items: center;
    justify-content: center;
    top: 6px;
    right: 10px;
    font-size: 8px;
    font-family: monospace;
  }
}
</style>
