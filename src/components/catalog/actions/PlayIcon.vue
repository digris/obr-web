<script lang="ts">
import { defineComponent } from 'vue';
import PlayAction from '@/components/catalog/actions/PlayAction.vue';
import IconPlay from '@/components/ui/icon/IconPlay.vue';

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
  <div
    class="play-icon"
  >
    <PlayAction
      :obj-key="objKey"
      :filter="filter"
    >
      <IconPlay
        :size="40"
        color="rgb(var(--c-white))"
      />
    </PlayAction>
  </div>
</template>

<style lang="scss" scoped>
.play-icon {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  /* stylelint-disable-next-line selector-pseudo-class-no-unknown */
  :deep(.container) {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    background: rgba(var(--c-black), 0.6);
    border: 1px solid rgba(var(--c-white), 0.5);
    border-radius: 24px;
    cursor: pointer;
    transition: background 100ms;
    &:hover {
      background: rgba(var(--c-black), 0.9);
    }
    &.is-loading {
      cursor: wait;
      opacity: 0.8;
    }
  }
}
</style>
