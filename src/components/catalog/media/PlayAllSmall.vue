<script lang="ts">
import { defineComponent } from "vue";
import { useI18n } from "vue-i18n";

import CircleButton from "@/components/ui/button/CircleButton.vue";
import PlayAction from "@/components/catalog/actions/PlayAction.vue";
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
  },
  setup() {
    const { t } = useI18n();
    const iconSize = 48;
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
      <CircleButton :size="iconSize" :outlined="true">
        <IconPlay :size="iconSize" color="black" />
      </CircleButton>
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
    .circle-button {
      margin-right: 1rem;
    }
  }
}
</style>
