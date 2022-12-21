<script lang="ts">
import { defineComponent } from "vue";

import IconShuffle from "@/components/ui/icon/IconShuffle.vue";
import { useDevice } from "@/composables/device";
import { useQueueControls } from "@/composables/queue";
import { useSettings } from "@/composables/settings";

import Circle from "./button/Circle.vue";

export default defineComponent({
  components: {
    IconShuffle,
    Circle,
  },
  setup() {
    const { shuffleMode } = useSettings();
    const { shuffleQueue } = useQueueControls();
    const { isWeb } = useDevice();
    const onClick = () => {
      if (isWeb) {
        shuffleMode.value = !shuffleMode.value;
        if (shuffleMode.value) {
          shuffleQueue();
        }
      } else {
        shuffleQueue();
      }
    };
    return {
      shuffleMode,
      onClick,
    };
  },
});
</script>

<template>
  <Circle
    class="shuffle-control"
    :background-color="shuffleMode ? 'rgb(var(--c-light))' : 'rgb(var(--c-dark))'"
    :hover-background-color="
      shuffleMode ? 'rgb(var(--c-light) / 90%)' : 'rgb(var(--c-light) / 10%)'
    "
    @click.prevent="onClick"
  >
    <IconShuffle :color-var="shuffleMode ? '--c-dark' : '--c-light'" />
  </Circle>
</template>
