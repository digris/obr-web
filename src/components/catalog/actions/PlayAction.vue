<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import type { PropType } from "vue";
import { useMagicKeys, useVibrate } from "@vueuse/core";
import { useRatingStore } from "@/stores/rating";
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
    iconScale: {
      type: Number,
      default: 1,
    },
    outlined: {
      type: Boolean,
      default: true,
    },
    filled: {
      type: Boolean,
      default: false,
    },
    color: {
      type: Array as PropType<Array<number>>,
      default: () => [0, 100, 200],
    },
  },
  setup(props) {
    const { objCt, objUid } = useObjCtUid(props.objKey);
    const { shift: shiftKey } = useMagicKeys();
    const { injectRatings } = useRatingStore();
    const { queuedMedia, currentIndex: currentQueueIndex } = useQueueState();
    const { enqueueMedia, startPlayCurrent, playFromIndex } = useQueueControls();
    const { isPlaying, isBuffering, isPaused, scope, color: currentColor } = usePlayerState();
    const { pause, resume } = usePlayerControls();
    const inScope = computed(() => {
      return scope.value.includes(props.objKey);
    });
    const queueIndex = computed(() => {
      if (currentQueueIndex.value < 0) {
        return null;
      }
      const index = queuedMedia.value.findIndex((obj: any) => {
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
    const objIsPaused = computed(() => inScope.value && isPaused.value);

    const baseColor = computed(() => {
      return props.color;
    });

    const activeColor = computed(() => {
      return currentColor.value;
    });

    const fillColor = computed(() => {
      if (props.filled) {
        return getContrastColor(baseColor.value);
      }
      return props.color;
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
      // const scope = props.objKey ? [props.objKey] : [];
      if (props.objKey) {
        filter.obj_key = props.objKey;
      }
      const { results } = await getMedia(100, 0, filter, ordering);
      // TODO: implement play behaviour in case (single) media is already queued
      // see: player/queue.ts:58
      // await enqueueMedia(results, mode, scope.value);
      await enqueueMedia(results, mode, [props.objKey]);
      await startPlayCurrent(true);
      isLoading.value = false;
      await injectRatings(results);
    };
    const { vibrate } = useVibrate({ pattern: 10 });
    const onClick = requireSubscription(async (e: MouseEvent) => {
      vibrate();
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
      onClick,
      isPlaying: objIsPlaying,
      isBuffering: objIsBuffering,
      isPaused: objIsPaused,
      isLoading,
      inScope,
      inQueue,
      queuePosition,
      //
      shiftKey,
      objCt,
      objUid,
      //
      baseColor,
      activeColor,
      fillColor,
    };
  },
});
</script>

<template>
  <div class="play-action">
    <div
      @click.prevent="onClick"
      class="container"
      :class="{
        'is-loading': isLoading,
      }"
    >
      <slot name="default">
        <ButtonPlay
          :is-active="inScope"
          :is-playing="isPlaying && !shiftKey"
          :is-buffering="isLoading || isBuffering"
          :in-queue="queuePosition > 0 || queuePosition < 0"
          :scale="iconScale"
          :outlined="outlined"
          :filled="filled"
          :base-color="baseColor"
          :active-color="activeColor"
          :fill-color="fillColor"
        />
      </slot>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.play-action {
  display: inline-grid;
  position: relative;

  .container {
    display: inline-grid;
  }

  .is-loading {
    cursor: wait;
  }
}
</style>
