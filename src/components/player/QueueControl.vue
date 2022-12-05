<script lang="ts">
import { defineComponent, ref } from "vue";

import IconQueue from "@/components/ui/icon/IconQueue.vue";
import AnimatedNumber from "@/components/ui/number/AnimatedNumber.vue";

import Circle from "./button/Circle.vue";

export default defineComponent({
  components: {
    IconQueue,
    AnimatedNumber,
    Circle,
  },
  props: {
    queueVisible: {
      type: Boolean,
      default: false,
    },
    numQueued: {
      type: Number,
      required: true,
      default: 0,
    },
  },
  emits: ["toggleVisibility"],
  setup(setup, { emit }) {
    const isTweening = ref(false);
    const onClick = () => {
      emit("toggleVisibility");
    };
    const onTweenStart = (diff: number) => {
      if (diff === -1) {
        return;
      }
      isTweening.value = true;
    };
    const onTweenEnd = (diff: number) => {
      if (diff === -1) {
        return;
      }
      isTweening.value = false;
    };
    return {
      isTweening,
      onClick,
      onTweenStart,
      onTweenEnd,
    };
  },
});
</script>

<template>
  <Circle
    class="queue-control"
    :disabled="numQueued < 1"
    @click.prevent="onClick"
    :style="{
      color: queueVisible ? 'rgb(var(--c-bg))' : 'rgb(var(--c-fg))',
    }"
  >
    <IconQueue color-var="--c-fg" :num-queued="numQueued" />
    <div
      v-if="numQueued > 0"
      class="number"
      :class="{
        'is-tweening': isTweening,
      }"
    >
      <AnimatedNumber @tween-start="onTweenStart" @tween-end="onTweenEnd" :value="numQueued" />
    </div>
  </Circle>
</template>

<style lang="scss" scoped>
.queue-control {
  .number {
    top: -4px;
    position: absolute;
    width: auto;
    pointer-events: none;
    display: flex;
    right: -3px;
    background: rgb(var(--c-white));
    min-width: 20px;
    min-height: 20px;
    border-radius: 10px;
    color: rgb(var(--c-black));
    padding: 0 6px;
    font-size: 12px;
    box-shadow: 0 0 3px rgb(0 0 0 / 40%);
    align-items: center;
    justify-content: center;
    transition: font-size 200ms;

    &.is-tweening {
      font-size: 20px;
    }
  }
}
</style>
