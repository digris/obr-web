<script lang="ts">
import { defineComponent, ref, watch } from "vue";
import { tween } from "shifty";

export default defineComponent({
  props: {
    value: {
      type: Number,
      default: 0,
    },
  },
  emits: ["tweenStart", "tweenEnd"],
  setup(props, { emit }) {
    const display = ref(props.value);

    const tweenValue = async (fromValue: number, toValue: number) => {
      const diff = toValue - fromValue;
      emit("tweenStart", diff);
      tween({
        from: { n: fromValue },
        to: { n: toValue },
        duration: 800,
        easing: "easeOutQuad",
        render: (state) => {
          display.value = state.n.toFixed(0);
        },
      });
      setTimeout(() => {
        emit("tweenEnd", diff);
      }, 1000);
    };
    watch(
      () => props.value,
      async (newValue, oldValue) => {
        await tweenValue(oldValue, newValue);
      }
    );
    return {
      display,
    };
  },
});
</script>
<template>
  <span v-text="display" />
</template>
