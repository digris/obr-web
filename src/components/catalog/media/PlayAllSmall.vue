<script lang="ts">
import { defineComponent } from "vue";
import { useI18n } from "vue-i18n";

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
  },
  setup() {
    const { t } = useI18n();
    const iconSize = 42;
    const iconColor = "rgb(var(--c-black))";
    return {
      t,
      iconSize,
      iconColor,
    };
  },
});
</script>

<template>
  <PlayAction class="play-all-small" :obj-key="objKey" :restart-queue="true">
    <div class="wrapper">
      <IconPlay :size="36" color="black" />
      <slot name="default" />
    </div>
  </PlayAction>
</template>

<style lang="scss" scoped>
.play-all-small {
  .wrapper {
    display: flex;
    align-items: center;
    cursor: pointer;
    margin-left: -20px;
    padding-right: 1rem;
  }
}
</style>
