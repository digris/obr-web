<script lang="ts">
import { defineComponent } from "vue";

import PlayAction from "@/components/catalog/actions/PlayAction.vue";
import CircleButton from "@/components/ui/button/CircleButton.vue";
import IconPlay from "@/components/ui/icon/IconPlay.vue";

export default defineComponent({
  components: {
    CircleButton,
    PlayAction,
    IconPlay,
  },
  props: {
    objKey: {
      type: String,
      required: false,
      default: null,
    },
    filter: {
      type: Object,
      required: false,
      default: () => {},
    },
    ordering: {
      type: Array,
      default: () => [],
    },
  },
  setup() {
    return {};
  },
});
</script>

<template>
  <PlayAction
    class="play-all-small"
    :obj-key="objKey"
    :filter="filter"
    :ordering="ordering"
    :restart-queue="true"
    mode="replace"
  >
    <div class="wrapper">
      <CircleButton
        :outlined="true"
        :filled="false"
        fill-color-var="--c-white"
        hover-background-opacity="10%"
      >
        <IconPlay color-var="--c-black" />
      </CircleButton>
      <slot name="default" />
    </div>
  </PlayAction>
</template>

<style lang="scss" scoped>
.play-all-small {
  transition: opacity 100ms;

  .wrapper {
    display: flex;
    align-items: center;
    cursor: pointer;
    padding-right: 1rem;

    .circle-button {
      margin-right: 1rem;
    }
  }

  &:has(.is-loading) {
    pointer-events: none;
    cursor: wait;
    opacity: 0.5;
  }
}
</style>
