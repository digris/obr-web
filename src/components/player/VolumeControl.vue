<script lang="ts">
import { ref, defineComponent } from "vue";
import { storeToRefs } from "pinia";
import { useSettingsStore } from "@/stores/settings";

import IconSpeaker from "@/components/ui/icon/IconSpeaker.vue";
import Circle from "./button/Circle.vue";

export default defineComponent({
  components: {
    IconSpeaker,
    Circle,
  },
  setup() {
    const { volume } = storeToRefs(useSettingsStore());
    const isExpanded = ref(false);
    const onClick = () => {
      isExpanded.value = !isExpanded.value;
    };
    return {
      volume,
      onClick,
      isExpanded,
    };
  },
});
</script>

<template>
  <Circle class="volume-control" @click.prevent="onClick">
    <IconSpeaker :volume="volume * 100" />
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
