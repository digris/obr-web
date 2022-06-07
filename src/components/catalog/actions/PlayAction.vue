<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import { useMagicKeys } from "@vueuse/core";
import { usePlayerState, usePlayerControls } from "@/composables/player";
import { useQueueControls } from "@/composables/queue";
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
  setup(props) {
    const { shift: shiftKey } = useMagicKeys();
    const { enqueueMedia, startPlayCurrent } = useQueueControls();
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
    const objIsPlaying = computed(() => inScope.value && isPlaying.value);
    const objIsBuffering = computed(() => inScope.value && isBuffering.value);
    const objIsPaused = computed(() => inScope.value && issPaused.value);
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
      isLoading.value = true;
      const filter = { ...props.filter };
      const ordering = props.ordering;
      const mode = props.mode;
      const scope = props.objKey ? [props.objKey] : [];
      if (props.objKey) {
        filter.obj_key = props.objKey;
      }
      const { results } = await getMedia(100, 0, filter, ordering);
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
      onClick,
      isPlaying: objIsPlaying,
      isBuffering: objIsBuffering,
      isPaused: objIsPaused,
      isLoading,
      inScope,
      buttonCssVars,
      buttonColor,
      //
      shiftKey,
    };
  },
});
</script>

<template>
  <div class="play-action">
    <div @click="onClick" class="container" :class="{ 'is-loading': isLoading }">
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
}
</style>
