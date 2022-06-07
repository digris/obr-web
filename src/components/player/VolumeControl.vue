<script lang="ts">
import { ref, defineComponent, computed } from 'vue';
import { useSettingsStore } from "@/stores/settings";
import { storeToRefs } from "pinia";

import IconSpeaker from "@/components/ui/icon/IconSpeaker.vue";
import IconSpeakerOff from "@/components/ui/icon/IconSpeakerOff.vue";
import Circle from "./button/Circle.vue";

export default defineComponent({
  components: {
    IconSpeaker,
    IconSpeakerOff,
    Circle,
  },
  setup() {
    const { volume } = storeToRefs(useSettingsStore());
    const isExpanded = ref(false);
    const onClick = () => {
      console.debug("VC click");
      isExpanded.value = !isExpanded.value;
    };
    const icon = computed(() => {
      if (volume.value < 1) {
        return IconSpeakerOff;
      }
      return IconSpeaker;
    });
    return {
      icon,
      volume,
      onClick,
      isExpanded,
    };
  },
});
</script>

<template>
  <Circle class="volume-control" :size="48" :outlined="false" @click.prevent="onClick">
    <component :is="icon" :size="48" color="rgb(var(--c-fg))" />
  </Circle>
  <div v-if="isExpanded">
    <input class="slider" type="range" min="0" max="100" v-model="volume" />
  </div>
</template>

<style lang="scss" scoped>
.volume-control {
  cursor: pointer;
}
.slider {
  //position: absolute;
  bottom: 0;
}
</style>
