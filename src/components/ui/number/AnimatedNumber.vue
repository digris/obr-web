<script lang="ts">
import { tween } from "shifty";
import { defineComponent, ref, watch } from "vue";

export default defineComponent({
  props: {
    value: {
      type: Number,
      default: 0,
    },
  },
  setup(props) {
    const display = ref(props.value);

    const tweenValue = async (fromValue: number, toValue: number) => {
      console.debug("tweenValue", fromValue, toValue);
      tween({
        from: { n: fromValue },
        to: { n: toValue },
        duration: 500,
        easing: "easeOutQuad",
        step: (state) => {
          display.value = state.n.toFixed(0);
        },
      });
    };
    watch(
      () => props.value,
      async (newValue, oldValue) => {
        console.debug("NC", newValue, oldValue);
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
