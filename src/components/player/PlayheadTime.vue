<script lang="ts">
import { defineComponent } from "vue";

import Duration from "@/components/ui/time/Duration.vue";

export default defineComponent({
  components: {
    Duration,
  },
  props: {
    time: {
      type: Number,
      default: null,
    },
  },
  setup() {
    return {};
  },
});
</script>

<template>
  <transition name="fade">
    <div v-if="time" class="playhead-time">
      <Duration class="playhead-time__value" :seconds="time" />
    </div>
  </transition>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";

.playhead-time {
  height: 22px;
  width: 60px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;

  &__value {
    @include typo.small;

    border-radius: 3px;
    height: inherit;
    padding: 0.5rem;
    display: inline-flex;
    color: rgb(var(--c-white));
    background: rgb(var(--c-black));
    align-items: center;
    justify-content: center;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 200ms;
}

.fade-enter-from {
  opacity: 0;
}

.fade-leave-to {
  opacity: 0;
}
</style>
