<script lang="ts">
import { storeToRefs } from "pinia";
import { defineComponent } from "vue";

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
    :background-color="shuffleMode ? 'rgb(var(--c-white))' : 'rgb(var(--c-black))'"
    :hover-background-color="
      shuffleMode ? 'rgba(var(--c-white), 0.9)' : 'rgba(var(--c-white), 0.1)'
    "
    @click.prevent="onClick"
  >
    <IconShuffle :color-var="shuffleMode ? '--c-black' : '--c-white'" />
  </Circle>
</template>
