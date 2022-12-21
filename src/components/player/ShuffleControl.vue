<script lang="ts">
import { defineComponent } from "vue";
import { storeToRefs } from "pinia";

import IconShuffle from "@/components/ui/icon/IconShuffle.vue";
import { useQueueControls } from "@/composables/queue";
import { useSettingsStore } from "@/stores/settings";

import Circle from "./button/Circle.vue";

export default defineComponent({
  components: {
    IconShuffle,
    Circle,
  },
  setup() {
    const { shuffleMode } = storeToRefs(useSettingsStore());
    const { shuffleQueue } = useQueueControls();
    const onClick = () => {
      shuffleMode.value = !shuffleMode.value;
      if (shuffleMode.value) {
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
