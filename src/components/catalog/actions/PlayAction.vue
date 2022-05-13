<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import { usePlayerState } from "@/composables/player";
import { requireSubscription } from "@/utils/account";
import { getMedia } from "@/api/catalog";
import { getContrastColor } from "@/utils/color";
import ButtonPlay from "@/components/player/button/ButtonPlay.vue";
import { useQueueControls } from "@/composables/queue";

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
    shadowed: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const { playerState, currentScope, currentColor } = usePlayerState();
    const { enqueueMedia, startPlayCurrent } = useQueueControls();
    const inScope = computed(() => {
      return currentScope.value.includes(props.objKey);
    });
    const isPlaying = computed(() => {
      return inScope.value && playerState.value.isPlaying;
    });
    const isBuffering = computed(() => {
      return inScope.value && playerState.value.isBuffering;
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
    const play = requireSubscription(async () => {
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
    });
    return {
      play,
      isPlaying,
      isBuffering,
      isLoading,
      inScope,
      buttonCssVars,
      buttonColor,
    };
  },
});
</script>

<template>
  <div class="play-action">
    <div @click="play" class="container" :class="{ 'is-loading': isLoading }">
      <slot name="default">
        <ButtonPlay
          :is-active="inScope"
          :is-playing="isPlaying"
          :is-buffering="isLoading || isBuffering"
          :size="size"
          :outlined="outlined"
          :shadowed="shadowed"
          :style="buttonCssVars"
          :color="`rgb(${buttonColor.join(',')})`"
          :backgroundColor="backgroundColor"
        />
      </slot>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.play-action {
  .is-loading {
    cursor: wait;
  }
}
</style>
