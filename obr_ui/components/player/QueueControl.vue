<script setup lang="ts">
import { ref } from "vue";

import IconQueue from "@/components/ui/icon/IconQueue.vue";
import AnimatedNumber from "@/components/ui/number/AnimatedNumber.vue";
import { useAnalytics } from "@/composables/analytics";

import Circle from "./button/Circle.vue";
const { logUIAction } = useAnalytics();

const props = defineProps<{
  queueVisible?: boolean;
  numQueued: number;
}>();

const emit = defineEmits<{
  (e: "toggleVisibility"): void;
}>();

const isTweening = ref(false);

const onClick = () => {
  emit("toggleVisibility");

  logUIAction(props.queueVisible ? "queue:hide" : "queue:show");
};

const onTweenStart = (diff: number) => {
  if (diff === -1) return;
  isTweening.value = true;
};

const onTweenEnd = (diff: number) => {
  if (diff === -1) return;
  isTweening.value = false;
};
</script>

<template>
  <Circle
    class="queue-control"
    :disabled="numQueued < 1"
    @click.prevent="onClick"
    :style="{
      color: queueVisible ? 'rgb(var(--c-bg) / 100%)' : 'rgb(var(--c-fg) / 100%)',
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
    background: rgb(var(--c-light));
    min-width: 20px;
    min-height: 20px;
    border-radius: 10px;
    color: rgb(var(--c-dark));
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
