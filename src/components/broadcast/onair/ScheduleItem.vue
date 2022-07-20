<script lang="ts">
import { computed, defineComponent } from "vue";
import { usePlayerControls } from "@/composables/player";
import { useStreamControls } from "@/composables/stream";
import { useQueueControls } from "@/composables/queue";
import { DateTime } from "luxon";
import { requireSubscription } from "@/utils/account";
import LazyImage from "@/components/ui/LazyImage.vue";
import PlayButton from "./button/Play.vue";

const NUM_ITEMS_IN_VIEWPORT = 4;

export default defineComponent({
  components: {
    LazyImage,
    PlayButton,
  },
  props: {
    hasFocus: {
      type: Boolean,
      default: false,
    },
    isCurrent: {
      type: Boolean,
      default: false,
    },
    position: {
      type: Number,
      default: 0,
    },
    scheduleItem: {
      type: Object,
      required: false,
      default: null,
    },
  },
  emits: ["play", "pause"],
  setup(props, { emit }) {
    const { pause } = usePlayerControls();
    const { startPlayStream } = useStreamControls();
    const { enqueueObj, startPlayCurrent } = useQueueControls();
    // eslint-disable-next-line arrow-body-style
    const isPlaceholder = computed(() => {
      return props.scheduleItem === null;
    });
    // eslint-disable-next-line arrow-body-style
    const media = computed(() => {
      return props.scheduleItem ? props.scheduleItem.media : null;
    });
    const objKey = computed(() => {
      return media.value ? `${media.value.ct}:${media.value.uid}` : null;
    });
    const release = computed(() => {
      if (media.value && media.value.releases.length) {
        return media.value.releases[0];
      }
      return null;
    });
    const inViewport = computed(() => {
      return props.position <= NUM_ITEMS_IN_VIEWPORT;
    });
    const image = computed(() => {
      if (!inViewport.value) {
        return null;
      }
      return release.value && release.value.image ? release.value.image : null;
    });
    const cssVars = computed(() => {
      if (!image.value && image.value.rgb) {
        return {};
      }
      return {
        "--c-bg": image.value.rgb.join(","),
      };
    });
    const timeFormat = DateTime.TIME_WITH_SECONDS;
    // eslint-disable-next-line @typescript-eslint/no-shadow
    const playMedia = requireSubscription(async (media: object) => {
      await enqueueObj(media, "replace");
      await startPlayCurrent(true);
    });
    const play = () => {
      if (props.isCurrent) {
        const startTime = -10;
        // playStream(startTime);
        startPlayStream(startTime);
        emit("play");
      } else {
        playMedia(props.scheduleItem.media);
      }
    };
    // const pause = () => {
    //   eventBus.emit("player:controls", { do: "pause" });
    //   emit("pause");
    // };
    return {
      isPlaceholder,
      objKey,
      cssVars,
      media,
      release,
      image,
      timeFormat,
      play,
      pause,
    };
  },
});
</script>

<template>
  <div
    class="schedule-item"
    :style="cssVars"
    :class="{
      'has-focus': hasFocus,
      'is-placeholder': isPlaceholder,
    }"
  >
    <div v-if="isPlaceholder" class="panel"></div>
    <div v-else class="panel">
      <LazyImage :image="image" />
    </div>
    <div class="actions">
      <PlayButton :media="media" @play="play" @pause="pause" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/live-color";
@use "@/style/base/typo";
.schedule-item {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgb(var(--c-black));
  &.is-placeholder {
    background: rgb(var(--c-black));
  }
  .panel {
    width: 100%;
    height: 100%;
    //crop a couple of pixels
    overflow: hidden;
    :deep(img) {
      transform: scale(1.02);
      //transform: scale(0.95);
    }
  }
  .actions {
    position: absolute;
    .circle-button {
      background: rgba(var(--c-bg), 1);
      &:hover {
        background: rgba(var(--c-bg), 0.8);
      }
    }
  }
}
</style>
