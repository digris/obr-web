<script lang="ts">
import { defineComponent } from "vue";

import PlayAction from "@/components/catalog/actions/PlayAction.vue";
import IconPlay from "@/components/ui/icon/IconPlay.vue";

export default defineComponent({
  components: {
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
  },
});
</script>

<template>
  <div class="play-icon">
    <PlayAction :obj-key="objKey" :filter="filter">
      <IconPlay color="rgb(var(--c-light))" />
    </PlayAction>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";

.play-icon {
  inset: 0;
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  /* stylelint-disable-next-line selector-pseudo-class-no-unknown */
  :deep(.container) {
    height: 48px;
    width: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgb(var(--c-dark) / 60%);
    border: 1px solid rgb(var(--c-light) / 50%);
    border-radius: 24px;
    cursor: pointer;
    transition: background 100ms;

    @include responsive.on-hover {
      background: rgb(var(--c-dark) / 90%);
    }

    &.is-loading {
      cursor: wait;
      opacity: 0.8;
    }
  }
}
</style>
