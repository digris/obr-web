<script lang="ts">
import { ref, defineComponent, computed } from "vue";
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
      isExpanded.value = !isExpanded.value;
    };
    // const onChange = () => {
    //   isExpanded.value = false;
    // };
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
      // onChange,
      isExpanded,
    };
  },
});
</script>

<template>
  <Circle class="volume-control" :size="48" :outlined="false" @click.prevent="onClick">
    <component :is="icon" :size="48" color="rgb(var(--c-fg))" />
  </Circle>
  <transition name="slide">
    <div v-if="isExpanded">
      <input class="slider" type="range" min="0" max="100" v-model="volume" />
    </div>
  </transition>
</template>

<style lang="scss" scoped>
.volume-control {
  cursor: pointer;
}
.slider {
  //position: absolute;
  bottom: 0;
  width: 130px;
}
.slide-enter-active,
.slide-leave-active {
  transition: width 200ms, transform 200ms, opacity 200ms;
  transform: scaleX(1);
  width: 130px;
  overflow: hidden;
}
.slide-enter-from {
  transform: scaleX(0);
  opacity: 0;
  width: 0;
  overflow: hidden;
}
.slide-leave-to {
  transform: scale(0);
  width: 0;
  overflow: hidden;
}
</style>
