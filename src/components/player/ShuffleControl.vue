<script lang="ts">
import { defineComponent } from "vue";
import { useSettingsStore } from "@/stores/settings";
import { storeToRefs } from "pinia";

import IconShuffle from "@/components/ui/icon/IconShuffle.vue";
import Circle from "./button/Circle.vue";

export default defineComponent({
  components: {
    IconShuffle,
    Circle,
  },
  setup() {
    const { shuffle } = storeToRefs(useSettingsStore());
    const onClick = () => {
      shuffle.value = !shuffle.value;
    };
    return {
      shuffle,
      onClick,
    };
  },
});
</script>

<template>
  <Circle
    class="shuffle-control"
    :size="48"
    :inactive="!shuffle"
    :outlined="false"
    @click.prevent="onClick"
  >
    <IconShuffle :size="48" color="rgb(var(--c-fg))" />
  </Circle>
</template>
